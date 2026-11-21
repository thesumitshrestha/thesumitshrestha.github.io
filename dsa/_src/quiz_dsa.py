"""Extra quiz questions for the DSA pages (added to each page's own QUIZ).
Every page must end up with 20+ questions and at least 6 easy, 6 medium and 6 hard.
Answer options are shuffled in the browser, so `a` is just the index in the list below.
"""


def Q(lvl, q, opts, a, why, code=None):
    d = dict(lvl=lvl, q=q, opts=opts, a=a, why=why)
    if code:
        d["code"] = code
    return d


E, M, H = "easy", "medium", "hard"

MORE = {
"big-o": [
    Q(E, "What is the Big-O of this function?", ["O(1)", "O(n)", "O(n²)", "O(log n)"], 1, "One pass over the list with constant work per item. Space is O(1).",
      "def total(nums):\n    s = 0\n    for x in nums:\n        s += x\n    return s"),
    Q(E, "What is the Big-O of this function?", ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"], 2, "Nested loops over the same list: n × n prints.",
      "def pairs(nums):\n    for a in nums:\n        for b in nums:\n            print(a, b)"),
    Q(E, "O(2n + 5) simplifies to:", ["O(2n)", "O(n)", "O(n + 5)", "O(1)"], 1, "Drop constants and lower terms: only the growth shape matters."),
    Q(E, "Average cost of `d[key]` on a Python dict:", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 0, "The key is hashed straight to its slot."),
    Q(E, "Which grows fastest as n gets large?", ["O(n log n)", "O(n²)", "O(2ⁿ)", "O(n)"], 2, "Exponential beats any polynomial: 2ⁿ doubles with every extra item."),
    Q(E, "Binary search over 1,000,000 sorted items needs about how many checks?", ["20", "1,000", "500,000", "1,000,000"], 0, "2²⁰ ≈ 1,048,576, so about 20 halvings."),
    Q(E, "Extra space used by reversing a list in place with two pointers:", ["O(n)", "O(1)", "O(log n)", "O(n²)"], 1, "Only two index variables, regardless of list size."),
    Q(M, "What is the Big-O of this function?", ["O(log n)", "O(n)", "O(√n)", "O(1)"], 0, "n halves every iteration, so the loop runs about log₂ n times.",
      "def halve(n):\n    steps = 0\n    while n > 1:\n        n //= 2\n        steps += 1\n    return steps"),
    Q(M, "What is the Big-O of this function?", ["O(n)", "O(n log n)", "O(n²)", "O(1)"], 1, "Sorting is O(n log n) and dominates the O(n) scan. A set would make it O(n) time, O(n) space.",
      "def has_dup(nums):\n    nums.sort()\n    for i in range(1, len(nums)):\n        if nums[i] == nums[i-1]:\n            return True\n    return False"),
    Q(M, "In an interview, what is the Big-O of building a string like this?", ["O(n)", "O(n²)", "O(1)", "O(log n)"], 1, "Strings are immutable, so += can copy the whole string each time. CPython sometimes optimizes it, but say O(n²) and use a list + `\"\".join()`.",
      "def build(s):\n    out = \"\"\n    for ch in s:\n        out += ch.upper()\n    return out"),
    Q(M, "Two separate (not nested) loops over the same list of n items:", ["O(n²)", "O(n)", "O(log n)", "O(n log n)"], 1, "n + n = 2n, and constants are dropped."),
    Q(M, "How many times does this loop run?", ["O(n)", "O(log n)", "O(n / 3)", "O(√n)"], 1, "i triples each time, so it reaches n after about log₃ n steps, which is still O(log n).",
      "i = 1\nwhile i < n:\n    i *= 3"),
    Q(M, "A recursive function goes n levels deep and does O(1) work per call. Its space complexity is:", ["O(1)", "O(n)", "O(log n)", "O(n²)"], 1, "Each waiting call sits on the call stack."),
    Q(M, "A LeetCode problem says n ≤ 10⁵. Which complexity should you aim for?", ["O(n²)", "O(n log n) or better", "O(2ⁿ)", "O(n!)"], 1, "10¹⁰ operations (n²) is far too slow; ~10⁶ (n log n) is fine."),
    Q(H, "What is the Big-O, where `b` is a list?", ["O(a + b)", "O(a · b)", "O(a)", "O(b)"], 1, "`x in b` scans b each time. Convert b to a set first and it becomes O(a + b).",
      "def common(a, b):\n    out = []\n    for x in a:\n        if x in b:\n            out.append(x)\n    return out"),
    Q(H, "What is the Big-O of generating all subsets this way?", ["O(n²)", "O(2ⁿ) subsets (O(n · 2ⁿ) to copy them)", "O(n!)", "O(n log n)"], 1, "Each element is in or out: 2ⁿ subsets.",
      "def subsets(nums):\n    if not nums:\n        return [[]]\n    rest = subsets(nums[1:])\n    return rest + [[nums[0]] + r for r in rest]"),
    Q(H, "What is the Big-O?", ["O(n)", "O(n log n)", "O(n²)", "O(n³)"], 2, "The inner loop runs n, n−1, …, 1 times: n(n+1)/2, which is O(n²).",
      "for i in range(n):\n    for j in range(i, n):\n        work()"),
    Q(H, "What is the Big-O?", ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], 1, "The outer loop runs n times; the inner loop doubles j, so it runs log n times each.",
      "for i in range(n):\n    j = 1\n    while j < n:\n        j *= 2"),
    Q(H, "`fib(n)` with memoization (`@cache`) runs in:", ["O(2ⁿ)", "O(n)", "O(n²)", "O(log n)"], 1, "Each fib(k) for k ≤ n is computed once; later calls are lookups."),
    Q(H, "Appending to a Python list n times costs O(n) total even though resizing copies the list. Why?", ["Lists never resize", "The capacity grows by a constant factor, so copies happen rarely and add up to O(n) (amortized O(1) per append)", "Python copies in O(1)", "It's actually O(n²)"], 1, "Copies of size 1, 2, 4, … n sum to about 2n."),
],

