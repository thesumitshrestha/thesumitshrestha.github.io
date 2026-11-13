META = dict(
    title="Sorting", page_title="Sorting · DSA Field Guide", week="Week 11", group="Algorithms",
    h1="Sorting",
    lead="You'll rarely write a sort from scratch in an interview, but you must know how merge sort and quicksort work, what O(n log n) costs, and when sorting first turns a hard problem into an easy one.",
    blurb="Merge sort, quicksort, counting/bucket sort, intervals, custom comparators.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>Putting a hand of cards in order</h2>
  <div class="real big-real">
    <p>You can sort cards three ways. <strong>Insertion:</strong> pick up one card at a time and slide it into place (fine for a hand of 7, slow for a deck). <strong>Merge:</strong> split the deck between friends, each sorts their half, then you merge the two sorted piles by always taking the smaller top card. <strong>Quick:</strong> pick a card, toss smaller cards left and bigger right, then repeat on each side. The last two are O(n log n), the best possible when you can only compare cards.</p>
  </div>
  <div class="tbl"><table>
    <thead><tr><th>Algorithm</th><th>Best</th><th>Average</th><th>Worst</th><th>Space</th><th>Stable?</th></tr></thead>
    <tbody>
      <tr><td>Bubble / selection</td><td>O(n)/O(n²)</td><td><span class="pill on2">O(n²)</span></td><td>O(n²)</td><td>O(1)</td><td>Bubble yes, selection no</td></tr>
      <tr><td>Insertion</td><td>O(n)</td><td><span class="pill on2">O(n²)</span></td><td>O(n²)</td><td>O(1)</td><td>Yes</td></tr>
      <tr><td>Merge sort</td><td>O(n log n)</td><td><span class="pill onlog">O(n log n)</span></td><td>O(n log n)</td><td>O(n)</td><td>Yes</td></tr>
      <tr><td>Quicksort</td><td>O(n log n)</td><td><span class="pill onlog">O(n log n)</span></td><td>O(n²)</td><td>O(log n)</td><td>No</td></tr>
      <tr><td>Heap sort</td><td>O(n log n)</td><td><span class="pill onlog">O(n log n)</span></td><td>O(n log n)</td><td>O(1)</td><td>No</td></tr>
      <tr><td>Counting / bucket</td><td>O(n + k)</td><td><span class="pill on">O(n + k)</span></td><td>O(n + k)</td><td>O(n + k)</td><td>Yes</td></tr>
      <tr><td>Python <code>sort()</code> (Timsort)</td><td>O(n)</td><td><span class="pill onlog">O(n log n)</span></td><td>O(n log n)</td><td>O(n)</td><td>Yes</td></tr>
    </tbody>
  </table></div>
  <div class="real"><p><strong>Stable</strong> means equal items keep their original order. Sort a spreadsheet by city, then (stably) by state, and cities stay alphabetized inside each state. That's why stable sorts matter.</p></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Six sorting patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Merge sort (divide and conquer)</h3><span class="cx">O(n log n) · O(n) space</span></div>
    <div class="real"><p>Two librarians each alphabetize half the returned books, then one merges both carts by always shelving whichever cart's front book comes first.</p></div>
    <p class="when"><b>Use when</b>you need a guaranteed O(n log n) stable sort, sorting a linked list, or counting inversions ("how many pairs are out of order") during the merge.</p>
<pre><code><span class="k">def</span> merge_sort(a):
    <span class="k">if</span> len(a) &lt;= 1: <span class="k">return</span> a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    <span class="k">while</span> i &lt; len(left) <span class="k">and</span> j &lt; len(right):
        <span class="k">if</span> left[i] &lt;= right[j]: out.append(left[i]); i += 1   <span class="c"># &lt;= keeps it stable</span>
        <span class="k">else</span>:                  out.append(right[j]); j += 1
    <span class="k">return</span> out + left[i:] + right[j:]</code></pre>
    <figure class="anim" data-anim="sort-merge"><figcaption>Bottom-up merge sort on eight values</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Quicksort partition</h3><span class="cx">O(n log n) average</span></div>
    <div class="real"><p>A teacher lining students up by height picks one student as a marker; everyone shorter goes to the left, taller to the right. The marker is now standing exactly where they belong. Repeat in each group.</p></div>
    <p class="when"><b>Use when</b>sorting in place, or in <strong>quickselect</strong> to find the k-th element in O(n) average (recurse into one side only).</p>
<pre><code><span class="k">import</span> random
<span class="k">def</span> quickselect(a, k):              <span class="c"># k-th smallest, 0-based</span>
    lo, hi = 0, len(a) - 1
    <span class="k">while True</span>:
        p = random.randint(lo, hi)        <span class="c"># random pivot avoids O(n²) on sorted input</span>
        a[p], a[hi] = a[hi], a[p]
        i = lo
        <span class="k">for</span> j <span class="k">in</span> range(lo, hi):
            <span class="k">if</span> a[j] &lt; a[hi]:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]         <span class="c"># pivot in final spot</span>
        <span class="k">if</span> i == k: <span class="k">return</span> a[i]
        <span class="k">if</span> i &lt; k: lo = i + 1
        <span class="k">else</span>: hi = i - 1</code></pre>
    <figure class="anim" data-anim="sort-partition"><figcaption>Partitioning around pivot 5</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Counting sort / three-way partition</h3><span class="cx">O(n + k)</span></div>
    <div class="real"><p>Sorting laundry into whites, darks and colors: you don't compare shirts with each other, you drop each into its basket. Sort Colors (only 0, 1, 2) is exactly this, done in one pass with three pointers (the Dutch national flag).</p></div>
    <p class="when"><b>Use when</b>values come from a small known range.</p>
