"use strict";

/**
 * Selection Tray — persistent bottom bar for collecting concepts across
 * taxonomy views and launching comparison modes.
 *
 * Exported:
 *   SelectionTray.init(containerParent, registry)
 *   SelectionTray.add(concept)
 *   SelectionTray.remove(conceptId)
 *   SelectionTray.toggle(concept)
 *   SelectionTray.has(conceptId)
 *   SelectionTray.getIds()
 *   SelectionTray.showPopover(concept, anchorRect)
 *   SelectionTray.hidePopover()
 *   SelectionTray.onChange(callback)
 */
var SelectionTray = (function () {

  // ---------------------------------------------------------------------------
  // Tunable constants
  // ---------------------------------------------------------------------------

  var MIN_INTEGRATED = 1;
  var MAX_INTEGRATED = 3;
  var MIN_LANDSCAPE = 1;
  var MAX_LANDSCAPE = 6;

  // ---------------------------------------------------------------------------
  // Module state
  // ---------------------------------------------------------------------------

  var _selected = new Map();       // concept_id -> { concept_id, name, confinement_family }
  var _modeledIds = null;          // Set of analysis IDs with cost models
  var _registry = null;            // concept_id -> ConceptTaxonomy (for URL restore)
  var _changeListeners = [];       // Array<Function(selectedIds: string[])>
  var _trayEl = null;              // .selection-tray root element
  var _chipsEl = null;             // .selection-tray__chips container
  var _clearBtn = null;            // Clear All button
  var _integratedBtn = null;       // Integrated action button
  var _landscapeBtn = null;        // Landscape action button
  var _popoverEl = null;           // .selection-popover element (reused)
  var _popoverDismissHandler = null;
  var _popoverEscHandler = null;

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function familyKey(family) {
    if (!family) return "nonstandard";
    return family.toLowerCase().replace(/[^a-z]/g, "");
  }

  function familyLabel(family) {
    var labels = { MFE: "MFE", IFE: "IFE", MIF: "MIF", NONSTANDARD: "NST" };
    return labels[family] || family || "NST";
  }

  // ---------------------------------------------------------------------------
  // init
  // ---------------------------------------------------------------------------

  function init(containerParent, registry) {
    _registry = registry;

    // Build tray DOM
    _trayEl = el("div", "selection-tray");

    _clearBtn = el("button", "selection-tray__clear", "Clear All");
    _clearBtn.disabled = true;
    _clearBtn.addEventListener("click", function () {
      _selected.clear();
      _renderChips();
      _syncUrl();
      _notifyListeners();
    });

    _chipsEl = el("div", "selection-tray__chips");

    var actionsEl = el("div", "selection-tray__actions");
    _integratedBtn = el("button", "selection-tray__action", "Integrated (0)");
    _integratedBtn.setAttribute("data-mode", "integrated");
    _integratedBtn.disabled = true;
    _integratedBtn.addEventListener("click", function () {
      if (!_integratedBtn.disabled) {
        _navigateToCompare("integrated");
      }
    });

    _landscapeBtn = el("button", "selection-tray__action", "Landscape (0)");
    _landscapeBtn.setAttribute("data-mode", "landscape");
    _landscapeBtn.disabled = true;
    _landscapeBtn.addEventListener("click", function () {
      if (!_landscapeBtn.disabled) {
        _navigateToCompare("landscape");
      }
    });

    actionsEl.appendChild(_integratedBtn);
    actionsEl.appendChild(_landscapeBtn);

    _trayEl.appendChild(_clearBtn);
    _trayEl.appendChild(_chipsEl);
    _trayEl.appendChild(actionsEl);

    containerParent.appendChild(_trayEl);

    // Render initial empty state
    _renderChips();

    // Restore from URL
    _restoreFromUrl();
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  function add(concept) {
    if (!concept || !concept.concept_id) return;
    _selected.set(concept.concept_id, {
      concept_id: concept.concept_id,
      name: concept.name,
      confinement_family: concept.confinement_family
    });
    _renderChips();
    _syncUrl();
    _notifyListeners();
  }

  function remove(conceptId) {
    if (!_selected.has(conceptId)) return;
    _selected.delete(conceptId);
    _renderChips();
    _syncUrl();
    _notifyListeners();
  }

  function toggle(concept) {
    if (!concept || !concept.concept_id) return "removed";
    if (_selected.has(concept.concept_id)) {
      remove(concept.concept_id);
      return "removed";
    }
    return "pending";
  }

  function has(conceptId) {
    return _selected.has(conceptId);
  }

  function getIds() {
    return Array.from(_selected.keys());
  }

  function onChange(callback) {
    _changeListeners.push(callback);
  }

  // ---------------------------------------------------------------------------
  // Popover
  // ---------------------------------------------------------------------------

  function showPopover(concept, anchorRect) {
    hidePopover();

    if (!_popoverEl) {
      _popoverEl = el("div", "selection-popover");
      document.body.appendChild(_popoverEl);
    }

    var count = _selected.size;
    var maxDisplay = MAX_LANDSCAPE; // show against the larger limit

    // Build popover content
    _popoverEl.innerHTML = "";

    var header = el("div", "selection-popover__header", "Add to comparison?");
    _popoverEl.appendChild(header);

    var nameRow = el("div", "selection-popover__name");
    var badge = el("span", "badge badge-" + familyKey(concept.confinement_family),
      familyLabel(concept.confinement_family));
    nameRow.appendChild(badge);
    nameRow.appendChild(document.createTextNode(" " + concept.name));
    _popoverEl.appendChild(nameRow);

    // FR-14: cost model info line (only shown when absent)
    if (!_modeledIds || !_modeledIds.has(concept.concept_id)) {
      var info = el("div", "selection-popover__info", "No cost model \u2014 Categorical view only");
      _popoverEl.appendChild(info);
    }

    var countLine = el("div", "selection-popover__count",
      count + " of " + maxDisplay + " selected");
    _popoverEl.appendChild(countLine);

    var confirmBtn = el("button", "selection-popover__confirm", "Add");
    confirmBtn.addEventListener("click", function () {
      add(concept);
      hidePopover();
    });
    _popoverEl.appendChild(confirmBtn);

    // Position: fixed, viewport-aware
    _popoverEl.style.display = "";
    _popoverEl.style.visibility = "hidden"; // measure first

    // Force layout to get dimensions
    var popRect = _popoverEl.getBoundingClientRect();
    var popW = popRect.width || 240;
    var popH = popRect.height || 160;

    var left = anchorRect.left + (anchorRect.width || 0) + 8;
    var top = anchorRect.top;

    // Flip if overflow
    if (left + popW > window.innerWidth - 8) {
      left = anchorRect.left - popW - 8;
    }
    if (top + popH > window.innerHeight - 8) {
      top = window.innerHeight - popH - 8;
    }
    if (left < 8) left = 8;
    if (top < 8) top = 8;

    _popoverEl.style.left = left + "px";
    _popoverEl.style.top = top + "px";
    _popoverEl.style.visibility = "";

    // Dismiss listeners (deferred so the current click doesn't trigger them)
    setTimeout(function () {
      _popoverDismissHandler = function (e) {
        if (_popoverEl && !_popoverEl.contains(e.target)) {
          hidePopover();
        }
      };
      _popoverEscHandler = function (e) {
        if (e.key === "Escape") {
          hidePopover();
        }
      };
      document.addEventListener("click", _popoverDismissHandler, true);
      document.addEventListener("keydown", _popoverEscHandler, true);
    }, 0);
  }

  function hidePopover() {
    if (_popoverEl) {
      _popoverEl.style.display = "none";
      _popoverEl.innerHTML = "";
    }
    if (_popoverDismissHandler) {
      document.removeEventListener("click", _popoverDismissHandler, true);
      _popoverDismissHandler = null;
    }
    if (_popoverEscHandler) {
      document.removeEventListener("keydown", _popoverEscHandler, true);
      _popoverEscHandler = null;
    }
  }

  // ---------------------------------------------------------------------------
  // Internal: render chips
  // ---------------------------------------------------------------------------

  function _renderChips() {
    _chipsEl.innerHTML = "";

    if (_selected.size === 0) {
      var hint = el("span", "selection-tray__empty", "Ctrl+click concepts to compare");
      _chipsEl.appendChild(hint);
      _clearBtn.disabled = true;
    } else {
      _clearBtn.disabled = false;
      _selected.forEach(function (concept) {
        var chip = el("div", "selection-tray__chip");
        chip.setAttribute("data-concept-id", concept.concept_id);
        if (!_modeledIds || !_modeledIds.has(concept.concept_id)) {
          chip.classList.add("selection-tray__chip--no-model");
        }

        var badge = el("span", "selection-tray__chip-badge badge-" + familyKey(concept.confinement_family));
        var name = el("span", "selection-tray__chip-name", concept.name);
        var removeBtn = el("button", "selection-tray__chip-remove", "\u00d7");
        removeBtn.setAttribute("aria-label", "Remove " + concept.name);
        removeBtn.addEventListener("click", function () {
          remove(concept.concept_id);
        });

        chip.appendChild(badge);
        chip.appendChild(name);
        chip.appendChild(removeBtn);
        _chipsEl.appendChild(chip);
      });
    }

    _updateActionButtons();
  }

  // ---------------------------------------------------------------------------
  // Internal: action buttons
  // ---------------------------------------------------------------------------

  function _updateActionButtons() {
    var count = _selected.size;

    var intEnabled = count >= MIN_INTEGRATED && count <= MAX_INTEGRATED;
    _integratedBtn.disabled = !intEnabled;
    _integratedBtn.textContent = "Integrated (" + count + ")";

    var landEnabled = count >= MIN_LANDSCAPE && count <= MAX_LANDSCAPE;
    _landscapeBtn.disabled = !landEnabled;
    _landscapeBtn.textContent = "Landscape (" + count + ")";
  }

  function _navigateToCompare(mode) {
    var ids = getIds();
    if (ids.length === 0) return;
    window.location.href = "/compare?mode=" + mode + "&concepts=" + ids.join(",");
  }

  // ---------------------------------------------------------------------------
  // Internal: URL sync
  // ---------------------------------------------------------------------------

  function _syncUrl() {
    var params = new URLSearchParams(window.location.search);
    var ids = getIds();
    if (ids.length > 0) {
      params.set("selected", ids.join(","));
    } else {
      params.delete("selected");
    }
    var qs = params.toString();
    var url = window.location.pathname + (qs ? "?" + qs : "");
    history.replaceState(null, "", url);
  }

  function _restoreFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var raw = params.get("selected");
    if (!raw) return;

    var ids = raw.split(",");
    for (var i = 0; i < ids.length; i++) {
      var id = ids[i].trim();
      if (id && _registry && _registry[id]) {
        add(_registry[id]);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Internal: notify listeners
  // ---------------------------------------------------------------------------

  function _notifyListeners() {
    var ids = getIds();
    for (var i = 0; i < _changeListeners.length; i++) {
      _changeListeners[i](ids);
    }
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  return {
    init: init,
    add: add,
    remove: remove,
    toggle: toggle,
    has: has,
    getIds: getIds,
    showPopover: showPopover,
    hidePopover: hidePopover,
    onChange: onChange,
    setModeledIds: function(ids) { _modeledIds = ids; }
  };
})();
