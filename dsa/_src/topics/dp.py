META = dict(
    title="DP and recursion", page_title="Dynamic Programming · DSA Field Guide", week="Week 7", group="Algorithms",
    h1="Recursion, backtracking, and dynamic programming",
    lead="These three are one idea at different speeds: break a problem into smaller copies of itself. Backtracking tries every choice; DP notices the same subproblems repeat and remembers their answers.",
    blurb="Base cases, backtracking, memoization, tabulation, 1D/2D DP, knapsack.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>Don't solve the same thing twice</h2>
  <div class="real big-real">
    <p>Someone writes "1 + 1 + 1 + 1 + 1 + 1 + 1" on a board and asks the total. You count: 7. Then they add "+ 1" and ask again. You don't recount; you say 8, because you <em>remembered</em> 7. That's dynamic programming: store answers to smaller problems so bigger ones are a single step.</p>
  </div>
<pre class="diagram">fib(5) without memory             fib(5) with memory
              f5                      f5 → f4 → f3 → f2 → f1
            /    \                         ↘    ↘    ↘
          f4      f3                       (each f computed once,
         /  \    /  \                       later calls are lookups)
       f3   f2  f2  f1
      / \                             O(2ⁿ) calls  →  O(n) calls
    f2  f1   ← f3 computed twice, f2 three times</pre>
</section>

<section id="recursion">
  <span class="eyebrow">Recursion first</span>
  <h2>Every recursive function has two parts</h2>
  <div class="real"><p>A line of people asking "what row am I in?" Each person asks the person in front and adds 1. The person in the front row knows the answer without asking: that's the base case. Without it, the question is passed forward forever.</p></div>
  <ol>
    <li><strong>Base case:</strong> the smallest input you can answer directly.</li>
    <li><strong>Recursive case:</strong> express the answer using the same function on a smaller input.</li>
  </ol>
  <p>Trust that the smaller call works (the "recursive leap of faith"), and check only that each call moves toward the base case.</p>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Six patterns from brute force to DP</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Backtracking: choose, explore, un-choose</h3><span class="cx">O(2ⁿ) subsets · O(n!) permutations</span></div>
    <div class="real"><p>Trying on outfits. Put on a shirt (choose), try every pants option with it (explore), take the shirt off (un-choose), and try the next shirt. Taking the shirt off is what lets you reuse the same body for the next combination.</p></div>
    <p class="when"><b>Use when</b>the problem says "all": all subsets, permutations, combinations, partitions, or board placements.</p>
<pre><code><span class="k">def</span> subsets(nums):
    res, path = [], []
    <span class="k">def</span> go(i):
        <span class="k">if</span> i == len(nums):
            res.append(path[:]); <span class="k">return</span>         <span class="c"># copy!</span>
        path.append(nums[i]); go(i + 1)      <span class="c"># choose nums[i]</span>
        path.pop();           go(i + 1)      <span class="c"># un-choose, skip it</span>
    go(0)
    <span class="k">return</span> res

<span class="k">def</span> combination_sum(cands, target):
    res, path = [], []
    <span class="k">def</span> go(start, remain):
        <span class="k">if</span> remain == 0: res.append(path[:]); <span class="k">return</span>
        <span class="k">for</span> i <span class="k">in</span> range(start, len(cands)):
            <span class="k">if</span> cands[i] &gt; remain: <span class="k">continue</span>        <span class="c"># prune</span>
            path.append(cands[i])
            go(i, remain - cands[i])           <span class="c"># i, not i+1: reuse allowed</span>
            path.pop()
    go(0, target)
    <span class="k">return</span> res</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Memoization (top-down DP)</h3><span class="cx">O(states × work per state)</span></div>
    <div class="real"><p>A tax accountant with a filing cabinet. Before calculating a client's deduction, they check whether it's already in the cabinet. Same recursion as before, plus a cabinet.</p></div>
    <p class="when"><b>Use when</b>you've written a correct recursive solution and the same arguments repeat.</p>
<pre><code><span class="k">from</span> functools <span class="k">import</span> cache
<span class="k">def</span> climb_stairs(n):
    @cache                          <span class="c"># the filing cabinet</span>
    <span class="k">def</span> ways(i):
        <span class="k">if</span> i &lt;= 1: <span class="k">return</span> 1
        <span class="k">return</span> ways(i - 1) + ways(i - 2)
    <span class="k">return</span> ways(n)</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Tabulation (bottom-up DP)</h3><span class="cx">Same time, no recursion</span></div>
    <div class="real"><p>Building a staircase from the ground up: you can't place step 5 until steps 1 to 4 exist. A table filled in order means every answer you need is already there when you get to it.</p></div>
    <p class="when"><b>Use when</b>the order of subproblems is clear; it avoids recursion limits and often allows space savings.</p>
<pre><code><span class="k">def</span> coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount             <span class="c"># dp[a] = fewest coins for a</span>
    <span class="k">for</span> a <span class="k">in</span> range(1, amount + 1):
        <span class="k">for</span> c <span class="k">in</span> coins:
            <span class="k">if</span> c &lt;= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    <span class="k">return</span> dp[amount] <span class="k">if</span> dp[amount] != INF <span class="k">else</span> -1</code></pre>
    <figure class="anim" data-anim="dp-coins"><figcaption>Filling the Coin Change table for amount 11</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. 1D DP: take it or skip it</h3><span class="cx">O(n) time · O(1) space</span></div>
    <div class="real"><p>A burglar on a street can't rob two neighboring houses without setting off alarms. At each house the choice is: rob it plus the best from two houses back, or skip it and keep the best from one house back.</p></div>
    <p class="when"><b>Use when</b>each item's decision depends only on the last one or two decisions.</p>
<pre><code><span class="k">def</span> rob(nums):
    prev2 = prev1 = 0                     <span class="c"># best up to i-2, i-1</span>
    <span class="k">for</span> x <span class="k">in</span> nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    <span class="k">return</span> prev1</code></pre>
    <p class="note">House Robber II (houses in a circle): run this twice, once without the first house and once without the last, and take the max.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. 2D DP on two sequences or a grid</h3><span class="cx">O(m × n)</span></div>
    <div class="real"><p>Comparing two versions of a document (like Git's diff). You line one version along the top of a table and the other down the side; each cell answers "how similar are these two prefixes?" and builds on the cells above and to the left.</p></div>
    <p class="when"><b>Use when</b>there are two strings (LCS, Edit Distance) or a grid (Unique Paths, min path sum).</p>
<pre><code><span class="k">def</span> lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) <span class="k">for</span> _ <span class="k">in</span> range(m + 1)]
    <span class="k">for</span> i <span class="k">in</span> range(1, m + 1):
        <span class="k">for</span> j <span class="k">in</span> range(1, n + 1):
            <span class="k">if</span> a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1          <span class="c"># match: diagonal + 1</span>
            <span class="k">else</span>:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  <span class="c"># drop one letter</span>
    <span class="k">return</span> dp[m][n]</code></pre>
    <figure class="anim" data-anim="dp-lcs"><figcaption>Filling the LCS table for "abcde" and "ace"</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. 0/1 knapsack</h3><span class="cx">O(n × capacity)</span></div>
    <div class="real"><p>Packing a carry-on with a 7 kg limit. Each item either goes in once or doesn't. For every possible weight from 7 down to 0, you ask: is it better with this item or without it?</p></div>
    <p class="when"><b>Use when</b>each item is used at most once and you're hitting a target sum or capacity (Partition Equal Subset Sum, Target Sum).</p>
