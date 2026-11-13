META = dict(
    title="Hashing", page_title="Hashing · DSA Field Guide", week="Week 9", group="Data structures",
    h1="Hash maps and hash sets",
    lead="The single most useful tool in interviews. A hashmap turns \"search the whole array\" into one O(1) lookup, and it's the usual way to cut an O(n²) brute force down to O(n).",
    blurb="How hashing works, frequency maps, grouping, prefix sum + hashmap, O(1) designs.",
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A coat check with numbered hooks</h2>
  <div class="real big-real">
    <p>A library doesn't search every shelf for a book; the call number tells you exactly which shelf to walk to. A hash function is that call number: it turns any key ("priya", 42, a tuple) into a shelf number. Lookup becomes "compute the shelf, walk straight there," no matter how many books the library holds.</p>
  </div>
<pre class="diagram">key "cat" ──hash()──▶ 312 ──% 5──▶ bucket 2

bucket 0 │ ·
bucket 1 │ ·
bucket 2 │ "cat"
bucket 3 │ "owl" → "fox"     ← collision: two keys share a bucket
bucket 4 │ "dog"

(toy hash: sum of letter codes; "cat" = 99 + 97 + 116 = 312)</pre>
  <figure class="anim" data-anim="hash-buckets"><figcaption>Inserting six keys into five buckets</figcaption></figure>
  <p><strong>Collisions</strong> happen when two keys land in the same bucket. Python's <code>dict</code> handles them by probing for another open slot; the animation shows the simpler "chaining" idea. Either way, a good hash function and automatic resizing keep buckets short, so operations are <strong>O(1) on average</strong>. The rare worst case (everything colliding) is O(n).</p>
</section>

<section id="ops">
  <span class="eyebrow">Toolkit</span>
  <h2>Python's hashing toolkit</h2>
  <div class="tbl"><table>
    <thead><tr><th>Tool</th><th>What it's for</th><th>Example</th></tr></thead>
    <tbody>
      <tr><td><code>set()</code></td><td>Have I seen this?</td><td><code>if x in seen</code></td></tr>
      <tr><td><code>dict</code></td><td>Value → index, id → object</td><td><code>pos[x] = i</code></td></tr>
      <tr><td><code>Counter</code></td><td>Counting</td><td><code>Counter("google")["o"] == 2</code></td></tr>
      <tr><td><code>defaultdict(list)</code></td><td>Grouping without key checks</td><td><code>groups[key].append(w)</code></td></tr>
      <tr><td><code>d.get(k, 0)</code></td><td>Read with a default</td><td><code>d[k] = d.get(k, 0) + 1</code></td></tr>
    </tbody>
  </table></div>
  <div class="callout"><p><strong>Keys must be hashable (immutable):</strong> numbers, strings, tuples, frozensets. Lists, sets and dicts can't be keys. Convert with <code>tuple(lst)</code>.</p></div>
</section>

<section id="patterns">
  <span class="eyebrow">Patterns</span>
  <h2>Six hashing patterns</h2>

  <article class="pattern">
    <div class="pattern-head"><h3>1. Seen-before set</h3><span class="cx">O(n) time · O(n) space</span></div>
    <div class="real"><p>A bouncer with a guest list who ticks names off at the door. The second time someone with the same name shows up, the bouncer knows instantly.</p></div>
    <p class="when"><b>Use when</b>detecting duplicates or cycles (Happy Number: a repeated number means you're in a loop).</p>
<pre><code><span class="k">def</span> is_happy(n):
    seen = set()
    <span class="k">while</span> n != 1 <span class="k">and</span> n <span class="k">not in</span> seen:
        seen.add(n)
        n = sum(int(d) ** 2 <span class="k">for</span> d <span class="k">in</span> str(n))
    <span class="k">return</span> n == 1</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>2. Frequency map</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>Writing a ransom note from magazine letters: first count the letters you have, then spend them as you write. If you run out of any letter, you can't finish.</p></div>
    <p class="when"><b>Use when</b>comparing contents regardless of order.</p>
<pre><code><span class="k">def</span> can_construct(note, magazine):
    have = Counter(magazine)
    <span class="k">for</span> ch <span class="k">in</span> note:
        <span class="k">if</span> have[ch] == 0: <span class="k">return</span> False
        have[ch] -= 1
    <span class="k">return</span> True</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>3. Two-way mapping</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>A secret code where each letter always becomes the same symbol, and no two letters share a symbol. You keep a cipher table in both directions to catch either kind of cheating.</p></div>
    <p class="when"><b>Use when</b>checking a one-to-one correspondence (Isomorphic Strings, Word Pattern).</p>
<pre><code><span class="k">def</span> is_isomorphic(s, t):
    a2b, b2a = {}, {}
    <span class="k">for</span> x, y <span class="k">in</span> zip(s, t):
        <span class="k">if</span> a2b.setdefault(x, y) != y <span class="k">or</span> b2a.setdefault(y, x) != x:
            <span class="k">return</span> False
    <span class="k">return</span> True</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>4. Grouping by a signature</h3><span class="cx">O(n · key cost)</span></div>
    <div class="real"><p>Sorting mail by ZIP code: every letter's ZIP decides its bin, and letters to the same area end up together. The trick is picking a "ZIP code" that's identical for things that belong together.</p></div>
    <p class="when"><b>Use when</b>items that are "the same" in some sense must be bucketed (anagrams, shifted strings, same row in Valid Sudoku).</p>
<pre><code><span class="k">def</span> is_valid_sudoku(board):
    seen = set()
    <span class="k">for</span> r <span class="k">in</span> range(9):
        <span class="k">for</span> c <span class="k">in</span> range(9):
            v = board[r][c]
            <span class="k">if</span> v == '.': <span class="k">continue</span>
            keys = ((v, 'row', r), (v, 'col', c), (v, 'box', r // 3, c // 3))
            <span class="k">if</span> any(k <span class="k">in</span> seen <span class="k">for</span> k <span class="k">in</span> keys): <span class="k">return</span> False
            seen.update(keys)
    <span class="k">return</span> True</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>5. Prefix sum + hashmap</h3><span class="cx">O(n)</span></div>
    <div class="real"><p>A football match where you want the longest stretch with equal goals for both teams. Track the running score difference. If the difference was +1 at minute 20 and +1 again at minute 70, the goals between minutes 20 and 70 were tied. Remembering the first minute each difference appeared gives the longest stretch.</p></div>
    <p class="when"><b>Use when</b>looking for subarrays with a target sum, or balanced counts (Contiguous Array: treat 0 as −1).</p>
<pre><code><span class="k">def</span> find_max_length(nums):           <span class="c"># equal 0s and 1s</span>
    first = {0: -1}                    <span class="c"># balance → first index seen</span>
    bal = best = 0
    <span class="k">for</span> i, x <span class="k">in</span> enumerate(nums):
        bal += 1 <span class="k">if</span> x <span class="k">else</span> -1
        <span class="k">if</span> bal <span class="k">in</span> first: best = max(best, i - first[bal])
        <span class="k">else</span>: first[bal] = i              <span class="c"># keep the EARLIEST</span>
    <span class="k">return</span> best</code></pre>
  </article>

  <article class="pattern">
    <div class="pattern-head"><h3>6. Hashmap + array for O(1) design</h3><span class="cx">O(1) every operation</span></div>
    <div class="real"><p>A raffle drum with a register. The drum (array) lets you pick a random ticket instantly; the register (hashmap) tells you where any named ticket is so it can be removed instantly, by swapping it with the last ticket and dropping the end.</p></div>
    <p class="when"><b>Use when</b>designing a structure with O(1) insert, delete and random/indexed access.</p>
<pre><code><span class="k">import</span> random
<span class="k">class</span> RandomizedSet:
    <span class="k">def</span> __init__(self): self.vals, self.pos = [], {}
    <span class="k">def</span> insert(self, x):
        <span class="k">if</span> x <span class="k">in</span> self.pos: <span class="k">return</span> False
        self.pos[x] = len(self.vals); self.vals.append(x); <span class="k">return</span> True
    <span class="k">def</span> remove(self, x):
        <span class="k">if</span> x <span class="k">not in</span> self.pos: <span class="k">return</span> False
        i, last = self.pos[x], self.vals[-1]
        self.vals[i], self.pos[last] = last, i       <span class="c"># move last into the hole</span>
        self.vals.pop(); <span class="k">del</span> self.pos[x]; <span class="k">return</span> True
    <span class="k">def</span> getRandom(self): <span class="k">return</span> random.choice(self.vals)</code></pre>
  </article>
</section>

<section id="deep">
  <span class="eyebrow">Deep analysis</span>
  <h2>Find All Anagrams in a String: fixed window + counts</h2>
  <div class="real"><p>Scanning a long shelf of Scrabble tiles through a 3-tile magnifying window, looking for any arrangement of C-A-T. Slide one tile right: one tile enters, one leaves. You update two counts instead of recounting three tiles each time.</p></div>
  <div class="trace">
    <div><p>Brute force: for each start, count the window and compare: O(n · m).</p></div>
    <div><p>Fixed window of length m = len(p). Keep a 26-count array for the window; when sliding, add the new char and remove the old one: O(1) per step.</p></div>
    <div><p>Comparing two 26-arrays is O(26) = O(1), so the total is O(n).</p></div>
  </div>
<pre><code><span class="k">def</span> find_anagrams(s, p):
    m, res = len(p), []
    need, win = [0] * 26, [0] * 26
    <span class="k">for</span> ch <span class="k">in</span> p: need[ord(ch) - 97] += 1
    <span class="k">for</span> i, ch <span class="k">in</span> enumerate(s):
        win[ord(ch) - 97] += 1
        <span class="k">if</span> i &gt;= m: win[ord(s[i - m]) - 97] -= 1     <span class="c"># leaves the window</span>
        <span class="k">if</span> win == need: res.append(i - m + 1)
    <span class="k">return</span> res</code></pre>
  <div class="google"><p>When you hear yourself say "for each element, search for…", ask "could a hashmap answer that search in O(1)?" That question alone solves a large share of Medium problems.</p></div>
</section>

<section id="edge">
  <span class="eyebrow">Before you say "done"</span>
  <h2>Edge cases and pitfalls</h2>
  <div class="real"><p>A coat check that gives out two identical ticket numbers causes chaos. Make sure your keys really identify what you mean.</p></div>
  <ul>
    <li>Using a list as a key: <code>TypeError: unhashable type</code>. Use a tuple.</li>
    <li>Prefix-sum maps: seed with <code>{0: 1}</code> (counts) or <code>{0: -1}</code> (first index).</li>
    <li>Storing the latest index when you need the earliest (longest subarray problems).</li>
    <li>Say "O(1) average" if asked about worst case; mention resizing and collisions.</li>
    <li>Iteration order: Python dicts keep insertion order, but don't rely on that for correctness unless the problem says so.</li>
  </ul>
</section>
"""

PROBLEMS = [
    ("Happy Number", "happy-number", "easy", "Seen set (or fast/slow)"),
    ("Ransom Note", "ransom-note", "easy", "Counter"),
    ("Isomorphic Strings", "isomorphic-strings", "easy", "Two-way map"),
    ("Encode and Decode Strings", "encode-and-decode-strings", "medium", "Length-prefix each string"),
    ("Insert Delete GetRandom O(1)", "insert-delete-getrandom-o1", "medium", "Array + value→index map"),
    ("Find All Anagrams in a String", "find-all-anagrams-in-a-string", "medium", "Fixed window + counts"),
    ("Valid Sudoku", "valid-sudoku", "medium", "Set of (value, row/col/box) keys"),
    ("Contiguous Array", "contiguous-array", "medium", "Balance → first index"),
    ("Brick Wall", "brick-wall", "medium", "Count edge positions"),
    ("Max Points on a Line", "max-points-on-a-line", "hard", "Slope as reduced (dy, dx) per anchor"),
    ("Longest Duplicate Substring", "longest-duplicate-substring", "hard", "Binary search on length + rolling hash"),
]

QUIZ = [
    dict(lvl="easy", q="Average time for `x in my_set`?",
         opts=["O(1)", "O(log n)", "O(n)", "O(n log n)"], a=0, why="Hash the key and jump to its bucket."),
    dict(lvl="easy", q="Which can be a dict key?",
         opts=["[1, 2]", "{1, 2}", "(1, 2)", "{'a': 1}"], a=2, why="Tuples of hashable items are hashable; lists, sets and dicts are mutable and aren't."),
    dict(lvl="easy", q="What does this print?", code="from collections import Counter\nprint(Counter('banana').most_common(1))",
         opts=["[('b', 1)]", "[('a', 3)]", "[('n', 2)]", "3"], a=1, why="'a' appears 3 times, the most."),
    dict(lvl="medium", q="Contiguous Array: why seed the map with `{0: -1}`?",
         opts=["To avoid a KeyError only", "A balance of 0 at index i means the whole prefix [0..i] is balanced; length i − (−1) = i + 1", "It's the answer for empty input", "To make indices 1-based"], a=1,
         why="The empty prefix has balance 0 and 'ends' at index −1."),
    dict(lvl="medium", q="RandomizedSet.remove(x): why swap x with the last element first?",
         opts=["To keep the array sorted", "Popping from the end is O(1); deleting from the middle is O(n)", "To randomize the order", "getRandom requires it"], a=1,
         why="Swap-and-pop avoids shifting. Remember to update the moved element's index in the map."),
    dict(lvl="medium", q="Isomorphic: is \"badc\" → \"baba\" valid?",
         opts=["Yes", "No: 'b' and 'd' both map to 'b'", "No: different lengths", "Yes, counts match"], a=1,
         why="The reverse map catches it: 'b' would map back to both 'b' and 'd'."),
    dict(lvl="medium", q="Encode and Decode Strings: why is joining with a delimiter like ',' fragile?",
         opts=["It's slow", "The strings themselves may contain ','", "Python can't split", "It loses order"], a=1,
         why="Prefix each string with its length and a marker (e.g. `5#hello`), so the content can be anything."),
    dict(lvl="hard", q="Worst case of a hash table lookup, and when could it happen?",
         opts=["O(1), never", "O(n), if many keys collide into one bucket (bad hash or adversarial keys)", "O(log n), always", "O(n²) during resize"], a=1,
         why="Real implementations make this rare (randomized string hashing, resizing), but you should know it."),
    dict(lvl="hard", q="Max Points on a Line: why store slopes as reduced integer pairs instead of floats?",
         opts=["Floats are slower", "Floating-point division can make equal slopes look different (or different ones equal)", "Integers use less memory", "Tuples sort better"], a=1,
         why="Reduce (dy, dx) by gcd and normalize signs; then equal slopes give identical keys."),
    dict(lvl="hard", q="Longest Duplicate Substring combines binary search with a rolling hash. What does the binary search range over?",
         opts=["Indices of s", "The substring length L: if a duplicate of length L exists, one of length L−1 does too", "Characters a–z", "Hash values"], a=1,
         why="'Exists a duplicate of length L' is monotonic in L, so binary search the length and check each with a rolling hash in O(n)."),
]
