META = dict(
    title="Trees and tries", page_title="Trees and Tries · DSA Field Guide", week="Week 4", group="Data structures",
    h1="Trees and tries",
    lead="Trees are one of Google's favorite topics. Nearly every tree problem is a DFS where you decide what each node returns to its parent, or a BFS by levels.",
    blurb="DFS, BFS, traversals, BSTs, LCA, tree construction, tries.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A family tree, upside down</h2>
  <div class="real big-real">
    <p>A company org chart. The CEO is the <strong>root</strong>; each manager has direct reports (<strong>children</strong>); people with no reports are <strong>leaves</strong>. To ask "how many people are in Engineering?", you ask the head of Engineering, who asks each of their managers, who ask theirs, and the answers add up on the way back. That bottom-up reporting is recursion on a tree.</p>
  </div>
<pre class="diagram">            8          ← root          depth 0
          /   \
         3     10                      depth 1
        / \      \
       1   6      14                   depth 2
          / \    /
         4   7  13     ← leaves        depth 3      height = 3</pre>
<pre><code><span class="k">class</span> TreeNode:
    <span class="k">def</span> __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right</code></pre>
  <p>This particular tree is a <strong>binary search tree (BST)</strong>: everything in a node's left subtree is smaller, everything on the right is larger. That rule makes search O(height), which is O(log n) if the tree is balanced and O(n) if it degrades into a line.</p>
</section>

<section id="traversals">
  <span class="eyebrow">Traversals</span>
  <h2>Four ways to visit every node</h2>
  <div class="tbl"><table>
    <thead><tr><th>Order</th><th>Visit</th><th>On the tree above</th><th>Typical use</th></tr></thead>
    <tbody>
      <tr><td>Preorder</td><td>node, left, right</td><td><code>8 3 1 6 4 7 10 14 13</code></td><td>Copy / serialize a tree</td></tr>
      <tr><td>Inorder</td><td>left, node, right</td><td><code>1 3 4 6 7 8 10 13 14</code></td><td>BST → sorted order</td></tr>
      <tr><td>Postorder</td><td>left, right, node</td><td><code>1 4 7 6 3 13 14 10 8</code></td><td>Children's answers needed first (height, delete)</td></tr>
      <tr><td>Level order (BFS)</td><td>row by row</td><td><code>8 | 3 10 | 1 6 14 | 4 7 13</code></td><td>Anything "by level" or shortest depth</td></tr>
    </tbody>
  </table></div>
  <figure class="anim" data-anim="trees-inorder"><figcaption>Iterative inorder traversal with a stack</figcaption></figure>
  <div class="real"><p>Reading a book: preorder is reading each chapter title before its sections (a table of contents). Postorder is a manager who only reports a total after every team has reported (computing folder sizes on your disk). Level order is a seating chart, row by row.</p></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Six tree patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. DFS that returns a value (bottom-up)</h3><span class="cx">O(n) time · O(h) stack</span></div>
    <div class="real"><p>A building's fire warden asks each floor warden "how many people on your floor and above?" Each floor asks the floor above, adds its own count, and reports down. The question is the same at every level; only the numbers change.</p></div>
    <p class="when"><b>Use when</b>the answer for a node depends on answers from its children: height, size, balanced?, diameter, max path sum.</p>
<pre><code><span class="k">def</span> max_depth(root):
    <span class="k">if not</span> root: <span class="k">return</span> 0                      <span class="c"># base case</span>
    <span class="k">return</span> 1 + max(max_depth(root.left), max_depth(root.right))</code></pre>
    <p class="note">The recipe: (1) what does an empty tree return? (2) what does this node return, given its children's returns? Answer those two questions and the code writes itself.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. DFS with a global answer</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>Each regional office reports its best single-region sales number upward, but head office also tracks a separate leaderboard for the best combined deal between two regions. What a node returns and what it records are different things.</p></div>
    <p class="when"><b>Use when</b>the best answer may "bend" through a node (diameter, max path sum) but a parent can only extend one straight branch.</p>
<pre><code><span class="k">def</span> diameter(root):
    best = 0
    <span class="k">def</span> depth(node):
        <span class="k">nonlocal</span> best
        <span class="k">if not</span> node: <span class="k">return</span> 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)        <span class="c"># path bending here</span>
        <span class="k">return</span> 1 + max(l, r)           <span class="c"># straight branch for the parent</span>
    depth(root)
    <span class="k">return</span> best</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. BFS level by level</h3><span class="cx">O(n) time · O(width) space</span></div>
    <div class="real"><p>Ripples from a stone: everything one ring out is reached before anything two rings out. A queue holds the current ring; you finish it before starting the next.</p></div>
    <p class="when"><b>Use when</b>output is grouped by level, or you need the shallowest/closest node.</p>
