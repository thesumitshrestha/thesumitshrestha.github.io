META = dict(
    title="Bit manipulation", page_title="Bit Manipulation · DSA Field Guide", week="Week 10", group="Algorithms",
    h1="Bit manipulation",
    lead="Every integer is a row of on/off switches. A handful of tricks with AND, OR, XOR and shifts solve problems in O(1) space that would otherwise need a hashmap.",
    blurb="AND, OR, XOR, shifts, masks, counting bits, XOR cancellation.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A row of light switches</h2>
  <div class="real big-real">
    <p>A hotel corridor with 8 rooms and a light switch for each. Write "1" for on and "0" for off, and the whole corridor is one number: <code>00101100</code>. Asking "is room 3's light on?" or "flip room 5" are single operations on that number. File permissions on your laptop (read/write/execute = 4/2/1) work exactly this way.</p>
  </div>
<pre class="diagram">13 in binary:   1    1    0    1
place value:    8    4    2    1      →  8 + 4 + 1 = 13
bit index:      3    2    1    0</pre>
  <div class="tbl"><table>
    <thead><tr><th>Operator</th><th>Rule</th><th>Example (5 = 101, 3 = 011)</th><th>Think of it as</th></tr></thead>
    <tbody>
      <tr><td><code>a &amp; b</code> AND</td><td>1 if both are 1</td><td><code>101 &amp; 011 = 001</code> (1)</td><td>Keep only shared switches</td></tr>
      <tr><td><code>a | b</code> OR</td><td>1 if either is 1</td><td><code>101 | 011 = 111</code> (7)</td><td>Turn on everything either has</td></tr>
      <tr><td><code>a ^ b</code> XOR</td><td>1 if different</td><td><code>101 ^ 011 = 110</code> (6)</td><td>"Flip where they disagree"</td></tr>
      <tr><td><code>~a</code> NOT</td><td>flip every bit</td><td><code>~5 = -6</code> in Python</td><td>Invert (two's complement)</td></tr>
      <tr><td><code>a &lt;&lt; k</code></td><td>shift left</td><td><code>5 &lt;&lt; 1 = 1010</code> (10)</td><td>Multiply by 2ᵏ</td></tr>
      <tr><td><code>a &gt;&gt; k</code></td><td>shift right</td><td><code>5 &gt;&gt; 1 = 10</code> (2)</td><td>Floor-divide by 2ᵏ</td></tr>
    </tbody>
  </table></div>
</section>

<section id="tricks">
  <span class="eyebrow">Cheat sheet</span>
  <h2>One-line tricks to memorize</h2>
  <div class="real"><p>Like a light-switch panel with labeled buttons: check one room, turn one on, turn one off, flip one, or switch off the lowest lit room.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Goal</th><th>Code</th></tr></thead>
    <tbody>
      <tr><td>Is bit i set?</td><td><code>(x &gt;&gt; i) &amp; 1</code></td></tr>
      <tr><td>Set bit i</td><td><code>x | (1 &lt;&lt; i)</code></td></tr>
      <tr><td>Clear bit i</td><td><code>x &amp; ~(1 &lt;&lt; i)</code></td></tr>
      <tr><td>Toggle bit i</td><td><code>x ^ (1 &lt;&lt; i)</code></td></tr>
      <tr><td>Remove lowest set bit</td><td><code>x &amp; (x - 1)</code></td></tr>
      <tr><td>Isolate lowest set bit</td><td><code>x &amp; -x</code></td></tr>
      <tr><td>Power of two? (x &gt; 0)</td><td><code>x &amp; (x - 1) == 0</code></td></tr>
      <tr><td>Odd?</td><td><code>x &amp; 1</code></td></tr>
      <tr><td>Count set bits</td><td><code>bin(x).count('1')</code> or <code>x.bit_count()</code> (3.10+)</td></tr>
    </tbody>
  </table></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Five bit patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. XOR cancellation</h3><span class="cx">O(n) time · O(1) space</span></div>
    <div class="real"><p>Flipping a light switch twice leaves it where it started. If everyone in a group flips a switch for their name and everyone except one person appears twice, only the loner's switch stays on.</p></div>
    <p class="when"><b>Use when</b>everything appears in pairs except one (Single Number), or to find a missing number (XOR indices with values).</p>
<pre><code><span class="k">def</span> single_number(nums):
    acc = 0
    <span class="k">for</span> x <span class="k">in</span> nums: acc ^= x       <span class="c"># pairs cancel to 0</span>
    <span class="k">return</span> acc

<span class="k">def</span> missing_number(nums):         <span class="c"># 0..n with one missing</span>
    acc = len(nums)
    <span class="k">for</span> i, x <span class="k">in</span> enumerate(nums): acc ^= i ^ x
    <span class="k">return</span> acc</code></pre>
    <figure class="anim" data-anim="bits-xor"><figcaption>XOR cancelling pairs in [4, 1, 2, 1, 2]</figcaption></figure>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Brian Kernighan's bit count</h3><span class="cx">O(number of set bits)</span></div>
    <div class="real"><p>Counting lit rooms by switching off the lowest-numbered lit room each time and counting how many times you did it. You never visit dark rooms.</p></div>
    <p class="when"><b>Use when</b>counting 1-bits (Number of 1 Bits) or checking powers of two.</p>
<pre><code><span class="k">def</span> hamming_weight(n):
    count = 0
    <span class="k">while</span> n:
        n &amp;= n - 1          <span class="c"># drops the lowest 1</span>
        count += 1
    <span class="k">return</span> count</code></pre>
<pre class="diagram">n     = 1 0 1 1 0 0
n - 1 = 1 0 1 0 1 1     (borrow flips the lowest 1 and everything below it)
n&amp;n-1 = 1 0 1 0 0 0     → lowest 1 removed</pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. DP on bits</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>Counting coins in piggy banks numbered 0 to n: bank i holds the same coins as bank i ÷ 2, plus one more if i is odd. You reuse the answer you already have instead of recounting.</p></div>
    <p class="when"><b>Use when</b>you need bit counts for every number 0..n (Counting Bits).</p>
<pre><code><span class="k">def</span> count_bits(n):
    ans = [0] * (n + 1)
    <span class="k">for</span> i <span class="k">in</span> range(1, n + 1):
        ans[i] = ans[i &gt;&gt; 1] + (i &amp; 1)
    <span class="k">return</span> ans</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Bitmask as a set</h3><span class="cx">2ⁿ subsets</span></div>
    <div class="real"><p>A pizza order form with checkboxes for 4 toppings. Every possible order is a 4-bit number from 0000 (plain) to 1111 (everything), so looping from 0 to 15 lists every possible pizza.</p></div>
    <p class="when"><b>Use when</b>n is small (≤ 20) and you need all subsets or a compact "visited set" for DP.</p>
<pre><code><span class="k">def</span> subsets(nums):
    n = len(nums)
    <span class="k">return</span> [[nums[i] <span class="k">for</span> i <span class="k">in</span> range(n) <span class="k">if</span> mask &gt;&gt; i &amp; 1]
            <span class="k">for</span> mask <span class="k">in</span> range(1 &lt;&lt; n)]</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Adding without +</h3><span class="cx">O(bits)</span></div>
    <div class="real"><p>Adding by hand in school: write the digit sum without carrying (that's XOR), then write the carries one column to the left (that's AND then shift). Repeat until there's nothing left to carry.</p></div>
    <p class="when"><b>Use when</b>the problem forbids arithmetic operators (Sum of Two Integers).</p>
<pre><code><span class="k">def</span> get_sum(a, b):
    MASK = 0xFFFFFFFF                       <span class="c"># simulate 32-bit ints</span>
    <span class="k">while</span> b &amp; MASK:
        a, b = (a ^ b), (a &amp; b) &lt;&lt; 1
    a &amp;= MASK
    <span class="k">return</span> a <span class="k">if</span> a &lt;= 0x7FFFFFFF <span class="k">else</span> ~(a ^ MASK)</code></pre>
    <p class="note">Python integers have unlimited size, so negative numbers never "overflow" on their own. The mask emulates 32-bit behavior; that's why bit problems feel awkward in Python.</p>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Single Number II: every number appears three times except one</h2>
  <div class="real"><p>A school counts votes by tallying each checkbox column separately. If every student except one voted in groups of three identical ballots, each column's tally is a multiple of 3 plus the loner's mark. Taking every column's tally mod 3 reveals the loner's ballot.</p></div>
  <div class="trace">
    <div><p>XOR alone fails: triples don't cancel (x ^ x ^ x = x).</p></div>
    <div><p>Count each of the 32 bit positions across all numbers. Mod 3 removes the triples, leaving the single number's bit.</p></div>
    <div><p>Rebuild the answer from those bits, fixing the sign for 32-bit negatives.</p></div>
  </div>
<pre><code><span class="k">def</span> single_number_ii(nums):
    ans = 0
    <span class="k">for</span> i <span class="k">in</span> range(32):
        bit_sum = sum((x &gt;&gt; i) &amp; 1 <span class="k">for</span> x <span class="k">in</span> nums)
        <span class="k">if</span> bit_sum % 3: ans |= 1 &lt;&lt; i
    <span class="k">return</span> ans - (1 &lt;&lt; 32) <span class="k">if</span> ans &gt;= 1 &lt;&lt; 31 <span class="k">else</span> ans</code></pre>
  <p><strong>Complexity:</strong> O(32n) = O(n) time, O(1) space.</p>
  <div class="google"><p>Bit manipulation shows up less at Google than graphs or trees, but bitmask DP ("n ≤ 16, visit every node") does appear. Recognize the small-n signal.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Pitfalls</h2>
  <div class="real"><p>A light switch panel wired backwards: flipping the wrong one in the wrong order looks fine until a guest complains. Operator precedence is the miswired switch here.</p></div>
  <ul>
    <li>Precedence: <code>x &amp; 1 == 0</code> means <code>x &amp; (1 == 0)</code>. Always use parentheses.</li>
    <li>Negative numbers in Python have infinite leading 1s; mask with <code>0xFFFFFFFF</code> for 32-bit problems.</li>
    <li><code>~x</code> is <code>-x - 1</code>, not "unsigned flip."</li>
    <li><code>x &amp; (x - 1) == 0</code> is true for 0 too; check <code>x &gt; 0</code> for power of two.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Single Number", "single-number", "easy", "XOR everything"),
    ("Number of 1 Bits", "number-of-1-bits", "easy", "n &= n − 1"),
    ("Counting Bits", "counting-bits", "easy", "ans[i] = ans[i >> 1] + (i & 1)"),
    ("Missing Number", "missing-number", "easy", "XOR indices and values (or sum formula)"),
    ("Reverse Bits", "reverse-bits", "easy", "Shift out the low bit, shift into result"),
    ("Sum of Two Integers", "sum-of-two-integers", "medium", "XOR + carry, 32-bit mask"),
    ("Bitwise AND of Numbers Range", "bitwise-and-of-numbers-range", "medium", "Common prefix of left and right"),
    ("Single Number II", "single-number-ii", "medium", "Count each bit mod 3"),
    ("Divide Two Integers", "divide-two-integers", "medium", "Subtract shifted divisors"),
    ("Gray Code", "gray-code", "medium", "i ^ (i >> 1)"),
    ("Maximum XOR of Two Numbers in an Array", "maximum-xor-of-two-numbers-in-an-array", "hard", "Bitwise trie, greedy from high bit"),
    ("Minimum One Bit Operations to Make Integers Zero", "minimum-one-bit-operations-to-make-integers-zero", "hard", "Gray code inverse"),
]

QUIZ = [
    dict(lvl="easy", q="What is `6 & 3`?", opts=["1", "2", "7", "5"], a=1, why="110 & 011 = 010 = 2."),
    dict(lvl="easy", q="What is `5 ^ 5`?", opts=["0", "5", "10", "1"], a=0, why="XOR of a number with itself is always 0."),
    dict(lvl="easy", q="`1 << 4` equals:", opts=["4", "8", "16", "5"], a=2, why="Shifting 1 left by 4 places is 2⁴ = 16."),
    dict(lvl="medium", q="What does `x & (x - 1)` do?", opts=["Doubles x", "Clears the lowest set bit", "Sets the lowest bit", "Counts bits"], a=1,
         why="x − 1 flips the lowest 1 and the zeros below it; AND keeps everything above."),
    dict(lvl="medium", q="Why does `x & 1 == 0` give a surprising result?",
         opts=["It doesn't", "`==` binds tighter than `&`, so it's `x & (1 == 0)` = `x & False` = 0", "XOR is needed", "Python can't AND booleans"], a=1,
         why="Write `(x & 1) == 0`. Precedence bugs are common in bit code."),
    dict(lvl="medium", q="Counting Bits: `ans[i] = ans[i >> 1] + (i & 1)`. For i = 7?",
         opts=["2", "3", "4", "1"], a=1, why="ans[3] = 2 (binary 11), plus 1 because 7 is odd: 3 (binary 111)."),
    dict(lvl="medium", q="Missing Number for `[3, 0, 1]` via XOR of indices and values (start acc = n = 3):",
         opts=["2", "3", "0", "1"], a=0, why="3 ^ (0^3) ^ (1^0) ^ (2^1) = 2. Every present number cancels with its index."),
    dict(lvl="hard", q="Bitwise AND of Numbers Range [5, 7]:",
         opts=["5", "4", "7", "0"], a=1, why="101 & 110 & 111 = 100 = 4. The answer is the common binary prefix of left and right."),
    dict(lvl="hard", q="Why do Python bit problems sometimes need `& 0xFFFFFFFF`?",
         opts=["Speed", "Python ints are unbounded, so 32-bit overflow/negatives must be emulated", "To convert to strings", "To avoid recursion"], a=1,
         why="In C or Java ints wrap at 32 bits. Python's don't, so you mask and convert back to signed yourself."),
    dict(lvl="hard", q="Maximum XOR of Two Numbers: what structure gives O(32n)?",
         opts=["Heap", "A binary trie of the numbers' bits; for each number greedily walk the opposite bit", "Sorting", "Union-find"], a=1,
         why="From the highest bit down, prefer the branch that makes this bit 1 in the XOR."),
]
