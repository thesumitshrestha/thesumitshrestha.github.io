META = dict(
    title="SD 6: Distributed systems", page_title="Distributed Systems · DSA + System Design Guide", week="System design · Advanced", group="System design",
    h1="Distributed systems and reliability",
    lead="Once a system runs on thousands of machines, something is always broken. Advanced design is about expecting failure: timeouts, retries, circuit breakers, quorums, consensus, unique IDs, distributed transactions, and monitoring that tells you what went wrong.",
    blurb="Failure handling, retries with backoff, circuit breakers, quorums, consensus, unique IDs, sagas, observability.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>Planning a group trip by text message</h2>
  <div class="real big-real">
    <p>Ten friends plan a trip over group chat. Some messages arrive late, some phones die, and two people book different hotels because they didn't see each other's message. Nobody can be sure everyone has read the latest plan. Distributed systems have exactly these problems: messages are slow or lost, machines crash, clocks disagree, and there's no single moment when everyone knows the same thing.</p>
  </div>
  <h3>The fallacies of distributed computing</h3>
  <p>Beginners assume these are true. All of them are false:</p>
  <ul>
    <li>The network is reliable, and latency is zero.</li>
    <li>Bandwidth is infinite, and the network is secure.</li>
    <li>Nothing changes (topology), and there's one administrator.</li>
    <li>Transport cost is zero, and the network is uniform.</li>
  </ul>
</section>

<section id="patterns">
  <span class="eyebrow">Techniques</span>
  <h2>Eight techniques for staying up</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Timeouts</h3><span class="cx">Never wait forever</span></div>
    <div class="real"><p>If a friend doesn't reply to "dinner at 7?" by 6:30, you make other plans. Without a deadline you'd sit there all night.</p></div>
    <p class="when"><b>Rule</b>every network call gets a timeout, set from the dependency's normal p99 latency. A slow dependency without timeouts ties up all your threads and takes you down with it.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Retries with exponential backoff and jitter</h3><span class="cx">Retry politely</span></div>
    <div class="real"><p>Calling a busy restaurant: try again in 1 minute, then 2, then 4. If 1,000 people all redial at exactly the same second, the line stays jammed, so everyone waits a slightly random extra amount.</p></div>
    <p class="when"><b>Use for</b>temporary errors (timeouts, 503). Only retry idempotent operations, cap the attempts, and add randomness so clients don't retry in sync (a "retry storm").</p>
<pre><code><span class="k">import</span> random, time
<span class="k">def</span> call_with_retry(fn, attempts=5, base=0.1, cap=5.0):
    <span class="k">for</span> i <span class="k">in</span> range(attempts):
        <span class="k">try</span>:
            <span class="k">return</span> fn()
        <span class="k">except</span> TransientError:
            <span class="k">if</span> i == attempts - 1: <span class="k">raise</span>
            time.sleep(random.uniform(0, min(cap, base * 2 ** i)))   <span class="c"># full jitter</span></code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Circuit breaker</h3><span class="cx">Fail fast, let it recover</span></div>
    <div class="real"><p>The breaker in your home's fuse box cuts power when something shorts, so the wires don't catch fire. You reset it once the fault is fixed.</p></div>
    <p class="when"><b>Use</b>around calls to dependencies that can fail. After repeated failures, stop calling for a while and return a fallback, giving the dependency room to recover.</p>
    <figure class="anim" data-anim="sd-circuit"><figcaption>Closed → open → half-open → closed</figcaption></figure>
    <p class="note">Related: <strong>bulkheads</strong> (separate thread pools per dependency, like watertight compartments in a ship) and <strong>graceful degradation</strong> (show the feed without recommendations rather than an error page).</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Quorums (N, R, W)</h3><span class="cx">Tunable consistency</span></div>
    <div class="real"><p>A club with 5 board members. A decision needs 3 signatures (W = 3), and to check the latest decision you ask any 3 members (R = 3). Since 3 + 3 &gt; 5, at least one person you ask signed the latest decision.</p></div>
    <p class="when"><b>Rule</b>with N replicas, a write waits for W acknowledgements and a read asks R replicas. If <strong>R + W &gt; N</strong>, every read overlaps the latest write. Common: N = 3, W = 2, R = 2. Lower W or R for speed at the cost of consistency.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Leader election and consensus</h3><span class="cx">Agreeing despite failures</span></div>
    <div class="real"><p>A class electing a class president. Once a majority votes for someone, that's the president, even if a few students were absent. If the president leaves, a new vote happens. Two presidents at once would be chaos, so you always need a majority.</p></div>
    <p class="when"><b>Use</b>when nodes must agree on one value: who's the leader, the order of log entries, a configuration. <strong>Raft</strong> and <strong>Paxos</strong> do this with a majority of nodes (so 5 nodes tolerate 2 failures). In practice you use a system built on them (etcd, ZooKeeper, Chubby at Google, Spanner) rather than writing your own.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. Unique ID generation</h3><span class="cx">IDs without a central counter</span></div>
    <div class="real"><p>Tickets at a deli with many counters. Instead of everyone sharing one ticket machine, each counter prints "counter number + time + its own count," so numbers never clash and still roughly sort by time.</p></div>
    <p class="when"><b>Options</b>a database auto-increment (simple, a bottleneck at scale); UUIDs (no coordination, 128 bits, not sortable); <strong>Snowflake-style</strong> 64-bit IDs = timestamp + machine ID + per-millisecond sequence (sortable by time, no coordination).</p>
<pre class="diagram"> 41 bits: milliseconds since epoch │ 10 bits: machine │ 12 bits: sequence
 ≈ 69 years                         │ 1,024 machines   │ 4,096 IDs/ms per machine</pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>7. Distributed transactions: 2PC and sagas</h3><span class="cx">Changes across services</span></div>
    <div class="real"><p>Booking a trip with a flight, hotel and car. Two-phase commit is a travel agent who asks all three "can you hold it?" and only says "book it" if all agree. A saga books each one in turn, and if the car rental fails, it cancels the hotel and flight (compensating actions).</p></div>
    <p class="when"><b>2PC</b>gives atomicity but blocks if the coordinator dies, and is slow across services. <b>Sagas</b> are the usual microservice answer: a sequence of local transactions, each with an undo step. Pair with the <strong>outbox pattern</strong> (write the event into the same database transaction, publish it afterwards) so events are never lost.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>8. Observability</h3><span class="cx">Know what's broken before users tell you</span></div>
    <div class="real"><p>A car dashboard: the speedometer and fuel gauge (metrics), the trip computer's history (logs), and a mechanic's diagnostic trace of exactly which part misfired (traces).</p></div>
    <div class="tbl"><table>
      <thead><tr><th>Signal</th><th>Answers</th><th>Example</th></tr></thead>
      <tbody>
        <tr><td>Metrics</td><td>Is something wrong?</td><td>Error rate, p99 latency, QPS, CPU</td></tr>
        <tr><td>Logs</td><td>What happened in this event?</td><td>"payment 81 failed: card declined"</td></tr>
        <tr><td>Traces</td><td>Where did the time go across services?</td><td>Request spent 400 ms waiting on the recommendation service</td></tr>
      </tbody>
    </table></div>
    <p class="note">Google's SRE practice: define <strong>SLIs</strong> (what you measure, e.g. % of requests under 300 ms), <strong>SLOs</strong> (the target, e.g. 99.9%), and an <strong>error budget</strong> (the 0.1% you're allowed to fail, which you can "spend" on risky launches). Alert on symptoms users feel, not on every CPU blip.</p>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>A cascading failure, and how each technique stops it</h2>
  <div class="real"><p>One stalled car on a highway causes a jam that spreads miles back, blocking on-ramps and side streets that had nothing to do with the original problem.</p></div>
  <div class="trace">
    <div><p><strong>Trigger:</strong> the recommendations service slows from 50 ms to 5 s after a bad deploy.</p></div>
    <div><p><strong>Spread:</strong> the feed service waits on it with no timeout. Its threads fill up, so even requests that don't need recommendations queue up. <em>Fix: timeouts.</em></p></div>
    <div><p><strong>Amplify:</strong> clients see errors and retry immediately, tripling traffic. <em>Fix: backoff with jitter, retry budgets.</em></p></div>
    <div><p><strong>Collapse:</strong> the overloaded recommendations service can never recover because traffic never stops. <em>Fix: circuit breaker, load shedding (reject low-priority requests early).</em></p></div>
    <div><p><strong>Better outcome:</strong> the breaker opens, the feed shows posts without recommendations (graceful degradation), alerts fire on the SLO, and the deploy is rolled back.</p></div>
  </div>
  <div class="google"><p>For L4, you don't need to explain Paxos. You do need to say "timeouts, retries with backoff, idempotency, replication, and monitoring" naturally whenever you add a network call to your design.</p></div>