<pre><code><span class="k">from</span> collections <span class="k">import</span> deque
<span class="k">def</span> level_order(root):
    <span class="k">if not</span> root: <span class="k">return</span> []
    out, q = [], deque([root])
    <span class="k">while</span> q:
        level = []
        <span class="k">for</span> _ <span class="k">in</span> range(len(q)):          <span class="c"># exactly this level's nodes</span>
            node = q.popleft()
            level.append(node.val)
            <span class="k">if</span> node.left:  q.append(node.left)
            <span class="k">if</span> node.right: q.append(node.right)
        out.append(level)
    <span class="k">return</span> out</code></pre>
  <figure class="anim" data-anim="trees-bfs"><figcaption>BFS visiting the tree level by level</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. BST range checking (top-down)</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>A house-hunting filter: "price between $300k and $500k." Going left in a BST tightens the maximum; going right tightens the minimum. Each node is checked against the allowed range it inherited from all its ancestors, not just its parent.</p></div>
    <p class="when"><b>Use when</b>validating a BST, or any time constraints flow down from ancestors.</p>
<pre><code><span class="k">def</span> is_valid_bst(node, lo=float('-inf'), hi=float('inf')):
    <span class="k">if not</span> node: <span class="k">return</span> True
    <span class="k">if not</span> (lo &lt; node.val &lt; hi): <span class="k">return</span> False
    <span class="k">return</span> (is_valid_bst(node.left, lo, node.val) <span class="k">and</span>
            is_valid_bst(node.right, node.val, hi))</code></pre>
    <p class="note">The classic bug: only comparing a node with its parent. A 4 in the right subtree of 5's left child can still violate the root.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Lowest common ancestor</h3><span class="cx">O(h) in a BST · O(n) in a general tree</span></div>
    <div class="real"><p>Two cousins want their closest shared ancestor. Each walks up the family tree; the first person who appears on both paths is the answer. In a BST it's simpler: start at the root and walk toward both; the node where they'd split directions is the LCA.</p></div>
    <p class="when"><b>Use when</b>asked for the meeting point of two nodes.</p>
<pre><code><span class="k">def</span> lca_bst(root, p, q):
    <span class="k">while</span> root:
        <span class="k">if</span> p.val &lt; root.val <span class="k">and</span> q.val &lt; root.val: root = root.left
        <span class="k">elif</span> p.val &gt; root.val <span class="k">and</span> q.val &gt; root.val: root = root.right
        <span class="k">else</span>: <span class="k">return</span> root                 <span class="c"># they split here</span>

<span class="k">def</span> lca(root, p, q):                          <span class="c"># any binary tree</span>
    <span class="k">if not</span> root <span class="k">or</span> root <span class="k">is</span> p <span class="k">or</span> root <span class="k">is</span> q: <span class="k">return</span> root
    l, r = lca(root.left, p, q), lca(root.right, p, q)
    <span class="k">return</span> root <span class="k">if</span> l <span class="k">and</span> r <span class="k">else</span> l <span class="k">or</span> r</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. Trie (prefix tree)</h3><span class="cx">O(L) per word, L = word length</span></div>
    <div class="real"><p>Your phone's keyboard autocomplete. After you type "goo", it walks g → o → o in a tree of letters and suggests everything below that point: "good", "google", "goose". Words that share a prefix share the same path, so the prefix is stored once.</p></div>
    <p class="when"><b>Use when</b>the problem says prefix, autocomplete, dictionary of words, or searching many words in a grid (Word Search II).</p>
