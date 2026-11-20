META = dict(
    title="SD 3: Caching", page_title="Caching · DSA + System Design Guide", week="System design · Core", group="System design",
    h1="Caching",
    lead="A cache keeps a copy of popular data somewhere faster than its source. It's the single biggest performance win in most designs, and its two hard problems are keeping copies fresh and deciding what to throw away.",
    blurb="Cache layers, cache-aside and write strategies, LRU eviction, TTL, invalidation, stampedes, hot keys.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>The fridge, the pantry, and the supermarket</h2>
  <div class="real big-real">
    <p>Milk is in your fridge (seconds away), rice is in the pantry (a minute), and everything else is at the supermarket (30 minutes). You keep what you use most in the closest, smallest place. A cache is your fridge: small, fast, and you have to notice when the milk goes off (stale data) and throw things out when it's full (eviction).</p>
  </div>
  <div class="tbl"><table>
    <thead><tr><th>Cache layer</th><th>Where</th><th>Example</th></tr></thead>
    <tbody>
      <tr><td>Browser cache</td><td>User's device</td><td>Logo image saved for a week</td></tr>
      <tr><td>CDN</td><td>Edge servers in cities</td><td>Video segments, JS bundles</td></tr>
      <tr><td>Load balancer / gateway</td><td>Front door</td><td>Cached public API responses</td></tr>
      <tr><td>Application cache</td><td>Redis / Memcached cluster</td><td>User profiles, feed lists, sessions</td></tr>
      <tr><td>Database cache</td><td>Inside the DB</td><td>Buffer pool of hot pages</td></tr>
    </tbody>
  </table></div>
  <p class="note">Rule of thumb: about 20% of the data gets about 80% of the reads, so caching a small slice of hot data removes most of the load.</p>
</section>

<section id="patterns">
  <span class="eyebrow">Strategies</span>
  <h2>Five caching strategies</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Cache-aside (lazy loading)</h3><span class="cx">Most common</span></div>
    <div class="real"><p>A receptionist who doesn't know a phone number checks the big directory, then writes it on a sticky note by the phone. Next time it's on the note. Nobody writes notes in advance for numbers no one asks for.</p></div>
    <p class="when"><b>How</b>the app checks the cache; on a miss it reads the database and fills the cache. Writes go to the database and <em>delete</em> the cache entry.</p>
<pre><code><span class="k">def</span> get_user(uid):
    user = cache.get(f"user:{uid}")
    <span class="k">if</span> user <span class="k">is</span> None:                       <span class="c"># miss</span>
        user = db.query("SELECT * FROM users WHERE id=%s", uid)
        cache.set(f"user:{uid}", user, ttl=3600)
    <span class="k">return</span> user

<span class="k">def</span> update_user(uid, data):
    db.update(uid, data)
    cache.delete(f"user:{uid}")               <span class="c"># next read refills it</span></code></pre>
    <figure class="anim" data-anim="sd-cache"><figcaption>An LRU cache with room for three items</figcaption></figure>
    <p class="note">Pros: only caches what's used; a cache crash just means slower reads. Cons: the first read is slow; data can be stale until TTL or delete.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Write-through</h3><span class="cx">Cache always fresh</span></div>
    <div class="real"><p>A shop that updates the price tag on the shelf and the price in the computer at the same moment. Both always agree, but every price change takes a little longer.</p></div>
    <p class="when"><b>How</b>every write goes to the cache and the database together. Reads are always fresh. Writes are slower, and you may cache data nobody reads.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Write-back (write-behind)</h3><span class="cx">Fastest writes, risk of loss</span></div>
    <div class="real"><p>Writing notes on a whiteboard during a meeting and typing them up later. Very fast in the moment, but if someone wipes the board before you type them, they're gone.</p></div>
    <p class="when"><b>How</b>writes go to the cache, which flushes to the database later in batches. Great for counters like view counts and likes; risky for money or anything you can't lose.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Write-around</h3><span class="cx">Don't cache what won't be reread</span></div>
    <div class="real"><p>Filing old tax records straight into the archive box rather than on your desk, because you probably won't look at them again soon.</p></div>
    <p class="when"><b>How</b>writes skip the cache and go straight to the database; the cache fills only on reads. Good for logs, uploads and data written once and rarely read.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Read-through</h3><span class="cx">Cache does the loading</span></div>
    <div class="real"><p>A library assistant who fetches a book from storage when you ask at the desk. You only ever talk to the desk; you never go to storage yourself.</p></div>
    <p class="when"><b>How</b>like cache-aside, but the cache library loads from the database on a miss, so app code only talks to the cache.</p>
  </article>
</section>

<section id="eviction">
  <span class="eyebrow">Eviction</span>
  <h2>What to throw out when the cache is full</h2>
  <div class="real"><p>A full closet. You could toss whatever you haven't worn longest (LRU), whatever you wear least often (LFU), or the oldest thing you bought (FIFO). Most people use LRU without thinking about it.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Policy</th><th>Evicts</th><th>Good for</th></tr></thead>
    <tbody>
      <tr><td>LRU (least recently used)</td><td>Item untouched for longest</td><td>Most workloads; the default</td></tr>
      <tr><td>LFU (least frequently used)</td><td>Item used least often</td><td>Stable popularity (top songs)</td></tr>
      <tr><td>FIFO</td><td>Oldest inserted</td><td>Simple, rarely the best</td></tr>
      <tr><td>TTL (time to live)</td><td>Anything past its expiry</td><td>Bounding staleness; combine with LRU</td></tr>
    </tbody>
  </table></div>
  <p>An LRU cache is the classic coding question too: a hashmap for O(1) lookup plus a doubly linked list for O(1) "move to front" and "remove oldest." See <a href="linked-lists.html#deep">Linked lists</a>.</p>
</section>

<section id="hard">
  <span class="eyebrow">Hard parts</span>
  <h2>Invalidation, stampedes, and hot keys</h2>
  <div class="real"><p>A famous joke says there are two hard things in computer science: cache invalidation and naming things. Like a printed train timetable, a cached copy is useful until the schedule changes and nobody reprints it.</p></div>
  <div class="trace">
    <div><p><strong>Stale data.</strong> Use a TTL as a safety net, and delete (not update) the cache entry on writes. Deleting avoids a race where two writers leave the older value in the cache.</p></div>
    <div><p><strong>Cache stampede (thundering herd).</strong> A popular key expires and 10,000 requests all miss at once and hammer the database. Fixes: a lock so only one request refills while others wait or get the old value; refresh before expiry; add random jitter to TTLs so keys don't all expire together.</p></div>
    <div><p><strong>Hot keys.</strong> One key (a celebrity's profile, the World Cup final score) gets so many reads that its single cache node melts. Fixes: replicate that key to several nodes, add a tiny in-process cache on each app server, or split it into <code>key#1…key#10</code>.</p></div>
    <div><p><strong>Cold start.</strong> After a restart the cache is empty and everything misses. Warm it with known-popular keys, or bring nodes back gradually.</p></div>
    <div><p><strong>Cache penetration.</strong> Requests for keys that don't exist always miss and hit the database. Cache the "not found" result briefly, or use a Bloom filter.</p></div>
  </div>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>How much does a cache help?</h2>
  <div class="real"><p>If 9 out of 10 shopping trips are just to the fridge, your average trip is about 3 minutes instead of 30, even though the supermarket didn't get any closer.</p></div>
  <p>Average latency = hit rate × cache time + miss rate × (cache time + database time).</p>
  <div class="tbl"><table>
    <thead><tr><th>Hit rate</th><th>Avg latency (cache 1 ms, DB 20 ms)</th><th>DB queries/s for 50,000 reads/s</th></tr></thead>
    <tbody>
      <tr><td>0%</td><td>20 ms (no cache)</td><td>50,000</td></tr>
      <tr><td>80%</td><td>0.8 + 0.2 × 21 = 5.0 ms</td><td>10,000</td></tr>
      <tr><td>95%</td><td>0.95 + 0.05 × 21 = 2.0 ms</td><td>2,500</td></tr>
      <tr><td>99%</td><td>0.99 + 0.01 × 21 = 1.2 ms</td><td>500</td></tr>
    </tbody>
  </table></div>
  <p>Going from 95% to 99% hits cuts database load 5×. That's why teams fight for every point of hit rate.</p>
  <div class="google"><p>When you add a cache in an interview, say four things: what's cached and its key, the strategy (usually cache-aside), the TTL, and how writes invalidate it. Then mention stampede protection. That's a complete answer.</p></div>
</section>
"""

QUIZ = [
    dict(lvl="easy", q="Why does caching make reads faster?",
         opts=["It compresses data", "It keeps a copy in fast memory closer to the app than the database", "It deletes old data", "It encrypts data"], a=1, why="Memory over the local network (~1 ms) beats a database query (~10+ ms)."),
    dict(lvl="easy", q="In cache-aside, what happens on a cache miss?",
         opts=["Return an error", "Read from the database, then store it in the cache", "Wait for the cache to refill itself", "Read from the CDN"], a=1, why="Lazy loading: fetch from the source of truth, then populate the cache."),
    dict(lvl="easy", q="LRU evicts the item that was…",
         opts=["Inserted first", "Used least recently", "Used least often", "Largest"], a=1, why="Least Recently Used."),
    dict(lvl="medium", q="Why delete the cache entry on update instead of writing the new value into it?",
         opts=["Deleting is faster", "It avoids races where a slower writer leaves an older value in the cache", "Caches can't be updated", "It saves memory"], a=1,
         why="Two concurrent updates can finish in a different order in the cache than in the DB. Deleting makes the next read fetch the truth."),
    dict(lvl="medium", q="View counters on videos need very fast writes and can tolerate losing a few counts. Best strategy?",
         opts=["Write-through", "Write-back (batch flush to DB)", "No cache", "Write-around"], a=1, why="Write-back absorbs huge write volume; a few lost increments are acceptable."),
    dict(lvl="medium", q="What's a TTL for?",
         opts=["Encrypting keys", "Making entries expire after a set time, bounding staleness", "Choosing which server holds a key", "Compressing values"], a=1, why="Time To Live caps how old cached data can get."),
    dict(lvl="medium", q="Hit rate 95%, cache 1 ms, database 20 ms (a miss costs both). Average read latency?",
         opts=["~1 ms", "~2 ms", "~10 ms", "~20 ms"], a=1, why="0.95 × 1 + 0.05 × 21 ≈ 2 ms."),
    dict(lvl="hard", q="A trending video's cache key expires and 20,000 requests hit the database at once. What is this, and one fix?",
         opts=["Hot partition; add disks", "Cache stampede; let one request rebuild under a lock while others serve the old value", "Replication lag; read from leader", "Cold start; restart the cache"], a=1,
         why="Also: refresh before expiry, and jitter TTLs so keys don't expire together."),
    dict(lvl="hard", q="One key gets 2 million reads/s and overloads its Redis node. Which helps most?",
         opts=["Increase its TTL", "Replicate the key (key#1..#N across nodes) or add a small local cache on each app server", "Switch to write-through", "Move it to the database"], a=1,
         why="A hot key is limited by one node's capacity; spread its reads."),
    dict(lvl="hard", q="Attackers request random user IDs that don't exist, so every request misses and hits the DB. Fix?",
         opts=["Bigger cache", "Cache 'not found' briefly or check a Bloom filter of valid IDs first", "Longer TTL on real keys", "Turn off the cache"], a=1,
         why="This is cache penetration. Negative caching or a Bloom filter stops misses for keys that can't exist."),
]