</section>

<section id="google">
  <span class="eyebrow">Worth knowing</span>
  <h2>Google systems interviewers may mention</h2>
  <div class="real"><p>Knowing these is like a chef knowing the classic dishes: you won't cook them in the interview, but recognizing them helps you follow the conversation.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>System</th><th>What it is</th><th>Public equivalent</th></tr></thead>
    <tbody>
      <tr><td>GFS / Colossus</td><td>Distributed file system for huge files</td><td>HDFS, S3</td></tr>
      <tr><td>Bigtable</td><td>Wide-column store, sorted by row key</td><td>HBase, Cassandra</td></tr>
      <tr><td>Spanner</td><td>Globally distributed SQL with strong consistency (TrueTime clocks)</td><td>CockroachDB</td></tr>
      <tr><td>MapReduce</td><td>Batch processing by map and reduce steps</td><td>Hadoop, Spark</td></tr>
      <tr><td>Chubby</td><td>Lock service and leader election (Paxos)</td><td>ZooKeeper, etcd</td></tr>
      <tr><td>Borg</td><td>Cluster scheduler running everything</td><td>Kubernetes (its descendant)</td></tr>
      <tr><td>Pub/Sub</td><td>Global messaging</td><td>Kafka, SNS/SQS</td></tr>
    </tbody>
  </table></div>