"arrays": [
    Q(E, "Index of the last element in a list of n items:", ["n", "n − 1", "n + 1", "0"], 1, "Indexes start at 0, so the last is n − 1 (or `nums[-1]`)."),
    Q(E, "Average cost of `nums.append(x)`:", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 0, "Amortized O(1): the list occasionally resizes, but rarely."),
    Q(E, "Best Time to Buy and Sell Stock: what do you track while scanning prices?", ["The highest price so far", "The lowest price so far, and the best profit", "The average price", "Every pair of days"], 1, "Profit today = price − lowest earlier price."),
    Q(E, "\"Find two numbers in an unsorted array that add to target\" in O(n). Which tool?", ["Binary search", "A hashmap of values seen so far", "Sorting plus nested loops", "Kadane's"], 1, "Check `target − x` in the map as you go."),
    Q(M, "nums = [2, 3, 4, 5] has prefix sums pre = [0, 2, 5, 9, 14]. What is sum(nums[1..3])?", ["9", "12", "14", "7"], 1, "pre[4] − pre[1] = 14 − 2 = 12 (3 + 4 + 5)."),
    Q(M, "3Sum: why skip a value equal to the previous one when choosing the first number?", ["Speed only", "To avoid returning duplicate triplets", "Sorted arrays can't repeat", "Two pointers require it"], 1, "The same first value would produce the same triplets again."),
    Q(M, "Rotate Image (n×n, 90° clockwise, in place). The common two-step trick?", ["Sort each row", "Transpose, then reverse each row", "Reverse the columns twice", "Copy in a spiral into a new matrix"], 1, "Transposing swaps rows and columns; reversing rows finishes the rotation."),
    Q(H, "Maximum Product Subarray: why track both the max and the min product ending at each index?", ["To handle zeros only", "A negative number can turn the smallest product into the largest", "For O(1) space", "It's identical to Kadane's"], 1, "Multiply by a negative and min and max swap roles."),
    Q(H, "Set Matrix Zeroes with O(1) space uses row 0 and column 0 as markers. What extra detail matters?", ["Nothing", "Remember separately whether row 0 / column 0 had a zero originally, and zero them last", "Sort the matrix first", "Use a set of rows"], 1, "Otherwise the markers themselves get confused with real zeros."),
    Q(H, "Subarray Sum Equals K: why start the map as `{0: 1}`?", ["To avoid KeyError", "So a subarray starting at index 0 whose sum is exactly k gets counted", "Because k is never 0", "It handles negatives"], 1, "The empty prefix (sum 0) exists once before any element."),
],

"strings": [
    Q(E, "Python strings are:", ["Mutable", "Immutable", "Linked lists", "Always sorted"], 1, "You can't change a character in place; you create a new string."),
    Q(E, "`'racecar'[::-1]` returns:", ["'racecar'", "'rac'", "An error", "''"], 0, "Reversing a palindrome gives the same word."),
    Q(E, "Valid Anagram on \"rat\" and \"car\":", ["True", "False: the letter counts differ", "Error", "True, same length"], 1, "'t' vs 'c': counts don't match."),
    Q(E, "`'Google'.lower()` returns:", ["'GOOGLE'", "'google'", "'Google'", "An error"], 1, "lower() returns a new all-lowercase string."),
    Q(M, "Permutation in String (does s2 contain a rearrangement of s1?) is best solved with:", ["Expand around center", "A fixed-size sliding window of len(s1) comparing character counts", "Sorting every substring", "A trie"], 1, "Slide a window and update counts in O(1) per step."),
    Q(M, "Longest Common Prefix of [\"flower\", \"flow\", \"flight\"]:", ["'fl'", "'flo'", "'f'", "''"], 0, "All three start with 'fl'; 'flo' fails on 'flight'."),
    Q(M, "Checking every substring of a string for being a palindrome, naively:", ["O(n)", "O(n²)", "O(n³)", "O(n log n)"], 2, "O(n²) substrings × O(n) check each."),
    Q(H, "Edit Distance between \"horse\" and \"ros\":", ["2", "3", "4", "5"], 1, "horse → rorse (replace) → rose (delete r) → ros (delete e)."),
    Q(H, "Minimum Window Substring: total time with n = len(s), m = len(t)?", ["O(n · m)", "O(n + m)", "O(n²)", "O(m log n)"], 1, "Each pointer moves at most n times; building the counter is O(m)."),
    Q(H, "Longest Repeating Character Replacement: why is it OK never to lower `maxFreq` when the window shrinks?", ["It's a bug", "A stale, too-high maxFreq can never make a longer window look valid than one that truly is, so the answer stays correct", "Because k is constant", "Python requires it"], 1, "The answer only grows when a real higher frequency appears."),
],