<pre><code><span class="k">class</span> Trie:
    <span class="k">def</span> __init__(self):
        self.root = {}
    <span class="k">def</span> insert(self, word):
        node = self.root
        <span class="k">for</span> ch <span class="k">in</span> word:
            node = node.setdefault(ch, {})
        node['$'] = True                     <span class="c"># end-of-word marker</span>
    <span class="k">def</span> _walk(self, s):
        node = self.root
        <span class="k">for</span> ch <span class="k">in</span> s:
            <span class="k">if</span> ch <span class="k">not in</span> node: <span class="k">return</span> None
            node = node[ch]
        <span class="k">return</span> node
    <span class="k">def</span> search(self, word):
        node = self._walk(word); <span class="k">return</span> bool(node) <span class="k">and</span> '$' <span class="k">in</span> node
    <span class="k">def</span> startsWith(self, prefix):
        <span class="k">return</span> self._walk(prefix) <span class="k">is not</span> None</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Binary Tree Maximum Path Sum</h2>
  <div class="real"><p>A hiker plans a route across a mountain range where each peak gives or costs energy. The route can go up one side of a peak and down the other, but it can't branch. Bad sections (negative values) are simply skipped by starting or ending the route elsewhere.</p></div>
  <div class="trace">
    <div><p>At each node, ask each child for the best <em>straight</em> path going down from it. If that's negative, use 0 (don't take that branch).</p></div>
    <div><p>A path that <em>bends</em> at this node is worth <code>node.val + left + right</code>. Compare it with the global best.</p></div>
    <div><p>Return to the parent only <code>node.val + max(left, right)</code>, because the parent can extend just one branch.</p></div>
  </div>
<pre><code><span class="k">def</span> max_path_sum(root):
    best = float('-inf')
    <span class="k">def</span> gain(node):
        <span class="k">nonlocal</span> best
        <span class="k">if not</span> node: <span class="k">return</span> 0
        l = max(gain(node.left), 0)
        r = max(gain(node.right), 0)
        best = max(best, node.val + l + r)
        <span class="k">return</span> node.val + max(l, r)
    gain(root)
    <span class="k">return</span> best</code></pre>
  <p><strong>Complexity:</strong> O(n) time, O(h) space for recursion. Start <code>best</code> at negative infinity, not 0, so an all-negative tree returns its largest single value.</p>
  <div class="google"><p>When a tree problem stumps you, ask: "What should each node return to its parent, and is the final answer the same thing or something different?" If different, you need a global variable like <code>best</code>.</p></div>
</section>

<section id="construct">
  <span class="eyebrow">Construction</span>
  <h2>Building a tree from preorder + inorder</h2>
  <div class="real"><p>Rebuilding a seating plan from two lists: the order guests arrived (preorder tells you who's the head of each table first) and their left-to-right seat order (inorder tells you who sits left vs right of that head).</p></div>
  <p>Preorder's first value is the root. Find it in inorder: everything left of it is the left subtree, everything right is the right subtree. Recurse. Use a value → index map so each lookup is O(1), making the whole build O(n).</p>
<pre><code><span class="k">def</span> build(preorder, inorder):
    idx = {v: i <span class="k">for</span> i, v <span class="k">in</span> enumerate(inorder)}
    it = iter(preorder)
    <span class="k">def</span> go(lo, hi):
        <span class="k">if</span> lo &gt; hi: <span class="k">return</span> None
        val = next(it)
        node = TreeNode(val)
        node.left = go(lo, idx[val] - 1)
        node.right = go(idx[val] + 1, hi)
        <span class="k">return</span> node
    <span class="k">return</span> go(0, len(inorder) - 1)</code></pre>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases to test</h2>
  <div class="real"><p>An org chart with only the CEO, or one where everyone reports in a single chain, breaks more reporting tools than a normal company does.</p></div>
  <ul>
    <li>Empty tree (<code>root is None</code>) and a single node.</li>
    <li>A skewed tree (a straight line): height = n, recursion depth = n. Python's default limit is 1,000.</li>
    <li>Negative values (max path sum).</li>
    <li>Duplicate values in a BST: ask whether they go left, right, or are disallowed.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Maximum Depth of Binary Tree", "maximum-depth-of-binary-tree", "easy", "DFS returns height"),
    ("Invert Binary Tree", "invert-binary-tree", "easy", "Swap children recursively"),
    ("Same Tree", "same-tree", "easy", "Compare in lockstep"),
    ("Subtree of Another Tree", "subtree-of-another-tree", "easy", "Same Tree at every node"),
    ("Binary Tree Level Order Traversal", "binary-tree-level-order-traversal", "medium", "BFS with level size"),
    ("Validate Binary Search Tree", "validate-binary-search-tree", "medium", "Pass (lo, hi) down"),
    ("Lowest Common Ancestor of a Binary Search Tree", "lowest-common-ancestor-of-a-binary-search-tree", "medium", "Walk until paths split"),
    ("Diameter of Binary Tree", "diameter-of-binary-tree", "medium", "Return depth, record l + r"),
    ("Kth Smallest Element in a BST", "kth-smallest-element-in-a-bst", "medium", "Inorder, stop at k"),
    ("Construct Binary Tree from Preorder and Inorder Traversal", "construct-binary-tree-from-preorder-and-inorder-traversal", "medium", "Root from preorder, split by inorder"),
    ("Implement Trie (Prefix Tree)", "implement-trie-prefix-tree", "medium", "Nested dicts + end marker"),
    ("Binary Tree Maximum Path Sum", "binary-tree-maximum-path-sum", "hard", "Return one branch, record the bend"),
    ("Word Search II", "word-search-ii", "hard", "Trie + grid DFS with pruning"),
]

