META = dict(
    title="Interview playbook", page_title="Interview Playbook · DSA Field Guide", week="Weeks 13–14", group="Interview prep",
    h1="The Google interview playbook",
    lead="Knowing DSA is half the job. The other half is how you run the 45 minutes: clarifying, thinking out loud, testing, and handling being stuck. This page is the routine to rehearse in every mock.",
    blurb="The 45-minute routine, what's graded, getting unstuck, STAR stories.",
    needs_anim=False,
)

BODY = r"""
<section id="idea">
  <span class="eyebrow">The idea</span>
  <h2>A cooking show, not a cooking exam</h2>
  <div class="real big-real">
    <p>On a cooking show, the judges taste the dish, but they also watch the chef explain choices, adjust when something burns, and plate on time. A coding interview is the same. A perfect solution delivered in silence scores worse than a good solution where the interviewer heard your reasoning, saw you test it, and watched you recover from a mistake.</p>
  </div>
</section>

<section id="graded">
  <span class="eyebrow">Scoring</span>
  <h2>What Google interviewers write down</h2>
  <p>Google's public hiring guidance names four areas. Coding rounds feed mostly the first two, and every round contributes to the last.</p>
  <div class="tbl"><table>
    <thead><tr><th>Attribute</th><th>What it looks like in a coding round</th></tr></thead>
    <tbody>
      <tr><td>General cognitive ability</td><td>How you break the problem down, find the brute force, and improve it</td></tr>
      <tr><td>Role-related knowledge</td><td>Choosing the right data structure, correct Big-O, clean working code</td></tr>
      <tr><td>Leadership</td><td>Driving the conversation, proposing options, owning the plan</td></tr>
      <tr><td>Googleyness</td><td>Collaborating with the interviewer, handling feedback well, humility</td></tr>
    </tbody>
  </table></div>
  <p class="note">Source: <a href="https://www.google.com/about/careers/applications/how-we-hire/" target="_blank" rel="noopener">Google: How we hire</a>.</p>
</section>

<section id="routine">
  <span class="eyebrow">The routine</span>
  <h2>Seven steps for every coding question</h2>
  <div class="real"><p>A pilot runs the same takeoff checklist on every flight, even after 10,000 flights. Use the same seven steps on every practice problem until they're automatic, so stress can't knock them out.</p></div>
  <div class="tbl"><table>
    <thead><tr><th>Step</th><th>Minutes</th><th>What you do and say</th></tr></thead>
    <tbody>
      <tr><td>1. Clarify</td><td>3–5</td><td>Restate the problem. Ask about input size, empty input, duplicates, negatives, sorted?, return format.</td></tr>
      <tr><td>2. Examples</td><td>2–3</td><td>Work one normal and one edge example by hand. Confirm expected output.</td></tr>
      <tr><td>3. Brute force</td><td>2</td><td>State it and its Big-O. "This works but is O(n²)."</td></tr>
      <tr><td>4. Optimize</td><td>5–10</td><td>Name the bottleneck and the pattern that removes it. Get agreement before coding.</td></tr>
      <tr><td>5. Code</td><td>15–20</td><td>Clean names, small helper functions, narrate as you go.</td></tr>
      <tr><td>6. Test</td><td>5</td><td>Trace your example line by line. Then run an edge case. Fix bugs calmly.</td></tr>
      <tr><td>7. Analyze</td><td>2</td><td>Final time and space complexity, and one possible improvement or trade-off.</td></tr>
    </tbody>
  </table></div>
</section>

<section id="phrases">
  <span class="eyebrow">Out loud</span>
  <h2>Phrases that show your thinking</h2>
  <div class="real"><p>A GPS that says "recalculating" is reassuring; one that goes silent makes you think it's broken. Narrating keeps the interviewer confident you're making progress.</p></div>
  <ul>
    <li>"Before I start, can I check a few assumptions about the input?"</li>
    <li>"The brute force is to try every pair, which is O(n²). The repeated work is the inner search, so a hashmap could make that O(1)."</li>
    <li>"I'm choosing BFS rather than DFS because we want the fewest steps."</li>
    <li>"Let me trace this with the example to make sure the pointers move correctly."</li>
    <li>"I see a bug here: when the list has one node, <code>fast.next</code> is None. Let me guard that."</li>
    <li>"This uses O(n) extra space. If memory mattered more, I could sort and use two pointers instead, at O(n log n) time."</li>
  </ul>
</section>

<section id="stuck">
  <span class="eyebrow">When stuck</span>
  <h2>A ladder for getting unstuck</h2>
  <div class="real"><p>Lost on a hike, you don't sit down; you retrace to the last trail marker, check the map, and try the next path. Being stuck in an interview is normal. What's graded is what you do next.</p></div>
  <div class="trace">
    <div><p>Solve a tiny example by hand and watch what <em>you</em> do. Your hands often find the algorithm.</p></div>
    <div><p>Go back to the brute force and ask what work is repeated.</p></div>
    <div><p>Walk the <a href="patterns.html">pattern finder</a> list in your head: sorted? contiguous? all answers? top k? graph?</p></div>
    <div><p>Simplify: solve it for a sorted array, or with no duplicates, or for k = 1, then generalize.</p></div>
    <div><p>Say what you're thinking and ask, "Am I on the right track?" Using a hint well is a positive signal, not a failure.</p></div>
  </div>
</section>

<section id="behavioral">
  <span class="eyebrow">Googleyness and leadership</span>
  <h2>Behavioral answers with STAR</h2>
  <div class="real"><p>A good story at a dinner party has a setting, a problem, what you did, and how it ended. STAR is that, in 2 minutes: <strong>Situation, Task, Action, Result</strong>. Spend most of the time on Action, and use "I," not "we."</p></div>
  <p><strong>Example:</strong> "Tell me about a difficult bug."</p>
  <div class="trace">
    <div><p><strong>Situation:</strong> "Our checkout page started timing out for about 2% of users after a release."</p></div>
    <div><p><strong>Task:</strong> "I was on call and needed to find the cause without rolling back a release with an important fix."</p></div>
    <div><p><strong>Action:</strong> "I compared slow and normal requests in the logs and saw the slow ones all had large carts. I found an N+1 query that grew with cart size, rewrote it as one batched query, and added a load test with a 200-item cart."</p></div>
    <div><p><strong>Result:</strong> "Timeouts dropped to zero, p95 latency improved 40%, and the load test now runs in CI so it can't regress."</p></div>
  </div>
  <p>Prepare 6–8 stories you can adapt:</p>
  <ul>
    <li>A hard bug or production issue you diagnosed</li>
    <li>A disagreement with a teammate or manager, and how it was resolved</li>
    <li>A project with unclear or changing requirements</li>
    <li>A failure or mistake, and what you changed afterwards</li>
    <li>Leading or influencing without formal authority</li>
    <li>Helping or mentoring someone</li>
    <li>Learning a new technology quickly</li>
    <li>Making something more accessible or inclusive for users</li>
  </ul>
</section>

<section id="checklist">
  <span class="eyebrow">Logistics</span>
  <h2>The week before and the day of</h2>
  <div class="real"><p>Marathon runners don't train hardest the week before the race; they taper, rest, and lay out their kit the night before. Do the same.</p></div>
  <ul>
    <li>Week before: only review your mistakes log and redo 1–2 problems per topic. No new topics.</li>
    <li>Do two full mocks in a plain Google Doc, out loud, with a timer.</li>
    <li>Prepare 2–3 questions to ask each interviewer about their team and work.</li>
    <li>Day of: sleep, water, a working camera and mic (if virtual), a pen and paper for sketches.</li>
    <li>Between rounds: let the last round go. Each interviewer scores independently.</li>
  </ul>
</section>
"""