"linked-lists": [
    Q(E, "In a singly linked list, the last node's `next` is:", ["The head", "None", "Itself", "A random node"], 1, "None marks the end of the list."),
    Q(E, "Inserting a new node at the head costs:", ["O(1)", "O(n)", "O(log n)", "O(n²)"], 0, "Point the new node at the old head; no shifting."),
    Q(E, "Which technique finds the middle in one pass?", ["Pointers from both ends", "Slow and fast pointers", "Binary search", "Hashing"], 1, "When fast reaches the end, slow is halfway."),
    Q(E, "Merging two sorted lists of lengths m and n costs:", ["O(m · n)", "O(m + n)", "O(log(m + n))", "O(1)"], 1, "Each node is visited once."),
    Q(M, "Palindrome Linked List with O(1) extra space:", ["Copy values to an array", "Find the middle, reverse the second half, compare the halves", "Push every node on a stack", "Sort the list"], 1, "Optionally reverse back afterward to restore the list."),
    Q(M, "Add Two Numbers (digits stored in reverse). What's easy to forget at the end?", ["Reversing the result", "An extra node if a final carry of 1 remains", "Sorting", "Removing zeros"], 1, "99 + 1 = 100 needs a new leading digit."),
    Q(M, "Swap Nodes in Pairs on 1→2→3→4:", ["2→1→4→3", "4→3→2→1", "1→3→2→4", "2→1→3→4"], 0, "Each adjacent pair swaps."),
    Q(H, "Linked List Cycle II: after slow and fast meet, how do you find where the cycle starts?", ["Return the meeting node", "Move one pointer to head; step both by one until they meet", "Count the cycle length only", "Reverse the list"], 1, "Floyd's algorithm: the distances work out so they meet at the cycle start."),
    Q(H, "Find the Duplicate Number (values 1..n in n + 1 slots) can be solved like a linked-list cycle because:", ["Arrays are linked lists", "Treating i → nums[i] as a 'next' pointer creates a cycle whose entrance is the duplicate", "The array is sorted", "XOR cancels pairs"], 1, "Two indexes point to the same value: a cycle entrance."),
    Q(H, "Merging k sorted lists by folding them one at a time into the result costs (N total nodes):", ["O(N log k)", "O(N · k)", "O(N)", "O(k log N)"], 1, "Early nodes get re-scanned in every later merge. A heap or pairwise merging gives O(N log k)."),
],

"trees": [
    Q(E, "A node with no children is called a:", ["Root", "Leaf", "Parent", "Edge"], 1, "Leaves are at the bottom of the tree."),
    Q(E, "Maximum number of nodes in a binary tree of height 2 (root at depth 0)?", ["3", "4", "7", "8"], 2, "1 + 2 + 4 = 7."),
    Q(E, "Which DFS order visits a node before its children?", ["Inorder", "Preorder", "Postorder", "None of them"], 1, "Pre = node first."),
    Q(E, "Invert Binary Tree means:", ["Reverse the values", "Swap the left and right child at every node", "Sort the tree", "Delete the leaves"], 1, "A mirror image of the tree."),
    Q(M, "Binary Tree Right Side View: the simplest approach?", ["Inorder traversal", "BFS and take the last node of each level", "Sort the values", "Postorder"], 1, "The last node in each level is what you'd see from the right."),
    Q(M, "Checking whether a tree is height-balanced in O(n):", ["Compute height separately at every node", "One DFS that returns the height, or −1 as soon as any subtree is unbalanced", "BFS only", "Sort the nodes"], 1, "Recomputing heights at every node is O(n²)."),
    Q(M, "Insert 5, 3, 8, 1, 4 into an empty BST. The inorder traversal is:", ["5 3 8 1 4", "1 3 4 5 8", "1 4 3 8 5", "8 5 4 3 1"], 1, "Inorder of any BST is sorted."),
    Q(H, "When serializing a binary tree, why must you record null children?", ["To save space", "Without them, different trees can produce the same sequence", "For speed", "You don't need to"], 1, "Nulls pin down the exact shape."),
    Q(H, "LCA in a general binary tree (recursive). When does a call return the current node?", ["Always", "When p and q are found in different subtrees, or the node itself is p or q", "When it's a leaf", "Never"], 1, "That's the first node where the two paths split."),
    Q(H, "A trie holding N words of average length L: insert cost per word and worst-case number of nodes?", ["O(1) and N", "O(L) and about N · L", "O(log N) and N", "O(N) and L"], 1, "One node per character in the worst case (no shared prefixes)."),
],

