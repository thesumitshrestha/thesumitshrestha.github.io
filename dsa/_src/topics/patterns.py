META = dict(
    title="Pattern finder", page_title="Pattern Finder · DSA Field Guide", week="Use anytime", group="Interview prep",
    h1="Pattern finder: from problem to approach",
    lead="Most interview problems are a known pattern in disguise. This page maps the clues in a problem statement to the technique that solves it, with a practice quiz that drills exactly that skill.",
    blurb="Clue → technique lookup, a decision path, and a pattern-spotting quiz.",
    needs_anim=False,
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>Diagnose before you treat</h2>
  <div class="real big-real">
    <p>A doctor doesn't try every medicine. They notice symptoms (fever, rash, cough), match them to a short list of likely conditions, then confirm. Interview problems work the same way: words like "sorted," "top k," "shortest," or "all combinations" are symptoms that point to a short list of techniques.</p>
  </div>
</section>

<section id="clues">
  <span class="eyebrow">Lookup table</span>
  <h2>If you see this, think that</h2>
  <div class="tbl"><table>
    <thead><tr><th>Clue in the problem</th><th>Think</th><th>Page</th></tr></thead>
    <tbody>
      <tr><td>Array is sorted; find a pair/triple</td><td>Two pointers</td><td><a href="arrays.html#patterns">Arrays</a></td></tr>
      <tr><td>Sorted array, find a value or boundary</td><td>Binary search</td><td><a href="searching.html">Searching</a></td></tr>
      <tr><td>"Minimize the maximum" / "smallest value that works"</td><td>Binary search on the answer</td><td><a href="searching.html#deep">Searching</a></td></tr>
      <tr><td>Longest/shortest contiguous substring or subarray with a condition</td><td>Sliding window</td><td><a href="strings.html#patterns">Strings</a></td></tr>
      <tr><td>Subarray sum equals k (negatives allowed)</td><td>Prefix sum + hashmap</td><td><a href="hashing.html#patterns">Hashing</a></td></tr>
      <tr><td>"Have I seen this?" / pair with a sum / duplicates</td><td>Hash set or hashmap</td><td><a href="hashing.html">Hashing</a></td></tr>
      <tr><td>Anagrams, "same letters," permutation of a string</td><td>Frequency count</td><td><a href="strings.html#patterns">Strings</a></td></tr>
      <tr><td>Next greater/smaller element, "days until," histogram</td><td>Monotonic stack</td><td><a href="stacks-queues.html#patterns">Stacks</a></td></tr>
      <tr><td>Brackets, nested structure, undo</td><td>Stack</td><td><a href="stacks-queues.html">Stacks</a></td></tr>
      <tr><td>Linked list middle, cycle, k-th from end</td><td>Fast/slow pointers</td><td><a href="linked-lists.html#patterns">Linked lists</a></td></tr>
      <tr><td>Top k, k-th largest, closest k, merge k sorted</td><td>Heap</td><td><a href="heaps.html">Heaps</a></td></tr>
      <tr><td>Running median</td><td>Two heaps</td><td><a href="heaps.html#patterns">Heaps</a></td></tr>
      <tr><td>Tree: height, diameter, path sums, balanced?</td><td>DFS returning a value</td><td><a href="trees.html#patterns">Trees</a></td></tr>
      <tr><td>Tree: by level, rightmost per level, min depth</td><td>BFS</td><td><a href="trees.html#patterns">Trees</a></td></tr>
      <tr><td>Prefix, autocomplete, many words in a grid</td><td>Trie</td><td><a href="trees.html#patterns">Trees</a></td></tr>
      <tr><td>Grid regions, islands, flood fill</td><td>DFS/BFS on grid</td><td><a href="graphs.html#patterns">Graphs</a></td></tr>
      <tr><td>Fewest steps, unweighted</td><td>BFS</td><td><a href="graphs.html#patterns">Graphs</a></td></tr>
      <tr><td>Fewest cost, non-negative weights</td><td>Dijkstra</td><td><a href="graphs.html#patterns">Graphs</a></td></tr>
      <tr><td>Prerequisites, ordering, dependency</td><td>Topological sort</td><td><a href="graphs.html#patterns">Graphs</a></td></tr>
      <tr><td>Connecting things over time, redundant edge</td><td>Union-find</td><td><a href="graphs.html#patterns">Graphs</a></td></tr>
      <tr><td>"All" subsets / permutations / combinations</td><td>Backtracking</td><td><a href="dp.html#patterns">DP</a></td></tr>
      <tr><td>"Number of ways," "min/max cost," choices that overlap</td><td>Dynamic programming</td><td><a href="dp.html">DP</a></td></tr>
      <tr><td>Two strings compared character by character</td><td>2D DP</td><td><a href="dp.html#patterns">DP</a></td></tr>
      <tr><td>Intervals, meetings, overlaps</td><td>Sort by start, sweep</td><td><a href="sorting.html#patterns">Sorting</a></td></tr>
      <tr><td>Appears twice except one; O(1) space</td><td>XOR</td><td><a href="bits.html#patterns">Bits</a></td></tr>
      <tr><td>n ≤ 20 and "all subsets"</td><td>Bitmask</td><td><a href="bits.html#patterns">Bits</a></td></tr>
    </tbody>
  </table></div>
</section>

<section id="path">
  <span class="eyebrow">Decision path</span>
  <h2>Five questions to ask in order</h2>
  <div class="real"><p>A mechanic's diagnostic: "Does it start? Is the battery charged? Is there fuel?" Asking the questions in a fixed order narrows the problem fast without guessing.</p></div>
  <div class="trace">
    <div><p><strong>What's the input shape?</strong> Array/string, linked list, tree, graph/grid, or a stream? This picks the page.</p></div>
    <div><p><strong>Is it sorted, or would sorting help?</strong> If yes: two pointers or binary search.</p></div>
    <div><p><strong>Contiguous range?</strong> Sliding window (all positive / "at most k distinct") or prefix sums (negatives, exact sums).</p></div>
    <div><p><strong>"All" answers, or one best answer?</strong> All → backtracking. Best with overlapping choices → DP. Best with a clear greedy choice → sort + greedy or heap.</p></div>
    <div><p><strong>What does the constraint on n allow?</strong> n ≤ 20 → exponential is fine. n ≤ 10⁴ → O(n²) is OK. n ≤ 10⁵+ → you need O(n log n) or O(n). See the <a href="big-o.html">Big-O page</a>.</p></div>
  </div>
  <div class="google"><p>Say the pattern you're considering, and why, before coding: "Because the array is sorted and we need a pair, I'm thinking two pointers." Even if it's wrong, the interviewer can steer you, and your reasoning counts toward the score.</p></div>
</section>
"""

QUIZ = [
    dict(lvl="easy", q="\"Given a sorted array, return indices of two numbers that add up to target, using O(1) extra space.\"",
         opts=["Hashmap", "Two pointers", "Sliding window", "Heap"], a=1, why="Sorted + pair + O(1) space is the textbook two-pointer signal."),
    dict(lvl="easy", q="\"Return the k most frequent words.\"",
         opts=["Binary search", "Counter + heap (or bucket sort)", "Backtracking", "Union-find"], a=1, why="Count first, then top-k means heap."),
    dict(lvl="easy", q="\"Count the number of islands in a grid of '1's and '0's.\"",
         opts=["DFS/BFS flood fill", "Kadane's", "Binary search", "Monotonic stack"], a=0, why="Each unvisited land cell starts a flood fill; count the starts."),
    dict(lvl="easy", q="\"Determine if a string of brackets is valid.\"",
         opts=["Queue", "Stack", "Heap", "Two pointers"], a=1, why="Nested open/close order = stack."),
    dict(lvl="medium", q="\"Find the length of the longest substring with at most 2 distinct characters.\"",
         opts=["Sliding window + count map", "Sort then scan", "DP on two strings", "Trie"], a=0, why="Contiguous + \"at most\" condition = variable sliding window."),
    dict(lvl="medium", q="\"Given course prerequisites, return a valid order to take all courses, or [] if impossible.\"",
         opts=["Dijkstra", "Topological sort", "Binary search", "Kadane's"], a=1, why="Dependencies + ordering + impossible (cycle) = topological sort."),
    dict(lvl="medium", q="\"Return all possible ways to place n queens on an n×n board.\"",
         opts=["DP table", "Backtracking", "BFS", "Greedy"], a=1, why="\"All\" configurations with constraints = backtracking with pruning."),
    dict(lvl="medium", q="\"For each day, how many days until a higher stock price?\"",
         opts=["Monotonic stack", "Heap", "Prefix sum", "Two heaps"], a=0, why="Next greater element = monotonic stack."),
    dict(lvl="medium", q="\"Count subarrays whose sum equals k; values can be negative.\"",
         opts=["Sliding window", "Prefix sum + hashmap", "Two pointers", "Binary search"], a=1, why="Negatives break sliding windows; prefix sums handle any sign."),
    dict(lvl="hard", q="\"Ship packages in order within D days; find the minimum ship capacity.\"",
         opts=["DP over days", "Binary search on capacity with a greedy check", "Heap of weights", "Union-find"], a=1,
         why="\"Minimum capacity such that it works\" with a monotonic check = binary search on the answer."),
    dict(lvl="hard", q="\"Find the cheapest flight from A to B with at most k stops.\"",
         opts=["Plain BFS", "Bellman-Ford style DP over k+1 rounds (or Dijkstra with stop count in the state)", "Topological sort", "Union-find"], a=1,
         why="Weighted + a limit on edges: relax edges k+1 times, or put (cost, node, stops) in the heap."),
    dict(lvl="hard", q="\"Edges are added one at a time; after each, report the number of connected components.\"",
         opts=["Re-run DFS each time", "Union-find: components decrease by 1 each successful union", "Heap", "Sliding window"], a=1,
         why="Incremental connectivity is exactly what union-find is for: nearly O(1) per edge."),
    dict(lvl="hard", q="\"Minimum number of operations (insert, delete, replace) to turn word1 into word2.\"",
         opts=["Greedy", "2D DP (Edit Distance)", "BFS over strings", "Two pointers"], a=1,
         why="Two strings compared prefix by prefix with three choices = 2D DP. BFS over strings would explode."),
]
