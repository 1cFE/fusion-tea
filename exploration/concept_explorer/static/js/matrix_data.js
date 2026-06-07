/**
 * matrix_data.js — the pure, DOM-free data core of the ontology matrix (B1).
 *
 * The matrix is one in-memory table projected through a pure pipeline. On load
 * the page fetches three endpoints ONCE and left-joins them by `concept_id`:
 *
 *   /api/manifest          → the served set (the row spine; omit-list applied)
 *   /api/taxonomy/registry → the 7 ontology dimensions (live only here)
 *   /api/taxonomy/tree      → the family hierarchy (used by grouping, Phase 2)
 *
 * Every interaction (filter / regroup / sort) is then a pure transform over the
 * resulting `rows[]` — no refetch, ever. This module owns that join (and, from
 * Phase 2, `facetValuesFor` + `project`). It touches no DOM and reads no color,
 * name, or facet vocabulary of its own — those are Theme A's authorities,
 * consumed in matrix_page.js. Exposed as `window.matrixData`.
 */

"use strict";

(function () {
  // The 7 ontology dimensions that live ONLY on the registry (taxonomy_models.py
  // ConceptTaxonomy). `confinement_family` is intentionally absent: it is already
  // on the manifest spine and the two layers agree (registry is the identity
  // source). Each name matches a `facetModel` facet's `field` exactly, so a flat
  // row lets cell coloring, filtering, and grouping all read `row[facet.field]`.
  var REGISTRY_FIELDS = [
    "fuel",
    "magnet_type",
    "driver_type",
    "energy_capture",
    "blanket_config",
    "operation_mode",
    "repetition_rate",
  ];

  /**
   * Left-join the manifest (spine) with the registry's ontology dimensions.
   *
   * @param {Object} manifest  ConceptManifest payload ({concepts: [...]})
   * @param {Object} registry  ConceptRegistry payload ({concepts: [...]})
   * @returns {Object[]} one flat row per served concept: the full manifest entry
   *   plus the 7 registry ontology fields. A manifest concept missing from the
   *   registry gets `undefined` ontology fields (→ honest "not recorded" cells),
   *   never a crash — the manifest is the spine (Required Invariant: served-set
   *   spine). Suffix variants (17a/20a) carry through as distinct rows by id.
   */
  function joinConcepts(manifest, registry) {
    var regById = {};
    var regConcepts = (registry && registry.concepts) || [];
    for (var i = 0; i < regConcepts.length; i++) {
      regById[regConcepts[i].concept_id] = regConcepts[i];
    }

    var manifestConcepts = (manifest && manifest.concepts) || [];
    return manifestConcepts.map(function (entry) {
      var row = Object.assign({}, entry); // manifest entry is the spine
      var reg = regById[entry.concept_id];
      REGISTRY_FIELDS.forEach(function (field) {
        row[field] = reg ? reg[field] : undefined;
      });
      return row;
    });
  }

  // The 8 ontology dimensions that are matrix COLUMNS, in display order (design
  // Appendix). `family` is both the first column and the tree-grouping default;
  // the other 7 are the registry fields above. The two non-dimension facets
  // (fitGrade, hasCostModel) are filter-only — never columns (Decision 3). These
  // are facet KEYS into the shared `facetModel` (window.facetModel), so the
  // column set, labels, cell colors, and value order all derive from that one
  // authority — the matrix authors no facet list of its own.
  var COLUMN_FACET_KEYS = [
    "family",
    "fuel",
    "magnet",
    "driver",
    "capture",
    "blanket",
    "opMode",
    "repRate",
  ];

  /**
   * Extract `{facetKey: value}` from a row, for `filterState.matches`.
   *
   * Reads `row[facet.field]` for every facet in the shared `facetModel`.
   * `has_cost_model` is a boolean but its facet values are the strings
   * "true"/"false" — coerce so the membership test lines up. Absent ontology
   * fields stay `undefined` (match no selected chip → correctly filtered out
   * when that facet is constrained, ignored when it isn't).
   */
  function facetValuesFor(row) {
    var out = {};
    (window.facetModel || []).forEach(function (f) {
      var v = row[f.field];
      out[f.key] = f.key === "hasCostModel" ? String(v) : v;
    });
    return out;
  }

  /**
   * Compare two rows by concept code (the default within-band order).
   * Numeric-aware so "02" < "17a" < "17b" < "20"; non-numeric falls back to
   * string order. Suffix variants keep their letter order.
   */
  function byCode(a, b) {
    var ca = String(a.concept_id), cb = String(b.concept_id);
    var na = parseInt(ca, 10), nb = parseInt(cb, 10);
    if (!isNaN(na) && !isNaN(nb) && na !== nb) return na - nb;
    return ca < cb ? -1 : ca > cb ? 1 : 0;
  }

  /**
   * Group rows into flat, path-labeled bands by walking the decision tree
   * (Decision 2A). Every node carrying `concepts` becomes one band whose label
   * is its path from the top-level family (e.g. "Magnetic Fusion Energy ›
   * Stellarator › Modular"); bands are ordered by depth-first traversal.
   *
   * The band's `family` is the TOP-LEVEL TREE family (threaded down the walk),
   * NOT the member rows' flat `confinement_family` enum — the two can disagree
   * (e.g. Dense Plasma Focus is enum-MFE but lives under the tree's Non-Standard
   * branch), and the spec is explicit that group color must follow the rich
   * hierarchy, not the flat enum. The renderer maps this key through
   * `ontologyPalette.family`. Non-standard branches (Compact Toroid /
   * Electrostatic / Other Non-Standard) all fold to `NONSTANDARD`.
   *
   * No-silent-drop invariant: a served row in no tree leaf lands in an explicit
   * trailing `"— ungrouped"` band (pruning/orphan safety, FR-B1.5 sibling).
   */
  function familyKeyForTopLevel(node) {
    // The top-level tree nodes carry value MFE/IFE/MIF (direct family keys) or a
    // non-standard tag (Cmpt-Tor/Estatic/Other). Validate against the palette's
    // family keys (the authority) rather than hardcoding the family names here.
    var fam = (window.ontologyPalette && window.ontologyPalette.family) || {};
    var v = node.value;
    if (Object.prototype.hasOwnProperty.call(fam, v)) return v; // MFE / IFE / MIF
    return Object.prototype.hasOwnProperty.call(fam, "NONSTANDARD") ? "NONSTANDARD" : null;
  }

  function groupByTree(rows, tree) {
    var byId = {};
    rows.forEach(function (r) {
      byId[r.concept_id] = r;
    });
    var assigned = {};
    var bands = [];
    var root = tree && tree.root;

    function walk(node, pathLabels, familyKey) {
      var isRoot = node === root;
      var label = node.label || node.value || "";
      // The root's own label is not part of any band path.
      var here = isRoot ? pathLabels : pathLabels.concat([label]);
      var ids = node.concepts || [];
      if (ids.length) {
        var bandRows = [];
        ids.forEach(function (id) {
          if (byId[id]) {
            bandRows.push(byId[id]);
            assigned[id] = true;
          }
        });
        if (bandRows.length) {
          bands.push({
            kind: "tree",
            label: here.join(" › "),
            family: familyKey,
            rows: bandRows,
          });
        }
      }
      (node.children || []).forEach(function (ch) {
        // Family is established at the top level (root's children) and inherited.
        walk(ch, here, isRoot ? familyKeyForTopLevel(ch) : familyKey);
      });
    }

    if (root) walk(root, [], null);

    var orphans = rows.filter(function (r) {
      return !assigned[r.concept_id];
    });
    if (orphans.length) {
      bands.push({ kind: "ungrouped", label: "— ungrouped", family: null, rows: orphans });
    }
    return bands;
  }

  /**
   * Does a value fold into the "— unspecified" band when grouping by a
   * dimension? Covers `null`/`undefined`, every `N/A*` flavor (magnet "N/A",
   * blanket "N/A (no tritium)"/"N/A (non-power)", …), `TBD`, and `Unknown`
   * (FR-B1.5). Distinct from cell rendering, where these are honest recorded
   * chips — only as a *grouping key* do they collapse together.
   */
  function isUnspecifiedGroupValue(v) {
    if (v == null) return true;
    var s = String(v);
    return s === "TBD" || s === "Unknown" || s.indexOf("N/A") === 0;
  }

  /**
   * Group rows by a single ontology dimension's category values, ordered by the
   * facet's declared `values[]` (the palette/category order). Rows whose value
   * is unspecified collect into an explicit trailing `"— unspecified"` band
   * (FR-B1.5) — never silently dropped. Unexpected (non-enum) values get their
   * own bands after the declared ones. Band color is the value's palette color
   * (the renderer reads `band.color`).
   */
  function groupByDimension(rows, groupByKey) {
    var facet = (window.facetModel || []).find(function (f) {
      return f.key === groupByKey;
    });
    if (!facet) return [{ kind: "ungrouped", label: "— ungrouped", family: null, rows: rows.slice() }];

    var buckets = {};
    var unspecified = [];
    rows.forEach(function (row) {
      var v = row[facet.field];
      if (isUnspecifiedGroupValue(v)) {
        unspecified.push(row);
        return;
      }
      var k = String(v);
      (buckets[k] = buckets[k] || []).push(row);
    });

    var bands = [];
    facet.values.forEach(function (o) {
      var k = String(o.value);
      if (buckets[k] && buckets[k].length) {
        bands.push({ kind: "dim", facetKey: groupByKey, value: o.value, label: o.label, color: o.color, rows: buckets[k] });
        delete buckets[k];
      }
    });
    // Any recorded values not declared in the palette (unexpected enums).
    Object.keys(buckets).forEach(function (k) {
      bands.push({ kind: "dim", facetKey: groupByKey, value: k, label: k, color: null, rows: buckets[k] });
    });
    if (unspecified.length) {
      bands.push({ kind: "unspecified", label: "— unspecified", family: null, rows: unspecified });
    }
    return bands;
  }

  /**
   * Build the within-band comparator for `sortKey` / `sortDir`.
   *
   * `sortKey ∈ {"code", "name", <dimension facet key>}`. A dimension sort orders
   * by the facet's declared `values[]` order (the palette/category order, not
   * alphabetical), with unexpected values after the declared ones and
   * absent/`undefined` values LAST regardless of direction. Code is the stable
   * tiebreak. Sort is orthogonal to `groupBy` (applied per band), so it persists
   * across regroupings — the band set changes, the row order rule does not.
   */
  function makeComparator(sortKey, sortDir) {
    var dir = sortDir === "desc" ? -1 : 1;

    if (sortKey === "name") {
      // Sort by the canonical name via the identity authority (conceptLabel),
      // never a raw `.name` read — same value, and keeps the one naming source.
      return function (a, b) {
        var na = window.conceptLabel(a).name || "";
        var nb = window.conceptLabel(b).name || "";
        if (na !== nb) return dir * (na < nb ? -1 : 1);
        return byCode(a, b);
      };
    }

    var facet =
      sortKey && sortKey !== "code"
        ? (window.facetModel || []).find(function (f) {
            return f.key === sortKey;
          })
        : null;

    if (facet) {
      var order = {};
      facet.values.forEach(function (o, i) {
        order[String(o.value)] = i;
      });
      var ABSENT = facet.values.length + 1; // null/undefined sort last
      var UNEXPECTED = facet.values.length; // recorded-but-undeclared, just before absent
      var rank = function (v) {
        if (v == null) return ABSENT;
        var i = order[String(v)];
        return i != null ? i : UNEXPECTED;
      };
      return function (a, b) {
        var ra = rank(a[facet.field]),
          rb = rank(b[facet.field]);
        if (ra !== rb) return dir * (ra - rb);
        return byCode(a, b); // stable tiebreak (not direction-flipped)
      };
    }

    // Default: by concept code.
    return function (a, b) {
      return dir * byCode(a, b);
    };
  }

  /**
   * The pure projection pipeline: filter → group → sort-within-band.
   *
   * Every interaction is a pure recomputation over the SAME `rows[]` — no
   * refetch (Required Invariant: one fetch).
   *
   * @param {Object[]} rows       the joined rows (the served-set spine)
   * @param {Object} viewState    {groupBy, sortKey, sortDir, filter}
   * @param {Object} tree         the /api/taxonomy/tree payload (for groupBy="tree")
   * @returns {Object[]} bands: [{kind, label, family|color, rows}]
   */
  function project(rows, viewState, tree) {
    var filter = viewState.filter;
    var filtered = filter
      ? rows.filter(function (row) {
          return window.filterState.matches(filter, facetValuesFor(row));
        })
      : rows.slice();

    var bands =
      viewState.groupBy === "tree"
        ? groupByTree(filtered, tree)
        : groupByDimension(filtered, viewState.groupBy);

    var cmp = makeComparator(viewState.sortKey, viewState.sortDir);
    bands.forEach(function (b) {
      b.rows.sort(cmp);
    });
    return bands;
  }

  // Group-by options surfaced by the control (Phase 3 wires the <select>): the
  // tree (default) + the 8 dimension columns. The flat `family` facet is among
  // the 8, so "Family" appears as a flat re-group option distinct from the tree.
  var GROUP_OPTIONS = [{ value: "tree", label: "Family (tree)" }].concat(
    COLUMN_FACET_KEYS.map(function (key) {
      var f = (window.facetModel || []).find(function (x) {
        return x.key === key;
      });
      return { value: key, label: f ? f.label : key };
    })
  );

  window.matrixData = {
    REGISTRY_FIELDS: REGISTRY_FIELDS,
    COLUMN_FACET_KEYS: COLUMN_FACET_KEYS,
    GROUP_OPTIONS: GROUP_OPTIONS,
    joinConcepts: joinConcepts,
    facetValuesFor: facetValuesFor,
    project: project,
  };
})();