"stacks-queues": [
    Q(E, "The simplest stack in Python is:", ["A list with append() and pop()", "A tuple", "A set", "A string"], 0, "Both operations are O(1) at the end of a list."),
    Q(E, "`stack[-1]` does what?", ["Pops the top", "Looks at the top without removing it", "Removes the bottom", "Raises an error"], 1, "Peek. Check the stack isn't empty first."),
    Q(E, "FIFO stands for:", ["First In, First Out", "Fast In, Fast Out", "First In, Final Out", "Final In, First Out"], 0, "That's a queue."),
    Q(E, "Next Greater Element for [2, 1, 3]:", ["[3, 3, -1]", "[1, 3, -1]", "[3, -1, -1]", "[-1, 3, 3]"], 0, "Both 2 and 1 see 3 next; 3 has nothing greater."),
    Q(M, "Simplify Path \"/a/./b/../c/\":", ["\"/a/b/c\"", "\"/a/c\"", "\"/c\"", "\"/a/b\""], 1, "'.' stays put, '..' pops 'b', then push 'c'."),
    Q(M, "Decode String \"3[a2[c]]\":", ["\"accaccacc\"", "\"acacac\"", "\"aaacc\"", "\"acc\""], 0, "a2[c] = \"acc\", repeated 3 times."),
    Q(M, "Asteroid Collision on [5, 10, -5]:", ["[5, 10]", "[5]", "[10]", "[]"], 0, "−5 hits 10 and explodes; 5 and 10 move the same way."),
    Q(H, "A monotonic stack has a while loop inside a for loop. Total time for n elements?", ["O(n²)", "O(n): each index is pushed and popped at most once", "O(n log n)", "O(log n)"], 1, "Count total pushes and pops, not per-iteration work."),
    Q(H, "Basic Calculator (+, −, parentheses): what goes on the stack at '('?", ["Nothing", "The running result and the sign before the '(', restored at ')'", "Each digit", "The whole string"], 1, "Start a fresh sub-result inside the parentheses."),
    Q(H, "Online Stock Span in amortized O(1): what does each stack entry hold?", ["Only prices", "(price, span) pairs, so popped spans are absorbed into the new one", "Indexes sorted ascending", "Nothing"], 1, "Each day is popped at most once."),
],

"graphs": [
    Q(E, "In an undirected graph's adjacency list, edge (a, b) is stored:", ["Only under a", "Under both a and b", "Not at all", "Only in a matrix"], 1, "Each side lists the other as a neighbor."),
    Q(E, "Which traversal uses a stack (or recursion)?", ["BFS", "DFS", "Kahn's algorithm", "Level order"], 1, "DFS goes deep first, backtracking via the stack."),
    Q(E, "A connected graph with no cycles is a:", ["Tree", "Heap", "Grid", "Trie"], 0, "n nodes and n − 1 edges."),
    Q(E, "Flood Fill is basically:", ["Sorting", "DFS/BFS from one cell, recoloring connected same-colored cells", "Binary search", "Dijkstra"], 1, "Same as counting one island."),
    Q(M, "Number of Provinces given an n × n adjacency matrix. Time?", ["O(n)", "O(n²)", "O(n³)", "O(log n)"], 1, "Each node scans a full row of n entries."),
    Q(M, "Clone Graph: why keep an old → new node map?", ["To sort nodes", "To reuse already-cloned nodes and avoid looping forever on cycles", "For speed only", "It isn't needed"], 1, "It doubles as the visited set."),
    Q(M, "Cycle detection in a directed graph with DFS uses which node states?", ["Visited only", "Unvisited / on the current path / finished", "Red and black", "Depth only"], 1, "Reaching a node that's still on the current path means a cycle."),
    Q(H, "Dijkstra with a binary heap runs in:", ["O(V²)", "O((V + E) log V)", "O(V + E)", "O(E²)"], 1, "Each edge may push into the heap; each push/pop is O(log V)."),
    Q(H, "Cheapest Flights Within K Stops: why can plain Dijkstra give the wrong answer?", ["Negative weights", "The cheapest path to a node may use too many stops, so the state must include the stop count", "The graph is unweighted", "The graph is too big"], 1, "Use Bellman-Ford for k+1 rounds, or put (cost, node, stops) in the heap."),
    Q(H, "Swim in Rising Water (minimize the highest cell on a path). Which approaches work?", ["Only plain BFS", "Dijkstra on max-so-far, or binary search on time + BFS, or union-find by elevation", "Topological sort", "Kadane's"], 1, "All three solve this 'minimize the maximum edge' style problem."),
],