</section>
"""

QUIZ = [
    dict(lvl="easy", q="Why should every network call have a timeout?",
         opts=["To save bandwidth", "So a slow dependency can't hold your threads forever", "Timeouts make calls faster", "HTTP requires them"], a=1, why="Without timeouts, one slow service drags down everything that calls it."),
    dict(lvl="easy", q="What does a circuit breaker do after many failures?",
         opts=["Retries faster", "Stops calling the failing service for a while and fails fast", "Deletes the service", "Doubles traffic"], a=1, why="It gives the dependency time to recover and keeps callers responsive."),
    dict(lvl="easy", q="Logs, metrics and traces are together called:", opts=["Sharding", "Observability", "Caching", "Consensus"], a=1, why="They let you see what a running system is doing."),
    dict(lvl="medium", q="Why add random jitter to retry delays?",
         opts=["To make retries slower for fun", "So thousands of clients don't retry at the same moment and re-overload the server", "To encrypt requests", "It's required by TCP"], a=1, why="Synchronized retries create repeated traffic spikes."),
    dict(lvl="medium", q="N = 3 replicas. Which (R, W) guarantees reads see the latest write?",
         opts=["R=1, W=1", "R=1, W=2", "R=2, W=2", "R=0, W=3"], a=2, why="R + W must exceed N: 2 + 2 = 4 > 3."),
    dict(lvl="medium", q="Why are Snowflake-style IDs preferred over a single auto-increment database at scale?",
         opts=["They're shorter", "Each machine generates unique, time-sortable IDs without a central bottleneck", "They're random", "They're encrypted"], a=1, why="Timestamp + machine ID + sequence avoids coordination."),
    dict(lvl="medium", q="A 5-node Raft cluster can keep working with how many failed nodes?", opts=["0", "1", "2", "4"], a=2, why="It needs a majority (3 of 5), so it tolerates 2 failures."),
    dict(lvl="hard", q="An order flow spans payment, inventory and shipping services. Shipping fails after payment succeeded. Microservice-friendly fix?",
         opts=["Two-phase commit across all services", "A saga: run compensating actions (release inventory, refund payment)", "Retry shipping forever", "Ignore it"], a=1,
         why="Sagas trade atomicity for availability, undoing completed steps when a later one fails."),
    dict(lvl="hard", q="A service updates its database then publishes an event, but sometimes crashes in between, so the event is lost. Standard fix?",
         opts=["Publish first, then write", "Outbox pattern: write the event to an outbox table in the same transaction, then a relay publishes it", "Use a bigger server", "Disable retries"], a=1,
         why="The database transaction makes the state change and the pending event atomic."),
    dict(lvl="hard", q="Your SLO is 99.9% of requests succeed per month. You've already failed 0.08% this month. What does the error budget suggest?",
         opts=["Launch risky features freely", "Most of the budget is spent; slow down risky launches and focus on reliability", "Lower the SLO", "Nothing"], a=1,
         why="Only 0.02% remains. Error budgets turn reliability into an explicit decision about launch risk."),
]
