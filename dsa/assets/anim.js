// DSA Field Guide — step-by-step algorithm animations.
// Usage in a page: <figure class="anim" data-anim="KEY"><figcaption>…</figcaption></figure>
// Each generator returns an array of frames; renderers draw a frame from scratch.
(function () {
  "use strict";
  const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const clone = o => JSON.parse(JSON.stringify(o));

  // ---------- renderers ----------
  function vars(f) {
    if (!f.vars || !f.vars.length) return "";
    return '<div class="a-vars">' + f.vars.map(([k, v]) =>
      '<span><b>' + esc(k) + '</b> ' + esc(Array.isArray(v) ? "[" + v.join(", ") + "]" : v) + "</span>").join("") + "</div>";
  }

  function rArray(f) {
    const n = f.cells.length;
    const ptrAt = {};
    Object.entries(f.ptr || {}).forEach(([name, i]) => {
      if (i == null || i < 0 || i >= n) return;
      (ptrAt[i] = ptrAt[i] || []).push(name);
    });
    let h = '<div class="a-row">';
    f.cells.forEach((v, i) => {
      const c = (f.cls && f.cls[i]) || "";
      h += '<div class="a-col"><span class="a-idx">' + (f.noIdx ? "&nbsp;" : i) + '</span>' +
        '<span class="a-cell ' + c + '">' + esc(v) + "</span>" +
        '<span class="a-ptr">' + (ptrAt[i] ? esc(ptrAt[i].join(" ")) : "&nbsp;") + "</span></div>";
      if (f.arrows && i < n - 1) h += '<span class="a-arrow">' + esc(f.arrows[i] || " ") + "</span>";
    });
    if (f.tail) h += '<span class="a-arrow">' + esc(f.tail) + "</span>";
    return h + "</div>";
  }

  function rBars(f) {
    const max = Math.max(...f.vals, 1);
    let h = '<div class="a-bars">';
    f.vals.forEach((v, i) => {
      const c = (f.cls && f.cls[i]) || "";
      h += '<div class="a-barcol"><span class="a-bar ' + c + '" style="height:' + (8 + 92 * v / max) + '%"></span><span class="a-idx">' + v + "</span></div>";
    });
    return h + "</div>";
  }

  function rGrid(f) {
    let h = '<div class="a-gridwrap"><table class="a-grid">';
    if (f.colLabels) h += "<tr><th></th>" + f.colLabels.map(c => "<th>" + esc(c) + "</th>").join("") + "</tr>";
    f.cells.forEach((row, r) => {
      h += "<tr>" + (f.rowLabels ? "<th>" + esc(f.rowLabels[r]) + "</th>" : "");
      row.forEach((v, c) => {
        const k = (f.cls && f.cls[r + "," + c]) || "";
        h += '<td class="' + k + '">' + esc(v) + "</td>";
      });
      h += "</tr>";
    });
    return h + "</table></div>";
  }

  // nodes: {id:{v,x,y}}, edges: [[a,b,label?]], directed?: bool
  function rGraph(f) {
    const xs = Object.values(f.nodes).map(n => n.x), ys = Object.values(f.nodes).map(n => n.y);
    const W = Math.max(...xs) + 44, H = Math.max(...ys) + 48;
    let s = '<svg class="a-svg" viewBox="0 0 ' + W + " " + H + '" style="max-width:' + W + 'px" role="img" aria-label="diagram">';
    if (f.ring) s += '<circle class="a-ring" cx="' + f.ring.cx + '" cy="' + f.ring.cy + '" r="' + f.ring.r + '"/>';
    s += '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="a-ah"/></marker></defs>';
    (f.edges || []).forEach(([a, b, lab]) => {
      const A = f.nodes[a], B = f.nodes[b];
      if (!A || !B) return;
      const dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy) || 1, r = 19;
      const x1 = A.x + dx / d * r, y1 = A.y + dy / d * r, x2 = B.x - dx / d * (r + (f.directed ? 3 : 0)), y2 = B.y - dy / d * (r + (f.directed ? 3 : 0));
      const ec = (f.ecls && f.ecls[a + "-" + b]) || "";
      s += '<line class="a-edge ' + ec + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '"' + (f.directed ? ' marker-end="url(#ah)"' : "") + "/>";
      if (lab != null) s += '<text class="a-elab" x="' + ((A.x + B.x) / 2 + 6) + '" y="' + ((A.y + B.y) / 2 - 6) + '">' + esc(lab) + "</text>";
    });
    Object.entries(f.nodes).forEach(([id, n]) => {
      const c = (f.cls && f.cls[id]) || "";
      s += '<g class="a-node ' + c + '"><circle cx="' + n.x + '" cy="' + n.y + '" r="18"/><text x="' + n.x + '" y="' + (n.y + 5) + '">' + esc(n.v) + "</text>";
      if (n.tag != null) s += '<text class="a-tag" x="' + n.x + '" y="' + (n.y + 34) + '">' + esc(n.tag) + "</text>";
      s += "</g>";
    });
    return '<div class="a-svgwrap">' + s + "</svg></div>";
  }

  const R = { array: rArray, bars: rBars, grid: rGrid, graph: rGraph };
  function draw(f) {
    const parts = (f.panels || [f]).map(p => R[p.type](p));
    return parts.join("") + vars(f);
  }

  // ---------- helpers ----------
  function treeLayout(vals) { // level-order array (null = gap) → nodes/edges, positions by index
    const nodes = {}, edges = [];
    const depth = Math.floor(Math.log2(vals.length)) + 1, W = Math.max(320, Math.pow(2, depth - 1) * 52);
    vals.forEach((v, i) => {
      if (v == null) return;
      const d = Math.floor(Math.log2(i + 1)), pos = i + 1 - Math.pow(2, d), slots = Math.pow(2, d);
      nodes[i] = { v, x: 20 + (pos + 0.5) * (W - 40) / slots, y: 26 + d * 64 };
      if (i > 0 && vals[Math.floor((i - 1) / 2)] != null) edges.push([Math.floor((i - 1) / 2), i]);
    });
    return { nodes, edges };
  }

  // ---------- generators ----------
  const G = {};

  G["arrays-two-pointers"] = () => {
    const a = [1, 2, 4, 6, 8, 11, 15], t = 14, fr = [];
    let l = 0, r = a.length - 1;
    fr.push({ type: "array", cells: a, ptr: { l, r }, cls: {}, vars: [["target", t]], note: "Sorted array, target 14. Start l at the smallest value and r at the largest." });
    while (l < r) {
      const s = a[l] + a[r];
      const cls = {}; cls[l] = "cur"; cls[r] = "cur";
      if (s === t) { cls[l] = cls[r] = "hit"; fr.push({ type: "array", cells: a, ptr: { l, r }, cls, vars: [["sum", s], ["target", t]], note: a[l] + " + " + a[r] + " = 14. Found the pair in " + (fr.length) + " steps, not 21 pairs." }); break; }
      fr.push({ type: "array", cells: a, ptr: { l, r }, cls, vars: [["sum", s], ["target", t]], note: a[l] + " + " + a[r] + " = " + s + (s < t ? " is too small, so move l right to a bigger value." : " is too big, so move r left to a smaller value.") });
      if (s < t) l++; else r--;
    }
    return fr;
  };

  G["arrays-kadane"] = () => {
    const a = [-2, 1, -3, 4, -1, 2, 1, -5, 4], fr = [];
    let cur = a[0], best = a[0], start = 0, bs = 0, be = 0;
    const mk = (i, note) => { const cls = {}; for (let k = start; k <= i; k++) cls[k] = "win"; for (let k = bs; k <= be; k++) if (cls[k] !== "win") cls[k] = "done"; cls[i] = "cur"; return { type: "array", cells: a, cls, ptr: { i }, vars: [["cur", cur], ["best", best], ["best range", "[" + bs + ".." + be + "]"]], note }; };
    fr.push(mk(0, "Start: cur = best = -2. The shaded block is the subarray we're currently extending."));
    for (let i = 1; i < a.length; i++) {
      const ext = cur + a[i];
      let note;
      if (a[i] > ext) { note = "cur + " + a[i] + " = " + ext + " is worse than starting fresh at " + a[i] + ", so restart here."; cur = a[i]; start = i; }
      else { note = "Extend: cur + " + a[i] + " = " + ext + "."; cur = ext; }
      if (cur > best) { best = cur; bs = start; be = i; note += " New best: " + best + "."; }
      fr.push(mk(i, note));
    }
    fr[fr.length - 1].note += " Answer: " + best + " from index " + bs + " to " + be + ".";
    return fr;
  };

  G["strings-window"] = () => {
    const s = "abcabcbb".split(""), fr = [], last = {};
    let left = 0, best = 0;
    const mk = (r, note) => { const cls = {}; for (let k = left; k <= r; k++) cls[k] = "win"; if (r >= 0) cls[r] = "cur"; return { type: "array", cells: s, cls, ptr: { L: left, R: r }, vars: [["window", s.slice(left, r + 1).join("")], ["best", best], ["last seen", Object.entries(last).map(([k, v]) => k + ":" + v).join(" ")]], note }; };
    fr.push(mk(-1, "Find the longest substring with no repeated letters. R grows the window; L jumps forward past a repeat."));
    s.forEach((ch, r) => {
      let note = "R reads '" + ch + "'.";
      if (ch in last && last[ch] >= left) { note += " '" + ch + "' is already in the window at " + last[ch] + ", so L jumps to " + (last[ch] + 1) + "."; left = last[ch] + 1; }
      last[ch] = r;
      if (r - left + 1 > best) { best = r - left + 1; note += " New best length " + best + "."; }
      fr.push(mk(r, note));
    });
    fr[fr.length - 1].note += " Answer: " + best + ". Each pointer only moves forward, so it's O(n).";
    return fr;
  };

  G["strings-center"] = () => {
    const s = "xabacabz".split(""), fr = [], c = 4;
    fr.push({ type: "array", cells: s, cls: { [c]: "cur" }, ptr: { center: c }, note: "Expand around center: pick a center (here index 4, 'c') and grow outward while both ends match." });
    let l = c, r = c;
    while (l - 1 >= 0 && r + 1 < s.length && s[l - 1] === s[r + 1]) {
      l--; r++;
      const cls = {}; for (let k = l; k <= r; k++) cls[k] = "win"; cls[l] = cls[r] = "hit";
      fr.push({ type: "array", cells: s, cls, ptr: { l, r }, vars: [["palindrome", s.slice(l, r + 1).join("")]], note: "'" + s[l] + "' == '" + s[r] + "', so the palindrome grows to \"" + s.slice(l, r + 1).join("") + "\"." });
    }
    const cls = {}; for (let k = l; k <= r; k++) cls[k] = "done"; if (l - 1 >= 0) cls[l - 1] = "bad"; if (r + 1 < s.length) cls[r + 1] = "bad";
    fr.push({ type: "array", cells: s, cls, ptr: { l: l - 1, r: r + 1 }, vars: [["palindrome", s.slice(l, r + 1).join("")]], note: "'" + s[l - 1] + "' ≠ '" + s[r + 1] + "', stop. Longest from this center: \"" + s.slice(l, r + 1).join("") + "\". Repeat for all 2n − 1 centers." });
    return fr;
  };

  G["ll-reverse"] = () => {
    const v = [1, 2, 3, 4], fr = [];
    const arrows = ["→", "→", "→"];
    const mk = (prev, cur, note) => ({ type: "array", noIdx: true, cells: v, arrows: arrows.slice(), tail: cur === null ? "" : (prev === v.length - 1 ? "" : ""), cls: Object.fromEntries([[prev, "done"], [cur, "cur"]].filter(([k]) => k != null && k >= 0 && k < v.length)), ptr: { prev, cur, nxt: cur != null && cur + 1 < v.length ? cur + 1 : null }, note });
    fr.push(mk(-1, 0, "prev = None, cur = 1. Arrows show where each node's next points."));
    for (let i = 0; i < v.length; i++) {
      if (i > 0) arrows[i - 1] = "←";
      fr.push(mk(i, i + 1 < v.length ? i + 1 : null, "Save nxt, point " + v[i] + ".next back to " + (i === 0 ? "None" : v[i - 1]) + ", then step prev and cur forward."));
    }
    fr[fr.length - 1].note = "cur is None. Every arrow is flipped; prev (4) is the new head.";
    return fr;
  };

  G["ll-fast-slow"] = () => {
    const v = [1, 2, 3, 4, 5, 6, 7], fr = [];
    let s = 0, f = 0;
    fr.push({ type: "array", noIdx: true, cells: v, arrows: v.slice(1).map(() => "→"), cls: { 0: "cur" }, ptr: { "slow fast": 0 }, note: "Both start at the head. slow moves 1 node per step, fast moves 2." });
    while (f + 1 < v.length && f + 2 <= v.length) {
      s += 1; f += 2;
      if (f >= v.length) { f = v.length; }
      const cls = { [s]: "cur" }; if (f < v.length) cls[f] = "hit";
      const ptr = s === f ? { "slow fast": s } : { slow: s, fast: f < v.length ? f : null };
      fr.push({ type: "array", noIdx: true, cells: v, arrows: v.slice(1).map(() => "→"), cls, ptr, note: f >= v.length - 1 ? "fast reached the end, so slow (" + v[s] + ") is the middle." : "slow → " + v[s] + ", fast → " + v[f] + "." });
      if (f >= v.length - 1) break;
    }
    return fr;
  };

  G["trees-bfs"] = () => {
    const vals = [8, 3, 10, 1, 6, null, 14, null, null, 4, 7, null, null, 13, null];
    const T = treeLayout(vals), fr = [], cls = {};
    let q = [0], out = [], level = [];
    fr.push({ type: "graph", nodes: T.nodes, edges: T.edges, cls: { 0: "hit" }, vars: [["queue", [8]], ["output", "[]"]], note: "BFS starts with the root in the queue." });
    let lvl = 0;
    while (q.length) {
      const size = q.length; level = [];
      for (let k = 0; k < size; k++) {
        const i = q.shift(); level.push(vals[i]); cls[i] = "done";
        [2 * i + 1, 2 * i + 2].forEach(j => { if (j < vals.length && vals[j] != null) { q.push(j); cls[j] = "hit"; } });
        const c = clone(cls); c[i] = "cur";
        fr.push({ type: "graph", nodes: T.nodes, edges: T.edges, cls: c, vars: [["queue", q.map(j => vals[j])], ["this level", level], ["output", JSON.stringify(out.concat([level]))]], note: "Pop " + vals[i] + " (level " + lvl + "), push its children onto the back of the queue." });
      }
      out.push(level); lvl++;
    }
    fr[fr.length - 1].note = "Queue empty. Levels: " + JSON.stringify(out) + ".";
    return fr;
  };

  G["trees-inorder"] = () => {
    const vals = [8, 3, 10, 1, 6, null, 14];
    const T = treeLayout(vals), fr = [], cls = {}, out = [], stack = [];
    let cur = 0;
    const push = note => fr.push({ type: "graph", nodes: T.nodes, edges: T.edges, cls: clone(cls), vars: [["stack", stack.map(i => vals[i])], ["output", out]], note });
    push("Iterative inorder: go left as far as possible, pushing nodes on a stack.");
    while (cur != null || stack.length) {
      while (cur != null && cur < vals.length && vals[cur] != null) { stack.push(cur); cls[cur] = "hit"; push("Push " + vals[cur] + " and go left."); cur = 2 * cur + 1; }
      const i = stack.pop(); out.push(vals[i]); cls[i] = "done";
      const c = 2 * i + 2; cur = c < vals.length && vals[c] != null ? c : null;
      push("Pop " + vals[i] + " and output it" + (cur != null ? ", then go to its right child " + vals[cur] + "." : "."));
    }
    fr[fr.length - 1].note = "Output " + out.join(", ") + ": sorted, because this is a BST.";
    return fr;
  };

  G["stacks-temps"] = () => {
    const t = [73, 74, 75, 71, 69, 72, 76, 73], ans = t.map(() => 0), st = [], fr = [];
    fr.push({ panels: [{ type: "array", cells: t, cls: {} }, { type: "array", cells: ans, noIdx: true, cls: {} }], vars: [["stack (indices)", "[]"]], note: "Daily Temperatures: top row = temps, bottom row = days until warmer. The stack holds days still waiting for a warmer day." });
    t.forEach((x, i) => {
      const popped = [];
      while (st.length && t[st[st.length - 1]] < x) { const j = st.pop(); ans[j] = i - j; popped.push(j); }
      st.push(i);
      const c1 = { [i]: "cur" }; st.forEach(j => { if (j !== i) c1[j] = "win"; });
      const c2 = {}; popped.forEach(j => c2[j] = "hit");
      fr.push({ panels: [{ type: "array", cells: t, cls: c1 }, { type: "array", cells: ans.slice(), noIdx: true, cls: c2 }], vars: [["stack (indices)", "[" + st.join(", ") + "]"]], note: popped.length ? x + "° is warmer than day " + popped.join(", ") + ", so pop them and record the wait. Then push day " + i + "." : x + "° isn't warmer than the top of the stack, so push day " + i + " and wait." });
    });
    fr[fr.length - 1].note += " Each day is pushed and popped once: O(n).";
    return fr;
  };

  G["stacks-parens"] = () => {
    const s = "{[()]}(]".split(""), st = [], fr = [], pair = { ")": "(", "]": "[", "}": "{" };
    fr.push({ type: "array", cells: s, cls: {}, vars: [["stack", "[]"]], note: "Openers go on the stack. A closer must match the most recent opener (the top)." });
    for (let i = 0; i < s.length; i++) {
      const ch = s[i], cls = { [i]: "cur" };
      if ("([{".includes(ch)) { st.push(ch); fr.push({ type: "array", cells: s, cls, vars: [["stack", st.join(" ")]], note: "'" + ch + "' opens: push." }); }
      else if (st.length && st[st.length - 1] === pair[ch]) { st.pop(); cls[i] = "hit"; fr.push({ type: "array", cells: s, cls, vars: [["stack", st.join(" ") || "empty"]], note: "'" + ch + "' matches the top '" + pair[ch] + "': pop." }); }
      else { cls[i] = "bad"; fr.push({ type: "array", cells: s, cls, vars: [["stack", st.join(" ")]], note: "'" + ch + "' doesn't match the top '" + (st[st.length - 1] || "nothing") + "'. Invalid, return False." }); break; }
    }
    return fr;
  };

  G["graphs-islands"] = () => {
    const g = ["11000", "11010", "00100", "00011"].map(r => r.split(""));
    const R = g.length, C = g[0].length, fr = [], cls = {}, seen = new Set();
    let count = 0;
    const cells = () => g.map(r => r.slice());
    fr.push({ type: "grid", cells: cells(), cls: {}, vars: [["islands", 0]], note: "Number of Islands: scan cells; each unvisited '1' starts a BFS that floods its whole island." });
    for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
      if (g[r][c] !== "1" || seen.has(r + "," + c)) continue;
      count++;
      const q = [[r, c]]; seen.add(r + "," + c);
      const tag = "i" + ((count - 1) % 4 + 1);
      while (q.length) {
        const [y, x] = q.shift(); cls[y + "," + x] = tag;
        const snap = clone(cls); snap[y + "," + x] = tag + " cur";
        fr.push({ type: "grid", cells: cells(), cls: snap, vars: [["islands", count], ["queue", q.map(p => "(" + p + ")").join(" ") || "empty"]], note: "Island " + count + ": visit (" + y + "," + x + ") and queue its unvisited land neighbors." });
        [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dy, dx]) => { const ny = y + dy, nx = x + dx, k = ny + "," + nx; if (ny >= 0 && ny < R && nx >= 0 && nx < C && g[ny][nx] === "1" && !seen.has(k)) { seen.add(k); q.push([ny, nx]); } });
      }
    }
    fr.push({ type: "grid", cells: cells(), cls: clone(cls), vars: [["islands", count]], note: "Done: " + count + " islands. Every cell is visited once: O(rows × cols)." });
    return fr;
  };

  G["graphs-topo"] = () => {
    const nodes = { A: { v: "A", x: 40, y: 40 }, B: { v: "B", x: 40, y: 150 }, C: { v: "C", x: 170, y: 95 }, D: { v: "D", x: 300, y: 40 }, E: { v: "E", x: 300, y: 150 } };
    const edges = [["A", "C"], ["B", "C"], ["C", "D"], ["C", "E"], ["D", "E"]];
    const indeg = { A: 0, B: 0, C: 0, D: 0, E: 0 }; edges.forEach(([, b]) => indeg[b]++);
    const tagged = () => { const n = clone(nodes); Object.keys(n).forEach(k => n[k].tag = "in " + indeg[k]); return n; };
    const fr = [], cls = {}, order = [];
    let q = Object.keys(indeg).filter(k => indeg[k] === 0);
    q.forEach(k => cls[k] = "hit");
    fr.push({ type: "graph", directed: true, nodes: tagged(), edges, cls: clone(cls), vars: [["queue", q], ["order", order]], note: "Kahn's algorithm. Arrow X → Y means X must come before Y. Nodes with in-degree 0 have no prerequisites: queue them." });
    while (q.length) {
      const u = q.shift(); order.push(u); cls[u] = "done";
      const freed = [];
      edges.forEach(([a, b]) => { if (a === u) { indeg[b]--; if (indeg[b] === 0) { q.push(b); cls[b] = "hit"; freed.push(b); } } });
      const c = clone(cls); c[u] = "cur";
      fr.push({ type: "graph", directed: true, nodes: tagged(), edges, cls: c, vars: [["queue", q], ["order", order]], note: "Take " + u + ". Remove its arrows, lowering neighbors' in-degree." + (freed.length ? " " + freed.join(", ") + " now has in-degree 0: queue it." : "") });
    }
    fr[fr.length - 1].note += " Order " + order.join(" → ") + ". If fewer nodes come out than exist, there's a cycle.";
    return fr;
  };

  G["dp-coins"] = () => {
    const coins = [1, 2, 5], amt = 11, INF = "∞", dp = Array(amt + 1).fill(INF); dp[0] = 0;
    const fr = [];
    fr.push({ type: "array", cells: dp.slice(), cls: { 0: "done" }, vars: [["coins", coins]], note: "dp[a] = fewest coins to make amount a. dp[0] = 0; everything else starts unknown." });
    for (let a = 1; a <= amt; a++) {
      let best = Infinity, from = null, coin = null;
      coins.forEach(c => { if (c <= a && dp[a - c] !== INF && dp[a - c] + 1 < best) { best = dp[a - c] + 1; from = a - c; coin = c; } });
      dp[a] = best === Infinity ? INF : best;
      const cls = {}; for (let k = 0; k < a; k++) cls[k] = "done"; coins.forEach(c => { if (a - c >= 0) cls[a - c] = "win"; }); if (from != null) cls[from] = "hit"; cls[a] = "cur";
      fr.push({ type: "array", cells: dp.slice(), cls, vars: [["dp[" + a + "]", dp[a]]], note: "Amount " + a + ": check dp[" + coins.filter(c => c <= a).map(c => a - c).join("], dp[") + "] (shaded). Best is dp[" + from + "] + one " + coin + "-coin = " + dp[a] + "." });
    }
    fr[fr.length - 1].note += " Answer: 3 coins (5 + 5 + 1).";
    return fr;
  };

  G["dp-lcs"] = () => {
    const a = "abcde", b = "ace", R = a.length, C = b.length, fr = [];
    const t = Array.from({ length: R + 1 }, () => Array(C + 1).fill(0));
    const cells = () => t.map(r => r.map(String));
    fr.push({ type: "grid", cells: cells(), rowLabels: ["", ...a], colLabels: ["", ...b], cls: {}, note: "LCS of \"abcde\" and \"ace\". Cell (i, j) = LCS of the first i letters of one and first j of the other. Row and column 0 are empty strings: 0." });
    for (let i = 1; i <= R; i++) for (let j = 1; j <= C; j++) {
      const cls = {}; let note;
      if (a[i - 1] === b[j - 1]) { t[i][j] = t[i - 1][j - 1] + 1; cls[(i - 1) + "," + (j - 1)] = "hit"; note = "'" + a[i - 1] + "' = '" + b[j - 1] + "': take the diagonal + 1 = " + t[i][j] + "."; }
      else { t[i][j] = Math.max(t[i - 1][j], t[i][j - 1]); cls[(i - 1) + "," + j] = "win"; cls[i + "," + (j - 1)] = "win"; note = "'" + a[i - 1] + "' ≠ '" + b[j - 1] + "': take the larger of above and left = " + t[i][j] + "."; }
      cls[i + "," + j] = "cur";
      fr.push({ type: "grid", cells: cells(), rowLabels: ["", ...a], colLabels: ["", ...b], cls, note });
    }
    fr[fr.length - 1].note += " Bottom-right = 3 (\"ace\").";
    return fr;
  };

  G["heaps-push"] = () => {
    const h = [], fr = [], ins = [5, 3, 8, 1, 4];
    const mk = (cls, note) => { const T = treeLayout(h.length ? h : [""]); return { type: "graph", nodes: T.nodes, edges: T.edges, cls, vars: [["array", h]], note }; };
    ins.forEach(x => {
      h.push(x); let i = h.length - 1;
      fr.push(mk({ [i]: "cur" }, "Push " + x + ": add it at the next free spot (end of the array)."));
      while (i > 0) {
        const p = Math.floor((i - 1) / 2);
        if (h[p] <= h[i]) { fr.push(mk({ [i]: "done", [p]: "done" }, "Parent " + h[p] + " ≤ " + h[i] + ": heap property holds. Stop.")); break; }
        [h[p], h[i]] = [h[i], h[p]];
        fr.push(mk({ [p]: "cur", [i]: "hit" }, "Parent was bigger, so swap " + h[p] + " up. (sift up)"));
        i = p;
      }
    });
    fr.push(mk({ 0: "hit" }, "The smallest value (" + h[0] + ") is always at the root. Each push moves up at most log n levels."));
    return fr;
  };

  G["hash-buckets"] = () => {
    const B = 5, keys = ["cat", "dog", "owl", "ant", "bee", "fox"];
    const hash = k => [...k].reduce((s, c) => s + c.charCodeAt(0), 0);
    const buckets = Array.from({ length: B }, () => []), fr = [];
    const cells = () => buckets.map(b => b.length ? b.slice() : ["·"]);
    fr.push({ type: "grid", cells: cells(), rowLabels: [0, 1, 2, 3, 4], cls: {}, note: "A hash table with 5 buckets. hash(key) % 5 picks the bucket, so lookups jump straight there." });
    keys.forEach(k => {
      const hv = hash(k), b = hv % B, collide = buckets[b].length > 0;
      buckets[b].push(k);
      const cls = { [b + "," + (buckets[b].length - 1)]: collide ? "hit" : "cur" };
      fr.push({ type: "grid", cells: cells(), rowLabels: [0, 1, 2, 3, 4], cls, vars: [["hash(\"" + k + "\")", hv], ["% 5", b]], note: "Insert \"" + k + "\" → bucket " + b + "." + (collide ? " Collision: the bucket already has a key, so chain it alongside. Lookups here compare both." : "") });
    });
    fr[fr.length - 1].note += " With a good hash and resizing, buckets stay short: O(1) average.";
    return fr;
  };

  G["bits-xor"] = () => {
    const a = [4, 1, 2, 1, 2], fr = [], bin = x => x.toString(2).padStart(3, "0").split("");
    let acc = 0;
    const rows = [], labels = [];
    fr.push({ type: "grid", cells: [bin(0)], rowLabels: ["acc = 0"], colLabels: ["4s", "2s", "1s"], cls: {}, note: "Single Number: XOR everything. x ^ x = 0 and x ^ 0 = x, so pairs cancel and the loner survives." });
    a.forEach((x, i) => {
      acc ^= x;
      rows.push(bin(x)); labels.push("^ " + x);
      const cells = rows.concat([bin(acc)]), rl = labels.concat(["acc = " + acc]);
      const cls = {}; bin(x).forEach((b, c) => { if (b === "1") cls[(rows.length - 1) + "," + c] = "cur"; });
      bin(acc).forEach((b, c) => { if (b === "1") cls[rows.length + "," + c] = "hit"; });
      fr.push({ type: "grid", cells, rowLabels: rl, colLabels: ["4s", "2s", "1s"], cls, note: "acc ^= " + x + " → " + acc + "." + (i >= 3 ? " The second " + x + " flips its bits back off." : "") });
    });
    fr[fr.length - 1].note += " Only 4 appears once: answer 4, in O(n) time and O(1) space.";
    return fr;
  };

  G["sort-merge"] = () => {
    let a = [38, 27, 43, 3, 9, 82, 10, 19];
    const fr = [{ type: "bars", vals: a.slice(), cls: {}, note: "Bottom-up merge sort: treat each item as a sorted run of size 1, then merge neighbors into runs of 2, 4, 8." }];
    for (let w = 1; w < a.length; w *= 2) {
      for (let lo = 0; lo < a.length; lo += 2 * w) {
        const mid = Math.min(lo + w, a.length), hi = Math.min(lo + 2 * w, a.length);
        if (mid >= hi) continue;
        const merged = []; let i = lo, j = mid;
        while (i < mid || j < hi) merged.push(j >= hi || (i < mid && a[i] <= a[j]) ? a[i++] : a[j++]);
        a = a.slice(0, lo).concat(merged, a.slice(hi));
        const cls = {}; for (let k = lo; k < hi; k++) cls[k] = "cur";
        fr.push({ type: "bars", vals: a.slice(), cls, vars: [["run size", w + " + " + w]], note: "Merge the two sorted runs in positions " + lo + "–" + (hi - 1) + ": repeatedly take the smaller front item." });
      }
    }
    fr.push({ type: "bars", vals: a.slice(), cls: Object.fromEntries(a.map((_, i) => [i, "done"])), note: "Sorted. log₂ 8 = 3 rounds, each touching all n items: O(n log n)." });
    return fr;
  };

  G["sort-partition"] = () => {
    const a = [7, 2, 9, 4, 1, 8, 3, 5], fr = [], hi = a.length - 1, p = a[hi];
    let i = 0;
    const mk = (j, note) => { const cls = { [hi]: "hit" }; for (let k = 0; k < i; k++) cls[k] = "done"; if (j != null && j < hi) cls[j] = "cur"; return { type: "bars", vals: a.slice(), cls, vars: [["pivot", p], ["i (next small slot)", i]], note }; };
    fr.push(mk(null, "Quicksort partition (Lomuto). Pivot = last value, 5. Goal: everything smaller than 5 to the left."));
    for (let j = 0; j < hi; j++) {
      if (a[j] < p) { [a[i], a[j]] = [a[j], a[i]]; i++; fr.push(mk(j, a[i - 1] + " < 5: swap it into the small zone (green) and grow the zone.")); }
      else fr.push(mk(j, a[j] + " ≥ 5: leave it."));
    }
    [a[i], a[hi]] = [a[hi], a[i]];
    const cls = {}; for (let k = 0; k < a.length; k++) cls[k] = k < i ? "done" : k === i ? "hit" : "win";
    fr.push({ type: "bars", vals: a.slice(), cls, note: "Swap the pivot into slot " + i + ". It's now in its final sorted position; recurse on each side." });
    return fr;
  };

  G["search-binary"] = () => {
    const a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], t = 23, fr = [];
    let lo = 0, hi = a.length - 1;
    const mk = (mid, note, hit) => { const cls = {}; a.forEach((_, k) => { if (k < lo || k > hi) cls[k] = "dim"; }); if (mid != null) cls[mid] = hit ? "hit" : "cur"; return { type: "array", cells: a, cls, ptr: { lo, mid, hi }, vars: [["target", t]], note }; };
    fr.push(mk(null, "Find 23 in a sorted array. Each check throws away half of what's left (greyed out)."));
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (a[mid] === t) { fr.push(mk(mid, "a[" + mid + "] = 23. Found in " + fr.length + " checks; 10 items need at most 4.", true)); break; }
      fr.push(mk(mid, "a[" + mid + "] = " + a[mid] + (a[mid] < t ? " < 23, so the answer is to the right: lo = mid + 1." : " > 23, so the answer is to the left: hi = mid − 1.")));
      if (a[mid] < t) lo = mid + 1; else hi = mid - 1;
    }
    return fr;
  };

  G["search-answer"] = () => {
    const piles = [3, 6, 7, 11], h = 8, fr = [];
    const hours = k => piles.reduce((s, p) => s + Math.ceil(p / k), 0);
    const speeds = Array.from({ length: 11 }, (_, i) => i + 1);
    let lo = 1, hi = 11;
    const mk = (mid, note) => { const cls = {}; speeds.forEach((_, k) => { if (k + 1 < lo || k + 1 > hi) cls[k] = "dim"; }); if (mid) cls[mid - 1] = "cur"; return { type: "array", cells: speeds, noIdx: true, cls, ptr: { lo: lo - 1, mid: mid ? mid - 1 : null, hi: hi - 1 }, vars: [["piles", piles], ["hours allowed", h]], note }; };
    fr.push(mk(null, "Koko Eating Bananas: binary search over possible SPEEDS 1–11, not over the array. Faster always means fewer hours."));
    while (lo < hi) {
      const mid = (lo + hi) >> 1, hr = hours(mid);
      fr.push(mk(mid, "Speed " + mid + " takes " + hr + " hours. " + (hr <= h ? "That fits, so try slower: hi = " + mid + "." : "Too slow, so lo = " + (mid + 1) + ".")));
      if (hr <= h) hi = mid; else lo = mid + 1;
    }
    const f = mk(lo, "lo = hi = " + lo + ": the slowest speed that finishes in " + h + " hours."); f.cls[lo - 1] = "hit"; fr.push(f);
    return fr;
  };


  // ================= system design =================
  const SDN = (v, x, y, tag) => ({ v, x, y, tag });

  G["sd-request"] = () => {
    const nodes = { U: SDN("You", 34, 100, "browser"), D: SDN("DNS", 124, 30, "DNS"), C: SDN("CDN", 124, 180, "CDN"), L: SDN("LB", 214, 100, "load bal."), S: SDN("App", 304, 100, "app"), K: SDN("$", 394, 30, "cache"), B: SDN("DB", 394, 180, "database") };
    const edges = [["U", "D"], ["U", "C"], ["U", "L"], ["L", "S"], ["S", "K"], ["S", "B"]];
    const st = (on, cls, note) => ({ type: "graph", directed: true, nodes, edges, cls, ecls: Object.fromEntries(on.map(e => [e, "on"])), note });
    return [
      st([], { U: "cur" }, "You type youtube.com and press Enter. Seven parts work together to answer you in under a second."),
      st(["U-D"], { U: "done", D: "cur" }, "DNS is the internet's phone book: it turns the name youtube.com into an IP address, usually cached on your laptop or router."),
      st(["U-C"], { U: "done", C: "cur" }, "Images, videos and JavaScript come from a CDN server near you, so they travel a few miles instead of across the ocean."),
      st(["U-L"], { U: "done", L: "cur" }, "Your API request (\"get my home feed\") reaches a load balancer, which spreads traffic over many identical servers."),
      st(["U-L", "L-S"], { L: "done", S: "cur" }, "The load balancer forwards it to a healthy app server, which runs the business logic."),
      st(["L-S", "S-K"], { S: "done", K: "bad" }, "The server checks the cache first (~1 ms). Miss: this feed isn't cached yet."),
      st(["S-B"], { S: "done", B: "cur" }, "So it reads the database (~10 ms or more) and saves the result in the cache for next time."),
      st(["S-K"], { S: "done", K: "hit" }, "The next request for the same feed is a cache hit: no database work at all. The response flows back the way it came.")
    ];
  };

  G["sd-lb"] = () => {
    const base = { L: SDN("LB", 40, 115, "load bal."), A: SDN("S1", 240, 30), B: SDN("S2", 240, 115), C: SDN("S3", 240, 200) };
    const cnt = { A: 0, B: 0, C: 0 }, fr = [], order = ["A", "B", "C"];
    let down = false, rr = 0;
    const mk = (target, note) => {
      const nodes = clone(base); order.forEach(k => nodes[k].tag = (k === "B" && down ? "DOWN" : cnt[k] + " req"));
      const cls = { L: "done" }; if (down) cls.B = "bad"; if (target) cls[target] = "cur";
      return { type: "graph", directed: true, nodes, edges: [["L", "A"], ["L", "B"], ["L", "C"]], cls, ecls: target ? { ["L-" + target]: "on" } : {}, note };
    };
    fr.push(mk(null, "Round robin: the load balancer hands requests to S1, S2, S3 in turn, like a host seating diners at tables in rotation."));
    for (let r = 1; r <= 8; r++) {
      if (r === 5) { down = true; fr.push(mk(null, "S2 crashes. Its health check (a ping every few seconds) fails, so the load balancer takes it out of rotation.")); }
      let t; do { t = order[rr++ % 3]; } while (down && t === "B");
      cnt[t]++;
      fr.push(mk(t, "Request " + r + " → " + base[t].v + "." + (down ? " S2 is skipped; users never notice the crash." : "")));
    }
    fr[fr.length - 1].note += " This is why servers should be stateless: any server can handle any request.";
    return fr;
  };

  G["sd-cache"] = () => {
    const cap = 3, reqs = ["A", "B", "C", "A", "D", "B", "E", "A"], cache = [], fr = [];
    let hits = 0, miss = 0;
    const cells = () => { const c = cache.slice(); while (c.length < cap) c.push("·"); return c; };
    fr.push({ type: "array", cells: cells(), noIdx: true, cls: {}, vars: [["capacity", cap], ["requests", reqs.join(" ")]], note: "LRU cache with room for 3 items. Left = most recently used, right = least recently used (next to be evicted)." });
    reqs.forEach((k, i) => {
      const at = cache.indexOf(k); let note;
      if (at >= 0) { hits++; cache.splice(at, 1); cache.unshift(k); note = "Get " + k + ": HIT (~1 ms). Move it to the front because it was just used."; }
      else {
        miss++; let ev = "";
        if (cache.length === cap) ev = " Cache is full, so evict " + cache.pop() + ", the least recently used.";
        cache.unshift(k); note = "Get " + k + ": MISS. Read the database (~10 ms), then store it." + ev;
      }
      fr.push({ type: "array", cells: cells(), noIdx: true, cls: { 0: at >= 0 ? "hit" : "cur" }, vars: [["request", (i + 1) + " of " + reqs.length], ["hits", hits], ["misses", miss], ["hit rate", Math.round(100 * hits / (hits + miss)) + "%"]], note });
    });
    fr[fr.length - 1].note += " Real caches hold millions of items and often reach 90%+ hit rates on popular data.";
    return fr;
  };

  G["sd-replication"] = () => {
    const nodes = (l, f1, f2) => ({ W: SDN("App", 40, 110, "client"), L: SDN("L", 210, 110, "leader " + l), F: SDN("F1", 380, 40, "follower " + f1), G: SDN("F2", 380, 180, "follower " + f2) });
    const edges = [["W", "L"], ["L", "F"], ["L", "G"]];
    const g = (n, cls, on, note) => ({ type: "graph", directed: true, nodes: n, edges, cls, ecls: Object.fromEntries(on.map(e => [e, "on"])), note });
    return [
      g(nodes("x=4", "x=4", "x=4"), {}, [], "Leader–follower replication. All three copies hold x = 4. Writes go to the leader; reads can go to any copy."),
      g(nodes("x=5", "x=4", "x=4"), { L: "cur" }, ["W-L"], "The app writes x = 5. Only the leader accepts writes, so there's one source of truth."),
      g(nodes("x=5", "x=5", "x=4"), { L: "done", F: "cur" }, ["L-F"], "The leader streams the change to its followers. F1 has applied it."),
      g(nodes("x=5", "x=5", "x=4"), { G: "bad" }, ["W-G"].filter(Boolean), "A read lands on F2 before the change arrives: it returns x = 4. This is replication lag, and it's why replicas are \"eventually consistent.\""),
      g(nodes("x=5", "x=5", "x=5"), { L: "done", F: "done", G: "done" }, ["L-G"], "F2 catches up a few milliseconds later. Fix for stale reads that matter: read your own writes from the leader."),
      g(nodes("down", "x=5", "x=5"), { L: "bad", F: "hit" }, [], "If the leader dies, a follower is promoted (failover). Data survives because it existed on more than one machine.")
    ];
  };

  G["sd-hashring"] = () => {
    const cx = 170, cy = 160, R = 120, pos = deg => ({ x: Math.round(cx + R * Math.sin(deg * Math.PI / 180)), y: Math.round(cy - R * Math.cos(deg * Math.PI / 180)) });
    const servers = { A: 60, B: 180, C: 300 }, keys = { k1: 15, k2: 95, k3: 135, k4: 205, k5: 260, k6: 340 };
    const colorOf = { A: "o1", B: "o2", C: "o3", D: "o4" };
    const owner = (deg, sv) => { const s = Object.entries(sv).sort((a, b) => a[1] - b[1]); const hit = s.find(([, d]) => d >= deg); return (hit || s[0])[0]; };
    const frame = (sv, moved, note, showOwner) => {
      const nodes = {}, cls = {};
      Object.entries(sv).forEach(([k, d]) => { const p = pos(d); nodes[k] = SDN(k, p.x, p.y, "server"); cls[k] = colorOf[k] + " srv"; });
      Object.entries(keys).forEach(([k, d]) => { const p = pos(d), o = owner(d, sv); nodes[k] = SDN(k, p.x, p.y, showOwner ? "→" + o : ""); if (showOwner) cls[k] = colorOf[o]; if (moved.includes(k)) cls[k] += " moved"; });
      return { type: "graph", ring: { cx, cy, r: R }, nodes, edges: [], cls, note };
    };
    return [
      frame(servers, [], "Consistent hashing puts servers and keys on the same circle (hash value 0 → max wraps around). Three servers: A, B, C.", false),
      frame(servers, [], "Each key walks clockwise to the first server it meets. k1 → A; k2, k3 → B; k4, k5 → C; k6 wraps past the top → A.", true),
      frame(Object.assign({}, servers, { D: 230 }), ["k4"], "Add server D between B and C. Only k4 (between B and D) moves. Everything else stays put.", true),
      frame(Object.assign({}, servers, { D: 230 }), ["k4"], "With plain hash(key) % N, going from 3 to 4 servers moves about 75% of keys and floods the database. Here only ~1/N move. Real systems add \"virtual nodes\" so load stays even.", true)
    ];
  };

  G["sd-queue"] = () => {
    const fr = [], q = [], done = [];
    let n = 0;
    const mk = (note, cls) => ({ panels: [{ type: "array", cells: q.length ? q.slice() : ["empty"], noIdx: true, cls: cls || {} }], vars: [["queue length", q.length], ["emails sent", done.length ? done.join(", ") : "none"]], note });
    fr.push(mk("A shop's \"order confirmed\" emails go through a message queue. The website adds a job and replies to the shopper right away; a worker sends emails at its own pace."));
    [3, 2].forEach(burst => {
      for (let i = 0; i < burst; i++) q.push("#" + (++n));
      fr.push(mk("Flash sale: " + burst + " orders arrive at once. They join the back of the queue. Shoppers already saw \"Order placed!\" in ~50 ms.", Object.fromEntries(q.map((_, i) => [i, i >= q.length - burst ? "cur" : ""]))));
      for (let i = 0; i < 2 && q.length; i++) { const j = q.shift(); done.push(j); fr.push(mk("Worker takes " + j + " from the front and sends its email (~1 s each).", {})); }
    });
    while (q.length) { const j = q.shift(); done.push(j); fr.push(mk("Worker takes " + j + ". The spike is absorbed without the website slowing down.", {})); }
    fr[fr.length - 1].note += " If emails pile up, add more workers; if a worker crashes mid-job, the unacknowledged job is retried.";
    return fr;
  };

  G["sd-token"] = () => {
    const cap = 4, per = [3, 0, 4, 1, 0, 0, 2], fr = [];
    let tokens = cap, ok = 0, no = 0;
    const bucket = () => Array.from({ length: cap }, (_, i) => i < tokens ? "●" : "·");
    fr.push({ panels: [{ type: "array", cells: bucket(), noIdx: true, cls: {} }], vars: [["capacity", cap], ["refill", "1 token / second"]], note: "Token bucket rate limiter. Each request spends one token. The bucket refills 1 token per second, up to 4. Bursts are allowed; sustained floods aren't." });
    per.forEach((r, t) => {
      if (t > 0 && tokens < cap) tokens++;
      const res = [];
      for (let i = 0; i < r; i++) { if (tokens > 0) { tokens--; ok++; res.push("200 ✓"); } else { no++; res.push("429 ✗"); } }
      const cls = {}; res.forEach((x, i) => cls[i] = x[0] === "2" ? "done" : "bad");
      fr.push({ panels: [{ type: "array", cells: bucket(), noIdx: true, cls: {} }, { type: "array", cells: res.length ? res : ["no requests"], noIdx: true, cls }], vars: [["second", t], ["allowed", ok], ["rejected", no]], note: "Second " + t + (t ? ": +1 token refilled. " : ": bucket starts full. ") + (r ? r + " request" + (r > 1 ? "s" : "") + " arrive." : "Quiet second; tokens build back up.") + (res.includes("429 ✗") ? " Out of tokens → HTTP 429 Too Many Requests." : "") });
    });
    return fr;
  };

  G["sd-circuit"] = () => {
    const out = [], fr = [];
    let state = "CLOSED", fails = 0;
    const push = (cell, cls, note) => { out.push(cell); const c = {}; out.forEach((x, i) => c[i] = x === "✓" ? "done" : x === "⚡" ? "dim" : "bad"); c[out.length - 1] += " cur"; fr.push({ type: "array", cells: out.slice(), noIdx: true, cls: c, vars: [["breaker", state], ["failures in a row", fails]], note }); };
    fr.push({ type: "array", cells: ["…"], noIdx: true, cls: {}, vars: [["breaker", state]], note: "Circuit breaker around a payment service, like the breaker in your home's fuse box. CLOSED means calls go through normally." });
    push("✓", "", "Call 1 succeeds.");
    ["Payment service is overloaded: call times out after 2 s.", "Fails again.", "Third failure in a row."].forEach((t, i) => { fails++; if (fails === 3) state = "OPEN"; push("✗", "", t + (fails === 3 ? " Threshold reached: the breaker trips OPEN." : "")); });
    for (let i = 0; i < 3; i++) push("⚡", "", "OPEN: fail instantly (\"payments are busy, try again shortly\") instead of waiting 2 s. The struggling service gets room to recover.");
    state = "HALF-OPEN"; push("✓", "", "After a 30 s cool-down the breaker goes HALF-OPEN and lets one trial call through. It succeeds.");
    state = "CLOSED"; fails = 0; push("✓", "", "Trial worked, so the breaker CLOSES and traffic flows normally again. Without it, every user would have waited for timeouts and piled more load on.");
    return fr;
  };

  G["sd-base62"] = () => {
    const A = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", id0 = 11157, fr = [], digits = [];
    let n = id0;
    fr.push({ type: "array", cells: ["?"], noIdx: true, cls: {}, vars: [["database id", id0], ["alphabet", "0-9 a-z A-Z (62 chars)"]], note: "URL shortener: the database gives each new link a unique number. Base-62 turns that number into a short code, the same way base 10 turns a count into digits." });
    while (n > 0) {
      const r = n % 62, q = Math.floor(n / 62);
      digits.unshift(A[r]);
      fr.push({ type: "array", cells: digits.slice(), noIdx: true, cls: { 0: "cur" }, vars: [["n", n], ["n % 62", r + " → '" + A[r] + "'"], ["n // 62", q]], note: n + " ÷ 62 = " + q + " remainder " + r + ". Remainder " + r + " is the character '" + A[r] + "'; keep going with " + q + "." });
      n = q;
    }
    fr.push({ type: "array", cells: digits.slice(), noIdx: true, cls: Object.fromEntries(digits.map((_, i) => [i, "done"])), vars: [["short URL", "sho.rt/" + digits.join("")]], note: "id " + id0 + " → \"" + digits.join("") + "\". Seven characters give 62⁷ ≈ 3.5 trillion codes, enough for decades. Decoding is the reverse, so no lookup table is needed." });
    return fr;
  };

  G["sd-fanout"] = () => {
    const nodes = { P: SDN("Ana", 46, 60, "posts"), S: SDN("★", 46, 220, "celebrity"), F1: SDN("F1", 300, 20, "feed"), F2: SDN("F2", 300, 100, "feed"), F3: SDN("F3", 300, 180, "feed"), F4: SDN("F4", 300, 260, "feed") };
    const edges = [["P", "F1"], ["P", "F2"], ["P", "F3"], ["P", "F4"], ["S", "F3"]];
    const g = (cls, on, note) => ({ type: "graph", directed: true, nodes, edges, cls, ecls: Object.fromEntries(on.map(e => [e, "on"])), note });
    return [
      g({}, [], "News feed. Ana has 4 followers. Each follower has a precomputed feed list in a cache, so opening the app is one fast read."),
      g({ P: "cur" }, [], "Ana posts a photo. The post is saved once in the posts table."),
      g({ P: "done", F1: "hit", F2: "hit", F3: "hit", F4: "hit" }, ["P-F1", "P-F2", "P-F3", "P-F4"], "Fan-out on write (push): a background worker inserts the post ID into all 4 followers' feeds. Reading a feed is now instant."),
      g({ S: "bad" }, [], "Problem: a celebrity with 100 million followers would need 100 million inserts per post. That's far too slow and expensive."),
      g({ S: "done", F3: "cur" }, ["S-F3"], "Fan-out on read (pull) for celebrities: when F3 opens the app, fetch the few celebrities they follow at read time and merge with their precomputed feed."),
      g({ P: "done", S: "done", F3: "hit" }, ["P-F3", "S-F3"], "Hybrid: push for normal users, pull for celebrities. This is the standard interview answer, and roughly how large social apps work.")
    ];
  };

  // ---------- player ----------
  function mount(fig) {
    const key = fig.dataset.anim, gen = G[key];
    if (!gen) { fig.insertAdjacentHTML("beforeend", '<p class="note">Animation "' + esc(key) + '" not found.</p>'); return; }
    const frames = gen();
    let i = 0, timer = null, speed = 1;
    const stage = document.createElement("div"); stage.className = "a-stage";
    const note = document.createElement("p"); note.className = "a-note"; note.setAttribute("aria-live", "polite");
    const ctl = document.createElement("div"); ctl.className = "a-ctl";
    ctl.innerHTML = '<button type="button" data-a="first" aria-label="Restart">⏮</button>' +
      '<button type="button" data-a="prev" aria-label="Previous step">◀</button>' +
      '<button type="button" data-a="play" class="a-play">▶ Play</button>' +
      '<button type="button" data-a="next" aria-label="Next step">▶|</button>' +
      '<span class="a-step"></span>' +
      '<button type="button" data-a="speed" class="a-speed" aria-label="Playback speed">1×</button>';
    fig.append(stage, note, ctl);
    const stepEl = ctl.querySelector(".a-step"), playBtn = ctl.querySelector(".a-play"), spBtn = ctl.querySelector(".a-speed");
    const show = () => {
      stage.innerHTML = draw(frames[i]);
      note.textContent = frames[i].note || "";
      stepEl.textContent = "Step " + (i + 1) + " / " + frames.length;
    };
    const stop = () => { clearInterval(timer); timer = null; playBtn.textContent = "▶ Play"; };
    const play = () => {
      if (i >= frames.length - 1) i = 0;
      show(); playBtn.textContent = "⏸ Pause";
      timer = setInterval(() => { if (i < frames.length - 1) { i++; show(); } else stop(); }, 1500 / speed);
    };
    ctl.addEventListener("click", e => {
      const a = e.target.closest("button"); if (!a) return;
      const act = a.dataset.a;
      if (act === "play") { timer ? stop() : play(); return; }
      if (act === "speed") { speed = speed === 1 ? 2 : speed === 2 ? 0.5 : 1; spBtn.textContent = speed + "×"; if (timer) { stop(); play(); } return; }
      stop();
      if (act === "first") i = 0;
      if (act === "prev") i = Math.max(0, i - 1);
      if (act === "next") i = Math.min(frames.length - 1, i + 1);
      show();
    });
    show();
  }
  window.DSA_ANIMS = Object.keys(G);
  document.querySelectorAll("figure.anim").forEach(mount);
})();