"dp": [
    Q(E, "Dynamic programming works when a problem has:", ["Sorted input", "Overlapping subproblems and optimal substructure", "A graph", "Only strings"], 1, "Same subproblems repeat, and best answers build from best sub-answers."),
    Q(E, "Climbing Stairs (1 or 2 steps at a time) for n = 4:", ["4", "5", "6", "8"], 1, "1, 2, 3, 5: it's Fibonacci."),
    Q(E, "Memoization stores results:", ["On disk", "In a cache keyed by the function's arguments", "In a queue", "Nowhere"], 1, "Repeat calls become lookups."),
    Q(E, "Min Cost Climbing Stairs: each state depends on how many earlier states?", ["1", "2", "All of them", "None"], 1, "You arrive from one or two steps below."),
    Q(M, "Decode Ways for \"226\":", ["2", "3", "4", "1"], 1, "2-2-6, 22-6, 2-26."),
    Q(M, "Coin Change II (count combinations): why loop over coins in the outer loop?", ["Speed", "So each combination is counted once rather than every ordering", "Python requires it", "It doesn't matter"], 1, "Amount-outer counts 1+2 and 2+1 separately."),
    Q(M, "How many permutations do n distinct items have?", ["n²", "2ⁿ", "n!", "n"], 2, "n choices for the first, n − 1 for the second, …"),
    Q(H, "LCS uses an (m+1) × (n+1) table. You can reduce space to:", ["O(1)", "O(min(m, n)) by keeping only two rows", "Nothing smaller", "O(log n)"], 1, "Each row depends only on the previous row."),
    Q(H, "Edit Distance transition when s[i] ≠ t[j]:", ["dp[i-1][j-1]", "1 + min(insert, delete, replace)", "The max of the neighbors", "0"], 1, "Try all three operations; take the cheapest."),
    Q(H, "N-Queens: what makes each placement check O(1)?", ["Sorting", "Sets for used columns, diagonals (r − c) and anti-diagonals (r + c)", "A heap", "Binary search"], 1, "Every square on a diagonal shares r − c (or r + c)."),
],

"heaps": [
    Q(E, "The root of a max-heap holds:", ["The smallest value", "The largest value", "The median", "The newest value"], 1, "Every parent ≥ its children."),
    Q(E, "`heapq.heappop(h)` with h = [1, 3, 5] returns:", ["5", "1", "3", "[3, 5]"], 1, "heapq is a min-heap."),
    Q(E, "Is a heap's array fully sorted?", ["Yes", "No, only each parent ≤ its children", "Only the leaves", "Only the root"], 1, "That partial order is why push and pop are O(log n)."),
    Q(E, "Last Stone Weight (always smash the two heaviest) uses:", ["A min-heap", "A max-heap (negate values in Python)", "A queue", "A stack"], 1, "You repeatedly need the two largest."),
    Q(M, "Parent index of the node at index 6:", ["2", "3", "4", "5"], 0, "(6 − 1) // 2 = 2."),
    Q(M, "Task Scheduler: tasks [A, A, A, B, B, B], cooldown n = 2. Minimum time?", ["6", "7", "8", "9"], 2, "A B idle A B idle A B = 8."),
    Q(M, "Heap sort's time and extra space:", ["O(n log n) and O(1)", "O(n²) and O(1)", "O(n) and O(n)", "O(n log n) and O(n)"], 0, "Heapify in place, then pop to the end n times."),
    Q(H, "Sliding Window Median: why two heaps plus lazy deletion?", ["Heaps can't remove arbitrary items cheaply, so you mark leaving items and discard them when they reach the top", "To sort the window", "It's always faster than sorting", "It isn't needed"], 0, "Removing from the middle of a heap is O(k); lazy deletion keeps O(log k)."),
    Q(H, "IPO (pick k projects to maximize capital). The strategy?", ["Sort by profit only", "Sort by required capital; push affordable projects into a max-heap by profit; take the top k times", "DP over subsets", "BFS"], 1, "Greedy: always take the most profitable project you can afford now."),
    Q(H, "Kth Smallest Element in a Sorted Matrix (n × n) with a heap of row heads. Time?", ["O(n²)", "O(k log n)", "O(log n)", "O(n)"], 1, "k pops from a heap of at most n entries."),
],

