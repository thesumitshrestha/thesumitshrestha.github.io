META = dict(
    title="Heaps", page_title="Heaps · DSA Field Guide", week="Week 8", group="Data structures",
    h1="Heaps and priority queues",
    lead="A heap always hands you the smallest (or largest) item in O(log n), without sorting everything. Whenever a problem says \"top k,\" \"k-th largest,\" \"closest,\" or \"merge sorted,\" think heap.",
    blurb="Min/max heaps, top K, two heaps for medians, merging sorted streams.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A hospital emergency room</h2>
  <div class="real big-real">
    <p>An emergency room doesn't serve patients in arrival order. The most urgent patient is always seen next, and new arrivals slot in according to urgency. Nobody keeps the whole waiting room perfectly sorted; staff only need to know who's most urgent right now. That's a priority queue, and a heap is how it's built.</p>
  </div>
  <p>A <strong>min-heap</strong> is a complete binary tree where every parent is ≤ its children, so the minimum is at the root. It's stored in a plain array: the children of index <code>i</code> are at <code>2i + 1</code> and <code>2i + 2</code>, and its parent is at <code>(i − 1) // 2</code>.</p>
<pre class="diagram">          1                 array: [1, 3, 8, 5, 4]
        /   \               index:  0  1  2  3  4
       3     8
      / \                   children of 1 (index 1): indices 3, 4 → 5, 4
     5   4                  parent of 4 (index 4): (4−1)//2 = 1 → 3</pre>
  <figure class="anim" data-anim="heaps-push"><figcaption>Pushing 5, 3, 8, 1, 4 into a min-heap</figcaption></figure>
  <div class="tbl"><table>
    <thead><tr><th>Operation</th><th>Python (<code>heapq</code>)</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>Peek min</td><td><code>h[0]</code></td><td><span class="pill o1">O(1)</span></td></tr>
      <tr><td>Push</td><td><code>heapq.heappush(h, x)</code></td><td><span class="pill olog">O(log n)</span></td></tr>
      <tr><td>Pop min</td><td><code>heapq.heappop(h)</code></td><td><span class="pill olog">O(log n)</span></td></tr>
      <tr><td>Push then pop (fast)</td><td><code>heapq.heappushpop(h, x)</code></td><td><span class="pill olog">O(log n)</span></td></tr>
      <tr><td>Build from a list</td><td><code>heapq.heapify(lst)</code></td><td><span class="pill on">O(n)</span></td></tr>
      <tr><td>k smallest / largest</td><td><code>heapq.nsmallest(k, xs)</code></td><td><span class="pill onlog">O(n log k)</span></td></tr>
    </tbody>
  </table></div>
  <div class="callout"><p><strong>Python only has a min-heap.</strong> For a max-heap, push negated values (<code>-x</code>) and negate again when popping. For objects, push tuples: <code>(priority, tiebreaker, item)</code>.</p></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Five heap patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Top K with a size-k min-heap</h3><span class="cx">O(n log k) time · O(k) space</span></div>
    <div class="real"><p>A talent show keeps only 3 chairs for finalists. When a new act beats the weakest finalist, the weakest leaves and the new act sits down. The chairs are a min-heap of size 3, so the weakest finalist is always easy to find.</p></div>
    <p class="when"><b>Use when</b>you need the k largest (use a min-heap) or k smallest (use a max-heap) items.</p>
<pre><code><span class="k">import</span> heapq
<span class="k">def</span> find_kth_largest(nums, k):
    h = []
    <span class="k">for</span> x <span class="k">in</span> nums:
        heapq.heappush(h, x)
        <span class="k">if</span> len(h) &gt; k: heapq.heappop(h)     <span class="c"># evict the weakest</span>
    <span class="k">return</span> h[0]                             <span class="c"># k-th largest</span></code></pre>
    <p class="note">Why a <em>min</em>-heap for the largest? Because you need to throw away the smallest of your current top k quickly.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Count, then heap by frequency</h3><span class="cx">O(n log k)</span></div>
    <div class="real"><p>A music app's "your top 5 songs this year": first count plays per song, then keep only the five most played.</p></div>
    <p class="when"><b>Use when</b>the ranking is by how often something appears.</p>
<pre><code><span class="k">from</span> collections <span class="k">import</span> Counter
<span class="k">def</span> top_k_frequent(nums, k):
    cnt = Counter(nums)
    <span class="k">return</span> heapq.nlargest(k, cnt.keys(), key=cnt.get)</code></pre>
    <p class="note">O(n) alternative: bucket sort by frequency (index = count, holding the values with that count), then read buckets from high to low.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. K-way merge</h3><span class="cx">O(N log k), N = total items</span></div>
    <div class="real"><p>Merging k sorted checkout lines into one: look only at the person at the front of each line, send the earliest arrival through, and the next person in that line steps up. The heap holds just the k front-runners.</p></div>
    <p class="when"><b>Use when</b>merging k sorted lists, k-th smallest in a sorted matrix, or smallest pairs across arrays.</p>
<pre><code><span class="k">def</span> merge_k_lists(lists):
    h = [(node.val, i, node) <span class="k">for</span> i, node <span class="k">in</span> enumerate(lists) <span class="k">if</span> node]
    heapq.heapify(h)
    dummy = tail = ListNode()
    <span class="k">while</span> h:
        _, i, node = heapq.heappop(h)          <span class="c"># i breaks ties (nodes aren't comparable)</span>
        tail.next = tail = node
        <span class="k">if</span> node.next: heapq.heappush(h, (node.next.val, i, node.next))
    <span class="k">return</span> dummy.next</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Two heaps for a running median</h3><span class="cx">O(log n) add · O(1) median</span></div>
    <div class="real"><p>Splitting a class into a short half and a tall half for a photo. The tallest of the short half and the shortest of the tall half stand in the middle. Each new student joins one half, and if the halves get uneven, one person switches sides.</p></div>
    <p class="when"><b>Use when</b>you need the median of a growing stream.</p>
<pre><code><span class="k">class</span> MedianFinder:
    <span class="k">def</span> __init__(self):
        self.lo, self.hi = [], []          <span class="c"># lo: max-heap (negated), hi: min-heap</span>
    <span class="k">def</span> addNum(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))   <span class="c"># keep lo ≤ hi</span>
        <span class="k">if</span> len(self.hi) &gt; len(self.lo):                     <span class="c"># rebalance</span>
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
    <span class="k">def</span> findMedian(self):
        <span class="k">if</span> len(self.lo) &gt; len(self.hi): <span class="k">return</span> -self.lo[0]
        <span class="k">return</span> (-self.lo[0] + self.hi[0]) / 2</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Greedy scheduling with a heap</h3><span class="cx">O(n log n)</span></div>
    <div class="real"><p>A barista with a cooldown rule (the same drink can't be made twice in a row within n orders) always makes the most-ordered drink that's allowed right now, so the long queue for lattes doesn't end up stuck at the end.</p></div>
    <p class="when"><b>Use when</b>you repeatedly pick the "biggest remaining" item under a constraint (Task Scheduler, Reorganize String, meeting rooms).</p>
<pre><code><span class="k">def</span> reorganize_string(s):
    h = [(-c, ch) <span class="k">for</span> ch, c <span class="k">in</span> Counter(s).items()]
    heapq.heapify(h)
    out, prev = [], None                      <span class="c"># prev = item cooling down</span>
    <span class="k">while</span> h:
        c, ch = heapq.heappop(h)
        out.append(ch)
        <span class="k">if</span> prev: heapq.heappush(h, prev)
        prev = (c + 1, ch) <span class="k">if</span> c + 1 &lt; 0 <span class="k">else</span> None
    <span class="k">return</span> "".join(out) <span class="k">if</span> len(out) == len(s) <span class="k">else</span> ""</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Kth Largest: heap vs sort vs quickselect</h2>
  <div class="real"><p>Finding the 10th fastest runner among 50,000 marathon finishers. You could rank everyone (sort), keep a short list of the 10 fastest so far (heap), or repeatedly split the field around a random runner's time until the 10th lands in place (quickselect).</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Approach</th><th>Time</th><th>Space</th><th>When to pick it</th></tr></thead>
    <tbody>
      <tr><td>Sort and index</td><td>O(n log n)</td><td>O(n) or O(1)</td><td>Simplest; fine as a first answer</td></tr>
      <tr><td>Size-k min-heap</td><td>O(n log k)</td><td>O(k)</td><td>Streaming data, or k much smaller than n</td></tr>
      <tr><td>Quickselect</td><td>O(n) average, O(n²) worst</td><td>O(1)</td><td>One-off query on an array you may modify</td></tr>
    </tbody>
  </table></div>
  <div class="google"><p>Give the heap answer, then mention quickselect and its worst case. Saying "if the data were a stream, only the heap works" shows you're thinking about real systems, which Google values.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases and pitfalls</h2>
  <div class="real"><p>In an ER, two patients with the same urgency still need a fair rule for who goes first. Heaps need tie-breakers too.</p></div>
  <ul>
    <li>Tuples with equal priorities compare the next field; if that's an uncomparable object, Python raises <code>TypeError</code>. Add an index tiebreaker.</li>
    <li>Forgetting to negate for a max-heap, or negating only on push.</li>
    <li>k larger than n, or k = 0.</li>
    <li><code>h[0]</code> on an empty heap raises <code>IndexError</code>.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Last Stone Weight", "last-stone-weight", "easy", "Max-heap via negation"),
    ("Kth Largest Element in a Stream", "kth-largest-element-in-a-stream", "easy", "Size-k min-heap"),
    ("Kth Largest Element in an Array", "kth-largest-element-in-an-array", "medium", "Size-k min-heap or quickselect"),
    ("Top K Frequent Elements", "top-k-frequent-elements", "medium", "Counter + heap or buckets"),
    ("K Closest Points to Origin", "k-closest-points-to-origin", "medium", "Size-k max-heap by distance"),
    ("Task Scheduler", "task-scheduler", "medium", "Greedy by frequency (or formula)"),
    ("Reorganize String", "reorganize-string", "medium", "Max-heap + cooldown slot"),
    ("Find K Pairs with Smallest Sums", "find-k-pairs-with-smallest-sums", "medium", "K-way merge"),
    ("Find Median from Data Stream", "find-median-from-data-stream", "hard", "Two heaps"),
    ("Merge k Sorted Lists", "merge-k-sorted-lists", "hard", "K-way merge with tiebreaker"),
]

