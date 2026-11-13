META = dict(
    title="Linked lists", page_title="Linked Lists · DSA Field Guide", week="Week 3", group="Data structures",
    h1="Linked lists",
    lead="Linked list problems are pointer puzzles. The algorithms are short; the difficulty is not losing a node while you rewire. Draw boxes and arrows every time.",
    blurb="Fast/slow pointers, reversal, dummy nodes, merging, cycle detection.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A treasure hunt of clues</h2>
  <div class="real big-real">
    <p>A scavenger hunt: each clue tells you where the next clue is hidden. To reach clue 50 you must follow clues 1 to 49; there's no jumping. But adding a new clue in the middle is easy: rewrite one clue to point to the new spot, and have the new clue point to where the old one used to go. That's a linked list: slow to reach position k, cheap to insert once you're there.</p>
  </div>
<pre class="diagram">head
 │
 ▼
┌───┬──┐    ┌───┬──┐    ┌───┬──┐    ┌───┬──────┐
│ 3 │ ─┼──▶ │ 7 │ ─┼──▶ │ 1 │ ─┼──▶ │ 9 │ None │
└───┴──┘    └───┴──┘    └───┴──┘    └───┴──────┘
 val next</pre>
<pre><code><span class="k">class</span> ListNode:
    <span class="k">def</span> __init__(self, val=0, next=None):
        self.val = val
        self.next = next</code></pre>
</section>

<section id="ops">
  <span class="eyebrow">Costs</span>
  <h2>Linked list vs array</h2>
  <div class="tbl"><table>
    <thead><tr><th>Operation</th><th>Linked list</th><th>Array</th></tr></thead>
    <tbody>
      <tr><td>Access k-th item</td><td><span class="pill on">O(n)</span></td><td><span class="pill o1">O(1)</span></td></tr>
      <tr><td>Insert/delete at head</td><td><span class="pill o1">O(1)</span></td><td><span class="pill on">O(n)</span></td></tr>
      <tr><td>Insert/delete after a node you hold</td><td><span class="pill o1">O(1)</span></td><td><span class="pill on">O(n)</span></td></tr>
      <tr><td>Search</td><td><span class="pill on">O(n)</span></td><td><span class="pill on">O(n)</span></td></tr>
      <tr><td>Extra memory per item</td><td>One pointer</td><td>None</td></tr>
    </tbody>
  </table></div>
  <div class="real"><p>Where you've used one: your browser's back/forward history, a music playlist's "next song," and an LRU cache (a hashmap plus a doubly linked list) behind almost every web service.</p></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Five linked list patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Dummy (sentinel) node</h3><span class="cx">Removes head special cases</span></div>
    <div class="real"><p>A queue of people where the person at the front might leave. Instead of handling "the first person left" separately, you put a cardboard cutout at the very front. Nobody ever removes the cutout, so the real front is always <code>cutout.next</code>.</p></div>
    <p class="when"><b>Use when</b>the head might change: merging, deleting nodes, partitioning.</p>
<pre><code><span class="k">def</span> merge(a, b):
    dummy = tail = ListNode()
    <span class="k">while</span> a <span class="k">and</span> b:
        <span class="k">if</span> a.val &lt;= b.val: tail.next, a = a, a.next
        <span class="k">else</span>:              tail.next, b = b, b.next
        tail = tail.next
    tail.next = a <span class="k">or</span> b          <span class="c"># attach the leftovers</span>
    <span class="k">return</span> dummy.next</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Reversal (three pointers)</h3><span class="cx">O(n) time · O(1) space</span></div>
    <div class="real"><p>Turning around a conga line one person at a time. Before you turn someone to face backwards, someone must hold the hand of the next person, or the rest of the line wanders off. That held hand is <code>nxt</code>.</p></div>
    <p class="when"><b>Use when</b>reversing all or part of a list (Reverse Nodes in k-Group, Reorder List, palindrome check).</p>
<pre><code><span class="k">def</span> reverse(head):
    prev, cur = None, head
    <span class="k">while</span> cur:
        nxt = cur.next     <span class="c"># 1. save the rest</span>
        cur.next = prev    <span class="c"># 2. flip the arrow</span>
        prev = cur         <span class="c"># 3. step prev forward</span>
        cur = nxt          <span class="c"># 4. step cur forward</span>
    <span class="k">return</span> prev           <span class="c"># new head</span></code></pre>
<pre class="diagram">before:  None   1 → 2 → 3 → None
step 1:  None ← 1   2 → 3 → None     prev=1 cur=2
step 2:  None ← 1 ← 2   3 → None     prev=2 cur=3
step 3:  None ← 1 ← 2 ← 3            prev=3 cur=None → return 3</pre>
  <figure class="anim" data-anim="ll-reverse"><figcaption>Reversing 1 → 2 → 3 → 4</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Fast and slow pointers</h3><span class="cx">O(n) time · O(1) space</span></div>
    <div class="real"><p>Two runners on a track, one twice as fast. On a straight road, when the fast one finishes, the slow one is exactly halfway (find the middle). On a circular track, the fast one eventually laps the slow one (cycle detection).</p></div>
    <p class="when"><b>Use when</b>finding the middle, detecting a cycle, or finding where a cycle starts.</p>
<pre><code><span class="k">def</span> middle(head):
    slow = fast = head
    <span class="k">while</span> fast <span class="k">and</span> fast.next:
        slow, fast = slow.next, fast.next.next
    <span class="k">return</span> slow

<span class="k">def</span> has_cycle(head):
    slow = fast = head
    <span class="k">while</span> fast <span class="k">and</span> fast.next:
        slow, fast = slow.next, fast.next.next
        <span class="k">if</span> slow <span class="k">is</span> fast: <span class="k">return</span> True
    <span class="k">return</span> False</code></pre>
  <figure class="anim" data-anim="ll-fast-slow"><figcaption>Slow and fast pointers finding the middle</figcaption></figure>
    <p class="note">Floyd's bonus: after they meet, reset one pointer to <code>head</code> and move both one step at a time. They meet again exactly at the start of the cycle.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Gap of n (two pointers, fixed distance)</h3><span class="cx">One pass</span></div>
    <div class="real"><p>Two hikers tied by a 5-metre rope walk a trail. When the front hiker reaches the end, the back hiker is exactly 5 metres from the end. That's how you find the n-th node from the end in one pass.</p></div>
    <p class="when"><b>Use when</b>the problem says "k-th from the end."</p>
<pre><code><span class="k">def</span> remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    <span class="k">for</span> _ <span class="k">in</span> range(n + 1): fast = fast.next   <span class="c"># gap of n+1</span>
    <span class="k">while</span> fast:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next      <span class="c"># slow is just before the target</span>
    <span class="k">return</span> dummy.next</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Hashmap old → new (deep copy)</h3><span class="cx">O(n) time · O(n) space</span></div>
    <div class="real"><p>Copying a school's buddy system to a new school. First make a new student for every old student and write down "old Alice → new Alice." Then, for each pair, look up the new versions of their buddies. Copy List with Random Pointer works the same way.</p></div>
    <p class="when"><b>Use when</b>cloning a structure whose pointers can go anywhere.</p>
<pre><code><span class="k">def</span> copy_random_list(head):
    old2new = {None: None}
    cur = head
    <span class="k">while</span> cur:                         <span class="c"># pass 1: make nodes</span>
        old2new[cur] = Node(cur.val); cur = cur.next
    cur = head
    <span class="k">while</span> cur:                         <span class="c"># pass 2: wire pointers</span>
        old2new[cur].next = old2new[cur.next]
        old2new[cur].random = old2new[cur.random]
        cur = cur.next
    <span class="k">return</span> old2new[head]</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Reorder List: three patterns in one</h2>
  <div class="real"><p>Shuffling a deck by cutting it in half, flipping the bottom half over, and riffling the two halves together one card at a time.</p></div>
  <p>Turn <code>1 → 2 → 3 → 4 → 5</code> into <code>1 → 5 → 2 → 4 → 3</code> in O(1) extra space.</p>
  <div class="trace">
    <div><p><strong>Find the middle</strong> with fast/slow pointers: node 3.</p></div>
    <div><p><strong>Cut and reverse the second half:</strong> <code>4 → 5</code> becomes <code>5 → 4</code>. Set <code>middle.next = None</code> so the first half ends cleanly.</p></div>
    <div><p><strong>Merge alternately:</strong> 1, 5, 2, 4, 3. Save both <code>next</code> pointers before rewiring each pair.</p></div>
  </div>
<pre><code><span class="k">def</span> reorder(head):
    slow = fast = head
    <span class="k">while</span> fast.next <span class="k">and</span> fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = reverse(slow.next), None
    first = head
    <span class="k">while</span> second:
        n1, n2 = first.next, second.next
        first.next, second.next = second, n1
        first, second = n1, n2</code></pre>
  <div class="google"><p>Google interviewers like problems that combine patterns. Name each step out loud ("I'll find the middle, reverse the back half, then merge") before writing any code.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases to test</h2>
  <div class="real"><p>A train conductor checks the engine, the caboose, and a one-car train, because that's where couplings go wrong.</p></div>
  <ul>
    <li>Empty list (<code>head is None</code>) and a single node.</li>
    <li>Two nodes (middle and reversal logic often break here).</li>
    <li>Removing the head itself, which is why dummy nodes exist.</li>
    <li>Even vs odd length when finding the middle.</li>
    <li>Calling <code>.next</code> on <code>None</code>: check <code>fast and fast.next</code> in that order.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Reverse Linked List", "reverse-linked-list", "easy", "Three pointers"),
    ("Merge Two Sorted Lists", "merge-two-sorted-lists", "easy", "Dummy node"),
    ("Linked List Cycle", "linked-list-cycle", "easy", "Fast/slow"),
    ("Middle of the Linked List", "middle-of-the-linked-list", "easy", "Fast/slow"),
    ("Remove Nth Node From End of List", "remove-nth-node-from-end-of-list", "medium", "Gap of n + dummy"),
    ("Reorder List", "reorder-list", "medium", "Middle + reverse + merge"),
    ("Add Two Numbers", "add-two-numbers", "medium", "Dummy node + carry"),
    ("Copy List with Random Pointer", "copy-list-with-random-pointer", "medium", "Hashmap old → new"),
    ("Swap Nodes in Pairs", "swap-nodes-in-pairs", "medium", "Dummy + rewire pairs"),
    ("Sort List", "sort-list", "medium", "Merge sort: middle, split, merge"),
    ("Reverse Nodes in k-Group", "reverse-nodes-in-k-group", "hard", "Count k, reverse segment, reconnect"),
]

