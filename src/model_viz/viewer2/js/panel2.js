// Shell: v2's panel. Composes the shared renderers (panel.js, part_panel.js) and appends v2's own
// pieces through their DOM hooks (design D38, D44, Appendix B). Holds no state.
window.ModelViz = window.ModelViz || {};

ModelViz.panel2 = (function () {
  const { el, calcLink } = ModelViz.panel.dom;
  const { plural } = ModelViz.structure;

  const PLACEHOLDER_TEXT = "Select a calc or a part to see its details and reach.";
  const UNSCOPED_NOTE = "These calcs have a scope that names no occurrence in this snapshot.";
  const NO_REACH = "none";

  function button(props, text, onClick) {
    const node = el("button", { ...props, text });
    node.type = "button";
    node.addEventListener("click", onClick);
    return node;
  }

  // D38 (3): the panel bar sits before the shared header, outside everything a dumper reads.
  function panelBar(handlers) {
    return el("div", { "data-role": "panel-bar" }, [button({ className: "panel-clear", "data-action": "clear-selection" }, "Clear", () => handlers.onClear())]);
  }

  // D38 (2), A9: one direction of the reach section. lists: [{partId, path, calcs}] from
  // reach.reachLists; the heading carries the direction's canvas colour, which is the key.
  function reachDirection(name, title, groups, onCalc) {
    const count = groups.reduce((n, group) => n + group.calcs.length, 0);
    const children = [el("h4", { className: `reach-heading reach-${name}`, text: `${title} (${count})` })];
    if (count === 0) {
      children.push(el("div", { className: "muted", text: NO_REACH }));
    }
    for (const group of groups) {
      const items = group.calcs.map((calc) => el("li", {}, [calcLink(calc, onCalc, {}, calc.name)]));
      children.push(el("div", { className: "reach-group", "data-part-path": group.path }, [el("h5", { text: group.path }), el("ul", {}, items)]));
    }
    return el("div", { "data-reach": name }, children);
  }

  // D38 (2): the reach section, Upstream then Downstream, each grouped by the owning part.
  function reachSection(lists, handlers) {
    return el("section", { "data-section": "reach" }, [
      el("h3", { text: "Reach" }),
      reachDirection("upstream", "Upstream", lists.upstream, handlers.onCalc),
      reachDirection("downstream", "Downstream", lists.downstream, handlers.onCalc),
    ]);
  }

  // The same markup part_panel.js makes for a part with children (part_panel.js:17-20), so one DOM
  // hook and one handler serve every collapsible part (D38 (1)).
  function toggleButton(occurrenceId, collapsed, handlers) {
    const props = { className: "part-toggle", "data-action": "toggle-part", "data-part-collapsed": String(collapsed) };
    return button(props, collapsed ? "Expand" : "Collapse", () => handlers.onTogglePart(occurrenceId));
  }

  function clearDataAttributes(panelElement) {
    delete panelElement.dataset.calcNodeId;
    delete panelElement.dataset.partOccurrenceId;
  }

  function showPlaceholder(panelElement) {
    clearDataAttributes(panelElement);
    panelElement.replaceChildren(el("p", { className: "placeholder", text: PLACEHOLDER_TEXT }));
  }

  // handlers: {onCalc(key), onPart(occurrenceId, attrNodeId), onTogglePart(occurrenceId), onClear()}
  function showCalcPanel(panelElement, model, key, handlers, lists) {
    ModelViz.panel.renderPanel(panelElement, model, key, handlers.onCalc);
    panelElement.querySelector("section[data-section=outputs]").after(reachSection(lists, handlers));
    panelElement.prepend(panelBar(handlers));
    panelElement.scrollTop = 0;
  }

  // part: the overlay tree's container; collapsed: whether it is closed (picks the button's word).
  function showPartPanel(panelElement, model, part, collapsed, handlers, lists) {
    if (part.occurrenceId === null) {
      showUnscopedPanel(panelElement, model, part, collapsed, handlers, lists);
      return;
    }
    ModelViz.partPanel.renderPart(panelElement, model, part.occurrenceId, collapsed, handlers);
    if (part.childCount === 0 && part.calcCount > 0) {
      panelElement.querySelector(".part-title").appendChild(toggleButton(part.occurrenceId, collapsed, handlers));
    }
    panelElement.querySelector("section[data-section=part-calcs]").after(reachSection(lists, handlers));
    panelElement.prepend(panelBar(handlers));
    panelElement.scrollTop = 0;
  }

  // D44: the part without an occurrence; partDetail would throw, so this renders its own panel.
  function showUnscopedPanel(panelElement, model, part, collapsed, handlers, lists) {
    const calcs = part.calcKeys.map((key) => model.byKey.get(key));
    const title = el("div", { className: "part-title" }, [el("h2", { "data-role": "part-name", text: part.label }), toggleButton(null, collapsed, handlers)]);
    const header = el("header", {}, [
      title,
      el("div", { "data-role": "part-path", className: "port", text: part.path }),
      el("p", { "data-role": "unscoped-note", className: "muted", text: UNSCOPED_NOTE }),
      el("div", { "data-role": "calc-count", className: "muted", text: plural(calcs.length, "calc", "calcs") }),
    ]);
    const items = calcs.map((calc) => el("li", {}, [calcLink(calc, handlers.onCalc, {}, calc.name)]));
    const calcsSection = el("section", { "data-section": "part-calcs" }, [el("h3", { text: `Calcs (${calcs.length})` }), el("ul", {}, items)]);
    clearDataAttributes(panelElement);
    panelElement.replaceChildren(panelBar(handlers), header, calcsSection, reachSection(lists, handlers));
    panelElement.dataset.partUnscoped = "";
    panelElement.scrollTop = 0;
  }

  return { PLACEHOLDER_TEXT, UNSCOPED_NOTE, showPlaceholder, showCalcPanel, showPartPanel, showUnscopedPanel };
})();
