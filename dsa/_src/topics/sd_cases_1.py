META = dict(
    title="SD 7: Designs I", page_title="Design Walkthroughs I · DSA + System Design Guide", week="System design · Practice", group="System design",
    h1="Design walkthroughs I: URL shortener, rate limiter, web crawler",
    lead="Three classic interview designs, worked end to end with the same steps you'll use in the interview: requirements, estimates, API, data model, high-level design, deep dives, and trade-offs.",
    blurb="Full walkthroughs: URL shortener, distributed rate limiter, web crawler.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">How to read these</span>
  <h2>Practice like a pilot in a simulator</h2>
  <div class="real big-real">
    <p>Pilots don't learn emergencies during real flights; they rehearse them in a simulator until the steps are automatic. Read each walkthrough once, then close the page, set a 40-minute timer, and design it yourself out loud on paper. Compare afterwards. The steps match the framework on the <a href="sd-interview.html">interview page</a>.</p>
  </div>
</section>

<section id="url">
  <span class="eyebrow">Walkthrough 1 · Beginner</span>
  <h2>Design a URL shortener (like bit.ly)</h2>
  <div class="real"><p>A coat check: you hand over a long coat (the long URL) and get a small ticket (the short code). Anyone with the ticket gets the coat back instantly. The hard part is printing billions of unique tickets and finding coats fast.</p></div>

  <h3>1. Requirements</h3>
  <ul>
    <li><strong>Functional:</strong> create a short URL from a long one (optional custom alias, optional expiry); redirect short → long.</li>
    <li><strong>Non-functional:</strong> redirects in &lt; 50 ms, very high availability (broken links are bad), codes not guessable in sequence, links never lost.</li>
  </ul>
  <h3>2. Estimates</h3>
  <ul>
    <li>100 M new URLs/month ≈ 40 writes/s. Reads 100× more ≈ <strong>4,000 redirects/s</strong> (~10,000 at peak).</li>
    <li>Storage: 100 M × 12 months × 5 years × 500 bytes ≈ <strong>3 TB</strong>. Small enough for a few database nodes.</li>
    <li>Codes needed: 6 billion over 5 years. 62⁷ ≈ 3.5 trillion, so <strong>7 characters</strong> is plenty.</li>
  </ul>
  <h3>3. API</h3>
<pre><code>POST /v1/urls  {"long_url": "https://...", "alias": "optional", "expires_at": null}
     → 201 {"short_url": "https://sho.rt/2TX"}
GET  /{code}   → 301 or 302 Location: https://...   (404 if unknown or expired)</code></pre>
  <h3>4. Data model</h3>
<pre><code>urls: code (PK, 7 chars) | long_url | user_id | created_at | expires_at</code></pre>
  <h3>5. High-level design</h3>
<pre class="diagram">client ──▶ LB ──▶ API servers ──▶ cache (code → long_url, ~90%+ hits)
                     │                     │ miss
                     ├── ID generator ──┐  ▼
                     └─────────────────▶ key-value DB (sharded by code)</pre>
  <h3>6. Deep dive: generating the code</h3>
  <figure class="anim" data-anim="sd-base62"><figcaption>Turning a unique number into a short code</figcaption></figure>
  <div class="tbl"><table>
    <thead><tr><th>Option</th><th>How</th><th>Trade-off</th></tr></thead>
    <tbody>
      <tr><td>Hash the URL (MD5) and take 7 chars</td><td>Same URL → same code</td><td>Collisions need checking and retrying</td></tr>
      <tr><td>Counter + base-62</td><td>Unique number → code</td><td>No collisions; sequential codes are guessable unless you shuffle/encrypt the number</td></tr>
      <tr><td>Pre-generated key service</td><td>Batch of unused random codes handed to each server</td><td>Fast, unguessable; must track used keys</td></tr>
    </tbody>
  </table></div>
  <p>A good answer: a distributed ID generator (each server reserves a range of 1,000 numbers at a time from a coordinator, so no per-request coordination), shuffle the bits so codes aren't sequential, then base-62 encode.</p>
  <h3>7. Other decisions</h3>
  <ul>
    <li><strong>301 vs 302:</strong> 301 (permanent) lets browsers cache the redirect, which cuts load but hides clicks from analytics. 302 keeps every click visible.</li>
    <li><strong>Analytics:</strong> publish a click event to a queue; never slow the redirect for it.</li>
    <li><strong>Abuse:</strong> rate-limit creation per user, scan long URLs against malware lists.</li>
    <li><strong>Expiry:</strong> check on read, and clean up with a background job.</li>
  </ul>
</section>

<section id="ratelimit">
  <span class="eyebrow">Walkthrough 2 · Intermediate</span>
  <h2>Design a distributed rate limiter</h2>
  <div class="real"><p>A theme park ride with a ticket scanner at each of several gates. Each family has a limit of 5 rides per hour, and all gates must share one count, otherwise a family could go through each gate separately and ride 5 times per gate.</p></div>
  <h3>1. Requirements</h3>
  <ul>
    <li>Limit requests per key (user ID, API key or IP) per time window, with different rules per endpoint ("100 posts/hour," "10 logins/minute").</li>
    <li>Adds less than ~1–2 ms per request; works across many API servers; if the limiter itself fails, let traffic through (fail open) rather than take down the site.</li>
    <li>Return <code>429</code> with <code>Retry-After</code> and remaining-quota headers.</li>
  </ul>
  <h3>2. Where it runs</h3>
  <p>In the API gateway or as middleware on every API server, with counters in a shared Redis cluster so all servers see one count.</p>
<pre class="diagram">client ─▶ API gateway ─(check key)─▶ Redis cluster (counters, sharded by key)
               │ allowed                       ▲
               ▼                               │ rules cached locally,
          backend services            rules DB ┘ refreshed every minute</pre>
  <h3>3. Algorithm</h3>
  <figure class="anim" data-anim="sd-token"><figcaption>Token bucket for one user</figcaption></figure>
  <p>Token bucket per key, stored as <code>(tokens, last_refill_time)</code>. On each request, compute refill since last time, subtract one if available. Do the read-modify-write atomically in Redis (a Lua script) so two servers can't both spend the last token.</p>
  <h3>4. Deep dives</h3>
  <ul>
    <li><strong>Hot keys:</strong> one abusive client hammering one Redis shard. Add a small local limiter per server as a first filter.</li>
    <li><strong>Latency:</strong> Redis in the same data center (~0.5 ms). For extreme scale, each server can take a batch of tokens locally and sync periodically, trading precision for speed.</li>
    <li><strong>Multi-region:</strong> per-region limits, or approximate global counts synced asynchronously.</li>
    <li><strong>Failure:</strong> if Redis is unreachable, fail open with a conservative local limit and alert.</li>
  </ul>
</section>

<section id="crawler">
  <span class="eyebrow">Walkthrough 3 · Advanced (very Google)</span>
  <h2>Design a web crawler</h2>
  <div class="real"><p>A librarian tasked with cataloguing every book in every library in the world. Each book's bibliography points to more books. They keep a to-visit list, never visit the same book twice, don't overwhelm any single library with visits, and skip libraries that say "no visitors."</p></div>
  <h3>1. Requirements</h3>
  <ul>
    <li>Start from seed URLs; download pages; extract links; repeat. Store pages for indexing.</li>
    <li>Scale: 1 billion pages/month ≈ <strong>400 pages/s</strong>. At 500 KB each ≈ 500 TB/month of raw HTML.</li>
    <li>Be <strong>polite</strong> (obey robots.txt, limit requests per site), avoid duplicates, handle traps (infinite calendars), and keep pages fresh.</li>
  </ul>
  <h3>2. High-level design</h3>
<pre class="diagram">seed URLs ─▶ URL frontier (priority + per-host queues)
                 │
                 ▼
        fetcher workers ──(DNS cache, robots.txt cache)──▶ the web
                 │ HTML
                 ▼
        content store (object storage) ──▶ dedup (content fingerprint)
                 │
                 ▼
        link extractor ──▶ URL filter + "seen URLs" set ──▶ back to frontier</pre>
  <h3>3. Deep dives</h3>
  <div class="trace">
    <div><p><strong>URL frontier:</strong> front queues by priority (PageRank, how often the page changes) and back queues per host, each host handled by one worker with a delay between requests. That's how politeness is enforced.</p></div>
    <div><p><strong>Seen-URL check at billions of URLs:</strong> a Bloom filter in memory answers "definitely new" or "probably seen" using a few bits per URL, backed by a disk store for certainty.</p></div>
    <div><p><strong>Duplicate content:</strong> many URLs serve the same page. Store a fingerprint (hash or SimHash for near-duplicates) of each page and skip repeats.</p></div>
    <div><p><strong>Traps and junk:</strong> cap URL length and depth per site, normalize URLs (lowercase host, strip tracking parameters), blacklist known traps.</p></div>
    <div><p><strong>Scale out:</strong> partition by hostname (consistent hashing), so each worker owns a set of hosts; this also keeps politeness local to one machine.</p></div>
    <div><p><strong>Freshness:</strong> re-crawl news sites hourly and static pages monthly, based on how often each page has changed before.</p></div>
  </div>
  <div class="google"><p>This is Google's origin story, so interviewers may push on politeness, dedup and prioritization. Mention BFS over the link graph, a Bloom filter for seen URLs, and per-host queues, and you've covered the core.</p></div>
</section>
"""

PROBLEMS = [
    ("Design a URL shortener (40 min, on paper)", "#url", "easy", "Base-62 IDs, cache-heavy reads"),
    ("Design Pastebin", "#url", "easy", "Like the URL shortener, plus blob storage for the text"),
    ("Design a distributed rate limiter", "#ratelimit", "medium", "Token bucket in Redis, atomic updates"),
    ("Design a unique ID generator", "sd-reliability.html#patterns", "medium", "Snowflake: time + machine + sequence"),
    ("Design a web crawler", "#crawler", "hard", "Frontier, politeness, Bloom filter, dedup"),
]

META["problems_title"] = "Practice these designs"
META["problems_intro"] = "Tick each one after you've designed it yourself, out loud, in 40 minutes, then compared with the walkthrough."

QUIZ = [
    dict(lvl="easy", q="How many characters of base-62 cover about 3.5 trillion short URLs?", opts=["5", "6", "7", "10"], a=2, why="62⁷ ≈ 3.5 × 10¹²."),
    dict(lvl="easy", q="A URL shortener is read-heavy. Which component helps redirects most?", opts=["Message queue", "Cache of code → long URL", "Search index", "Batch jobs"], a=1, why="Most redirects hit a small set of popular links; caching them avoids the database."),
    dict(lvl="easy", q="What does robots.txt tell a crawler?", opts=["The site's password", "Which paths it may or may not crawl", "The page's language", "The server's IP"], a=1, why="Polite crawlers obey it."),
    dict(lvl="medium", q="Why might a URL shortener use 302 instead of 301 redirects?",
         opts=["302 is faster", "Browsers cache 301s, so later clicks never reach your server and aren't counted", "301 is deprecated", "302 is more secure"], a=1,
         why="302 keeps clicks visible for analytics at the cost of more traffic."),
    dict(lvl="medium", q="Sequential IDs base-62 encoded make codes guessable (2TX, 2TY…). A fix?",
         opts=["Use longer URLs", "Shuffle or encrypt the ID bits before encoding, or use pre-generated random keys", "Use base 10", "Remove the cache"], a=1, why="Non-sequential codes stop people walking through everyone's links."),
    dict(lvl="medium", q="Rate limiter across 30 servers: why must the token check be atomic?",
         opts=["For logging", "Otherwise two servers can read 1 token at once and both allow a request", "Redis requires it", "To save memory"], a=1, why="Read-modify-write races let clients exceed the limit."),
    dict(lvl="medium", q="If the rate limiter's Redis goes down, the usual choice is to:",
         opts=["Reject all traffic (fail closed)", "Allow traffic, maybe with a local fallback limit (fail open), and alert", "Shut down the site", "Retry forever"], a=1,
         why="The limiter protects the product; it shouldn't be the reason the product is down. (Security-critical limits like login attempts may fail closed.)"),
    dict(lvl="hard", q="A crawler must check billions of URLs for \"already seen\" quickly with little memory. Best structure?",
         opts=["Sorted list", "Bloom filter (with a disk-backed store to confirm)", "Linked list", "Trie of full URLs in RAM"], a=1,
         why="A Bloom filter uses a few bits per item with no false negatives; occasional false positives skip a few new URLs."),
    dict(lvl="hard", q="How does a crawler stay polite to each website at 400 pages/s overall?",
         opts=["Crawl slower everywhere", "Per-host queues, each assigned to one worker that waits between requests to that host", "Ignore robots.txt", "Use more DNS servers"], a=1,
         why="Partitioning by host means one machine controls the request rate to each site."),
    dict(lvl="hard", q="Many URLs (with tracking parameters, mirrors) serve the same content. How do you avoid storing duplicates?",
         opts=["Compare URLs only", "Normalize URLs and also fingerprint page content (hash or SimHash) to skip duplicates", "Store everything", "Crawl only home pages"], a=1,
         why="URL normalization catches some duplicates; content fingerprints catch the rest, including near-duplicates."),
]