QUIZ = [
    dict(lvl="easy", q="What is the cost of accessing the 1,000th node of a linked list?",
         opts=["O(1)", "O(log n)", "O(n)", "O(n²)"], a=2, why="You must follow 999 `next` pointers from the head; there's no address arithmetic."),
    dict(lvl="easy", q="Why use a dummy node when merging two sorted lists?",
         opts=["It makes the code faster", "It avoids a special case for choosing the head", "Python requires it", "It saves memory"], a=1,
         why="You always append to `tail.next`, and return `dummy.next` at the end, so the first node needs no special handling."),
    dict(lvl="easy", q="In the reversal loop, what goes wrong if you skip `nxt = cur.next`?",
         opts=["Nothing", "After `cur.next = prev` you've lost the rest of the list", "It reverses twice", "It loops forever on short lists"], a=1,
         why="Flipping the arrow overwrites the only reference to the remainder. Save it first."),
    dict(lvl="medium", q="For `1→2→3→4` (even length), where does `slow` end with `while fast and fast.next`?",
         opts=["Node 1", "Node 2", "Node 3", "Node 4"], a=2,
         why="fast: 1→3→None. slow: 1→2→3. You get the second middle. Use `while fast.next and fast.next.next` for the first middle."),
    dict(lvl="medium", q="Why does the fast pointer always meet the slow one inside a cycle?",
         opts=["Luck", "Inside the loop, fast gains exactly one node per step, so the gap shrinks to 0 without skipping over", "Because fast restarts at head", "It doesn't always"], a=1,
         why="Relative speed is 1 node per step, so the distance decreases by exactly 1 each step and must hit 0."),
    dict(lvl="medium", q="Remove Nth From End: why move `fast` n+1 steps from the dummy instead of n?",
         opts=["Off-by-one so slow stops on the node *before* the target", "To skip the head", "To handle cycles", "It's a typo"], a=0,
         why="To delete a node you need its predecessor. The extra step leaves slow one node earlier."),
    dict(lvl="medium", q="Time and space of Sort List using merge sort on the list?",
         opts=["O(n²), O(1)", "O(n log n), O(log n) recursion stack", "O(n), O(n)", "O(n log n), O(n) for an array copy"], a=1,
         why="Splitting with fast/slow and merging is n log n. Linked lists merge without extra arrays; recursion depth is log n."),
    dict(lvl="hard", q="After Floyd's pointers meet inside a cycle, why does resetting one to head and stepping both by 1 find the cycle start?",
         opts=["Coincidence", "Distance from head to start equals distance from meeting point to start (mod cycle length)", "Because the list is sorted", "The fast pointer stops at the start"], a=1,
         why="If head→start is a and start→meet is b with cycle length c, then 2(a+b) = a+b+kc, so a = kc − b: walking a steps from the meeting point lands on the start."),
    dict(lvl="hard", q="An LRU cache needs O(1) get and put. Which structure combination?",
         opts=["Array + binary search", "Hashmap + doubly linked list", "Heap + hashmap", "Two stacks"], a=1,
         why="The hashmap finds a node in O(1); the doubly linked list moves it to the front or removes the oldest in O(1)."),
    dict(lvl="hard", q="Reverse Nodes in k-Group: what must you do if fewer than k nodes remain?",
         opts=["Reverse them anyway", "Leave them in original order", "Delete them", "Raise an error"], a=1,
         why="The problem keeps the leftovers as-is. Count k nodes ahead before reversing; if you can't, stop."),
]
