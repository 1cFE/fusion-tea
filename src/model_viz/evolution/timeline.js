// The evolution layer over the unmodified v2 viewer. It uses only what v2 exposes on
// window.modelVizApp (cy, model, loadText, toggleContainer, resetLayout, navigateTo) and the data
// build.py embeds. Every text goes in through textContent, as v2's panels do.
(async function () {
  const app = window.modelVizApp;
  const cy = app.cy;
  const HUE = { added: "#1baf7a", changed: "#eda100", moved: "#4a3aa7" };
  const FILL = { added: "#d8f5e9", changed: "#fdf0cf", moved: "#e4e0f7" };
  const METRICS = [
    ["calcs", "Calcs"],
    ["checks", "Checks (constraints)"],
    ["parts", "Parts"],
    ["attributes", "Attributes"],
    ["links", "Calc-to-calc links"],
    ["source_files", "Model source files"],
  ];
  const LIST_LIMIT = 40;

  const el = (tag, props, ...kids) => {
    const node = Object.assign(document.createElement(tag), props || {});
    for (const kid of kids) if (kid !== null && kid !== undefined) node.append(kid);
    return node;
  };
  const svg = (tag, attrs) => {
    const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
    return node;
  };

  const section = el("section", { className: "evo" });
  section.dataset.role = "evolution";
  const articleMode = document.body.classList.contains("writeup");
  (document.querySelector(".viewer-shell") || document.body).append(section);
  function refuse(message) {
    section.replaceChildren(el("div", { className: "evo-banner", textContent: message }));
    document.body.dataset.evoState = "error";
  }

  // build.py embeds gzip+base64 text; the browser's own DecompressionStream unpacks it.
  async function unpack(id) {
    const bytes = Uint8Array.from(atob(document.getElementById(id).textContent), (c) => c.charCodeAt(0));
    const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return new Response(stream).text();
  }
  if (typeof DecompressionStream === "undefined") {
    refuse("This page needs a browser with DecompressionStream (Chrome 80, Firefox 113, Safari 16.4, or newer).");
    return;
  }
  const data = JSON.parse(await unpack("evo-data"));
  const frames = data.frames;

  // ---- diff marks on the graph. A halo (underlay) and a fill: neither changes a box's size, and
  // neither touches the border colour v2 uses for reach and selection.
  const style = cy.style();
  if (articleMode) style.selector("node").style({ "font-family": getComputedStyle(document.body).fontFamily });
  for (const kind of Object.keys(HUE)) {
    style.selector(`node.evo-${kind}`).style({ "background-color": FILL[kind], "underlay-color": HUE[kind], "underlay-opacity": 0.55, "underlay-padding": 5 });
    style.selector(`node.evo-holds-${kind}`).style({ "underlay-color": HUE[kind], "underlay-opacity": 0.45, "underlay-padding": 6 });
  }
  style.update();

  let marks = new Map(); // calc key -> kind
  let holds = new Map(); // part path -> the strongest kind it hides while closed
  const STRENGTH = { moved: 1, changed: 2, added: 3 };
  function mark(node) {
    if (node.data("kind") === "calc" && marks.has(node.id())) node.addClass("evo-" + marks.get(node.id()));
    else if (node.data("kind") === "part" && node.data("collapsed") && holds.has(node.data("path"))) node.addClass("evo-holds-" + holds.get(node.data("path")));
  }
  // v2 removes and re-adds every element on each redraw, so marks are applied per add.
  cy.on("add", "node", (evt) => mark(evt.target));

  const ancestorPaths = (partPath) => partPath.split("/").map((_, i, all) => all.slice(0, i + 1).join("/"));
  function setMarks(frame) {
    marks = new Map();
    holds = new Map();
    if (frame.kind !== "goal") return;
    const groups = [["moved", frame.calcs.moved], ["changed", frame.calcs.changed.concat(frame.calcs.impl_only)], ["added", frame.calcs.added]];
    for (const [kind, rows] of groups)
      for (const row of rows) {
        marks.set(app.model.keyByNodeId.get(row.node_id), kind);
        for (const path of ancestorPaths(row.part)) if (!holds.has(path) || STRENGTH[kind] > STRENGTH[holds.get(path)]) holds.set(path, kind);
      }
  }

  // Open a set of parts with one layout run. v2 lays out on every toggle; the layout call is
  // stubbed while the toggles run, then v2's own resetLayout lays out and fits once.
  function openParts(wanted) {
    let opened = 0;
    cy.layout = () => ({ run() {}, stop() {} });
    try {
      for (let pass = 0; pass < 16; pass++) {
        const ids = cy.nodes("[kind='part']").filter((n) => n.data("collapsed") && wanted.has(n.data("path"))).map((n) => n.id());
        if (ids.length === 0) break;
        for (const id of ids) app.toggleContainer(id);
        opened += ids.length;
      }
    } finally {
      delete cy.layout;
    }
    if (opened > 0) app.resetLayout();
  }
  const openPathsNow = () => cy.nodes("[kind='part']").filter((n) => !n.data("collapsed") && !n.data("leaf")).map((n) => n.data("path"));

  // ---- the section under the graph
  const prev = el("button", { type: "button", textContent: "◀", title: "Previous goal (left arrow)" });
  const next = el("button", { type: "button", textContent: "▶", title: "Next goal (right arrow)" });
  const slider = el("input", { type: "range", min: 0, max: frames.length - 1, step: 1, value: 0 });
  slider.setAttribute("aria-label", "Frame");
  const position = el("span", { className: "evo-pos" });
  const jump = el("select");
  jump.setAttribute("aria-label", "Jump to goal");
  frames.forEach((f, i) => jump.append(el("option", { value: String(i), textContent: `${i + 1}. ${f.title}` })));
  const reveal = el("input", { type: "checkbox" });
  const busy = el("span", { className: "evo-busy" });
  const expand = el("button", { type: "button", textContent: "Expand viewer", title: "The graph fills the window; this bar stays so you can keep stepping (Esc to go back)" });
  const fullscreen = el("button", { type: "button", textContent: "Full screen" });
  const brief = el("span", { className: "evo-brief" }); // one line of what the goal changed, shown only while expanded
  for (const [node, role] of [[prev, "evo-prev"], [next, "evo-next"], [slider, "evo-slider"], [jump, "evo-jump"], [reveal, "evo-reveal"], [position, "evo-position"], [expand, "evo-expand"], [fullscreen, "evo-fullscreen"], [brief, "evo-brief"]]) node.dataset.role = role;
  const nav = el("div", { className: "evo-nav" }, prev, slider, next, position, jump, el("label", null, reveal, "Open changed parts"), busy, brief);
  const actions = el("div", { className: "evo-actions" }, expand, fullscreen);
  document.querySelector(".toolbar").before(actions);
  const swatch = (kind, text) => el("span", null, el("span", { className: "evo-swatch", style: `background:${HUE[kind]}` }), text);
  const legend = el("div", { className: "evo-legend" }, swatch("added", "new calc"), swatch("changed", "changed calc"), swatch("moved", "moved calc"), el("span", null, articleMode ? "Closed parts show the change color of their hidden calculations." : "A closed part wears the halo of the calcs it hides."));
  const tiles = el("div", { className: "evo-tiles" });
  const summary = el("div");
  const changes = el("div");
  summary.dataset.role = "evo-summary";
  changes.dataset.role = "evo-changes";
  section.append(nav, legend, tiles, el("div", { className: "evo-cols" }, summary, changes));
  // The page's name leads v2's toolbar, added the way export.py adds its note: appended, v2 untouched.
  const heading = el("strong", { className: "evo-title", textContent: data.title });
  heading.dataset.role = "evo-title";
  document.querySelector(".toolbar").prepend(heading);

  function sparkline(key, label, index) {
    const W = 200, H = 40, PAD = 5;
    const values = frames.map((f) => f.metrics[key]);
    const max = Math.max(...values), min = Math.min(...values);
    const x = (i) => PAD + (i * (W - 2 * PAD)) / Math.max(1, values.length - 1);
    const y = (v) => H - PAD - ((v - min) * (H - 2 * PAD)) / Math.max(1, max - min);
    // A step line: a count holds until the next goal changes it.
    const path = (upTo) => values.slice(0, upTo + 1).map((v, i) => (i === 0 ? `M${x(0)},${y(v)}` : `H${x(i)}V${y(v)}`)).join("");
    const chart = svg("svg", { class: "evo-spark", viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: "none", role: "img" });
    chart.setAttribute("aria-label", `${label} across ${values.length} frames, from ${values[0]} to ${values[values.length - 1]}`);
    const hover = svg("line", { class: "evo-hover", y1: 0, y2: H, visibility: "hidden" });
    chart.append(svg("path", { class: "evo-line-all", d: path(values.length - 1) }), svg("path", { class: "evo-line-now", d: path(index) }), hover, svg("circle", { class: "evo-dot", cx: x(index), cy: y(values[index]), r: 4 }));
    const nearest = (evt) => {
      const box = chart.getBoundingClientRect();
      return Math.max(0, Math.min(values.length - 1, Math.round((((evt.clientX - box.left) / box.width) * W - PAD) / ((W - 2 * PAD) / Math.max(1, values.length - 1)))));
    };
    return { chart, hover, nearest, x, values };
  }

  function renderTiles(index) {
    tiles.replaceChildren();
    for (const [key, label] of METRICS) {
      const value = frames[index].metrics[key];
      const delta = index === 0 ? null : value - frames[index - 1].metrics[key];
      // Growth is neither good nor bad here, so the delta stays in neutral ink.
      const deltaText = delta === null ? "starting point" : delta === 0 ? "no change from previous goal" : `${delta > 0 ? "+" : "−"}${Math.abs(delta).toLocaleString()} from previous goal`;
      const spark = sparkline(key, label, index);
      const tip = el("div", { className: "evo-tip", hidden: true });
      const tile = el("div", { className: "evo-tile" }, el("div", { className: "evo-label", textContent: label }), el("div", { className: "evo-value", textContent: value.toLocaleString() }), el("div", { className: "evo-delta", textContent: deltaText }), spark.chart, tip);
      tile.dataset.metric = key;
      spark.chart.addEventListener("mousemove", (evt) => {
        const i = spark.nearest(evt);
        spark.hover.setAttribute("x1", spark.x(i));
        spark.hover.setAttribute("x2", spark.x(i));
        spark.hover.setAttribute("visibility", "visible");
        tip.textContent = `${frames[i].title}: ${spark.values[i].toLocaleString()}`;
        tip.hidden = false;
        const box = spark.chart.getBoundingClientRect(), host = tile.getBoundingClientRect();
        tip.style.left = `${Math.max(70, Math.min(host.width - 70, box.left - host.left + (spark.x(i) / 200) * box.width))}px`;
        tip.style.top = `${box.top - host.top - 4}px`;
      });
      spark.chart.addEventListener("mouseleave", () => {
        spark.hover.setAttribute("visibility", "hidden");
        tip.hidden = true;
      });
      spark.chart.addEventListener("click", (evt) => show(spark.nearest(evt)));
      tiles.append(tile);
    }
  }

  function codeBlock(title, text, isDiff, path) {
    const pre = el("pre");
    if (!isDiff) pre.textContent = text;
    else
      for (const line of text.split("\n")) {
        const cls = line.startsWith("@@") ? "evo-hunk" : line.startsWith("+") ? "evo-plus" : line.startsWith("-") ? "evo-minus" : "";
        pre.append(el("span", { className: cls, textContent: line + (cls ? "" : "\n") }));
      }
    return el("details", null, el("summary", { textContent: title }), path ? el("span", { className: "evo-src", textContent: path }) : null, pre);
  }

  function calcItem(row, note) {
    const button = el("button", { className: "evo-calc", type: "button", textContent: row.name });
    button.addEventListener("click", () => {
      app.navigateTo(app.model.keyByNodeId.get(row.node_id));
      document.querySelector(".workspace").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    const item = el("li", null, button, el("span", { className: "evo-where", textContent: `  in ${row.part}` + (row.def ? ` · ${row.def}` : "") + (note ? ` · ${note}` : "") }));
    if (row.handwritten) item.append(el("span", { className: "evo-tag", title: "The executable body is handwritten Python. The snapshot does not carry it; it is read from the same git commit.", textContent: "handwritten body" }));
    if (row.inputs) item.append(el("div", { className: "evo-where", textContent: [row.inputs.added.length ? `inputs added: ${row.inputs.added.join(", ")}` : "", row.inputs.removed.length ? `inputs removed: ${row.inputs.removed.join(", ")}` : ""].filter(Boolean).join(" · ") }));
    if (row.rewired) {
      const shown = row.rewired.slice(0, 6).map((r) => el("div", { className: "evo-where evo-rewired", textContent: `${r.input}: ${r.before} → ${r.after}` }));
      if (row.rewired.length > 6) shown.push(el("div", { className: "evo-where", textContent: `and ${row.rewired.length - 6} more rewired inputs` }));
      item.append(...shown);
    }
    if (row.formula) item.append(codeBlock("Formula: before and after", row.formula.before.map((l) => "- " + l).concat(row.formula.after.map((l) => "+ " + l)).join("\n"), true, null));
    if (row.impl && row.impl.diff) item.append(codeBlock("Python body: what changed", row.impl.diff, true, row.impl.path));
    if (row.impl && row.impl.text) item.append(codeBlock(`Python body (${row.impl.lines} lines)`, data.impls[row.impl.text], false, row.impl.path));
    return item;
  }

  function group(title, items) {
    if (items.length === 0) return [];
    const shown = items.slice(0, LIST_LIMIT);
    if (items.length > LIST_LIMIT) shown.push(el("li", { className: "evo-more", textContent: `and ${items.length - LIST_LIMIT} more` }));
    return [el(articleMode ? "h4" : "h2", { textContent: `${title} (${items.length})` }), el("ul", null, ...shown)];
  }
  const mono = (text, note) => el("li", null, el("span", { className: "evo-mono", textContent: text }), note ? el("span", { className: "evo-where", textContent: "  " + note }) : null);

  const GRADE = { "OWNER-VERBATIM": "the owner's words", OWNER: "owner-stated", AGENT: "agent-worded" };
  function renderSummary(frame) {
    const meta = frame.kind === "baseline" ? `starting point · model ${frame.after} · fingerprint ${frame.fingerprint}` : `goal ${frame.slug} · ${frame.closed ? "closed " + frame.closed : "not formally closed"} · model ${frame.before} → ${frame.after}` + (frame.work_items && frame.work_items.length ? ` · ${frame.work_items.join(", ")}` : "");
    const kids = [el(articleMode ? "h3" : "h1", { textContent: frame.title }), el("div", { className: "evo-meta", textContent: meta })];
    if (frame.question) {
      const grade = frame.question_grade_detail || GRADE[frame.question_grade] || "grade not recorded";
      kids.push(el(articleMode ? "h4" : "h2", null, "Question ", el("span", { className: "evo-grade", textContent: `(${grade})` })), el("blockquote", { textContent: frame.question }), el("span", { className: "evo-src", textContent: frame.question_source }));
    }
    kids.push(el(articleMode ? "h4" : "h2", null, frame.kind === "baseline" ? "Where the goals started" : "Result ", frame.kind === "baseline" ? null : el("span", { className: "evo-grade", textContent: "(condensed by an agent from the source below)" })), el("p", { textContent: frame.result }), el("span", { className: "evo-src", textContent: frame.result_source }));
    summary.replaceChildren(...kids);
  }

  function renderChanges(frame) {
    if (frame.kind === "baseline") {
      changes.replaceChildren(el(articleMode ? "h4" : "h2", { textContent: "Changes" }), el("p", { className: "evo-none", textContent: "This is the starting model. Step forward to see what each goal changed." }));
      return;
    }
    const c = frame.calcs, k = frame.checks, a = frame.attrs;
    const kids = [
      ...group("New calcs", c.added.map((r) => calcItem(r))),
      ...group("Changed calcs", c.changed.map((r) => calcItem(r))),
      ...group("Python body changed, model record unchanged", c.impl_only.map((r) => calcItem(r))),
      ...group("Moved calcs", c.moved.map((r) => calcItem(r, `from ${r.from}`))),
      ...group("Removed calcs", c.removed.map((r) => mono(r.name, r.def))),
      ...group("New checks", k.added.map((r) => mono(r.name, r.def))),
      ...group("Changed checks", k.changed.map((r) => mono(r))),
      ...group("Removed checks", k.removed.map((r) => mono(r))),
      ...group("New parts", frame.parts.added.map((p) => mono(p))),
      ...group("Removed parts", frame.parts.removed.map((p) => mono(p))),
      ...group("Documentation changed only", c.doc_only.map((r) => calcItem(r))),
      ...group("Recorded values changed", a.values_changed.map((v) => mono(`${v.path}: ${JSON.stringify(v.before)} → ${JSON.stringify(v.after)}`))),
    ];
    if (a.added || a.removed) kids.push(el(articleMode ? "h4" : "h2", { textContent: "Attributes" }), el("p", { textContent: `${a.added.toLocaleString()} added (${a.added_with_value.toLocaleString()} with a recorded value), ${a.removed.toLocaleString()} removed.` }));
    if (kids.length === 0) kids.push(el(articleMode ? "h4" : "h2", { textContent: "Changes" }), el("p", { className: "evo-none", textContent: "The snapshot changed only in text the viewer does not compare (for example source citations)." }));
    changes.replaceChildren(...kids);
  }

  // ---- expanded view: the graph takes the window, the stepping bar stays along the bottom, and
  // v2's side panel gives its width back while nothing is selected. Classes sit on <html> so the
  // stylesheet can size html and body together.
  const root = document.documentElement;
  const refit = () => {
    cy.resize();
    if (app.model) app.fit();
  };
  function setExpanded(on) {
    root.classList.toggle("evo-expanded", on);
    expand.textContent = on ? "Collapse viewer" : "Expand viewer";
    expand.setAttribute("aria-pressed", String(on));
    if (on) window.scrollTo(0, 0);
    refit();
  }
  expand.addEventListener("click", () => setExpanded(!root.classList.contains("evo-expanded")));
  fullscreen.addEventListener("click", async () => {
    if (document.fullscreenElement) return document.exitFullscreen();
    setExpanded(true);
    try {
      await root.requestFullscreen();
    } catch (err) {
      // Refused (an embedding page can forbid it): the full-window view is already showing.
    }
  });
  document.addEventListener("fullscreenchange", () => {
    fullscreen.textContent = document.fullscreenElement ? "Exit full screen" : "Full screen";
    refit();
  });
  const panelElement = document.querySelector("[data-role=panel]");
  const syncPanel = () => {
    const wasEmpty = root.classList.contains("evo-panel-empty");
    const isEmpty = panelElement.querySelector(":scope > p.placeholder") !== null;
    root.classList.toggle("evo-panel-empty", isEmpty);
    if (isEmpty !== wasEmpty) cy.resize(); // the pane's width changed; keep the viewport
  };
  new MutationObserver(syncPanel).observe(panelElement, { childList: true });
  syncPanel();

  function briefOf(frame) {
    if (frame.kind !== "goal") return "starting model";
    const c = frame.calcs;
    const parts = [[c.added.length, "new"], [c.changed.length + c.impl_only.length, "changed"], [c.moved.length, "moved"], [c.removed.length, "removed"]].filter(([n]) => n > 0).map(([n, word]) => `${n} ${word}`);
    const calcs = parts.length ? `calcs: ${parts.join(", ")}` : "no calc changes";
    const extra = [[frame.checks.added.length, "new checks"], [frame.parts.added.length, "new parts"], [frame.attrs.values_changed.length, "values changed"]].filter(([n]) => n > 0).map(([n, word]) => `${n} ${word}`);
    return [calcs, ...extra].join(" · ");
  }

  // ---- stepping
  const cache = new Map(); // the last few unpacked snapshots; each is up to 6 MB of text
  let current = -1;
  let ticket = 0;
  async function show(index) {
    index = Math.max(0, Math.min(frames.length - 1, index));
    if (index === current) return;
    const mine = ++ticket;
    document.body.dataset.evoState = "loading";
    busy.textContent = "loading…";
    const frame = frames[index];
    if (!cache.has(frame.after)) {
      cache.set(frame.after, await unpack("evo-snap-" + frame.after));
      if (cache.size > 4) cache.delete(cache.keys().next().value);
    }
    if (mine !== ticket) return; // a later step overtook this one
    const carried = current === -1 ? [] : openPathsNow();
    marks = new Map();
    holds = new Map();
    app.loadText(cache.get(frame.after));
    if (document.body.dataset.loadState !== "ready") {
      refuse(`The viewer refused the snapshot for ${frame.title} (${frame.after}). Its message is in the banner above the graph.`);
      return;
    }
    const firstLoad = current === -1;
    current = index;
    setMarks(frame);
    cy.nodes().forEach(mark);
    const wanted = new Set(carried);
    if (reveal.checked) for (const path of holds.keys()) wanted.add(path);
    openParts(wanted);

    slider.value = String(index);
    jump.value = String(index);
    prev.disabled = index === 0;
    next.disabled = index === frames.length - 1;
    position.textContent = `${index + 1} / ${frames.length}`;
    // In the write-up the tab keeps the article's title; the standalone viewer names the frame.
    if (!articleMode) document.title = `${frame.title} · ${data.title}`;
    renderTiles(index);
    renderSummary(frame);
    renderChanges(frame);
    brief.textContent = briefOf(frame);
    busy.textContent = "";
    if (!articleMode || !firstLoad || frameOfHash() !== -1) history.replaceState(null, "", articleMode ? "#frame-" + (index + 1) : "#" + (frame.slug || "start"));
    document.body.dataset.evoFrame = String(index);
    document.body.dataset.evoState = "ready";
  }

  prev.addEventListener("click", () => show(current - 1));
  next.addEventListener("click", () => show(current + 1));
  slider.addEventListener("input", () => show(Number(slider.value)));
  jump.addEventListener("change", () => show(Number(jump.value)));
  reveal.addEventListener("change", () => {
    if (reveal.checked) openParts(new Set(holds.keys()));
  });
  document.addEventListener("keydown", (evt) => {
    // Arrow keys already mean something in a text box, the slider and a select; a focused checkbox or button is fine.
    const t = evt.target;
    const ownsArrows = t.tagName === "TEXTAREA" || t.tagName === "SELECT" || (t.tagName === "INPUT" && !/^(checkbox|button)$/.test(t.type));
    if (evt.altKey || evt.ctrlKey || evt.metaKey || ownsArrows) return;
    // In full screen the browser takes Esc for itself; this is the full-window case.
    if (evt.key === "Escape" && root.classList.contains("evo-expanded") && !document.fullscreenElement) setExpanded(false);
    if (evt.key === "ArrowLeft") show(current - 1);
    else if (evt.key === "ArrowRight") show(current + 1);
  });

  window.modelEvolution = { frames, show, get index() { return current; } };
  const frameOfHash = () => /^#frame-\d+$/.test(location.hash) ? Number(location.hash.slice(7)) - 1 : frames.findIndex((f) => (f.slug || "start") === decodeURIComponent(location.hash.slice(1)));
  if (articleMode) {
    document.addEventListener("click", async (event) => {
      const link = event.target.closest("a[data-frame]");
      if (!link) return;
      event.preventDefault();
      await show(Number(link.dataset.frame));
      document.getElementById("evolution-viewer").scrollIntoView({behavior: "instant", block: "start"});
    });
    const openTarget = () => {
      const target = document.getElementById(location.hash.slice(1));
      if (target?.closest("details")) target.closest("details").open = true;
    };
    addEventListener("hashchange", openTarget);
    openTarget();
  }
  // A link to another #goal does not reload an open page. show() writes the hash with replaceState,
  // which fires no hashchange, so this only ever answers a link or a typed address.
  window.addEventListener("hashchange", () => {
    if (frameOfHash() !== -1) show(frameOfHash());
  });
  await show(Math.max(0, frameOfHash()));
})();
