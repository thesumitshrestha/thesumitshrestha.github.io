META = dict(
    title="Stacks and queues", page_title="Stacks and Queues · DSA Field Guide", week="Week 5", group="Data structures",
    h1="Stacks and queues",
    lead="Two simple containers with strict rules about which item leaves next. The monotonic stack built on top of them solves a whole family of \"next greater\" problems in O(n).",
    blurb="LIFO and FIFO, monotonic stacks, parentheses, expression evaluation.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A stack of plates and a coffee line</h2>
  <div class="real big-real">
    <p><strong>Stack (LIFO, last in first out):</strong> a stack of plates in a cafeteria. You add to the top and take from the top. The plate washed most recently is used first. Your browser's Back button and your editor's Undo work the same way.</p>
    <p><strong>Queue (FIFO, first in first out):</strong> the line at a coffee shop. People join at the back and are served from the front, in arrival order. Printer jobs and BFS work the same way.</p>
  </div>
<pre class="diagram">STACK (list)                     QUEUE (deque)
  push → │ 9 │ ← pop               front                 back
         │ 4 │                     popleft ← │ 3 │ 8 │ 1 │ ← append
         │ 7 │                               └───┴───┴───┘
         └───┘</pre>
  <div class="tbl"><table>
    <thead><tr><th>Operation</th><th>Python</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>Stack push / pop / peek</td><td><code>st.append(x)</code>, <code>st.pop()</code>, <code>st[-1]</code></td><td><span class="pill o1">O(1)</span></td></tr>
      <tr><td>Queue enqueue / dequeue</td><td><code>q.append(x)</code>, <code>q.popleft()</code> on a <code>deque</code></td><td><span class="pill o1">O(1)</span></td></tr>
      <tr><td>Queue with a list (avoid)</td><td><code>lst.pop(0)</code></td><td><span class="pill on">O(n)</span></td></tr>
    </tbody>
  </table></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Five stack and queue patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Matching pairs</h3><span class="cx">O(n) time · O(n) space</span></div>
    <div class="real"><p>Russian nesting dolls. You can only close the doll you opened most recently. If you try to close the big doll while a small one is still open, something's wrong.</p></div>
    <p class="when"><b>Use when</b>things open and close in nested order: brackets, HTML tags, function calls.</p>
<pre><code><span class="k">def</span> is_valid(s):
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    <span class="k">for</span> ch <span class="k">in</span> s:
        <span class="k">if</span> ch <span class="k">in</span> pair:
            <span class="k">if not</span> st <span class="k">or</span> st.pop() != pair[ch]: <span class="k">return</span> False
        <span class="k">else</span>:
            st.append(ch)
    <span class="k">return not</span> st            <span class="c"># leftovers = unclosed</span></code></pre>
    <figure class="anim" data-anim="stacks-parens"><figcaption>Checking "{[()]}(]" with a stack</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Monotonic stack (next greater element)</h3><span class="cx">O(n) time · O(n) space</span></div>
    <div class="real"><p>People in a line at a parade, all facing the stage. Each person wants to know who is the first taller person in front of them. When a tall person arrives, everyone shorter who was still waiting finally gets their answer and drops out. The waiting group is always sorted tallest-at-the-back, which is why it's called monotonic.</p></div>
    <p class="when"><b>Use when</b>you see "next greater/smaller element," "days until warmer," "span," or "largest rectangle."</p>
<pre><code><span class="k">def</span> daily_temperatures(t):
    ans, st = [0] * len(t), []            <span class="c"># st holds indices still waiting</span>
    <span class="k">for</span> i, x <span class="k">in</span> enumerate(t):
        <span class="k">while</span> st <span class="k">and</span> t[st[-1]] &lt; x:      <span class="c"># x answers everyone cooler</span>
            j = st.pop()
            ans[j] = i - j
        st.append(i)
    <span class="k">return</span> ans</code></pre>
    <figure class="anim" data-anim="stacks-temps"><figcaption>Monotonic stack on Daily Temperatures</figcaption></figure>
    <p class="note">Why O(n) despite the inner while? Each index is pushed once and popped at most once: at most 2n operations in total.</p>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Stack that tracks its minimum</h3><span class="cx">O(1) every operation</span></div>
    <div class="real"><p>A climber's logbook where every page records both the current altitude and the lowest point reached so far. Tear off the top page and the page underneath still knows the lowest point as of then.</p></div>
    <p class="when"><b>Use when</b>you need min/max of a stack at any moment (Min Stack).</p>
<pre><code><span class="k">class</span> MinStack:
    <span class="k">def</span> __init__(self): self.st = []          <span class="c"># (value, min so far)</span>
    <span class="k">def</span> push(self, x):
        m = min(x, self.st[-1][1]) <span class="k">if</span> self.st <span class="k">else</span> x
        self.st.append((x, m))
    <span class="k">def</span> pop(self): self.st.pop()
    <span class="k">def</span> top(self): <span class="k">return</span> self.st[-1][0]
    <span class="k">def</span> getMin(self): <span class="k">return</span> self.st[-1][1]</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Stack for evaluation and decoding</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>A calculator receipt in Reverse Polish Notation: "3 4 + 2 ×". You keep numbers on a pile; each operator takes the top two, combines them, and puts the result back. Decode String does the same with "3[ab]": park what you have, build the inside, then multiply and reattach.</p></div>
    <p class="when"><b>Use when</b>evaluating expressions, nested repetitions, or simplifying paths.</p>
<pre><code><span class="k">def</span> eval_rpn(tokens):
    st = []
    <span class="k">for</span> t <span class="k">in</span> tokens:
        <span class="k">if</span> t <span class="k">in</span> "+-*/":
            b, a = st.pop(), st.pop()          <span class="c"># order matters!</span>
            <span class="k">if</span> t == '+': st.append(a + b)
            <span class="k">elif</span> t == '-': st.append(a - b)
            <span class="k">elif</span> t == '*': st.append(a * b)
            <span class="k">else</span>: st.append(int(a / b))     <span class="c"># truncate toward 0</span>
        <span class="k">else</span>:
            st.append(int(t))
    <span class="k">return</span> st[0]</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Monotonic deque (sliding window max)</h3><span class="cx">O(n) time · O(k) space</span></div>
    <div class="real"><p>Picking the tallest player for each 3-day training camp as players arrive and leave. A newcomer taller than people still in the group makes them irrelevant forever (they'll leave earlier and are shorter), so they're dropped. The tallest is always at the front of the line.</p></div>
    <p class="when"><b>Use when</b>you need the max/min of every window of size k.</p>
<pre><code><span class="k">from</span> collections <span class="k">import</span> deque
<span class="k">def</span> max_sliding_window(nums, k):
    dq, out = deque(), []                 <span class="c"># indices, values decreasing</span>
    <span class="k">for</span> i, x <span class="k">in</span> enumerate(nums):
        <span class="k">while</span> dq <span class="k">and</span> nums[dq[-1]] &lt;= x: dq.pop()   <span class="c"># drop the useless</span>
        dq.append(i)
        <span class="k">if</span> dq[0] &lt;= i - k: dq.popleft()            <span class="c"># left the window</span>
        <span class="k">if</span> i &gt;= k - 1: out.append(nums[dq[0]])
    <span class="k">return</span> out</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Largest Rectangle in Histogram</h2>
  <div class="real"><p>You want to hang the widest possible banner across a row of buildings of different heights. A banner at height h can stretch left and right until it hits a building shorter than h. For each building, find how far the banner at its height can stretch.</p></div>
  <div class="trace">
    <div><p>For each bar, the best rectangle using its full height spans from the first shorter bar on its left to the first shorter bar on its right. Those are "previous smaller" and "next smaller": a monotonic stack problem.</p></div>
    <div><p>Keep a stack of indices with increasing heights. When a shorter bar arrives at index i, it is the "next smaller" for every taller bar on the stack. Pop each one; its "previous smaller" is whatever is below it on the stack.</p></div>
    <div><p>Width = <code>i - stack[-1] - 1</code> after popping (or <code>i</code> if the stack is empty). Area = height × width.</p></div>
    <div><p>Append a sentinel height 0 at the end so every bar gets popped and measured.</p></div>
  </div>
<pre><code><span class="k">def</span> largest_rectangle(heights):
    st, best = [], 0
    <span class="k">for</span> i, h <span class="k">in</span> enumerate(heights + [0]):         <span class="c"># sentinel</span>
        <span class="k">while</span> st <span class="k">and</span> heights[st[-1]] &gt; h:
            height = heights[st.pop()]
            width = i <span class="k">if not</span> st <span class="k">else</span> i - st[-1] - 1
            best = max(best, height * width)
        st.append(i)
    <span class="k">return</span> best</code></pre>
  <p><strong>Complexity:</strong> O(n) time, O(n) space. Brute force (expand from every bar) is O(n²).</p>
  <div class="google"><p>If you spot "for each element, find the nearest bigger/smaller one," say "monotonic stack" out loud. It signals pattern fluency, which interviewers note in their write-up.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases to test</h2>
  <div class="real"><p>A cafeteria worker reaching for a plate on an empty rack: always check the stack isn't empty before you pop or peek.</p></div>
  <ul>
    <li>Empty input, and popping from an empty stack.</li>
    <li>Equal values in monotonic stacks: decide <code>&lt;</code> vs <code>&lt;=</code> deliberately.</li>
    <li>Leftover items at the end (unclosed brackets, bars never popped).</li>
    <li>Division in RPN: Python's <code>//</code> floors negatives; use <code>int(a / b)</code> to truncate toward zero.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Valid Parentheses", "valid-parentheses", "easy", "Matching pairs"),
    ("Implement Queue using Stacks", "implement-queue-using-stacks", "easy", "Inbox + outbox stacks"),
    ("Implement Stack using Queues", "implement-stack-using-queues", "easy", "Rotate after push"),
    ("Min Stack", "min-stack", "medium", "Store (value, min so far)"),
    ("Evaluate Reverse Polish Notation", "evaluate-reverse-polish-notation", "medium", "Operand stack"),
    ("Daily Temperatures", "daily-temperatures", "medium", "Monotonic decreasing stack"),
    ("Decode String", "decode-string", "medium", "Stack of (string so far, repeat count)"),
    ("Asteroid Collision", "asteroid-collision", "medium", "Stack, resolve collisions with the top"),
    ("Car Fleet", "car-fleet", "medium", "Sort by position, stack of arrival times"),
    ("Largest Rectangle in Histogram", "largest-rectangle-in-histogram", "hard", "Monotonic increasing stack + sentinel"),
    ("Sliding Window Maximum", "sliding-window-maximum", "hard", "Monotonic deque"),
]

QUIZ = [
    dict(lvl="easy", q="Which structure does your browser's Back button behave like?",
         opts=["Queue", "Stack", "Heap", "Hash set"], a=1, why="The most recently visited page is the first one you go back to: last in, first out."),
    dict(lvl="easy", q="Why use `collections.deque` instead of a list for a queue?",
         opts=["It sorts items", "`popleft()` is O(1), while `list.pop(0)` is O(n)", "It uses less memory", "Lists can't hold strings"], a=1,
         why="Removing from a list's front shifts every remaining element."),
    dict(lvl="easy", q="Is \"([)]\" valid?",
         opts=["Yes, every opener has a closer", "No, ')' arrives while '[' is on top of the stack", "Yes, the counts match", "No, it's too short"], a=1,
         why="Counts alone aren't enough; nesting order must match the stack's top."),
    dict(lvl="medium", q="Daily Temperatures for `[30, 40, 50, 60]`:",
         opts=["[1, 1, 1, 0]", "[3, 2, 1, 0]", "[0, 0, 0, 0]", "[1, 2, 3, 0]"], a=0, why="Each day is followed immediately by a warmer one; the last has none."),
    dict(lvl="medium", q="In RPN evaluation, for tokens `[\"6\", \"2\", \"-\"]`, why pop `b` before `a`?",
         opts=["No reason", "The top is the second operand: 6 − 2, not 2 − 6", "To keep the stack sorted", "Python requires it"], a=1,
         why="The last pushed value is the right-hand operand. Order matters for − and ÷."),
    dict(lvl="medium", q="What does `int(-7 / 2)` give vs `-7 // 2` in Python?",
         opts=["-3 and -4", "-4 and -3", "-3 and -3", "-4 and -4"], a=0,
         why="`//` floors toward negative infinity; `int()` truncates toward zero. LeetCode's RPN wants truncation."),
    dict(lvl="medium", q="Implement Queue using Stacks: amortized cost of `pop`?",
         opts=["O(n) always", "O(1) amortized", "O(log n)", "O(n²)"], a=1,
         why="Move items from the inbox to the outbox only when the outbox is empty. Each item moves once, so pops average O(1)."),
    dict(lvl="hard", q="Largest Rectangle in Histogram: what is the sentinel 0 at the end for?",
         opts=["Avoid index errors", "Force every remaining bar to be popped and measured", "Handle negative heights", "It's optional decoration"], a=1,
         why="Bars still on the stack never met a shorter bar. A final 0 is shorter than everything, so they all get processed."),
    dict(lvl="hard", q="Sliding Window Maximum: why can we drop a smaller element from the deque forever when a bigger one arrives?",
         opts=["To save memory only", "The bigger one is newer, so it stays in every future window the smaller one would, and beats it", "Because the deque must be sorted ascending", "Only works for positive numbers"], a=1,
         why="An older, smaller element can never be the max of any future window that also contains the newer, bigger one."),
    dict(lvl="hard", q="Car Fleet: cars at positions [10, 8, 0] with speeds [2, 4, 1], target 12. How many fleets?",
         opts=["1", "2", "3", "0"], a=1,
         why="Arrival times: car@10 → 1h, car@8 → 1h, car@0 → 12h. Sort by position descending: 10 (1h) leads; 8 (1h) catches it → same fleet; 0 (12h) is slower → new fleet. Total 2."),
]