"hashing": [
    Q(E, "Average cost to insert into a Python dict:", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 0, "Hash, then store in the slot."),
    Q(E, "Which removes duplicates from a list fastest?", ["sorted()", "set()", "list.reverse()", "len()"], 1, "A set keeps one copy of each value."),
    Q(E, "Two Sum with a hashmap: time and space?", ["O(n²) and O(1)", "O(n) and O(n)", "O(n log n) and O(1)", "O(1) and O(n)"], 1, "One pass, storing up to n values."),
    Q(E, "Majority Element (appears more than n/2 times) with O(1) space:", ["A hashmap", "Boyer–Moore voting", "Sorting is required", "A heap"], 1, "Keep a candidate and a count; the majority survives cancellation."),
    Q(M, "Longest Consecutive Sequence in O(n):", ["Sort first", "Put all values in a set; only start counting at x where x − 1 isn't in the set", "Use a heap", "Merge intervals"], 1, "Each run is walked once, from its start."),
    Q(M, "Brick Wall: what do you count?", ["Brick widths", "How many rows have an edge at each position; cut at the most common edge", "The number of rows", "The number of bricks"], 1, "Cuts through an edge don't cross a brick."),
    Q(M, "Word Pattern: \"abba\" with \"dog cat cat fish\":", ["True", "False", "Error", "Depends on case"], 1, "'a' would map to both 'dog' and 'fish'."),
    Q(H, "Why does Python randomize string hashes for each process?", ["Speed", "To stop attackers crafting keys that all collide (hash flooding)", "To save memory", "For sorting"], 1, "Unpredictable hashes defend against O(n) worst-case attacks."),
    Q(H, "A hash table's load factor is:", ["Number of keys ÷ number of buckets; when it gets high the table resizes", "Bytes per key", "Number of collisions", "Hash length"], 0, "Keeping it bounded keeps operations O(1) on average."),
    Q(H, "LRU Cache in Python with O(1) get and put. A built-in shortcut?", ["A list", "OrderedDict with move_to_end() and popitem(last=False)", "heapq", "A set"], 1, "It's a hashmap plus a doubly linked list internally."),
],

"bits": [
    Q(E, "Binary for 10:", ["1010", "1100", "1001", "0110"], 0, "8 + 2 = 10."),
    Q(E, "`7 | 8`:", ["15", "0", "1", "56"], 0, "0111 | 1000 = 1111."),
    Q(E, "`9 >> 1`:", ["18", "4", "5", "3"], 1, "Shifting right floor-divides by 2."),
    Q(E, "Does `64 & 63 == 0` show 64 is a power of two?", ["Yes: a power of two has exactly one 1-bit", "No", "Only for odd numbers", "Can't tell"], 0, "1000000 & 0111111 = 0."),
    Q(M, "Hamming Distance between 1 (001) and 4 (100):", ["1", "2", "3", "0"], 1, "XOR = 101, which has two 1-bits."),
    Q(M, "Reverse Bits: what does the loop body do, 32 times?", ["result = (result << 1) | (n & 1); n >>= 1", "n = ~n", "Sort the bits", "n ^= 1"], 0, "Move each bit from n's right end onto result's right end."),
    Q(M, "Gray Code for n = 2:", ["[0, 1, 3, 2]", "[0, 1, 2, 3]", "[0, 2, 1, 3]", "[3, 2, 1, 0]"], 0, "Neighbors differ by one bit: 00, 01, 11, 10."),
    Q(H, "Generating all subsets with bitmasks costs:", ["O(n)", "O(n · 2ⁿ)", "O(n²)", "O(n!)"], 1, "2ⁿ masks, each checking n bits."),
    Q(H, "`x & -x` gives:", ["The value of x's lowest set bit", "Zero", "x doubled", "The highest bit"], 0, "Two's complement makes −x flip everything above the lowest 1."),
    Q(H, "Divide Two Integers without * or /. The core idea?", ["Subtract 1 repeatedly", "Subtract the largest shifted divisor (divisor << k) that fits, adding 1 << k to the quotient", "Float division", "Binary search on strings"], 1, "That's long division in binary: O(log² n)."),
],

