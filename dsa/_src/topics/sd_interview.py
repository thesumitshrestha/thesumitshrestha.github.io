META = dict(
    title="SD 9: Interview guide", page_title="System Design Interview · DSA + System Design Guide", week="System design · Interview", group="System design",
    h1="The system design interview",
    lead="A 45-minute conversation where you design a system out loud. There's no single right answer; you're scored on structure, trade-offs, and communication. This page is the routine to rehearse, a cheat sheet to review, and a study plan.",
    blurb="The 45-minute framework, what's graded, building-block cheat sheet, mistakes, study plan.",
    needs_anim=False,
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>An architect meeting a client</h2>
  <div class="real big-real">
    <p>A client tells an architect "I want a house." A bad architect starts drawing a mansion immediately. A good one asks: how many people, what budget, which climate, do you work from home? Then sketches the floor plan, explains why the kitchen faces the garden, and adjusts when the client says "actually, we need a garage." System design interviews reward the second architect.</p>
  </div>
  <div class="callout"><p><strong>For Software Engineer III (L4):</strong> Google's loop for this level is mostly coding, but a system design round can be included, and coding rounds often end with design-flavored follow-ups ("how would this work at a billion users?"). Ask your recruiter exactly which rounds you'll have. Either way, L4 is expected to produce a sensible, working design and discuss trade-offs; deep expertise in distributed consensus is a senior-level expectation.</p></div>
</section>

<section id="framework">
  <span class="eyebrow">The routine</span>
  <h2>A 45-minute framework</h2>
  <div class="real"><p>A cooking competition with a clock: prep, cook, plate, present. If you spend 40 minutes on the sauce, there's no dish to taste. Watch the time and move on.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Step</th><th>Minutes</th><th>What you do</th></tr></thead>
    <tbody>
      <tr><td>1. Requirements</td><td>5</td><td>Clarify features (pick 3–4 core ones), users, scale, latency, consistency needs. Write them down.</td></tr>
      <tr><td>2. Estimates</td><td>3–5</td><td>QPS for reads and writes, storage per year, bandwidth. Note what dominates.</td></tr>
      <tr><td>3. API</td><td>3–5</td><td>4–6 endpoints with inputs and outputs.</td></tr>
      <tr><td>4. Data model</td><td>3–5</td><td>Main entities, keys, which database and why.</td></tr>
      <tr><td>5. High-level design</td><td>10</td><td>Boxes and arrows for the main flows. Walk one request end to end.</td></tr>
      <tr><td>6. Deep dives</td><td>10–15</td><td>The 1–2 hardest parts: scaling the bottleneck, a tricky algorithm, consistency. Let the interviewer steer.</td></tr>
      <tr><td>7. Wrap-up</td><td>2–3</td><td>Bottlenecks, failure handling, monitoring, what you'd do next.</td></tr>
    </tbody>
  </table></div>
  <h3>Questions to ask in step 1</h3>
  <ul>
    <li>Who are the users and how many (DAU)? Which features matter most?</li>
    <li>Read-heavy or write-heavy? What's the read/write ratio?</li>
    <li>How fresh must data be? Is losing data ever acceptable?</li>
    <li>Latency target? Global or one region? Mobile, web, or both?</li>
  </ul>
</section>

<section id="graded">
  <span class="eyebrow">Scoring</span>
  <h2>What interviewers look for</h2>
  <div class="real"><p>A driving test examiner doesn't only check that you reached the destination. They watch whether you checked mirrors, signaled, and explained what you'd do at a closed road.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Signal</th><th>Strong</th><th>Weak</th></tr></thead>
    <tbody>
      <tr><td>Scoping</td><td>Asks questions, writes requirements, picks a focus</td><td>Starts drawing immediately</td></tr>
      <tr><td>Structure</td><td>Clear steps, working end-to-end design first</td><td>Jumps between details, never finishes</td></tr>
      <tr><td>Trade-offs</td><td>"I'd choose X because…, at the cost of…"</td><td>Lists technologies without reasons</td></tr>
      <tr><td>Depth</td><td>Goes deep on the real bottleneck</td><td>Polishes unimportant parts</td></tr>
      <tr><td>Numbers</td><td>Estimates drive decisions</td><td>No estimates, or estimates never used</td></tr>
      <tr><td>Communication</td><td>Thinks aloud, checks in, adapts to hints</td><td>Silent, defensive about feedback</td></tr>
    </tbody>
  </table></div>
</section>

<section id="cheatsheet">
  <span class="eyebrow">Cheat sheet</span>
  <h2>When you hear this, reach for that</h2>
  <div class="real"><p>A mechanic's diagnostic chart: "squeal when braking → check pads." These pairings cover most design conversations.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Requirement or problem</th><th>Building block</th><th>Page</th></tr></thead>
    <tbody>
      <tr><td>Read-heavy, same data requested often</td><td>Cache (cache-aside + TTL), read replicas</td><td><a href="sd-caching.html">Caching</a></td></tr>
      <tr><td>Static files, global users</td><td>Object storage + CDN</td><td><a href="sd-scaling.html#patterns">Scaling</a></td></tr>
      <tr><td>More traffic than one server</td><td>Stateless servers behind a load balancer, autoscaling</td><td><a href="sd-scaling.html">Scaling</a></td></tr>
      <tr><td>Data too big or too many writes for one DB</td><td>Sharding by a good key, consistent hashing</td><td><a href="sd-data.html#patterns">Databases</a></td></tr>
      <tr><td>Money, inventory, unique names</td><td>SQL with transactions, strong consistency</td><td><a href="sd-data.html#cap">Databases</a></td></tr>
      <tr><td>Huge write volume, simple key access</td><td>Wide-column / key-value store</td><td><a href="sd-data.html#choose">Databases</a></td></tr>
      <tr><td>Slow work, spikes, decoupling</td><td>Message queue / pub/sub, workers</td><td><a href="sd-async.html#patterns">Async</a></td></tr>
      <tr><td>Real-time updates to users</td><td>WebSockets or server-sent events</td><td><a href="sd-async.html#patterns">Async</a></td></tr>
      <tr><td>Abuse, protecting capacity</td><td>Rate limiter (token bucket)</td><td><a href="sd-async.html#patterns">Async</a></td></tr>
      <tr><td>Retries and duplicates</td><td>Idempotency keys</td><td><a href="sd-async.html#patterns">Async</a></td></tr>
      <tr><td>Search, filters, full text</td><td>Search index (inverted index)</td><td><a href="sd-data.html#choose">Databases</a></td></tr>
      <tr><td>Prefix suggestions</td><td>Trie with precomputed top-k</td><td><a href="sd-cases-2.html#autocomplete">Designs II</a></td></tr>
      <tr><td>Nearby places / drivers</td><td>Geohash or quadtree index</td><td><a href="sd-cases-2.html#problems">Designs II</a></td></tr>
      <tr><td>Unique IDs at scale</td><td>Snowflake-style IDs</td><td><a href="sd-reliability.html#patterns">Distributed</a></td></tr>
      <tr><td>Dependencies fail</td><td>Timeouts, retries + backoff, circuit breaker</td><td><a href="sd-reliability.html#patterns">Distributed</a></td></tr>
      <tr><td>"How do you know it works?"</td><td>Metrics, logs, traces, SLOs and alerts</td><td><a href="sd-reliability.html#patterns">Distributed</a></td></tr>
    </tbody>
  </table></div>
</section>

<section id="phrases">
  <span class="eyebrow">Out loud</span>
  <h2>Phrases that show good judgment</h2>
  <div class="real"><p>A tour guide narrates as they walk: "on your left… we're heading here because…" Narration keeps the group with you and shows you know where you're going.</p></div>
  <ul>
    <li>"Let me confirm scope: I'll focus on posting and viewing the feed, and leave out search and ads unless you'd like them."</li>
    <li>"Reads outnumber writes about 100 to 1, so I'll optimize the read path first with a cache."</li>
    <li>"I'll start with one SQL database for simplicity and shard by user_id once we pass a few terabytes."</li>
    <li>"This is eventually consistent: a new post may take a couple of seconds to appear for followers, which fits the requirement."</li>
    <li>"The bottleneck here is the fan-out for celebrities. Two options are… I'd pick the hybrid because…"</li>
    <li>"If this service fails, we degrade gracefully: the feed still loads, without recommendations."</li>
  </ul>
</section>

<section id="mistakes">
  <span class="eyebrow">Avoid these</span>
  <h2>Common mistakes</h2>
  <div class="real"><p>Building a skyscraper's penthouse before pouring the foundation looks impressive for a minute and then falls over.</p></div>
  <ul>
    <li>Skipping requirements and designing the wrong thing.</li>
    <li>Naming technologies ("Kafka, Cassandra, Kubernetes") without saying why.</li>
    <li>Going deep on one detail before an end-to-end design exists.</li>
    <li>Over-engineering a small system (microservices and sharding for 1,000 users).</li>
    <li>Ignoring failure: no replication, no timeouts, single points of failure.</li>
    <li>Never doing math, or doing math and never using the result.</li>
    <li>Not listening: missing the interviewer's hint about what they want to explore.</li>
  </ul>
</section>

<section id="plan">
  <span class="eyebrow">Study plan</span>
  <h2>Four weeks, alongside your DSA plan</h2>
  <div class="real"><p>Learning a language: vocabulary first, then sentences, then real conversations. Don't jump to mock interviews before the building blocks feel familiar.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Week</th><th>Study (about 3 × 45 min)</th><th>Output</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><a href="sd-basics.html">Basics</a> and <a href="sd-scaling.html">Scaling</a></td><td>Redo the photo-app estimate from memory</td></tr>
      <tr><td>2</td><td><a href="sd-caching.html">Caching</a> and <a href="sd-data.html">Databases</a></td><td>Explain cache-aside, sharding and CAP to a friend in plain words</td></tr>
      <tr><td>3</td><td><a href="sd-async.html">APIs and async</a>, <a href="sd-reliability.html">Distributed systems</a></td><td>Design the URL shortener alone, then compare</td></tr>
      <tr><td>4</td><td><a href="sd-cases-1.html">Designs I</a>, <a href="sd-cases-2.html">Designs II</a></td><td>Two timed mock designs out loud (Pramp or a friend)</td></tr>
    </tbody>
  </table></div>
  <p class="note">Further reading: <em>Designing Data-Intensive Applications</em> by Martin Kleppmann (the best book on the topic), Alex Xu's <em>System Design Interview</em> volumes, Google's free <a href="https://sre.google/books/" target="_blank" rel="noopener">SRE books</a>, and the open-source <a href="https://github.com/donnemartin/system-design-primer" target="_blank" rel="noopener">System Design Primer</a>.</p>
</section>
"""

PROBLEMS = [
    ("Basics: redo the photo-app estimate from memory", "sd-basics.html#estimation", "easy", "Seconds/day ≈ 10⁵; reads vs writes; storage per year"),
    ("Scaling: draw an app from 1 server to multi-region", "sd-scaling.html#journey", "easy", "Name the bottleneck at each step"),
    ("Caching: explain four write strategies", "sd-caching.html#patterns", "easy", "Cache-aside, write-through, write-back, write-around"),
    ("Databases: pick a store and shard key for 3 apps", "sd-data.html#choose", "medium", "Match the access pattern"),
    ("Async: design a video upload pipeline", "sd-async.html#deep", "medium", "What's sync, what's queued"),
    ("Distributed: walk through a cascading failure", "sd-reliability.html#deep", "medium", "Timeouts, backoff, breaker, degrade"),
    ("Mock 1: URL shortener, timed and out loud", "sd-cases-1.html#url", "medium", "Use the 7-step framework"),
    ("Mock 2: news feed, timed and out loud", "sd-cases-2.html#feed", "hard", "Hybrid fan-out"),
    ("Mock 3: chat app with a partner asking follow-ups", "sd-cases-2.html#chat", "hard", "Presence, ordering, offline delivery"),
]

META["problems_title"] = "Your system design checklist"
META["problems_intro"] = "Work through these over four weeks. Ticks are saved in this browser and counted on the index page."

QUIZ = [
    dict(lvl="easy", q="What should you do in the first 5 minutes of a design interview?",
         opts=["Draw the architecture", "Clarify requirements and scale", "Pick a database", "Write code"], a=1, why="Scoping prevents designing the wrong system."),
    dict(lvl="easy", q="Which answer shows a trade-off?",
         opts=["\"I'll use Cassandra.\"", "\"I'll use Cassandra for messages because writes are huge and access is by chat ID; we lose easy joins, which we don't need here.\"", "\"Cassandra is popular.\"", "\"Any database works.\""], a=1,
         why="Reason + cost of the choice is what's graded."),
    dict(lvl="easy", q="When should you go into deep dives?", opts=["First", "After an end-to-end high-level design exists", "Never", "Only if asked about code"], a=1, why="Breadth first, then depth on the bottleneck."),
    dict(lvl="medium", q="The interviewer says \"what if traffic grows 100×?\" A good first step?",
         opts=["Rewrite in another language", "Find which component breaks first and propose the cheapest fix for it", "Add microservices everywhere", "Say it's fine"], a=1,
         why="Scaling is about bottlenecks, one at a time."),
    dict(lvl="medium", q="You're designing for 5,000 users total. What's the risk of proposing sharded databases and 12 microservices?",
         opts=["None", "Over-engineering: unnecessary complexity signals poor judgment", "It's too cheap", "It's not scalable"], a=1,
         why="Right-size the design to the requirements, and say what you'd change as it grows."),
    dict(lvl="medium", q="Your estimate shows 50,000 reads/s and 100 writes/s. Which focus follows?",
         opts=["Optimize writes with queues", "Optimize the read path: caching, replicas, CDN", "Shard immediately for writes", "Nothing"], a=1, why="Estimates should drive design decisions."),
    dict(lvl="medium", q="The interviewer hints \"what about users with millions of followers?\" What are they steering you to?",
         opts=["Database indexes", "The fan-out bottleneck (celebrity problem)", "DNS", "Login security"], a=1, why="Follow hints: they point at the part they want to see you reason about."),
    dict(lvl="hard", q="Asked \"how will you know this system is healthy in production?\" The best answer covers:",
         opts=["Unit tests only", "SLIs/SLOs (latency, error rate), dashboards, alerts on user-facing symptoms, logs and traces for debugging", "Asking users", "Restarting servers nightly"], a=1,
         why="Operational thinking is part of a complete design."),
    dict(lvl="hard", q="You realize mid-interview that your earlier data model can't support a requirement. What should you do?",
         opts=["Hope they don't notice", "Say so, explain the issue, and adjust the model", "Start over from scratch silently", "Change the requirement"], a=1,
         why="Catching and correcting your own design is a strong signal."),
    dict(lvl="hard", q="Two choices: strongly consistent reads (slower) or eventually consistent (faster). How do you decide in the interview?",
         opts=["Always strong", "Always eventual", "From the requirement: what's the cost of a stale read here? Money and inventory → strong; likes and feeds → eventual", "Let the database decide"], a=2,
         why="Tie each consistency choice to the product's tolerance for stale data."),
]