<pre><code><span class="k">def</span> sort_colors(nums):
    lo, i, hi = 0, 0, len(nums) - 1     <span class="c"># [0..lo) = 0s, (hi..] = 2s</span>
    <span class="k">while</span> i &lt;= hi:
        <span class="k">if</span> nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]; lo += 1; i += 1
        <span class="k">elif</span> nums[i] == 2:
            nums[hi], nums[i] = nums[i], nums[hi]; hi -= 1   <span class="c"># don't move i: recheck swapped value</span>
        <span class="k">else</span>:
            i += 1</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Sort intervals by start, then sweep</h3><span class="cx">O(n log n)</span></div>
    <div class="real"><p>Booking a meeting room: lay all meetings on a timeline in start order. If a meeting starts before the previous one ends, they overlap and you merge them into one block.</p></div>
    <p class="when"><b>Use when</b>you see intervals: merge, insert, count rooms, remove overlaps.</p>
<pre><code><span class="k">def</span> merge_intervals(iv):
    iv.sort(key=<span class="k">lambda</span> x: x[0])
    out = [iv[0]]
    <span class="k">for</span> s, e <span class="k">in</span> iv[1:]:
        <span class="k">if</span> s &lt;= out[-1][1]:                    <span class="c"># overlaps the last block</span>
            out[-1][1] = max(out[-1][1], e)
        <span class="k">else</span>:
            out.append([s, e])
    <span class="k">return</span> out</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Custom comparators</h3><span class="cx">O(n log n · compare cost)</span></div>
    <div class="real"><p>Arranging number magnets on a fridge to make the biggest possible number. You don't sort by size; you put "9" before "34" because "934" beats "349". The ordering rule is "which pair reads bigger when glued."</p></div>
    <p class="when"><b>Use when</b>the order is defined by a rule between two items rather than a single key (Largest Number).</p>
<pre><code><span class="k">from</span> functools <span class="k">import</span> cmp_to_key
<span class="k">def</span> largest_number(nums):
    s = list(map(str, nums))
    s.sort(key=cmp_to_key(<span class="k">lambda</span> a, b: (b + a &gt; a + b) - (b + a &lt; a + b)))
    res = "".join(s)
    <span class="k">return</span> "0" <span class="k">if</span> res[0] == "0" <span class="k">else</span> res

<span class="c"># Multi-key with a tuple: by frequency desc, then letter asc</span>
words.sort(key=<span class="k">lambda</span> w: (-cnt[w], w))</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. Sort first, then it's easy</h3><span class="cx">O(n log n) + the easy part</span></div>
    <div class="real"><p>Finding duplicates in a stack of exam papers is painful in random order; sorted by student name, duplicates sit right next to each other. Many problems become a single scan once sorted.</p></div>
    <p class="when"><b>Use when</b>order doesn't matter in the output and sorting reveals structure: duplicates, pairs (two pointers), H-Index, meeting rooms, greedy choices.</p>