"sorting": [
    Q(E, "Which algorithm splits the list in half and merges the sorted halves?", ["Quicksort", "Merge sort", "Bubble sort", "Counting sort"], 1, "Divide, sort, merge."),
    Q(E, "Insertion sort on already-sorted input runs in:", ["O(n)", "O(n log n)", "O(n²)", "O(1)"], 0, "Each item is already in place: one comparison each."),
    Q(E, "`sorted([3, 1, 2], reverse=True)`:", ["[1, 2, 3]", "[3, 2, 1]", "[3, 1, 2]", "None"], 1, "Largest first."),
    Q(E, "Sort Array By Parity (evens first) in O(n):", ["Sort normally", "Two pointers, swapping evens to the front", "A heap", "Binary search"], 1, "One pass, in place."),
    Q(M, "Quicksort's worst case happens when:", ["Data is random", "Pivots keep splitting very unevenly, e.g. sorted input with a first/last pivot", "The array has 2 items", "You use recursion"], 1, "Random pivots make this very unlikely."),
    Q(M, "Insert Interval: [[1, 3], [6, 9]] + [2, 5]:", ["[[1, 5], [6, 9]]", "[[1, 9]]", "[[2, 5], [6, 9]]", "[[1, 3], [2, 5], [6, 9]]"], 0, "[2, 5] overlaps [1, 3] → [1, 5]; [6, 9] doesn't overlap."),
    Q(M, "Non-overlapping Intervals (minimum removals). The greedy sorts by:", ["Start time", "End time, always keeping the interval that ends earliest", "Length", "Random order"], 1, "Ending early leaves the most room for the rest."),
    Q(H, "Counting sort for n values in the range [0, k): time and space?", ["O(n log n), O(1)", "O(n + k), O(n + k)", "O(k), O(1)", "O(n²), O(n)"], 1, "Fast when k isn't much bigger than n."),
    Q(H, "Maximum Gap in linear time uses:", ["Quicksort", "Bucket sort: with n − 1 gaps the biggest can't be inside one bucket", "A heap", "Merge sort"], 1, "Compare each bucket's min with the previous bucket's max."),
    Q(H, "Is Python's sort stable, and what does that let you do?", ["No", "Yes: sort by the secondary key, then by the primary key, to get a multi-key order", "Only for integers", "Only when reversed"], 1, "Equal items keep their earlier relative order."),
],

"searching": [
    Q(E, "Binary search takes how long on n sorted items?", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 1, "It halves the range each step."),
    Q(E, "Exact-match binary search: nums[mid] < target. Next step?", ["hi = mid", "lo = mid + 1", "lo = mid", "hi = mid + 1"], 1, "The target must be to the right of mid."),
    Q(E, "Guess Number Higher or Lower is:", ["DP", "Binary search on 1..n", "BFS", "Hashing"], 1, "Each guess halves the range."),
    Q(E, "Searching an unsorted array for a value costs:", ["O(log n)", "O(n)", "O(1)", "O(n²)"], 1, "No order means checking each item."),
    Q(M, "Capacity to Ship Packages Within D Days. The range to binary search over is:", ["[1, n]", "[max(weights), sum(weights)]", "[0, max(weights)]", "[min, max]"], 1, "The ship must carry the heaviest package; it never needs more than everything."),
    Q(M, "Peak Index in a Mountain Array [0, 2, 5, 3, 1]:", ["1", "2", "3", "4"], 1, "5 at index 2 is the top."),
    Q(M, "`bisect.bisect_right([1, 2, 2, 3], 2)`:", ["1", "2", "3", "4"], 2, "First index whose value is > 2."),
    Q(H, "Search in Rotated Sorted Array II (duplicates allowed): worst case?", ["O(log n)", "O(n): when nums[lo] == nums[mid] == nums[hi] you can only shrink by one", "O(1)", "O(n log n)"], 1, "Duplicates hide which half is sorted."),
    Q(H, "Minimum Number of Days to Make m Bouquets: each feasibility check is O(n). Total?", ["O(n)", "O(n log(max bloom day))", "O(n²)", "O(log n)"], 1, "Binary search over days, checking each in O(n)."),
    Q(H, "Searching for the *last* index where a condition holds, with `lo = mid`. How do you avoid an infinite loop?", ["mid = (lo + hi) // 2", "Round mid up: mid = (lo + hi + 1) // 2", "mid = lo", "Always set hi = mid − 1"], 1, "Rounding down leaves lo stuck when hi = lo + 1."),
],

"patterns": [
    Q(E, "\"Find the k-th largest element in an array.\"", ["Trie", "Heap (or quickselect)", "Union-find", "Kadane's"], 1, "Top-k means heap."),
    Q(E, "\"Reverse a linked list.\"", ["A heap", "Three pointers (prev, cur, next)", "Binary search", "DP"], 1, "Flip each arrow while saving the rest."),
    Q(E, "\"Maximum depth of a binary tree.\"", ["Sliding window", "DFS returning a value from children", "Two heaps", "Bitmask"], 1, "Depth = 1 + max(left, right)."),
    Q(M, "\"Merge overlapping meeting times.\"", ["A trie", "DFS", "Sort by start, then sweep", "XOR"], 2, "Intervals mean sort and sweep."),
    Q(M, "\"Find a peak element in O(log n).\"", ["BFS", "A hashmap", "Binary search on the slope", "A heap"], 2, "Walk uphill by comparing mid with mid + 1."),
    Q(H, "\"Return the number of ways to decode a digit string.\"", ["Backtracking that lists all outputs", "1D DP", "Union-find", "A heap"], 1, "\"Number of ways\" with overlapping choices is DP."),
    Q(H, "\"Report the median of a stream of numbers after each one.\"", ["Sort after every number", "Binary search", "Two heaps", "A trie"], 2, "A max-heap for the low half and a min-heap for the high half."),
],

