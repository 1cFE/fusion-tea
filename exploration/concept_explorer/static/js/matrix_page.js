/**
 * matrix_page.js — the DOM + events half of the ontology matrix (B1).
 *
 * Fetches the three endpoints ONCE, joins them via matrix_data.joinConcepts(),
 * then renders the field as a <table>. All four interactions (filter, regroup,
 * sort, hover) mutate a small `viewState` and re-project the SAME rows[] via
 * matrix_data.project() — never a refetch (Required Invariant: one fetch).
 * Color comes from ontologyPalette / facet value colors; identity from
 * conceptLabel; caveats from caveatMarker — none re-derived here (FR-B1.11).
 *
 * Phases 1–2 built the static read-only matrix. Phase 3 adds click-to-filter
 * (via the shared filterState), the filter panel + active-filter bar, and the
 * group-by control (tree + the 8 dimensions, with an explicit unspecified band).
 */

"use strict";

(function () {
  // ---- View state (the single mutable model; every interaction re-projects) --
  var rows = []; // the joined served-set spine, fetched once
  var tree = null; // /api/taxonomy/tree, for groupBy="tree"
  var viewState = null;

  /** Create a DOM element with optional attributes and text (mirrors index_page.js). */
  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") node.className = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    if (text != null) node.textContent = text;
    return node;
  }

  /** Resolve a fetch Response to JSON, throwing loudly on a non-2xx status. */
  function okJson(resp) {
    if (!resp.ok) throw new Error("HTTP " + resp.status + " for " + resp.url);
    return resp.json();
  }

  /** The 8 column facets, resolved from the shared facetModel in column order. */
  function columnFacets() {
    var byKey = {};
    (window.facetModel || []).forEach(function (f) {
      byKey[f.key] = f;
    });
    return matrixData.COLUMN_FACET_KEYS.map(function (k) {
      return byKey[k];
    }).filter(Boolean);
  }

  /**
   * Pick a readable text class for a chip given its background hex. Computes
   * sRGB-weighted luminance and toggles a CSS class (so no color literal is
   * authored in JS — the single-color-authority invariant + grep guard).
   */
  function inkClassFor(bgHex) {
    var hex = String(bgHex).replace(/^#/, "");
    var m = /^([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex);
    if (!m) return "onto-chip--paper"; // unknown format → assume dark bg
    var r = parseInt(m[1], 16),
      g = parseInt(m[2], 16),
      b = parseInt(m[3], 16);
    var lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
    return lum < 0.55 ? "onto-chip--paper" : "onto-chip--ink";
  }

  /** A colored ontology chip: background from the palette, text class by contrast. */
  function chip(label, bgHex, extraClass, title) {
    var c = el("span", { class: "onto-chip " + inkClassFor(bgHex) + (extraClass ? " " + extraClass : "") }, label);
    c.style.backgroundColor = bgHex;
    if (title) c.title = title;
    return c;
  }

  /** Toggle one facet/value in the live filter and re-project (no refetch). */
  function toggleFilter(facetKey, value) {
    filterState.toggle(viewState.filter, facetKey, value);
    applyView();
  }

  /**
   * Build one dimension cell with the three honest states (design Appendix):
   *   recorded value in the palette → colored chip (click to filter)
   *   recorded value NOT in palette → grey chip + raw value + "unrecognized"
   *   absent (null/undefined)       → explicit "not recorded" chip (caveatMarker)
   * A cell is never blank (FR-B1.8).
   */
  function buildDimCell(row, facet) {
    var td = el("td", { class: "matrix-cell" });
    var v = row[facet.field];
    var hit = facet.values.find(function (o) {
      return o.value === v;
    });
    if (hit) {
      var c = chip(hit.label, hit.color, "onto-chip--clickable", facet.label + ": " + hit.label + " · click to filter");
      c.addEventListener("click", function () {
        toggleFilter(facet.key, hit.value);
      });
      td.appendChild(c);
    } else if (v != null) {
      td.appendChild(
        chip(String(v), ontologyPalette.na, "onto-chip--na", facet.label + ": " + String(v) + " (unrecognized value)")
      );
    } else {
      var cav = caveatMarker({ missing: facet.label });
      td.appendChild(chip("not recorded", ontologyPalette.na, "onto-chip--missing", cav.title));
    }
    return td;
  }

  /**
   * Identity cell: #code chip + canonical Name (Fuel), linking to the concept
   * page, plus the concept-level caveat marker (low-grounding asterisk /
   * archetype-fit None) via caveatMarker — the same honest marker the cards carry.
   */
  function buildIdentityCell(row) {
    var lbl = conceptLabel(row);
    var td = el("td", { class: "matrix-cell matrix-cell--identity" });
    var a = el("a", { class: "matrix-identity", href: "/concept/" + row.concept_id });
    a.appendChild(lbl.codeChip());
    a.appendChild(document.createTextNode(" " + lbl.name));
    td.appendChild(a);
    var cav = caveatMarker({ asterisk: row.asterisk_in_comparison, fitGrade: row.fit_grade }).element();
    if (cav) td.appendChild(cav);
    return td;
  }

  /** Sort indicator suffix for a column header (only on the active sort key). */
  function sortArrow(key) {
    if (viewState.sortKey !== key) return "";
    return viewState.sortDir === "desc" ? " ▾" : " ▴";
  }

  /** Set the sort key (toggling direction if already active) and re-project. */
  function setSort(key) {
    if (viewState.sortKey === key) {
      viewState.sortDir = viewState.sortDir === "asc" ? "desc" : "asc";
    } else {
      viewState.sortKey = key;
      viewState.sortDir = "asc";
    }
    applyView();
  }

  /** Sticky header row: identity column + the 8 dimension column labels, each click-to-sort. */
  function buildHead(facets) {
    var thead = el("thead");
    var tr = el("tr", { class: "matrix-headrow" });
    var idTh = el("th", { class: "matrix-head matrix-head--identity matrix-head--sortable", scope: "col" }, "Concept" + sortArrow("code"));
    idTh.title = "Sort by concept code";
    idTh.addEventListener("click", function () {
      setSort("code");
    });
    tr.appendChild(idTh);
    facets.forEach(function (f) {
      var th = el("th", { class: "matrix-head matrix-head--sortable", scope: "col" }, f.label + sortArrow(f.key));
      th.title = "Sort by " + f.label;
      th.addEventListener("click", function () {
        setSort(f.key);
      });
      tr.appendChild(th);
    });
    thead.appendChild(tr);
    return thead;
  }

  /**
   * Full-width band header row. Tree bands take the family color as a left
   * accent (threaded from the tree hierarchy); dimension bands take the value's
   * palette color; the unspecified / ungrouped bands are neutral.
   */
  function buildBandHeader(band, colspan, index) {
    var tr = el("tr", { class: "matrix-band" });
    tr.setAttribute("data-band", String(index));
    var th = el("th", { class: "matrix-band__cell", colspan: String(colspan), scope: "colgroup" });
    var railColor = null;
    if (band.kind === "tree" && band.family) railColor = ontologyPalette.family[band.family];
    else if (band.kind === "dim" && band.color) railColor = band.color;
    if (railColor) th.style.borderLeftColor = railColor;
    else th.classList.add("matrix-band__cell--neutral");
    var toggle = el("span", { class: "matrix-band__toggle", "aria-hidden": "true" }, "▾");
    th.appendChild(toggle);
    th.appendChild(el("span", { class: "matrix-band__label" }, band.label));
    th.appendChild(el("span", { class: "matrix-band__count" }, "(" + band.rows.length + ")"));
    th.addEventListener("click", function () {
      var collapsed = tr.classList.toggle("is-collapsed");
      toggle.textContent = collapsed ? "▸" : "▾";
      var hidden = document.querySelectorAll('.matrix-row[data-band="' + index + '"]');
      Array.prototype.forEach.call(hidden, function (r) {
        r.classList.toggle("matrix-row--hidden", collapsed);
      });
    });
    tr.appendChild(th);
    return tr;
  }

  /** Render the projected bands into the matrix <table>. */
  function render(bands) {
    var facets = columnFacets();
    var colspan = 1 + facets.length;
    var table = document.getElementById("matrix-table");
    table.innerHTML = "";
    table.appendChild(buildHead(facets));

    var tbody = el("tbody");
    bands.forEach(function (band, i) {
      tbody.appendChild(buildBandHeader(band, colspan, i));
      band.rows.forEach(function (row) {
        var tr = el("tr", { class: "matrix-row" });
        tr.setAttribute("data-band", String(i));
        tr.appendChild(buildIdentityCell(row));
        facets.forEach(function (f) {
          tr.appendChild(buildDimCell(row, f));
        });
        tbody.appendChild(tr);
      });
    });
    table.appendChild(tbody);
  }

  // ---- Controls bar: group-by select + filter-panel toggle + summary (once) --
  function buildControls() {
    var bar = document.getElementById("matrix-controls");
    bar.innerHTML = "";

    var gb = el("label", { class: "matrix-control" });
    gb.appendChild(el("span", { class: "matrix-control__label" }, "Group by"));
    var sel = el("select", { class: "matrix-control__select", id: "matrix-groupby" });
    matrixData.GROUP_OPTIONS.forEach(function (opt) {
      sel.appendChild(el("option", { value: opt.value }, opt.label));
    });
    sel.value = viewState.groupBy;
    sel.addEventListener("change", function () {
      viewState.groupBy = sel.value;
      applyView();
    });
    gb.appendChild(sel);
    bar.appendChild(gb);

    var sortGroup = el("label", { class: "matrix-control" });
    sortGroup.appendChild(el("span", { class: "matrix-control__label" }, "Sort"));
    var ssel = el("select", { class: "matrix-control__select", id: "matrix-sortby" });
    sortOptions().forEach(function (opt) {
      ssel.appendChild(el("option", { value: opt.value }, opt.label));
    });
    ssel.value = viewState.sortKey;
    ssel.addEventListener("change", function () {
      if (ssel.value === viewState.sortKey) return;
      viewState.sortKey = ssel.value;
      viewState.sortDir = "asc";
      applyView();
    });
    sortGroup.appendChild(ssel);
    var dirBtn = el("button", { class: "matrix-control__btn", id: "matrix-sortdir", type: "button", "aria-label": "Toggle sort direction" }, "▲");
    dirBtn.addEventListener("click", function () {
      viewState.sortDir = viewState.sortDir === "asc" ? "desc" : "asc";
      applyView();
    });
    sortGroup.appendChild(dirBtn);
    bar.appendChild(sortGroup);

    var ft = el("button", { class: "matrix-control__btn", id: "matrix-filters-toggle", type: "button" }, "Filters");
    ft.addEventListener("click", function () {
      var p = document.getElementById("matrix-filter-panel");
      var open = p.classList.toggle("is-open");
      ft.classList.toggle("is-active", open);
    });
    bar.appendChild(ft);

    bar.appendChild(el("span", { class: "matrix-controls__summary", id: "matrix-summary" }));
  }

  /** Sort keys offered by the control: code + name + the 8 dimension columns. */
  function sortOptions() {
    return [
      { value: "code", label: "Code" },
      { value: "name", label: "Name" },
    ].concat(
      columnFacets().map(function (f) {
        return { value: f.key, label: f.label };
      })
    );
  }

  /** Reflect viewState onto the (statically-built) group-by + sort controls. */
  function syncControls() {
    var gb = document.getElementById("matrix-groupby");
    if (gb) gb.value = viewState.groupBy;
    var sb = document.getElementById("matrix-sortby");
    if (sb) sb.value = viewState.sortKey;
    var db = document.getElementById("matrix-sortdir");
    if (db) db.textContent = viewState.sortDir === "desc" ? "▼" : "▲";
  }

  // ---- Filter panel: one toggle group per facet (all 10 facets) (once) -------
  function buildFilterPanel() {
    var panel = document.getElementById("matrix-filter-panel");
    panel.innerHTML = "";
    (window.facetModel || []).forEach(function (facet) {
      var group = el("div", { class: "filter-group" });
      group.appendChild(el("span", { class: "filter-group__label" }, facet.label));
      var wrap = el("div", { class: "filter-group__chips" });
      facet.values.forEach(function (o) {
        var c = chip(o.label, o.color, "onto-chip--toggle");
        c.setAttribute("data-facet", facet.key);
        c.setAttribute("data-value", String(o.value));
        c.addEventListener("click", function () {
          toggleFilter(facet.key, o.value);
        });
        wrap.appendChild(c);
      });
      group.appendChild(wrap);
      panel.appendChild(group);
    });
  }

  /** Reflect the live filterState selection onto the filter-panel chips. */
  function syncFilterPanel() {
    var chips = document.querySelectorAll("#matrix-filter-panel .onto-chip--toggle");
    Array.prototype.forEach.call(chips, function (c) {
      var fk = c.getAttribute("data-facet");
      var val = c.getAttribute("data-value");
      var sel = viewState.filter[fk];
      c.classList.toggle("onto-chip--selected", !!(sel && sel.has(val)));
    });
  }

  /** Rebuild the active-filter bar: a removable pill per selected value + Clear all. */
  function updateActiveFilters() {
    var bar = document.getElementById("matrix-active-filters");
    bar.innerHTML = "";
    var any = false;
    (window.facetModel || []).forEach(function (facet) {
      var sel = viewState.filter[facet.key];
      if (!sel || sel.size === 0) return;
      sel.forEach(function (val) {
        any = true;
        var o = facet.values.find(function (x) {
          return String(x.value) === String(val);
        });
        var pill = el("span", { class: "active-filter" });
        pill.appendChild(el("span", { class: "active-filter__label" }, facet.label + ": " + (o ? o.label : String(val))));
        var rm = el("button", { class: "active-filter__remove", type: "button", "aria-label": "Remove filter" }, "✕");
        rm.addEventListener("click", function () {
          toggleFilter(facet.key, val);
        });
        pill.appendChild(rm);
        bar.appendChild(pill);
      });
    });
    if (any) {
      var clear = el("button", { class: "matrix-clear-btn", type: "button" }, "Clear all");
      clear.addEventListener("click", function () {
        viewState.filter = filterState.create();
        applyView();
      });
      bar.appendChild(clear);
      bar.classList.add("is-active");
    } else {
      bar.classList.remove("is-active");
    }
  }

  /** Update the controls-bar summary line. */
  function updateSummary(bands) {
    var visible = bands.reduce(function (n, b) {
      return n + b.rows.length;
    }, 0);
    var opt = matrixData.GROUP_OPTIONS.find(function (o) {
      return o.value === viewState.groupBy;
    });
    var groupLabel = opt ? opt.label : viewState.groupBy;
    var count = visible === rows.length ? rows.length + " concepts" : visible + " of " + rows.length + " concepts";
    var summary = document.getElementById("matrix-summary");
    if (summary) summary.textContent = count + " · grouped by " + groupLabel + " · " + bands.length + " groups";
  }

  /** The single re-render entry point: project the current viewState, then paint. */
  function applyView() {
    var bands = matrixData.project(rows, viewState, tree);
    render(bands);
    updateSummary(bands);
    updateActiveFilters();
    syncFilterPanel();
    syncControls();
  }

  async function init() {
    var loadingEl = document.getElementById("loading-state");
    var contentEl = document.getElementById("matrix-content");
    var errorEl = document.getElementById("error-state");

    loadingEl.style.display = "";
    contentEl.style.display = "none";
    errorEl.style.display = "none";

    var manifest, registry;
    try {
      var payloads = await Promise.all([
        fetch("/api/manifest").then(okJson),
        fetch("/api/taxonomy/registry").then(okJson),
        fetch("/api/taxonomy/tree").then(okJson),
      ]);
      manifest = payloads[0];
      registry = payloads[1];
      tree = payloads[2];
    } catch (err) {
      console.error("[matrix] Failed to load matrix data:", err);
      loadingEl.style.display = "none";
      errorEl.style.display = "";
      return;
    }

    rows = matrixData.joinConcepts(manifest, registry);
    viewState = {
      groupBy: "tree",
      sortKey: "code",
      sortDir: "asc",
      filter: filterState.create(),
    };

    buildControls();
    buildFilterPanel();
    applyView();

    loadingEl.style.display = "none";
    contentEl.style.display = "";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
