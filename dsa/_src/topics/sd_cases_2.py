META = dict(
    title="SD 8: Designs II", page_title="Design Walkthroughs II · DSA + System Design Guide", week="System design · Practice", group="System design",
    h1="Design walkthroughs II: news feed, chat, autocomplete",
    lead="Three product designs that test fan-out, real-time delivery and precomputation. Each follows the same interview steps so you can practice the routine, not memorize answers.",
    blurb="Full walkthroughs: news feed, chat app, search autocomplete.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">How to read these</span>
  <h2>Same recipe, different dishes</h2>
  <div class="real big-real">
    <p>A chef who knows how to make a sauce, braise and roast can cook almost any menu. These three designs reuse the same building blocks (cache, queue, shard, replicate) in different combinations. Notice which block solves which problem, because that's what transfers to a design you've never seen.</p>
  </div>
</section>

<section id="feed">
  <span class="eyebrow">Walkthrough 4 · Intermediate</span>
  <h2>Design a news feed (like Instagram or X)</h2>
  <div class="real"><p>A mail room in an apartment building. When someone sends a flyer, the mail room can put a copy in every resident's mailbox right away (push), or residents can come to the lobby and read the bulletin board when they want (pull). Pushing is great for small flyers; for a flyer to 100 million residents, a bulletin board is the only sane option.</p></div>
  <h3>1. Requirements</h3>
  <ul>
    <li>Users post (text, photos); follow others; see a feed of followed users' posts, newest or ranked first, paginated.</li>
    <li>200 M DAU, feed loads in &lt; 200 ms; a new post can take a few seconds to appear (eventual consistency is fine).</li>
  </ul>
  <h3>2. Estimates</h3>
  <ul>
    <li>Feed reads: 200 M × 10 opens/day = 2 B/day ≈ <strong>20,000/s</strong>. Posts: 200 M × 0.5 = 100 M/day ≈ <strong>1,000/s</strong>.</li>
    <li>Average 200 followers → 1,000 posts/s × 200 = <strong>200,000 feed inserts/s</strong> if we push to everyone.</li>
  </ul>
  <h3>3. Data model</h3>
<pre><code>users(user_id, name, ...)                      -- SQL
follows(follower_id, followee_id)              -- sharded by follower_id (and an index by followee)
posts(post_id, author_id, text, media_url, created_at)   -- sharded by author_id
feed_cache: user_id → [post_id, post_id, ...]  -- Redis list, newest 500</code></pre>
  <h3>4. High-level design</h3>
<pre class="diagram">post:  client ─▶ API ─▶ posts DB ─▶ queue ─▶ fan-out workers ─▶ followers' feed caches
read:  client ─▶ API ─▶ feed cache (post IDs) ─▶ post cache / DB (hydrate) ─▶ ranked page
media: client ─▶ object storage ─▶ CDN</pre>
  <h3>5. Deep dive: fan-out</h3>
  <figure class="anim" data-anim="sd-fanout"><figcaption>Push for most users, pull for celebrities</figcaption></figure>
  <div class="tbl"><table>
    <thead><tr><th></th><th>Fan-out on write (push)</th><th>Fan-out on read (pull)</th></tr></thead>
    <tbody>
      <tr><td>Post cost</td><td>High: one insert per follower</td><td>Low: one insert</td></tr>
      <tr><td>Read cost</td><td>Low: one cache read</td><td>High: query every followee and merge</td></tr>
      <tr><td>Problem case</td><td>Celebrities (millions of followers)</td><td>Users following thousands of accounts</td></tr>
    </tbody>
  </table></div>
  <p><strong>Hybrid answer:</strong> push for normal authors; for accounts above ~10,000 followers, skip the push and merge their recent posts in at read time. Skip pushing to inactive users too; build their feed when they return.</p>
  <h3>6. Other decisions</h3>
  <ul>
    <li><strong>Ranking:</strong> fetch a few hundred candidates, score them (recency, closeness, engagement) in a ranking service, return the top 20.</li>
    <li><strong>Pagination:</strong> cursor-based on (score or time, post_id).</li>
    <li><strong>Counts (likes):</strong> sharded counters with write-back caching; approximate is fine.</li>
  </ul>
</section>

<section id="chat">
  <span class="eyebrow">Walkthrough 5 · Intermediate</span>
  <h2>Design a chat app (like WhatsApp or Google Chat)</h2>
  <div class="real"><p>A switchboard operator with a phone line open to everyone who's awake. When Ana says something for Bob, the operator says it straight down Bob's line. If Bob's phone is off, the operator writes it in Bob's message book and reads it to him when he wakes up.</p></div>
  <h3>1. Requirements</h3>
  <ul>
    <li>1:1 and group chats (up to ~500 members); delivered/read receipts; online status; message history on all devices; push notifications when offline.</li>
    <li>500 M DAU × 40 messages ≈ 20 B/day ≈ <strong>230,000 messages/s</strong>. Delivery under ~200 ms; messages must never be lost and must keep order within a chat.</li>
  </ul>
  <h3>2. High-level design</h3>
<pre class="diagram">Ana ══ WebSocket ══ chat server 7 ─┐
                                   ├─▶ message store (wide-column, partition = chat_id)
Bob ══ WebSocket ══ chat server 3 ◀┤
                                   ├─▶ presence/session store (Redis: user → server)
                                   └─▶ push notification service (if Bob is offline)</pre>
  <h3>3. Sending a message, step by step</h3>
  <div class="trace">
    <div><p>Ana's app sends the message over her open WebSocket, with a client-generated ID (for idempotency on retry).</p></div>
    <div><p>Chat server 7 assigns a server timestamp/sequence, stores it in the message store, and acks Ana (one grey tick: sent).</p></div>
    <div><p>It looks up Bob in the session store: he's connected to server 3. It forwards the message there (directly or via pub/sub).</p></div>
    <div><p>Server 3 pushes it down Bob's WebSocket; Bob's app acks (two ticks: delivered). Opening the chat sends a read receipt.</p></div>
    <div><p>If Bob is offline, the message waits in storage and a push notification is sent. When Bob reconnects, his app asks "everything after the last message ID I have," per chat.</p></div>
  </div>
  <h3>4. Deep dives</h3>
  <ul>
    <li><strong>Millions of connections:</strong> each chat server holds ~50,000–100,000 WebSockets; ~10 M concurrent users means a few hundred servers. A load balancer assigns connections; the session store tracks who's where.</li>
    <li><strong>Ordering:</strong> a per-chat sequence number assigned by one owner of that chat (or the partition leader), not by client clocks.</li>
    <li><strong>Groups:</strong> fan out to each online member's server; for big groups, have members pull history.</li>
    <li><strong>Presence:</strong> heartbeats every ~30 s; mark offline after missed heartbeats; publish status changes only to friends who are online.</li>
    <li><strong>End-to-end encryption:</strong> servers store ciphertext they can't read; keys live on devices.</li>
  </ul>
</section>

<section id="autocomplete">
  <span class="eyebrow">Walkthrough 6 · Advanced (very Google)</span>
  <h2>Design search autocomplete (typeahead)</h2>
  <div class="real"><p>A librarian who has memorized the 10 most-asked book titles for every possible first few letters. As you say "har…", they instantly reply "Harry Potter, Harvard Business Review, Harper Lee…" without searching the shelves, because they prepared those lists last night.</p></div>
  <h3>1. Requirements</h3>
  <ul>
    <li>As the user types, show the top 10 completions by popularity. Must feel instant: &lt; 100 ms including network.</li>
    <li>Billions of queries/day; each keystroke is a request, so ~5× the search volume: <strong>hundreds of thousands of requests/s</strong>.</li>
    <li>Suggestions can lag reality by minutes to hours; trending topics should appear within ~an hour.</li>
  </ul>
  <h3>2. Core data structure</h3>
  <p>A <a href="trees.html#patterns">trie</a> of past queries, where <strong>each node stores its precomputed top 10 completions</strong>. A lookup is just "walk to the prefix's node, return its list": O(length of prefix), no searching subtrees at request time.</p>
<pre class="diagram">          (root)
           │ g
          [g] top: google, gmail, google maps, ...
           │ o
          [go] top: google, google maps, good morning, ...
           │ o
          [goo] top: google, google maps, google translate, ...</pre>
  <h3>3. High-level design</h3>
<pre class="diagram">read path:   browser (debounce, cache) ─▶ CDN/edge ─▶ suggestion servers (trie shards in RAM)
build path:  search logs ─▶ aggregation job (counts per query, time-decayed)
                         ─▶ trie builder ─▶ new trie snapshot ─▶ swapped into servers</pre>
  <h3>4. Deep dives</h3>
  <ul>
    <li><strong>Build offline, serve read-only:</strong> a batch job (MapReduce-style) recomputes counts and tries every hour or so; servers load the new snapshot and swap atomically. A small streaming layer can boost fast-trending queries.</li>
    <li><strong>Sharding:</strong> by prefix range (a–c, d–f…) adjusted for uneven letter popularity, with replicas of each shard for load and failover.</li>
    <li><strong>Client tricks:</strong> wait ~100 ms after the last keystroke (debounce), cache results in the browser ("goo" results are reusable while typing "goog"), and cancel outdated requests.</li>
    <li><strong>Personalization and safety:</strong> blend in the user's own history; filter offensive or harmful suggestions before they reach the trie.</li>
    <li><strong>Languages:</strong> separate tries per language/region.</li>
  </ul>
  <div class="google"><p>Interviewers want the key insight: precompute top-k at every trie node so serving is a lookup, and rebuild offline from logs. Then show you can shard it and keep it fast with client-side debouncing and caching.</p></div>
</section>
"""

PROBLEMS = [
    ("Design a news feed", "#feed", "medium", "Hybrid fan-out, feed cache, ranking"),
    ("Design a chat app", "#chat", "medium", "WebSockets, session store, per-chat ordering"),
    ("Design search autocomplete", "#autocomplete", "hard", "Trie with top-k per node, offline rebuild"),
    ("Design YouTube (upload + watch)", "sd-async.html#deep", "hard", "Async transcoding, object storage, CDN, adaptive bitrate"),
    ("Design a notification system", "sd-async.html#patterns", "medium", "Pub/sub, per-channel workers, retries, user preferences"),
    ("Design Google Drive / Dropbox", "sd-data.html#choose", "hard", "Chunked uploads, metadata DB vs blob storage, sync and conflicts"),
    ("Design a ride-sharing app (like Uber)", "sd-data.html#patterns", "hard", "Location updates, geo index (geohash/quadtree), matching"),
    ("Design a parking lot or ticket booking system", "sd-data.html#cap", "medium", "Consistency for seats, holds with expiry, transactions"),
]

META["problems_title"] = "Practice these designs"
META["problems_intro"] = "The first three are walked through above; the rest reuse ideas from the linked pages. Design each one out loud in 40 minutes before checking."

QUIZ = [
    dict(lvl="easy", q="Which protocol suits delivering chat messages instantly?", opts=["Email (SMTP)", "WebSockets", "FTP", "DNS"], a=1, why="A persistent two-way connection lets the server push messages immediately."),
    dict(lvl="easy", q="Where should photos in a feed be served from?", opts=["The SQL database", "Object storage behind a CDN", "The chat server", "Redis"], a=1, why="Blobs live in object storage; the CDN serves them close to users."),
    dict(lvl="easy", q="Autocomplete's core data structure is usually a:", opts=["Heap", "Trie", "Stack", "Linked list"], a=1, why="Prefixes map naturally onto trie paths."),
    dict(lvl="medium", q="Why not use fan-out on write for a celebrity with 80 M followers?",
         opts=["Celebrities post less", "One post would need 80 M feed inserts, which is slow and costly; pull their posts at read time instead", "Push is illegal", "Their followers are offline"], a=1,
         why="The hybrid model pushes for normal users and pulls for celebrities."),
    dict(lvl="medium", q="Chat: Bob is on chat server 3, Ana on server 7. How does server 7 know where to send Ana's message?",
         opts=["Broadcast to all servers", "Look up Bob in a session/presence store mapping user → server", "Ask Bob's phone", "DNS"], a=1,
         why="A shared store (e.g. Redis) tracks which server holds each live connection."),
    dict(lvl="medium", q="Why should autocomplete store the top 10 completions at every trie node?",
         opts=["To save memory", "So a request is just a walk to the prefix node, with no subtree search at request time", "Tries require it", "For security"], a=1,
         why="Precomputation moves expensive work from the hot read path to an offline build."),
    dict(lvl="medium", q="Why does the chat client send its own message ID?",
         opts=["For encryption", "So retries after a network blip don't create duplicate messages (idempotency)", "To sort messages", "It's required by WebSockets"], a=1,
         why="The server can recognize and ignore a resend of a message it already stored."),
    dict(lvl="hard", q="Feed reads are 20,000/s and each feed shows 20 posts. What keeps hydration (loading post content) fast?",
         opts=["Query the posts DB for each post", "Cache posts by ID and batch-get them (multi-get) in one round trip", "Store full posts in every feed cache", "Use a queue"], a=1,
         why="Feed caches hold IDs; a post cache plus multi-get avoids 20 separate DB queries per request."),
    dict(lvl="hard", q="How should messages within one chat be ordered reliably?",
         opts=["By each sender's phone clock", "By a per-chat sequence number assigned by a single owner (server or partition leader)", "Alphabetically", "By message size"], a=1,
         why="Device clocks drift and can be wrong; one sequencer per chat gives a single agreed order."),
    dict(lvl="hard", q="Autocomplete gets ~5 requests per search (one per keystroke). Two client-side tricks that cut load?",
         opts=["Bigger servers and more RAM", "Debounce keystrokes and cache prefix results in the browser", "Disable autocomplete on mobile", "Send the full query only"], a=1,
         why="Waiting ~100 ms between keystrokes and reusing earlier prefix results removes many requests before they leave the device."),
]