<pre><code><span class="k">def</span> can_partition(nums):
    total = sum(nums)
    <span class="k">if</span> total % 2: <span class="k">return</span> False
    target = total // 2
    dp = [True] + [False] * target       <span class="c"># dp[s]: can some subset make s?</span>
    <span class="k">for</span> x <span class="k">in</span> nums:
        <span class="k">for</span> s <span class="k">in</span> range(target, x - 1, -1):  <span class="c"># BACKWARDS: use x once</span>
            dp[s] = dp[s] <span class="k">or</span> dp[s - x]
    <span class="k">return</span> dp[target]</code></pre>
    <p class="note">Loop backwards for "each item once" (0/1 knapsack). Loop forwards for "unlimited copies" (Coin Change). Mixing these up is the most common knapsack bug.</p>
  </article>
</section>

<section id="framework">
  <span class="eyebrow">Method</span>
  <h2>The five-step DP recipe</h2>
  <div class="real"><p>Like writing a recipe card: what dish (state), the basic step (transition), what you start with (base case), the order you cook (iteration order), and what you serve (the answer cell).</p></div>
  <div class="trace">
    <div><p><strong>State:</strong> what does <code>dp[i]</code> (or <code>dp[i][j]</code>) mean, in one sentence? "dp[a] = fewest coins to make amount a."</p></div>
    <div><p><strong>Transition:</strong> how does a state use smaller states? "dp[a] = min over coins c of dp[a − c] + 1."</p></div>
    <div><p><strong>Base cases:</strong> the states you know without computing. "dp[0] = 0."</p></div>
    <div><p><strong>Order:</strong> fill so dependencies come first (small a to large a; top-left to bottom-right).</p></div>
    <div><p><strong>Answer:</strong> which cell, and what if it's unreachable? "dp[amount], or −1 if it's still infinity."</p></div>
  </div>
  <div class="google"><p>Say the state definition out loud before writing code. Most DP bugs are a fuzzy state definition, and interviewers will often accept a correct memoized solution even if you never convert it to a table.</p></div>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Longest Increasing Subsequence, two ways</h2>
  <div class="real"><p>Stacking boxes by size: you go through boxes in the order they arrived and want the tallest tower where each box is bigger than the one below. You can skip boxes but can't reorder them.</p></div>
  <p><strong>O(n²) DP.</strong> <code>dp[i]</code> = length of the longest increasing subsequence ending at index i. For each i, look at every earlier j with <code>nums[j] &lt; nums[i]</code>.</p>