QUIZ = [
    dict(lvl="easy", q="Where is the smallest element in a min-heap stored?",
         opts=["The last index", "Index 0 (the root)", "A random index", "The middle"], a=1, why="The heap property puts the minimum at the root, `h[0]`."),
    dict(lvl="easy", q="How do you get max-heap behavior with Python's `heapq`?",
         opts=["`heapq.maxheap()`", "Push negated values and negate when popping", "Sort descending first", "Use `reverse=True`"], a=1,
         why="heapq is min-only. Negating flips the order."),
    dict(lvl="easy", q="Index of the left child of the node at index 3?",
         opts=["4", "6", "7", "8"], a=2, why="Left child = 2i + 1 = 7; right child = 8."),
    dict(lvl="medium", q="Why does `heapify` run in O(n), not O(n log n)?",
         opts=["It doesn't", "Most nodes are near the bottom and sift down only a few levels; the total work sums to O(n)", "It uses sorting", "Python caches it"], a=1,
         why="Half the nodes are leaves (0 work), a quarter sift 1 level, and so on. The series converges to O(n)."),
    dict(lvl="medium", q="K Closest Points: which heap and what size?",
         opts=["Min-heap of all n points, pop k", "Max-heap (by distance) of size k, evicting the farthest", "Min-heap of size 1", "No heap; binary search"], a=1,
         why="Keeping k closest means evicting the farthest quickly: a max-heap of size k, O(n log k). (Popping k from a full min-heap also works: O(n + k log n).)"),
    dict(lvl="medium", q="What breaks here when two nodes have the same value?", code="heapq.heappush(h, (node.val, node))",
         opts=["Nothing", "Python compares the ListNode objects to break the tie and raises TypeError", "The heap loses one node", "It becomes a max-heap"], a=1,
         why="Add a unique tiebreaker: `(node.val, i, node)` or a counter."),
    dict(lvl="medium", q="Running median after adding 5, 2, 8:",
         opts=["2", "5", "8", "5.0 from (2+8)/2"], a=1, why="Sorted: 2, 5, 8. Odd count, so the middle value 5. The max-heap side holds the extra element."),
    dict(lvl="hard", q="Top K Frequent in O(n): what replaces the heap?",
         opts=["Quickselect only", "Bucket sort: an array indexed by frequency (max n), then read from high to low", "Binary search", "A trie"], a=1,
         why="Frequencies are bounded by n, so they can be array indices. No comparisons needed."),
    dict(lvl="hard", q="Merging k sorted lists of total size N: why is a heap better than merging pairs one after another?",
         opts=["Pairwise merging is O(N·k); the heap is O(N log k)", "Heaps use less memory always", "Pairwise is incorrect", "They're the same"], a=0,
         why="Merging list 1 with 2, then the result with 3, etc. re-copies early items k times. Divide-and-conquer pairing also reaches O(N log k)."),
    dict(lvl="hard", q="Interviewer: \"Data arrives as an endless stream; report the 100 largest seen so far.\" Best fit?",
         opts=["Sort everything each time", "A size-100 min-heap: O(log 100) per item, O(100) memory", "Quickselect on the whole stream", "A hash set"], a=1,
         why="You can't store or re-sort an endless stream. A bounded heap keeps exactly what matters."),
]