<pre><code><span class="k">def</span> h_index(citations):
    citations.sort(reverse=True)
    h = 0
    <span class="k">while</span> h &lt; len(citations) <span class="k">and</span> citations[h] &gt; h:
        h += 1
    <span class="k">return</span> h</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Why comparison sorting can't beat O(n log n)</h2>
  <div class="real"><p>A game of "20 Questions" where the secret is the correct order of n cards. Each comparison is a yes/no question. There are n! possible orders, and each question at best halves the possibilities, so you need about log₂(n!) questions.</p></div>
  <div class="trace">
    <div><p>n items have n! possible orderings; the algorithm must be able to produce any one of them.</p></div>
    <div><p>Each comparison has two outcomes, so k comparisons distinguish at most 2ᵏ orderings. Need 2ᵏ ≥ n!.</p></div>
    <div><p>So k ≥ log₂(n!), which is about n log₂ n. No comparison sort does better in the worst case.</p></div>
    <div><p>Counting and bucket sort escape this by never comparing items: they use values as indices. That's why they need a small value range.</p></div>
  </div>
  <div class="google"><p>"Can you do better than O(n log n)?" is a common follow-up. The answer is "not with comparisons, but yes if values are bounded integers: counting or bucket sort." That's the response they're looking for.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Pitfalls</h2>
  <div class="real"><p>Sorting the guest list for a wedding changes the original list. If someone else still needs the original order, make a copy first.</p></div>
  <ul>
    <li><code>a.sort()</code> sorts in place and returns <code>None</code>; <code>sorted(a)</code> returns a new list.</li>
    <li>Sorting changes indices. If you need original positions, sort pairs: <code>sorted(enumerate(a), key=…)</code>.</li>
    <li>Quicksort on already-sorted data with a fixed pivot is O(n²). Randomize.</li>
    <li>Largest Number on <code>[0, 0]</code> must return "0", not "00".</li>
    <li>Interval problems: ask whether touching intervals like [1,2] and [2,3] count as overlapping.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Merge Sorted Array", "merge-sorted-array", "easy", "Fill from the back"),
    ("Sort Array By Parity", "sort-array-by-parity", "easy", "Two pointers partition"),
    ("Squares of a Sorted Array", "squares-of-a-sorted-array", "easy", "Two pointers from both ends"),
    ("Sort an Array", "sort-an-array", "medium", "Implement merge sort"),
    ("Merge Intervals", "merge-intervals", "medium", "Sort by start, sweep"),
    ("Insert Interval", "insert-interval", "medium", "Before / overlapping / after"),
    ("Sort Colors", "sort-colors", "medium", "Dutch national flag"),
    ("Largest Number", "largest-number", "medium", "Comparator a+b vs b+a"),
    ("Sort Characters By Frequency", "sort-characters-by-frequency", "medium", "Counter + sort or buckets"),
    ("H-Index", "h-index", "medium", "Sort descending, scan"),
    ("Count of Smaller Numbers After Self", "count-of-smaller-numbers-after-self", "hard", "Merge sort counting (or BIT)"),
    ("Reverse Pairs", "reverse-pairs", "hard", "Count during merge sort"),
]

QUIZ = [
    dict(lvl="easy", q="Which sort guarantees O(n log n) in the worst case?",
         opts=["Quicksort", "Merge sort", "Insertion sort", "Bubble sort"], a=1, why="Merge sort always splits evenly. Quicksort can degrade to O(n²)."),
    dict(lvl="easy", q="What does `x = nums.sort()` store in x?",
         opts=["The sorted list", "None", "A copy", "An iterator"], a=1, why="`list.sort()` sorts in place and returns None. Use `sorted(nums)` for a new list."),
    dict(lvl="easy", q="Merge Intervals on `[[1,3],[2,6],[8,10]]`:",
         opts=["[[1,6],[8,10]]", "[[1,10]]", "[[1,3],[2,6],[8,10]]", "[[2,6],[8,10]]"], a=0, why="[1,3] and [2,6] overlap → [1,6]; [8,10] stands alone."),
    dict(lvl="medium", q="What does \"stable\" mean for a sort?",
         opts=["It never crashes", "Equal elements keep their original relative order", "It uses O(1) space", "It's always O(n log n)"], a=1,
         why="Stability lets you sort by a secondary key, then by a primary key, and keep both orders."),
    dict(lvl="medium", q="Sort Colors: why don't we advance `i` after swapping with `hi`?",
         opts=["Bug", "The value swapped in from `hi` hasn't been checked yet", "To keep it stable", "Because hi moves"], a=1,
         why="It could be a 0 or 2 that needs moving. Values swapped from `lo` are already known to be 1."),
    dict(lvl="medium", q="Largest Number for `[3, 30, 34, 5, 9]`:",
         opts=["9534330", "9534303", "9533430", "3033459"], a=0, why="Compare by concatenation: 9, 5, 34, 3, 30 → \"9534330\"."),
    dict(lvl="medium", q="Quickselect average and worst-case time:",
         opts=["O(n log n) and O(n log n)", "O(n) and O(n²)", "O(log n) and O(n)", "O(n) and O(n)"], a=1,
         why="Each round recurses into one side (n + n/2 + n/4 … ≈ 2n), but a bad pivot every time gives O(n²). Random pivots make that unlikely."),
    dict(lvl="hard", q="Lower bound for comparison-based sorting, and why?",
         opts=["O(n), you must read every element", "Ω(n log n), since k yes/no comparisons distinguish only 2ᵏ of the n! orders", "O(log n)", "None"], a=1,
         why="log₂(n!) ≈ n log₂ n."),
    dict(lvl="hard", q="Count of Smaller Numbers After Self: why does merge sort help?",
         opts=["It doesn't", "While merging, each left element can count how many right-half elements have already been placed before it (they're smaller and to its right)", "It sorts the answers", "It removes duplicates"], a=1,
         why="Track original indices; during merge, add the number of right items taken so far to each left item's count."),
    dict(lvl="hard", q="Meeting Rooms II (minimum rooms). A clean O(n log n) approach?",
         opts=["Sort by end only", "Sort starts and ends separately and sweep two pointers, or sort by start and keep a min-heap of end times", "Union-find", "Binary search only"], a=1,
         why="Rooms in use = starts so far − ends so far. The maximum over the sweep is the answer."),
]