<pre><code><span class="k">def</span> lis(nums):
    dp = [1] * len(nums)
    <span class="k">for</span> i <span class="k">in</span> range(len(nums)):
        <span class="k">for</span> j <span class="k">in</span> range(i):
            <span class="k">if</span> nums[j] &lt; nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    <span class="k">return</span> max(dp)</code></pre>
  <p><strong>O(n log n) patience sorting.</strong> Keep <code>tails[k]</code> = the smallest possible tail of an increasing subsequence of length k+1. For each number, binary-search the first tail ≥ it and replace it (or append).</p>
<pre><code><span class="k">import</span> bisect
<span class="k">def</span> lis_fast(nums):
    tails = []
    <span class="k">for</span> x <span class="k">in</span> nums:
        i = bisect.bisect_left(tails, x)
        <span class="k">if</span> i == len(tails): tails.append(x)
        <span class="k">else</span>: tails[i] = x                  <span class="c"># a smaller tail is never worse</span>
    <span class="k">return</span> len(tails)</code></pre>
  <div class="real"><p>The card game Patience: deal cards onto piles, always placing a card on the leftmost pile whose top card is bigger or equal. The number of piles you end with is the LIS length.</p></div>
  <p class="note"><code>tails</code> is not itself a valid subsequence; only its length is meaningful. Interviewers like asking that.</p>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases and pitfalls</h2>
  <div class="real"><p>A recipe that fails for zero guests or one guest isn't a recipe. Test the tiny inputs first.</p></div>
  <ul>
    <li>Empty input, n = 0 or 1, amount = 0.</li>
    <li>Unreachable states: initialize with infinity, and convert back to −1 at the end.</li>
    <li>Appending <code>path</code> instead of <code>path[:]</code> in backtracking: every result ends up empty.</li>
    <li>Recursion depth over 1,000: switch to tabulation, or raise the limit with <code>sys.setrecursionlimit</code>.</li>
    <li>Duplicates in input for subsets/permutations: sort, then skip equal neighbors at the same depth.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Climbing Stairs", "climbing-stairs", "easy", "dp[i] = dp[i-1] + dp[i-2]"),
    ("Fibonacci Number", "fibonacci-number", "easy", "Memoize or two variables"),
    ("Min Cost Climbing Stairs", "min-cost-climbing-stairs", "easy", "1D DP, min of last two"),
    ("House Robber", "house-robber", "medium", "Take or skip"),
    ("House Robber II", "house-robber-ii", "medium", "Run House Robber twice"),
    ("Coin Change", "coin-change", "medium", "Unbounded knapsack, min coins"),
    ("Unique Paths", "unique-paths", "medium", "Grid DP: above + left"),
    ("Longest Increasing Subsequence", "longest-increasing-subsequence", "medium", "O(n²) DP or patience + bisect"),
    ("Longest Common Subsequence", "longest-common-subsequence", "medium", "2D DP on two strings"),
    ("Partition Equal Subset Sum", "partition-equal-subset-sum", "medium", "0/1 knapsack, loop backwards"),
    ("Combination Sum", "combination-sum", "medium", "Backtracking with reuse"),
    ("Subsets", "subsets", "medium", "Backtracking: take or skip"),
    ("Permutations", "permutations", "medium", "Backtracking with a used set"),
    ("Burst Balloons", "burst-balloons", "hard", "Interval DP: which balloon bursts LAST"),
]

