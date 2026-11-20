META = dict(
    title="Resources", page_title="Learning Resources · DSA + System Design Guide", week="Use anytime", group="Resources",
    h1="Videos, courses, books and practice",
    lead="The best free (and a few paid) resources for DSA and system design, chosen to fit this guide. Every topic page also ends with a short \"Learn more\" list for that topic.",
    blurb="YouTube channels, free courses, books, practice sites, visualizers and Google papers.",
    needs_anim=False,
)


def row(name, url, what, cost="Free"):
    return f'<tr><td><a href="{url}" target="_blank" rel="noopener">{name}</a></td><td>{what}</td><td>{cost}</td></tr>'


def table(rows):
    return ('<div class="tbl"><table><thead><tr><th>Resource</th><th>Best for</th><th>Cost</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


DSA_VIDEOS = table([
    row("NeetCode (YouTube)", "https://www.youtube.com/@NeetCode", "Short, clear solutions to almost every checklist problem. Your main companion while practicing."),
    row("Abdul Bari (YouTube)", "https://www.youtube.com/@abdul_bari", "Whiteboard lectures on how algorithms work: sorting, DP, graphs, heaps."),
    row("William Fiset: Data Structures Easy to Advanced", "https://www.youtube.com/watch?v=RBSGKlAvoiM", "8-hour freeCodeCamp course by an ex-Google engineer."),
    row("William Fiset: graph theory videos", "https://www.youtube.com/results?search_query=William+Fiset+graph+theory", "The best graph algorithm explanations on YouTube (YouTube search)."),
    row("takeUforward (Striver)", "https://takeuforward.org/", "A2Z DSA sheet and long playlists on DP, graphs and trees."),
])
DSA_COURSES = table([
    row("MIT 6.006 Introduction to Algorithms (Spring 2020)", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/", "Full university course: lectures, notes, problem sets."),
    row("NeetCode roadmap", "https://neetcode.io/roadmap", "150 problems in a dependency tree, each with a video.", "Free (Pro paid)"),
    row("Tech Interview Handbook", "https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/", "One cheatsheet per topic, plus the whole interview process."),
    row("freeCodeCamp: DSA patterns for LeetCode", "https://www.freecodecamp.org/news/data-structure-and-algorithm-patterns-for-leetcode-interviews/", "Articles and videos on pattern recognition."),
])
VISUAL = table([
    row("VisuAlgo", "https://visualgo.net/en", "Animated arrays, lists, trees, heaps, hash tables, graphs and sorting."),
    row("USFCA algorithm visualizations", "https://www.cs.usfca.edu/~galles/visualization/Algorithms.html", "Step through BFS, DFS, Dijkstra, AVL trees, tries on your own input."),
    row("Python Tutor", "https://pythontutor.com/", "Paste your code and watch every variable change, line by line."),
    row("The Secret Lives of Data: Raft", "https://thesecretlivesofdata.com/raft/", "Animated consensus (leader election, log replication)."),
])
PRACTICE = table([
    row("LeetCode", "https://leetcode.com/", "The problems on your checklist. Use the Google tag in the last few weeks.", "Free (Premium paid)"),
    row("Pramp", "https://www.pramp.com/", "Free peer mock interviews, coding and system design."),
    row("Interviewing.io", "https://interviewing.io/", "Mocks with engineers from big tech, some free practice.", "Mostly paid"),
    row("Google Tech Dev Guide", "https://techdevguide.withgoogle.com/", "Google's own learning paths and practice problems."),
])
SD_VIDEOS = table([
    row("ByteByteGo (YouTube)", "https://www.youtube.com/@ByteByteGo", "Animated 5–10 minute explainers on every building block."),
    row("Gaurav Sen (YouTube)", "https://www.youtube.com/@gkcs", "Beginner-friendly whiteboard videos: consistent hashing, sharding, classic designs."),
    row("Jordan has no life (YouTube)", "https://www.youtube.com/@jordanhasnolife5163", "Detailed interview designs by an ex-Google engineer; great once you know the basics."),
    row("freeCodeCamp: System Design for Beginners", "https://www.youtube.com/watch?v=m8Icp_Cid5o", "A full beginner course in one video."),
    row("Hello Interview (YouTube)", "https://www.youtube.com/results?search_query=Hello+Interview+system+design", "Mock-style walkthroughs by former FAANG interviewers (YouTube search)."),
])
SD_READ = table([
    row("System Design Primer", "https://github.com/donnemartin/system-design-primer", "The most popular free guide: every building block plus solved questions."),
    row("ByteByteGo System Design 101", "https://github.com/ByteByteGoHq/system-design-101", "Hundreds of free diagrams explaining systems visually."),
    row("Hello Interview: System Design in a Hurry", "https://www.hellointerview.com/learn/system-design/in-a-hurry", "Interview framework, core concepts, written breakdowns.", "Mostly free"),
    row("Google SRE books", "https://sre.google/books/", "Google's own books on reliability, SLOs and running systems at scale."),
    row("Martin Kleppmann: Distributed Systems (Cambridge)", "https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/materials.html", "Free lecture videos and notes; clear and rigorous."),
    row("MIT 6.5840 Distributed Systems", "https://pdos.csail.mit.edu/6.824/", "Advanced: papers, lectures and labs (Raft, MapReduce)."),
])
BOOKS = table([
    row("Cracking the Coding Interview (McDowell)", "https://www.crackingthecodinginterview.com/", "The classic coding interview book.", "Paid"),
    row("Grokking Algorithms, 2nd ed. (Bhargava)", "https://www.manning.com/books/grokking-algorithms-second-edition", "Illustrated, gentle intro to algorithms.", "Paid"),
    row("Designing Data-Intensive Applications, 2nd ed. (Kleppmann)", "https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/", "The best book on how data systems really work.", "Paid"),
    row("System Design Interview, Vol. 1 and 2 (Alex Xu)", "https://bytebytego.com/", "Step-by-step designs in interview format.", "Paid"),
])
PAPERS = table([
    row("The Google File System (2003)", "https://research.google.com/archive/gfs-sosp2003.pdf", "Storing huge files across thousands of cheap machines."),
    row("MapReduce (2004)", "https://research.google.com/archive/mapreduce.html", "Batch processing at Google scale."),
    row("Bigtable (2006)", "https://research.google.com/archive/bigtable-osdi06.pdf", "Google's wide-column database."),
    row("Raft consensus", "https://raft.github.io/", "The understandable consensus algorithm, with paper and visualizations."),
])

BODY = rf"""
<section id="idea">
  <span class="eyebrow">How to use these</span>
  <h2>A gym membership, not a library card</h2>
  <div class="real big-real">
    <p>Owning a gym membership doesn't make you fit; using the machines does. In the same way, watching 50 videos won't prepare you as well as solving the problems yourself. Use videos when you're stuck or after you've tried a problem, then close the tab and write the solution from memory.</p>
  </div>
  <div class="tbl"><table>
    <thead><tr><th>When</th><th>Use</th></tr></thead>
    <tbody>
      <tr><td>Learning a new topic</td><td>This guide's page → one explainer video (Abdul Bari, Fiset, ByteByteGo) → a visualizer</td></tr>
      <tr><td>Stuck on a problem for 25+ minutes</td><td>NeetCode's video for that problem, then re-solve it tomorrow without help</td></tr>
      <tr><td>System design practice</td><td>Design it yourself first, then compare with Hello Interview, Jordan, or the Primer</td></tr>
      <tr><td>Weeks 13–14</td><td>Mock interviews (Pramp, Interviewing.io, a friend), not new videos</td></tr>
    </tbody>
  </table></div>
</section>

<section id="dsa-videos">
  <span class="eyebrow">DSA</span>
  <h2>YouTube channels for DSA</h2>
  {DSA_VIDEOS}
</section>

<section id="dsa-courses">
  <span class="eyebrow">DSA</span>
  <h2>Courses and cheatsheets</h2>
  {DSA_COURSES}
</section>

<section id="visual">
  <span class="eyebrow">See it move</span>
  <h2>Visualizers</h2>
  {VISUAL}
</section>

<section id="practice">
  <span class="eyebrow">Do it</span>
  <h2>Practice and mock interviews</h2>
  {PRACTICE}
</section>

<section id="sd-videos">
  <span class="eyebrow">System design</span>
  <h2>YouTube channels for system design</h2>
  {SD_VIDEOS}
  <p class="note">Suggested order: freeCodeCamp's beginner course → ByteByteGo and Gaurav Sen while reading pages 1–6 here → Jordan has no life and Hello Interview for the design walkthroughs.</p>
</section>

<section id="sd-read">
  <span class="eyebrow">System design</span>
  <h2>Guides, books and courses to read</h2>
  {SD_READ}
</section>

<section id="books">
  <span class="eyebrow">If you like books</span>
  <h2>Books worth buying</h2>
  {BOOKS}
  <p class="note">If you only buy one: <em>Designing Data-Intensive Applications</em> for system design depth. For coding, the free resources above are enough.</p>
</section>

<section id="papers">
  <span class="eyebrow">Advanced</span>
  <h2>Classic Google papers</h2>
  {PAPERS}
  <p class="note">You don't need these for an L4 interview, but reading GFS or Bigtable once makes Google's design conversations much easier to follow.</p>
</section>
"""
