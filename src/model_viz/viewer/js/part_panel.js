// Shell: the part panel. Renders one part's partDetail with textContent only; holds no state.
window.ModelViz = window.ModelViz || {};

ModelViz.partPanel = (function () {
  const { el, warning, section, displayValue, calcLink } = ModelViz.panel.dom;
  const { partDetail, plural } = ModelViz.structure;

  function button(props, text, onClick) {
    const node = el("button", { ...props, text });
    node.type = "button";
    node.addEventListener("click", onClick);
    return node;
  }

  function header(detail, collapsed, handlers) {
    const title = el("div", { className: "part-title" }, [el("h2", { "data-role": "part-name", text: detail.name })]);
    if (detail.childCount > 0) {
      const props = { className: "part-toggle", "data-action": "toggle-part", "data-part-collapsed": String(collapsed) };
      title.appendChild(button(props, collapsed ? "Expand" : "Collapse", () => handlers.onTogglePart(detail.occurrenceId)));
    }
    const type = detail.type;
    const children = [
      title,
      el("div", { "data-role": "part-path", className: "port", text: detail.path }),
      el("div", { "data-role": "type-name", "data-type-recorded": String(type.name !== null), text: type.name === null ? "type not recorded" : type.name }),
    ];
    if (type.name === null) children.push(el("div", { "data-role": "type-reason", className: "muted", text: type.reason }));
    children.push(el("div", { "data-role": "calc-count", className: "muted", text: plural(detail.calcs.length, "calc", "calcs") }));
    return el("header", {}, children);
  }

  function calcsSection(detail, handlers) {
    if (detail.calcs.length === 0) return section("part-calcs", "Calcs (0)", [el("div", { className: "muted", text: "this part owns no calcs" })]);
    const items = detail.calcs.map((calc) => el("li", {}, [calcLink(calc, handlers.onCalc, {}, calc.name)]));
    return section("part-calcs", `Calcs (${detail.calcs.length})`, [el("ul", {}, items)]);
  }

  // The text after "bound to", or the warning for an unresolved binding.
  function bindingNodes(binding, handlers) {
    if (binding.kind === "calc") {
      const props = { "data-output-id": binding.outputId };
      if (binding.outputName === null) props["data-undeclared-output"] = true;
      const link = calcLink({ key: binding.calcKey }, handlers.onCalc, props, binding.calcName);
      const output = binding.outputName === null ? warning(`undeclared output ${binding.outputId}`) : el("span", { className: "port", text: binding.outputName });
      return ["bound to ", link, ".", output];
    }
    if (binding.kind === "attr") {
      const name = binding.attrName === null ? "attribute name not recorded" : binding.attrName;
      const props = { className: "part-link", "data-target-occurrence-id": binding.occurrenceId, "data-target-attr-node-id": binding.attrNodeId };
      return ["bound to ", button(props, `${binding.partPath}.${name}`, () => handlers.onPart(binding.occurrenceId, binding.attrNodeId))];
    }
    if (binding.kind === "unresolved") {
      const nodes = [warning(binding.reason)];
      if (binding.raw !== null) nodes.push(el("div", { className: "port", text: binding.raw }));
      return nodes;
    }
    throw new Error(`part panel: binding kind ${binding.kind} has no renderer`);
  }

  function valueNodes(row, handlers) {
    if (row.kind === "recorded") {
      const nodes = [el("span", { className: "port", text: displayValue(row.value) })];
      if (row.binding !== null) nodes.push(" ", ...bindingNodes(row.binding, handlers));
      return nodes;
    }
    if (row.kind === "none") return [warning("no value in the snapshot")];
    return bindingNodes(row.binding, handlers);
  }

  function sourceNodes(row) {
    if (row.sourceFile === null) return [warning("source location not recorded")];
    if (row.sourceLine === null) return [el("span", { className: "muted", text: `${row.sourceFile}:` }), warning("line not recorded")];
    return [el("span", { className: "muted", text: `${row.sourceFile}:${row.sourceLine}` })];
  }

  function attributeRow(row, handlers) {
    const props = { "data-attr-node-id": row.nodeId, "data-value-kind": row.kind };
    if (row.name !== null) props["data-attr-name"] = row.name;
    if (row.owner !== null) props["data-owner"] = row.owner;
    if (row.sourceFile !== null && row.sourceLine !== null) props["data-source"] = `${row.sourceFile}:${row.sourceLine}`;
    if (row.kind === "recorded") props["data-value"] = displayValue(row.value);
    const name = row.name === null ? warning("attribute name not recorded") : el("span", { className: "attr-name", text: row.name });
    return el("li", props, [
      el("div", {}, [name, " = ", el("span", { "data-role": "value-cell", className: "value-cell" }, valueNodes(row, handlers))]),
      el("div", { "data-role": "source" }, sourceNodes(row)),
    ]);
  }

  function ownerGroup(group, handlers) {
    const heading = group.owner === null ? [warning("declaring owner not recorded")] : [group.owner];
    if (group.ownPart) heading.push(el("span", { className: "muted", text: " declared on this part" }));
    const props = { className: "owner-group", "data-owner": group.owner === null ? "" : group.owner };
    return el("div", props, [el("h4", {}, heading), el("ul", {}, group.rows.map((row) => attributeRow(row, handlers)))]);
  }

  function attributesSection(detail, handlers) {
    const children = detail.attrCount === 0 ? [el("p", { "data-role": "no-attributes", className: "muted", text: "no attributes recorded" })] : detail.ownerGroups.map((group) => ownerGroup(group, handlers));
    const node = section("attributes", `Attributes (${detail.attrCount})`, children);
    node.setAttribute("data-attr-count", String(detail.attrCount));
    return node;
  }

  // Render one part. collapsed: whether the part is in the structure view's collapse set (it picks the
  // toggle button's word). handlers: {onCalc(key), onPart(occurrenceId, attrNodeId), onTogglePart(occurrenceId)}.
  function renderPart(panelElement, model, occurrenceId, collapsed, handlers) {
    const detail = partDetail(model, occurrenceId);
    panelElement.replaceChildren(header(detail, collapsed, handlers), calcsSection(detail, handlers), attributesSection(detail, handlers));
    delete panelElement.dataset.calcNodeId;
    panelElement.dataset.partOccurrenceId = occurrenceId;
    panelElement.scrollTop = 0;
  }

  // Scroll an attribute row of the rendered part into view.
  function revealRow(panelElement, attrNodeId) {
    const row = [...panelElement.querySelectorAll("li[data-attr-node-id]")].find((li) => li.dataset.attrNodeId === attrNodeId);
    if (row === undefined) throw new Error(`part panel: no attribute row ${attrNodeId} is shown`);
    row.scrollIntoView({ block: "nearest" });
  }

  // The structure view's empty panel, with what the loaded snapshot leaves out of every part (Appendix B).
  function renderStructurePlaceholder(panelElement, model) {
    ModelViz.panel.renderPlaceholder(panelElement, "structure");
    if (model.occurrences.size === 0) panelElement.appendChild(el("p", {}, [warning("this snapshot records no parts")]));
    const unscoped = model.unscopedAttrIds.length;
    if (unscoped > 0) {
      const text = `${plural(unscoped, "attribute", "attributes")} in this snapshot ${unscoped === 1 ? "belongs" : "belong"} to no part and ${unscoped === 1 ? "is" : "are"} not shown.`;
      panelElement.appendChild(el("p", { "data-role": "unscoped-attrs" }, [warning(text)]));
    }
  }

  // A panel-level warning for a link or search whose part is not in the model.
  function renderMissingPart(panelElement, occurrenceId) {
    delete panelElement.dataset.calcNodeId;
    delete panelElement.dataset.partOccurrenceId;
    panelElement.replaceChildren(el("p", { "data-role": "missing-part" }, [warning(`No part ${occurrenceId} in this snapshot; nothing to show.`)]));
  }

  return { renderPart, revealRow, renderStructurePlaceholder, renderMissingPart };
})();
