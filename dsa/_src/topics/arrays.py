META = dict(
    title="Arrays", page_title="Arrays · DSA Field Guide", week="Week 1", group="Data structures",
    h1="Arrays",
    lead="The most common interview data structure. Almost every Google coding round touches an array, and six patterns cover nearly all of them.",
    blurb="Indexing, two pointers, prefix sums, Kadane's, in-place marking, matrices.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A row of numbered seats</h2>
  <div class="real big-real">
    <p>Think of a cinema row with seats numbered 0, 1, 2, … To find seat 14 you walk straight to it; you don't check seats 0 to 13 first. But if a latecomer needs to sit in seat 3 and everyone must stay in order, every person from seat 3 onward has to shuffle one seat right. That is an array: instant access by position, expensive inserts in the middle.</p>
  </div>
  <p>An array stores items in one continuous block of memory. Because every slot is the same size, the computer finds slot <code>i</code> with arithmetic instead of searching:</p>
<pre class="diagram">address of arr[i] = start + i × slot_size

 index:   0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
 value: │  7  │  2  │  9  │  4  │  5  │   ← one continuous block
        └─────┴─────┴─────┴─────┴─────┘
        start                  start + 4 × size</pre>
  <p>A Python <code>list</code> is a <strong>dynamic array</strong>. It reserves extra space, and when it fills up it moves everything into a block about 1.125–2× bigger. That move costs O(n), but it happens so rarely that <code>append</code> averages out to O(1). This averaging is called <em>amortized</em> cost.</p>
  <div class="real">
    <p>Amortized cost is like moving house. Moving takes a whole weekend, but if you only move when your family doubles in size, the cost per new family member stays small.</p>
  </div>
</section>

<section id="ops">
  <span class="eyebrow">Costs</span>
  <h2>What each operation costs</h2>
  <div class="tbl"><table>
    <thead><tr><th>Operation</th><th>Python</th><th>Time</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td>Read / write by index</td><td><code>a[i]</code>, <code>a[i] = x</code></td><td><span class="pill o1">O(1)</span></td><td>Address arithmetic</td></tr>
      <tr><td>Add / remove at end</td><td><code>a.append(x)</code>, <code>a.pop()</code></td><td><span class="pill o1">O(1)</span></td><td>Amortized; no shifting</td></tr>
      <tr><td>Insert / remove at front or middle</td><td><code>a.insert(i, x)</code>, <code>a.pop(0)</code></td><td><span class="pill on">O(n)</span></td><td>Everything after i shifts</td></tr>
      <tr><td>Search unsorted</td><td><code>x in a</code>, <code>a.index(x)</code></td><td><span class="pill on">O(n)</span></td><td>Checks each slot</td></tr>
      <tr><td>Search sorted</td><td><code>bisect.bisect_left(a, x)</code></td><td><span class="pill olog">O(log n)</span></td><td>Binary search</td></tr>
      <tr><td>Slice / copy</td><td><code>a[l:r]</code>, <code>a[:]</code></td><td><span class="pill on">O(k)</span></td><td>Copies k items</td></tr>
      <tr><td>Sort</td><td><code>a.sort()</code></td><td><span class="pill onlog">O(n log n)</span></td><td>Timsort</td></tr>
    </tbody>
  </table></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Six patterns that solve most array problems</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Hashmap complement lookup</h3><span class="cx">O(n) time · O(n) space</span></div>
    <div class="real"><p>At a party you need someone whose height plus yours equals 340 cm. Instead of comparing yourself with every guest, you write your height on a board as you arrive. Each newcomer checks the board for "340 minus my height." The first match is instant.</p></div>
    <p class="when"><b>Use when</b>you need a pair (or earlier element) that satisfies a condition with the current element.</p>
<pre><code><span class="k">def</span> two_sum(nums, target):
    seen = {}                       <span class="c"># value -> index</span>
    <span class="k">for</span> i, x <span class="k">in</span> enumerate(nums):
        <span class="k">if</span> target - x <span class="k">in</span> seen:      <span class="c"># O(1) lookup</span>
            <span class="k">return</span> [seen[target - x], i]
        seen[x] = i                 <span class="c"># store AFTER checking (no self-pairing)</span></code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Two pointers from both ends</h3><span class="cx">O(n) after sorting · O(1) space</span></div>
    <div class="real"><p>Two friends balance a seesaw using weights lined up from lightest to heaviest. One starts at the light end, one at the heavy end. Too heavy? The heavy-side friend steps toward lighter weights. Too light? The light-side friend steps up. They meet in the middle having checked every useful combination.</p></div>
    <p class="when"><b>Use when</b>the array is sorted (or you can sort it) and you're looking for pairs, or when the answer depends on two ends shrinking inward.</p>
<pre><code><span class="k">def</span> pair_with_sum(nums, target):   <span class="c"># nums sorted</span>
    l, r = 0, len(nums) - 1
    <span class="k">while</span> l &lt; r:
        s = nums[l] + nums[r]
        <span class="k">if</span> s == target: <span class="k">return</span> (l, r)
        <span class="k">if</span> s &lt; target: l += 1       <span class="c"># need bigger</span>
        <span class="k">else</span>: r -= 1                 <span class="c"># need smaller</span>
    <span class="k">return</span> None</code></pre>
  <figure class="anim" data-anim="arrays-two-pointers"><figcaption>Two pointers finding a pair that sums to 14</figcaption></figure>
    <p class="note">3Sum = fix one number, then run this on the rest: O(n²). Container With Most Water = always move the shorter wall, because moving the taller one can never help.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Prefix sums</h3><span class="cx">O(n) build · O(1) per range query</span></div>
    <div class="real"><p>Highway mile markers. To know the distance from exit 12 to exit 40 you don't add up every mile between them; you subtract the markers: 40 − 12. A prefix-sum array is a row of mile markers for your data.</p></div>
    <p class="when"><b>Use when</b>the problem asks about sums of contiguous subarrays, especially "how many subarrays sum to k."</p>
<pre><code><span class="c"># sum(nums[l..r]) == pre[r+1] - pre[l]</span>
pre = [0]
<span class="k">for</span> x <span class="k">in</span> nums: pre.append(pre[-1] + x)

<span class="c"># Subarray Sum Equals K: prefix sum + hashmap of counts</span>
<span class="k">def</span> subarray_sum(nums, k):
    count, run, seen = 0, 0, {0: 1}   <span class="c"># empty prefix seen once</span>
    <span class="k">for</span> x <span class="k">in</span> nums:
        run += x
        count += seen.get(run - k, 0)  <span class="c"># earlier prefix that makes a k-sum</span>
        seen[run] = seen.get(run, 0) + 1
    <span class="k">return</span> count</code></pre>
    <p class="note">Why not sliding window here? Negative numbers break it: growing the window can make the sum smaller. Prefix sums don't care about signs.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Kadane's algorithm</h3><span class="cx">O(n) time · O(1) space</span></div>
    <div class="real"><p>You run a lemonade stand and track daily profit. If your running total ever goes negative, carrying it forward only hurts tomorrow, so you "start a new business" from today. Kadane's keeps the best streak ever seen while doing exactly that.</p></div>
    <p class="when"><b>Use when</b>you need the best (max/min) contiguous subarray.</p>
<pre><code><span class="k">def</span> max_subarray(nums):
    cur = best = nums[0]
    <span class="k">for</span> x <span class="k">in</span> nums[1:]:
        cur = max(x, cur + x)   <span class="c"># extend, or restart at x</span>
        best = max(best, cur)
    <span class="k">return</span> best</code></pre>
  <figure class="anim" data-anim="arrays-kadane"><figcaption>Kadane's deciding to extend or restart</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. In-place marking (index as a hash)</h3><span class="cx">O(n) time · O(1) extra space</span></div>
    <div class="real"><p>A hotel with rooms 1 to n. Each guest holding key k walks to room k. Afterwards you walk the corridor: the first empty room is the smallest missing key. You used the rooms themselves as the record, with no extra notebook.</p></div>
    <p class="when"><b>Use when</b>values lie in the range 1..n and you're asked for O(1) extra space (First Missing Positive, find duplicates), or you must record flags inside a matrix (Set Matrix Zeroes uses row 0 and column 0 as flags).</p>
<pre><code><span class="k">def</span> first_missing_positive(nums):
    n = len(nums)
    <span class="k">for</span> i <span class="k">in</span> range(n):
        <span class="c"># keep swapping nums[i] into its "room" nums[i]-1</span>
        <span class="k">while</span> 1 &lt;= nums[i] &lt;= n <span class="k">and</span> nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    <span class="k">for</span> i <span class="k">in</span> range(n):
        <span class="k">if</span> nums[i] != i + 1: <span class="k">return</span> i + 1
    <span class="k">return</span> n + 1</code></pre>
    <p class="note">The while loop looks like O(n²), but each swap puts one number in its final room, so there are at most n swaps total: O(n).</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. Matrix traversal with boundaries</h3><span class="cx">O(rows × cols)</span></div>
    <div class="real"><p>Mowing a rectangular lawn in a spiral: mow the top edge, the right edge, the bottom, the left, then the lawn left to mow is a smaller rectangle. Each lap shrinks four boundaries by one.</p></div>
    <p class="when"><b>Use when</b>you walk a grid in a fixed shape (spiral, diagonal, layers) or rotate it.</p>
<pre><code><span class="k">def</span> spiral(m):
    res = []
    top, bot, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    <span class="k">while</span> top &lt;= bot <span class="k">and</span> left &lt;= right:
        <span class="k">for</span> c <span class="k">in</span> range(left, right + 1): res.append(m[top][c])
        top += 1
        <span class="k">for</span> r <span class="k">in</span> range(top, bot + 1): res.append(m[r][right])
        right -= 1
        <span class="k">if</span> top &lt;= bot:
            <span class="k">for</span> c <span class="k">in</span> range(right, left - 1, -1): res.append(m[bot][c])
            bot -= 1
        <span class="k">if</span> left &lt;= right:
            <span class="k">for</span> r <span class="k">in</span> range(bot, top - 1, -1): res.append(m[r][left])
            left += 1
    <span class="k">return</span> res</code></pre>
    <p class="note">The two <code>if</code> checks stop a single leftover row or column from being read twice. That is the most common bug in this problem.</p>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Trapping Rain Water, from brute force to optimal</h2>
  <div class="real"><p>Picture a city skyline after a storm. Water sitting on top of a building can only rise as high as the shorter of the tallest building to its left and the tallest building to its right. Any higher and it spills over the lower side.</p></div>
  <p>So the water above bar <code>i</code> is <code>min(maxLeft, maxRight) − height[i]</code>. The whole problem is about computing those two maxima cheaply.</p>
  <div class="trace">
    <div><p><strong>Brute force, O(n²) time, O(1) space.</strong> For each bar, scan left and right for the maxima. Correct, but 10⁵ bars means 10¹⁰ steps.</p></div>
    <div><p><strong>Precompute, O(n) time, O(n) space.</strong> Build <code>leftMax[i]</code> in one pass from the left and <code>rightMax[i]</code> in one pass from the right, then sum. Classic space-for-time trade.</p></div>
    <div><p><strong>Two pointers, O(n) time, O(1) space.</strong> Key insight: if <code>leftMax &lt; rightMax</code>, the left bar's water is decided by <code>leftMax</code> alone, because some bar on the right is at least that tall. So process whichever side has the smaller max and move inward.</p></div>
  </div>
<pre><code><span class="k">def</span> trap(h):
    l, r = 0, len(h) - 1
    lmax = rmax = water = 0
    <span class="k">while</span> l &lt; r:
        <span class="k">if</span> h[l] &lt; h[r]:
            lmax = max(lmax, h[l]); water += lmax - h[l]; l += 1
        <span class="k">else</span>:
            rmax = max(rmax, h[r]); water += rmax - h[r]; r -= 1
    <span class="k">return</span> water</code></pre>
  <div class="google"><p>Walking an interviewer through all three versions, in this order, is exactly what Google wants to see: a correct baseline, a named trade-off, then the insight that removes the trade-off.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases to test</h2>
  <div class="real"><p>A pilot's pre-flight checklist exists because experts skip obvious things under pressure. Run this list out loud on every array problem.</p></div>
  <ul>
    <li>Empty array, and a single element.</li>
    <li>All elements the same; all negative (breaks naive "max starts at 0").</li>
    <li>Duplicates (3Sum must skip them).</li>
    <li>Already sorted, and reverse sorted.</li>
    <li>Integer overflow doesn't happen in Python, but mention it if the interviewer is thinking in Java or C++.</li>
    <li>Off-by-one at the boundaries: <code>range(n)</code> vs <code>range(n - 1)</code>, <code>l &lt; r</code> vs <code>l &lt;= r</code>.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Two Sum", "two-sum", "easy", "Hashmap complement"),
    ("Best Time to Buy and Sell Stock", "best-time-to-buy-and-sell-stock", "easy", "Track running minimum"),
    ("Contains Duplicate", "contains-duplicate", "easy", "Set"),
    ("Maximum Subarray", "maximum-subarray", "easy", "Kadane's"),
    ("Product of Array Except Self", "product-of-array-except-self", "medium", "Prefix and suffix products"),
    ("3Sum", "3sum", "medium", "Sort + two pointers, skip duplicates"),
    ("Container With Most Water", "container-with-most-water", "medium", "Two pointers, move the shorter wall"),
    ("Subarray Sum Equals K", "subarray-sum-equals-k", "medium", "Prefix sum + hashmap"),
    ("Set Matrix Zeroes", "set-matrix-zeroes", "medium", "First row/column as markers"),
    ("Spiral Matrix", "spiral-matrix", "medium", "Shrinking boundaries"),
    ("Trapping Rain Water", "trapping-rain-water", "hard", "Two pointers with left/right max"),
    ("First Missing Positive", "first-missing-positive", "hard", "Index as hash (cyclic placement)"),
]

