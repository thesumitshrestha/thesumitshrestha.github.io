// DSA Field Guide — quiz engine, problem checklist, progress
(function () {
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) {} }
  };
  const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const inline = s => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*([^*\s][^*]*)\*/g, "<em>$1</em>");

  // ---- problem checklist ----
  document.querySelectorAll(".problems").forEach(list => {
    const out = list.parentElement.querySelector(".progress");
    const boxes = [...list.querySelectorAll("input[type=checkbox]")];
    const update = () => {
      const n = boxes.filter(b => b.checked).length;
      if (out) out.textContent = n + " / " + boxes.length + " solved";
    };
    boxes.forEach(b => {
      b.checked = store.get("dsa:p:" + b.id) === "1";
      b.closest(".prob").classList.toggle("done", b.checked);
      b.addEventListener("change", () => {
        store.set("dsa:p:" + b.id, b.checked ? "1" : null);
        b.closest(".prob").classList.toggle("done", b.checked);
        update();
      });
    });
    update();
  });

  // ---- index progress ----
  document.querySelectorAll("[data-ids]").forEach(tile => {
    const ids = tile.dataset.ids.split(",").filter(Boolean);
    const n = ids.filter(id => store.get("dsa:p:" + id) === "1").length;
    const bar = tile.querySelector(".meter span");
    const count = tile.querySelector(".count");
    if (bar) bar.style.width = (ids.length ? (100 * n / ids.length) : 0) + "%";
    if (count) count.textContent = n + " / " + ids.length + " problems solved";
  });
  const total = document.getElementById("overall");
  if (total) {
    const all = [...document.querySelectorAll("[data-ids]")].flatMap(t => t.dataset.ids.split(",").filter(Boolean));
    const n = all.filter(id => store.get("dsa:p:" + id) === "1").length;
    total.textContent = n + " of " + all.length + " checklist problems solved";
  }


  // ---- topic checklists (keys like dsa:t:<page>:<step>) ----
  const stepBoxes = [...document.querySelectorAll("input[data-key]")];
  const paintSteps = () => {
    stepBoxes.forEach(b => {
      const on = store.get(b.dataset.key) === "1";
      b.checked = on;
      const row = b.closest(".step-row"); if (row) row.classList.toggle("done", on);
    });
    document.querySelectorAll("[data-steps]").forEach(el => {
      const keys = el.dataset.steps.split(",").filter(Boolean);
      const n = keys.filter(k => store.get(k) === "1").length;
      const all = n === keys.length;
      if (el.classList.contains("chip-steps")) { el.textContent = "Checklist " + n + " / " + keys.length + (all ? " ✓" : ""); el.classList.toggle("all", all); }
      else if (el.classList.contains("steps-count")) el.textContent = n + " / " + keys.length + " steps";
      else el.textContent = n + " of " + keys.length + " steps done" + (all ? ". Topic complete!" : "");
    });
    const overall = document.getElementById("topics-overall");
    if (overall) {
      const tops = [...document.querySelectorAll("#topic-checklist input[data-key]")];
      const n = tops.filter(b => b.checked).length;
      overall.textContent = n + " of " + tops.length + " topics done";
    }
  };
  stepBoxes.forEach(b => b.addEventListener("change", () => {
    store.set(b.dataset.key, b.checked ? "1" : null);
    paintSteps();
  }));
  paintSteps();
  window.addEventListener("storage", e => { if (e.key && e.key.startsWith("dsa:")) location.reload(); });

  // ---- back up / move progress ----
  const codeBox = document.getElementById("progress-code");
  if (codeBox) {
    const msg = document.getElementById("progress-msg");
    const collect = () => {
      const o = {};
      try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && k.startsWith("dsa:") && localStorage.getItem(k) === "1") o[k] = 1; } } catch (e) {}
      return o;
    };
    const countEl = document.getElementById("progress-count");
    if (countEl) countEl.textContent = Object.keys(collect()).length + " ticks saved in this browser";
    document.getElementById("progress-copy").addEventListener("click", () => {
      const code = "DSA1:" + btoa(Object.keys(collect()).sort().join("\n"));
      codeBox.value = code;
      const done = () => { msg.textContent = "Copied. Paste it somewhere safe, like a note or an email to yourself."; };
      try {
        navigator.clipboard.writeText(code).then(done, () => { codeBox.select(); msg.textContent = "Selected. Press Copy (⌘C / Ctrl+C) to copy it."; });
      } catch (e) { codeBox.select(); msg.textContent = "Selected. Press Copy (⌘C / Ctrl+C) to copy it."; }
    });
    document.getElementById("progress-load").addEventListener("click", () => {
      const raw = codeBox.value.trim();
      let keys;
      try {
        if (!raw.startsWith("DSA1:")) throw new Error();
        keys = atob(raw.slice(5)).split("\n").filter(k => /^dsa:[a-z]:[\w\-:]+$/.test(k));
      } catch (e) { msg.textContent = "That doesn't look like a progress code. It should start with DSA1:"; return; }
      let added = 0;
      keys.forEach(k => { if (store.get(k) !== "1") { store.set(k, "1"); added++; } });
      msg.textContent = "Loaded. Added " + added + " new tick" + (added === 1 ? "" : "s") + "; nothing was removed. Refreshing…";
      setTimeout(() => location.reload(), 1200);
    });
  }

  // ---- quiz ----
  const dataEl = document.getElementById("quiz-data");
  const quiz = document.getElementById("quiz");
  if (!dataEl || !quiz) return;
  const qs = JSON.parse(dataEl.textContent);
  const score = document.getElementById("score");
  const filters = document.getElementById("filters");
  let right = 0, done = 0, level = "all";
  const cards = [];
  const label = { easy: "Easy", medium: "Medium", hard: "Hard" };

  qs.forEach((q, i) => {
    const el = document.createElement("div");
    el.className = "q";
    el.dataset.level = q.lvl;
    el.innerHTML =
      '<div class="q-top"><span class="lvl ' + q.lvl + '">' + label[q.lvl] + '</span><span class="note">Question ' + (i + 1) + "</span></div>" +
      '<p class="q-text">' + inline(q.q) + "</p>" +
      (q.code ? "<pre><code>" + esc(q.code) + "</code></pre>" : "") +
      '<div class="opts"></div><p class="explain" hidden></p>';
    const opts = el.querySelector(".opts"), ex = el.querySelector(".explain");
    q.opts.forEach((o, j) => {
      const b = document.createElement("button");
      b.type = "button";
      b.id = "q" + i + "o" + j;
      b.innerHTML = inline(o);
      b.addEventListener("click", () => {
        if (el.dataset.answered) return;
        el.dataset.answered = "1";
        done++;
        [...opts.children].forEach(c => (c.disabled = true));
        if (j === q.a) { b.classList.add("right"); right++; ex.innerHTML = "<strong>Correct.</strong> " + inline(q.why); }
        else { b.classList.add("wrong"); opts.children[q.a].classList.add("right"); ex.innerHTML = "<strong>Not quite.</strong> " + inline(q.why); }
        ex.hidden = false;
        showScore();
      });
      opts.appendChild(b);
    });
    quiz.appendChild(el);
    cards.push(el);
  });

  function showScore() {
    if (!score) return;
    const visible = cards.filter(c => !c.hidden).length;
    score.textContent = done ? "Score: " + right + " / " + done + " answered (" + visible + " showing)" : visible + " questions";
  }
  if (filters) {
    const counts = { all: qs.length };
    qs.forEach(q => (counts[q.lvl] = (counts[q.lvl] || 0) + 1));
    ["all", "easy", "medium", "hard"].forEach(lv => {
      if (lv !== "all" && !counts[lv]) return;
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = (lv === "all" ? "All" : label[lv]) + " (" + counts[lv] + ")";
      b.setAttribute("aria-pressed", String(lv === "all"));
      b.addEventListener("click", () => {
        level = lv;
        filters.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
        cards.forEach(c => (c.hidden = !(lv === "all" || c.dataset.level === lv)));
        showScore();
      });
      filters.appendChild(b);
    });
  }
  const reset = document.getElementById("quiz-reset");
  if (reset) reset.addEventListener("click", () => {
    right = 0; done = 0;
    cards.forEach(c => {
      delete c.dataset.answered;
      c.querySelectorAll(".opts button").forEach(b => { b.disabled = false; b.classList.remove("right", "wrong"); });
      c.querySelector(".explain").hidden = true;
    });
    showScore();
  });
  showScore();
})();