"python": [
    Q(E, "`len({1, 1, 2})`:", ["3", "2", "1", "Error"], 1, "Sets drop duplicates."),
    Q(E, "`list(range(5, 0, -2))`:", ["[5, 3, 1]", "[5, 4, 3, 2, 1]", "[1, 3, 5]", "[5, 3]"], 0, "Start 5, stop before 0, step −2."),
    Q(E, "Which counts how many times each letter appears?", ["Counter(s)", "set(s)", "sorted(s)", "list(s)"], 0, "Counter maps each item to its count."),
    Q(E, "`'a-b-c'.split('-')`:", ["['a', 'b', 'c']", "'abc'", "['a-b-c']", "('a', 'b', 'c')"], 0, "split returns a list of the pieces."),
    Q(M, "`divmod(17, 5)`:", ["(3, 2)", "(2, 3)", "3.4", "(17, 5)"], 0, "Quotient 3, remainder 2."),
    Q(M, "For a missing key k: `d.get(k, 0)` vs `d[k]`?", ["Both raise", "get returns 0; d[k] raises KeyError", "Both return 0", "d[k] returns None"], 1, "Use get (or defaultdict) when keys may be missing."),
    Q(M, "`[x * 2 for x in range(4) if x % 2]`:", ["[0, 2, 4, 6]", "[2, 6]", "[1, 3]", "[0, 4]"], 1, "Keeps odd x (1, 3), then doubles them."),
    Q(H, "What does this print?", ["[1, 2]", "[1, 2, 3]", "Error", "[3]"], 1, "b is another name for the same list, not a copy.", "a = [1, 2]\nb = a\nb.append(3)\nprint(a)"),
    Q(H, "`sorted([(2, 'b'), (1, 'z'), (2, 'a')])`:", ["[(1, 'z'), (2, 'a'), (2, 'b')]", "[(1, 'z'), (2, 'b'), (2, 'a')]", "[(2, 'a'), (2, 'b'), (1, 'z')]", "Error"], 0, "Tuples compare field by field."),
    Q(H, "`functools.lru_cache(maxsize=None)` compared with `functools.cache`:", ["Different results", "Equivalent: unbounded memoization", "cache is slower", "lru_cache only works on lists"], 1, "cache is the shorter spelling of an unbounded lru_cache."),
],

"interview": [
    Q(E, "How long is a typical Google coding interview?", ["15 minutes", "About 45 minutes", "2 hours", "A full day"], 1, "Usually one problem plus follow-ups in about 45 minutes."),
    Q(E, "Where do Google interviews often have you write code?", ["A full IDE with autocomplete", "A plain shared doc or simple editor, usually without running the code", "Paper only", "Your own IDE"], 1, "Practice without autocomplete."),
    Q(E, "Should you state time and space complexity without being asked?", ["No", "Yes, for each approach you propose and for the final code", "Only if asked", "Only space"], 1, "It's part of what's graded."),
    Q(E, "Before coding, a good habit is to:", ["Write every test first", "Work through an example by hand", "Ask for the answer", "Pick variable names"], 1, "It confirms you understand the problem."),
    Q(M, "How many STAR stories should you prepare?", ["1", "6–8 that you can adapt", "50", "None"], 1, "A handful of strong stories covers most behavioral questions."),
    Q(M, "In the last week before the interview you should mostly:", ["Learn new advanced topics", "Review your mistakes, redo weak problems, do mocks, and rest", "Stop practicing entirely", "Memorize solutions"], 1, "Taper like an athlete."),
    Q(M, "You've seen the question before. Best move?", ["Pretend it's new and rush", "Say so honestly; they may switch questions or ask you to solve it anyway", "Refuse to answer", "Recite memorized code"], 1, "Honesty is valued, and memorized answers show up in follow-ups."),
    Q(M, "You can't remember a library function's exact name. What do you do?", ["Freeze", "Say what you'd use, write a small helper or a reasonable name, and move on", "Switch languages", "Skip the problem"], 1, "Interviewers care about logic, not perfect API recall."),
    Q(H, "Your solution works but is one unclear 40-line function, with 3 minutes left. Best use of the time?", ["Nothing", "Explain how you'd split it into named helpers and which tests you'd add", "Rewrite it in another language", "Comment every line"], 1, "Shows code-quality judgment without risking working code."),
    Q(H, "The interviewer is quiet and gives no feedback. You should:", ["Assume you're failing", "Keep narrating and check in briefly (\"does this approach make sense?\")", "Stop talking", "Ask for the answer"], 1, "Many interviewers stay neutral on purpose."),
    Q(H, "After the interview loop, how are Google hiring decisions made?", ["The last interviewer decides", "All interviewers' written feedback is reviewed together, then team matching", "The recruiter decides alone", "Randomly"], 1, "No single interview decides on its own."),
],
}
