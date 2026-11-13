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