QUIZ = [
    dict(lvl="easy", q="You get the problem. What's the best first move?",
         opts=["Start coding immediately", "Restate it and ask clarifying questions about inputs and edge cases", "Ask for the optimal answer", "Stay silent and think for 10 minutes"], a=1,
         why="Clarifying prevents solving the wrong problem and is part of what's graded."),
    dict(lvl="easy", q="In STAR, which part should take the most time?", opts=["Situation", "Task", "Action", "Result"], a=2,
         why="Interviewers want to hear what *you* did and why."),
    dict(lvl="easy", q="You finish coding. What next?",
         opts=["Say \"done\"", "Trace through an example and an edge case, then state complexity", "Ask if you passed", "Refactor everything"], a=1,
         why="Testing your own code is explicitly expected."),
    dict(lvl="medium", q="You only see a brute-force O(n²) solution. What should you do?",
         opts=["Hide it and keep thinking silently", "State it with its complexity, then look for the repeated work to optimize", "Code it immediately without mentioning complexity", "Give up"], a=1,
         why="A stated brute force shows a baseline and often reveals the optimization."),
    dict(lvl="medium", q="The interviewer gives a hint. How is that viewed?",
         opts=["Automatic fail", "Fine, if you understand it and use it well", "Only allowed once", "It means you should start over"], a=1,
         why="Collaboration and coachability are part of what's assessed."),
    dict(lvl="medium", q="Which behavioral answer is strongest?",
         opts=["\"We fixed it as a team.\"", "\"I found the N+1 query, batched it, and added a load test; timeouts dropped to zero.\"", "\"It was a hard time.\"", "\"My manager handled it.\""], a=1,
         why="Specific actions by you, with a measurable result."),
    dict(lvl="hard", q="You find a bug in your code while testing. Best response?",
         opts=["Hope the interviewer didn't notice", "Name it, explain why it happens, fix it, and re-run the trace", "Rewrite the whole solution", "Say it's an edge case that doesn't matter"], a=1,
         why="Catching and fixing your own bug is a positive signal."),
    dict(lvl="hard", q="Ten minutes left and your optimal idea isn't coded yet. What's wise?",
         opts=["Keep designing silently", "Tell the interviewer, code the working approach cleanly, and describe how you'd optimize", "Start a third approach", "Stop talking"], a=1,
         why="Working code plus a clear explanation of the better approach beats an unfinished optimal attempt."),
    dict(lvl="hard", q="The interviewer asks \"Can we do better?\" after your O(n) time, O(n) space solution. A good reply?",
         opts=["\"No.\"", "\"Time can't beat O(n) since we must read the input. Space might drop to O(1) with two pointers if the array is sorted or we can sort it.\"", "Immediately recode", "\"Maybe with a heap.\""], a=1,
         why="Reason about lower bounds and trade-offs explicitly."),
]