QUIZ = [
    dict(lvl="easy", q="Why is reading `arr[i]` O(1) in an array?",
         opts=["The array is sorted", "The address is computed as start + i × slot size", "Python caches every index", "It uses binary search"],
         a=1, why="Slots are the same size and stored contiguously, so the address is simple arithmetic, no search."),
    dict(lvl="easy", q="What does `nums.insert(0, x)` cost on a list of n items?",
         opts=["O(1)", "O(log n)", "O(n)", "O(n²)"], a=2,
         why="Every existing item shifts one slot right. Use `collections.deque.appendleft` if you need fast front inserts."),
    dict(lvl="easy", q="In Two Sum with a hashmap, why do we store `nums[i]` *after* checking for its complement?",
         opts=["It's faster", "So an element can't pair with itself", "Dicts require it", "To keep the dict sorted"], a=1,
         why="If target = 6 and x = 3, storing first would find the same 3 and return [i, i]."),
    dict(lvl="medium", q="What does this return for `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`?",
         code="cur = best = nums[0]\nfor x in nums[1:]:\n    cur = max(x, cur + x)\n    best = max(best, cur)\nreturn best",
         opts=["4", "5", "6", "7"], a=2, why="The best subarray is [4, -1, 2, 1] = 6. Kadane's restarts at 4 because the running sum before it was negative."),
    dict(lvl="medium", q="Subarray Sum Equals K with negative numbers allowed. Why does sliding window fail?",
         opts=["It's O(n²)", "Adding an element can decrease the sum, so you can't decide when to shrink", "It uses too much memory", "It only works on strings"], a=1,
         why="Sliding window relies on the sum moving in one direction as the window grows. Negatives break that, so use prefix sums + a hashmap."),
    dict(lvl="medium", q="Container With Most Water: why move the pointer at the *shorter* wall?",
         opts=["It's arbitrary", "Moving the taller wall can only keep or shrink the area, since height is capped by the shorter wall and width shrinks", "The shorter wall is always on the left", "To avoid duplicates"], a=1,
         why="Area = min(h[l], h[r]) × width. Moving the taller wall never raises the min but always shrinks the width."),
    dict(lvl="medium", q="What's the time complexity of 3Sum using sort + two pointers?",
         opts=["O(n)", "O(n log n)", "O(n²)", "O(n³)"], a=2,
         why="Sorting is O(n log n), then for each of n fixed numbers you run an O(n) two-pointer scan: O(n²) dominates."),
    dict(lvl="hard", q="First Missing Positive has a `while` loop inside a `for` loop. Why is it still O(n)?",
         opts=["The while loop runs at most once", "Each swap places one number in its final slot, so total swaps across the whole run is at most n", "Python optimizes nested loops", "It isn't; it's O(n²)"], a=1,
         why="Amortized analysis: count total work across the run, not per iteration. Each value is moved into place at most once."),
    dict(lvl="hard", q="Product of Array Except Self without division in O(1) extra space (output array not counted). What's the trick?",
         opts=["Sort first", "Write prefix products into the output, then multiply in suffix products with a single running variable on a backward pass", "Use a hashmap of products", "Use logarithms"], a=1,
         why="Pass 1: out[i] = product of everything left of i. Pass 2 (right to left): keep `suffix` and do out[i] *= suffix; suffix *= nums[i]."),
    dict(lvl="hard", q="An interviewer asks: Two Sum, but the array is huge and already sorted, and memory is tight. Best approach?",
         opts=["Hashmap: O(n) time, O(n) space", "Two pointers: O(n) time, O(1) space", "Brute force: O(n²) time", "Sort again then hashmap"], a=1,
         why="Sorted input is the signal for two pointers, which matches the hashmap's time with constant space. Always ask whether input is sorted."),
]