QUIZ = [
    dict(lvl="easy", q="What is the time complexity of plain recursive `fib(n)` without memoization?",
         opts=["O(n)", "O(n log n)", "O(2ⁿ)", "O(n²)"], a=2, why="Two calls per level, n levels deep, with massive repetition."),
    dict(lvl="easy", q="What does `@functools.cache` do to a recursive function?",
         opts=["Makes it iterative", "Stores results by arguments so repeat calls return instantly", "Limits recursion depth", "Runs it in parallel"], a=1,
         why="It's memoization in one line. Arguments must be hashable."),
    dict(lvl="easy", q="How many subsets does a set of 4 elements have?",
         opts=["4", "8", "16", "24"], a=2, why="Each element is in or out: 2⁴ = 16, including the empty set."),
    dict(lvl="medium", q="Bug hunt: why does this return lists that are all empty?", code="res, path = [], []\ndef go(i):\n    if i == len(nums):\n        res.append(path)\n        return\n    ...",
         opts=["`res` should be a set", "It appends the same `path` object, which is emptied later; append `path[:]`", "Recursion depth", "`i` starts at 0"], a=1,
         why="Every entry in res points to one list that ends up empty after the final pops."),
    dict(lvl="medium", q="House Robber on `[2, 7, 9, 3, 1]`:",
         opts=["10", "11", "12", "13"], a=2, why="Rob 2 + 9 + 1 = 12. Robbing 7 + 3 = 10 is worse."),
    dict(lvl="medium", q="Unique Paths in a 3×3 grid (moves: right or down only):",
         opts=["4", "6", "9", "12"], a=1, why="Each cell = above + left. Or combinatorics: choose 2 of 4 moves to be 'down': C(4,2) = 6."),
    dict(lvl="medium", q="In 0/1 knapsack with a 1D array, why loop capacity *backwards*?",
         opts=["It's faster", "So dp[s − x] still holds the value from before this item, preventing reuse", "To avoid negative indices", "It doesn't matter"], a=1,
         why="Going forward, dp[s − x] may already include x, letting you use the same item twice (that's unbounded knapsack)."),
    dict(lvl="hard", q="LIS patience sorting: after processing `[3, 10, 2, 1, 20]`, what is `tails`?",
         opts=["[3, 10, 20]", "[1, 10, 20]", "[1, 2, 20]", "[2, 10, 20]"], a=1,
         why="3 → [3]; 10 → [3,10]; 2 replaces 3 → [2,10]; 1 replaces 2 → [1,10]; 20 → [1,10,20]. Length 3 is correct even though [1,10,20] isn't in order of appearance."),
    dict(lvl="hard", q="Burst Balloons is solved by choosing which balloon bursts *last* in an interval. Why last instead of first?",
         opts=["It's arbitrary", "If k bursts last in (i, j), its neighbors are exactly i and j, so the left and right parts are independent subproblems", "To reduce memory", "Bursting first is O(n!)"], a=1,
         why="Choosing the first burst changes the neighbors of everything else, coupling the subproblems."),
    dict(lvl="hard", q="Coin Change table has size `amount + 1` and tries every coin per cell. Complexity?",
         opts=["O(amount)", "O(amount × number of coins)", "O(2^coins)", "O(amount²)"], a=1,
         why="States × work per state: (amount + 1) states, each scanning all coins."),
]