QUIZ = [
    dict(lvl="easy", q="Which traversal of a BST gives values in sorted order?",
         opts=["Preorder", "Inorder", "Postorder", "Level order"], a=1, why="Left subtree (smaller), node, right subtree (larger)."),
    dict(lvl="easy", q="What data structure does BFS use?",
         opts=["Stack", "Queue (`deque`)", "Heap", "Set only"], a=1, why="First in, first out keeps nodes in level order. Use `deque.popleft()`, not `list.pop(0)`."),
    dict(lvl="easy", q="Search in a balanced BST with n nodes costs:",
         opts=["O(1)", "O(log n)", "O(n)", "O(n log n)"], a=1, why="Each step discards one subtree, and a balanced tree's height is about log n."),
    dict(lvl="medium", q="Is this a valid BST?", code="      5\n     / \\\n    3   8\n       / \\\n      4   9",
         opts=["Yes", "No, 4 is in 5's right subtree but less than 5", "No, 9 is too big", "No, 3 has no children"], a=1,
         why="4 < 8 satisfies its parent, but every node right of 5 must exceed 5. Pass bounds down, don't just compare with the parent."),
    dict(lvl="medium", q="What is the space complexity of recursive DFS on a tree with height h?",
         opts=["O(1)", "O(h)", "O(n²)", "O(log h)"], a=1, why="The call stack holds one frame per level. h is log n when balanced, n when skewed."),
    dict(lvl="medium", q="In Diameter of Binary Tree, why return `1 + max(l, r)` but record `l + r`?",
         opts=["They're the same", "A parent can extend only one branch; the diameter may bend through this node", "To avoid recursion", "It's a bug"], a=1,
         why="Returned value = longest straight path down. Recorded value = path through this node joining both sides."),
    dict(lvl="medium", q="Kth Smallest in a BST: the most direct approach?",
         opts=["BFS and sort", "Inorder traversal and stop at the k-th visited node", "Heap of all values", "Binary search on values"], a=1,
         why="Inorder visits BST values in sorted order, so the k-th visit is the answer: O(h + k) time with an iterative stack."),
    dict(lvl="hard", q="Max Path Sum on a tree whose only node is -3. What should be returned, and which init causes a bug?",
         opts=["0; init best = -inf", "-3; init best = 0 would wrongly return 0", "-3; init best = -inf would crash", "0; it's an empty path"], a=1,
         why="A path must contain at least one node. Starting best at 0 hides all-negative answers."),
    dict(lvl="hard", q="Word Search II with 10⁴ words on a grid. Why a trie instead of running Word Search for each word?",
         opts=["Tries use less memory", "One DFS from each cell explores all words sharing a prefix at once and prunes when no word continues", "Tries sort the words", "It isn't faster"], a=1,
         why="Per-word search repeats the same grid walks thousands of times. The trie shares prefixes and stops a path the moment no word matches it."),
    dict(lvl="hard", q="Build tree from preorder + inorder. What makes the naive version O(n²), and the fix?",
         opts=["Recursion; use iteration", "Searching inorder for the root each call; precompute value → index map", "Slicing is fine", "Sorting; avoid it"], a=1,
         why="Each `inorder.index(root)` (and list slicing) is O(n). A dict lookup plus passing index bounds makes it O(n) total."),
]
