"use strict";

/**
 * Tree view component for the decision tree.
 *
 * Renders a collapsible tree from /api/taxonomy/tree JSON. Branch nodes
 * expand/collapse on click; leaf concepts fire onConceptClick.
 *
 * Exported (module-scoped):
 *   renderTreeView(container, treeData, onConceptClick)
 *   highlightTreeConcept(conceptId)
 */
var TreeView = (function () {
  var _container = null;
  var _selectedId = null;

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /**
   * Count total concepts under a node (recursive).
   */
  function countConcepts(node) {
    var n = (node.concepts || []).length;
    if (node.children) {
      for (var i = 0; i < node.children.length; i++) {
        n += countConcepts(node.children[i]);
      }
    }
    return n;
  }

  /**
   * Build a branch node (expandable).
   */
  function buildBranch(node, onConceptClick, depth, onCtrlClick) {
    var wrapper = el("div", "tree-node");
    var count = countConcepts(node);

    // Header row
    var header = el("div", "tree-node__header");
    var toggle = el("span", "tree-node__toggle", "\u25B6"); // ▶
    var label = el("span", "tree-node__label", node.label || node.value);
    var countBadge = el("span", "tree-node__count", "(" + count + ")");

    header.appendChild(toggle);
    header.appendChild(label);
    header.appendChild(countBadge);
    wrapper.appendChild(header);

    // Children container
    var childrenEl = el("div", "tree-node__children");
    // Expand top level by default
    if (depth === 0) {
      childrenEl.className = "tree-node__children tree-node__children--open";
      toggle.className = "tree-node__toggle tree-node__toggle--open";
    }

    // Build child branches
    if (node.children) {
      for (var i = 0; i < node.children.length; i++) {
        childrenEl.appendChild(buildBranch(node.children[i], onConceptClick, depth + 1, onCtrlClick));
      }
    }

    // Build leaf concepts at this level
    if (node.concepts) {
      for (var j = 0; j < node.concepts.length; j++) {
        childrenEl.appendChild(buildLeaf(node.concepts[j], onConceptClick, onCtrlClick));
      }
    }

    wrapper.appendChild(childrenEl);

    // Toggle handler
    header.addEventListener("click", function () {
      var isOpen = childrenEl.classList.contains("tree-node__children--open");
      if (isOpen) {
        childrenEl.classList.remove("tree-node__children--open");
        toggle.classList.remove("tree-node__toggle--open");
      } else {
        childrenEl.classList.add("tree-node__children--open");
        toggle.classList.add("tree-node__toggle--open");
      }
    });

    return wrapper;
  }

  /**
   * Build a leaf concept node.
   */
  function buildLeaf(conceptId, onConceptClick, onCtrlClick) {
    var leaf = el("div", "tree-leaf");
    leaf.setAttribute("role", "button");
    leaf.setAttribute("tabindex", "0");
    leaf.setAttribute("data-concept-id", conceptId);

    var nameEl = el("span", "tree-leaf__name", conceptId);
    leaf.appendChild(nameEl);

    function select() {
      onConceptClick(conceptId);
    }
    leaf.addEventListener("click", function (e) {
      e.stopPropagation();
      if ((e.metaKey || e.ctrlKey) && onCtrlClick) {
        onCtrlClick(conceptId, e);
        return;
      }
      select();
    });
    leaf.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        select();
      }
    });

    return leaf;
  }

  /**
   * Update leaf labels after registry is loaded.
   */
  function updateLeafLabels(registry) {
    if (!_container) return;
    var leaves = _container.querySelectorAll(".tree-leaf");
    for (var i = 0; i < leaves.length; i++) {
      var id = leaves[i].getAttribute("data-concept-id");
      if (registry[id]) {
        var nameEl = leaves[i].querySelector(".tree-leaf__name");
        if (nameEl) nameEl.textContent = registry[id];
      }
    }
  }

  /**
   * Highlight a concept in the tree, expanding parents as needed.
   */
  function highlightTreeConcept(conceptId) {
    if (!_container) return;
    // Remove previous selection
    var prev = _container.querySelector(".tree-leaf--selected");
    if (prev) prev.classList.remove("tree-leaf--selected");
    _selectedId = conceptId;

    if (!conceptId) return;

    var leaf = _container.querySelector('[data-concept-id="' + conceptId + '"]');
    if (!leaf) return;

    leaf.classList.add("tree-leaf--selected");

    // Expand all parent tree-node__children
    var parent = leaf.parentElement;
    while (parent && parent !== _container) {
      if (parent.classList.contains("tree-node__children")) {
        parent.classList.add("tree-node__children--open");
        // Also update the toggle icon
        var header = parent.previousElementSibling;
        if (header) {
          var toggle = header.querySelector(".tree-node__toggle");
          if (toggle) toggle.classList.add("tree-node__toggle--open");
        }
      }
      parent = parent.parentElement;
    }

    // Scroll into view
    leaf.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  /**
   * Render the decision tree into a container element.
   */
  function renderTreeView(container, treeData, onConceptClick, onCtrlClick) {
    _container = container;
    container.innerHTML = "";

    var root = treeData.root;
    if (!root || !root.children) {
      container.textContent = "No tree data available.";
      return;
    }

    for (var i = 0; i < root.children.length; i++) {
      container.appendChild(buildBranch(root.children[i], onConceptClick, 0, onCtrlClick));
    }
  }

  /**
   * Toggle .tree-leaf--in-tray class on leaves based on selected IDs.
   */
  function updateTrayIndicators(selectedIds) {
    if (!_container) return;
    var idSet = {};
    for (var i = 0; i < selectedIds.length; i++) {
      idSet[selectedIds[i]] = true;
    }
    var leaves = _container.querySelectorAll(".tree-leaf");
    for (var j = 0; j < leaves.length; j++) {
      var id = leaves[j].getAttribute("data-concept-id");
      leaves[j].classList.toggle("tree-leaf--in-tray", !!idSet[id]);
    }
  }

  return {
    renderTreeView: renderTreeView,
    highlightTreeConcept: highlightTreeConcept,
    updateLeafLabels: updateLeafLabels,
    updateTrayIndicators: updateTrayIndicators
  };
})();
