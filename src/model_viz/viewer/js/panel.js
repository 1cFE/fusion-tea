// Shell: the detail panel. Renders one calc from the model with textContent only; holds no state.
window.ModelViz = window.ModelViz || {};

ModelViz.panel = (function () {
  const DERIVED_LABEL = "derived from expression structure; the snapshot has no formula text for this calc.";

  function el(tag, props, children) {
    const node = document.createElement(tag);
    for (const [name, value] of Object.entries(props || {})) {
      if (name === "text") node.textContent = value;
      else if (name === "className") node.className = value;
      else if (name === "title") node.title = value;
      else if (name.startsWith("data-")) node.setAttribute(name, value === true ? "" : value);
      else throw new Error(`panel.el: unsupported property ${name}`);
    }
    for (const child of children || []) node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
    return node;
  }

  function warning(text) {
    return el("span", { className: "warning", text });
  }

  function section(name, title, children) {
    return el("section", { "data-section": name }, [el("h3", { text: title }), ...children]);
  }

  function displayValue(value) {
    return typeof value === "string" ? value : JSON.stringify(value);
  }

  function withUnit(unit) {
    return unit === null ? [] : [el("span", { className: "muted", text: ` [${unit}]` })];
  }

  function calcLink(calc, onCalcLink, props, text) {
    const button = el("button", { className: "calc-link", "data-calc-key": calc.key, text, ...props });
    button.type = "button";
    button.addEventListener("click", () => onCalcLink(calc.key));
    return button;
  }

  function locationSection(model, calc) {
    const where = calc.sourceFile === null ? null : `${calc.sourceFile}:${calc.sourceLine === null ? "line not recorded" : calc.sourceLine}`;
    const text = where === null ? warning("source location not recorded") : el("span", { "data-role": "location-text", className: "port", text: where });
    const children = [el("div", {}, [text])];
    const hash = calc.sourceFile === null ? undefined : model.fileHashes.get(calc.sourceFile);
    if (hash === undefined) {
      children.push(el("div", {}, [warning("no file hash recorded")]));
    } else {
      children.push(el("div", { className: "muted" }, ["file SHA-256 ", el("span", { "data-role": "file-hash", className: "port", title: hash, text: hash.slice(0, 12) })]));
    }
    return section("location", "Location", children);
  }

  function derivedBlock(calc) {
    const children = [el("div", { className: "muted", text: DERIVED_LABEL })];
    if (calc.derivedFormula === null) {
      children.push(el("div", {}, [warning("No formula available")]));
    } else {
      const text = calc.outputs.length === 1 ? `${calc.outputs[0].name} = ${calc.derivedFormula}` : calc.derivedFormula;
      children.push(el("div", { "data-role": "derived-formula", className: "formula-text", text }));
    }
    return el("div", {}, children);
  }

  // D7: every entry verbatim, in order. Only the last entry can be the doc repeat that codegen
  // appends (Finding 12); it is noted, never hidden.
  function formulaSection(calc) {
    const children = [
      el("div", { "data-role": "formula-provenance", className: "muted", text: "Lines reconstructed by codegen from the parsed model; not verbatim source text." }),
    ];
    const lastIndex = calc.formulas.length - 1;
    const lastRepeats = lastIndex >= 0 && ModelViz.formula.endsWithDoc(calc.formulas[lastIndex], calc.doc);
    const onlyRepeat = lastIndex === 0 && lastRepeats;
    if (calc.formulas.length === 0 || (onlyRepeat && calc.hasExpressionIr)) children.push(derivedBlock(calc));
    if (onlyRepeat && !calc.hasExpressionIr) children.push(el("div", {}, [warning("No formula lines recorded for this calc.")]));
    if (calc.formulas.length > 0) {
      const list = el("ol");
      calc.formulas.forEach((entry, i) => {
        const item = el("li", { "data-formula-index": String(i) }, [el("span", { className: "formula-text", text: entry })]);
        if (i === lastIndex && lastRepeats) {
          item.setAttribute("data-doc-repeat", "");
          item.prepend(el("span", { className: "formula-note", text: "repeats the documentation below" }));
        }
        list.appendChild(item);
      });
      children.push(list);
    }
    return section("formula", "Formula", children);
  }

  function docSection(calc) {
    if (calc.doc === null) {
      const node = section("doc", "Documentation", [warning("No documentation in the snapshot for this calc.")]);
      node.setAttribute("data-doc-absent", "");
      return node;
    }
    return section("doc", "Documentation", [el("div", { className: "doc-text", text: calc.doc })]);
  }

  function kindLabel(kind) {
    return el("span", { className: "kind", text: kind });
  }

  function producerRow(model, input, onCalcLink) {
    const binding = model.bindingById.get(input.bindingId);
    const row = el("li", { "data-input-kind": "producer", "data-input-name": input.name, "data-producer-node-id": binding.producerNodeId, "data-output-id": binding.outputId }, [
      kindLabel("producer"),
      `${input.name} ← `,
    ]);
    if (!binding.resolved) {
      row.setAttribute("data-unresolved", "");
      row.append(warning("unresolved: the producer calc is not in this snapshot"), el("div", { className: "port", text: `${binding.producerNodeId} output ${binding.outputId}` }));
      return row;
    }
    const producer = model.byKey.get(binding.producer);
    const output = producer.outputs.find((o) => o.outputId === binding.outputId);
    row.append(calcLink(producer, onCalcLink, {}, producer.name), ".");
    if (output === undefined) row.append(warning(`undeclared output ${binding.outputId}`));
    else row.append(el("span", { className: "port", text: output.name }));
    return row;
  }

  function parameterRow(model, input) {
    const row = el("li", { "data-input-kind": "parameter", "data-input-name": input.name, "data-attr-node-id": input.attrNodeId }, [kindLabel("parameter"), `${input.name} ← `]);
    const attr = model.attrs.get(input.attrNodeId);
    if (attr === undefined) {
      row.append(warning("attribute not in snapshot"));
      return row;
    }
    row.append(el("span", { className: "port", text: attr.name === null ? "attribute name not recorded" : attr.name }), " = ");
    if (attr.hasValue) {
      row.setAttribute("data-value", displayValue(attr.value));
      row.append(displayValue(attr.value));
    } else {
      row.append(warning("no value in snapshot"));
    }
    return row;
  }

  function valueRow(input, missingText) {
    const row = el("li", { "data-input-kind": input.kind, "data-input-name": input.name }, [kindLabel(input.kind), `${input.name} = `]);
    if (input.hasValue) {
      row.setAttribute("data-value", displayValue(input.value));
      row.append(displayValue(input.value));
    } else {
      row.append(warning(missingText));
    }
    return row;
  }

  function inputRow(model, input, onCalcLink) {
    let row;
    if (input.kind === "producer") row = producerRow(model, input, onCalcLink);
    else if (input.kind === "parameter") row = parameterRow(model, input);
    else if (input.kind === "literal") row = valueRow(input, "no value in snapshot");
    else if (input.kind === "default") row = valueRow(input, "no default recorded");
    else if (input.kind === "unknown") row = el("li", { "data-input-kind": "unknown", "data-input-name": input.name }, [kindLabel("unknown"), `${input.name} `, warning(`unknown input kind: ${input.rawKind}`)]);
    else throw new Error(`panel: input kind ${input.kind} has no row renderer`);
    row.append(...withUnit(input.unit));
    return row;
  }

  function consumerList(model, calc, outputId, onCalcLink) {
    const portKey = calc.key + "|" + outputId;
    const ids = model.consumersOf.has(portKey) ? model.consumersOf.get(portKey) : [];
    const list = el("ul");
    for (const id of ids) {
      const binding = model.bindingById.get(id);
      const consumer = model.byKey.get(binding.consumer);
      const link = calcLink(consumer, onCalcLink, { "data-consumer-node-id": consumer.nodeId, "data-input-name": binding.inputName }, consumer.name);
      list.appendChild(el("li", {}, ["→ ", link, ".", el("span", { className: "port", text: binding.inputName })]));
    }
    return { list, count: ids.length };
  }

  function outputRow(model, calc, output, onCalcLink) {
    const row = el("li", { "data-output-id": output.outputId, "data-output-name": output.name }, [el("span", { className: "port", text: output.name }), ...withUnit(output.unit)]);
    const { list, count } = consumerList(model, calc, output.outputId, onCalcLink);
    if (count === 0) {
      row.setAttribute("data-no-consumer", "");
      row.append(el("div", { className: "muted", text: "no calc consumes this output" }));
    } else {
      row.append(list);
    }
    return row;
  }

  function undeclaredOutputRow(model, calc, outputId, onCalcLink) {
    const row = el("li", { "data-output-id": outputId, "data-undeclared-output": true }, [warning("undeclared output: bound by a consumer but not declared on this calc"), el("div", { className: "port", text: outputId })]);
    row.append(consumerList(model, calc, outputId, onCalcLink).list);
    return row;
  }

  function header(model, calc) {
    const group = model.groups.get(calc.sourceGroup);
    return el("header", {}, [
      el("h2", { "data-role": "calc-name", text: calc.name }),
      el("div", { className: "muted", text: group.path === null ? "no source file recorded" : group.path }),
    ]);
  }

  // Render one calc. onCalcLink(key) is called when an upstream or downstream calc link is clicked.
  function renderPanel(panelElement, model, key, onCalcLink) {
    const calc = model.byKey.get(key);
    if (calc === undefined) throw new Error(`panel: no calc ${key} in the model`);
    const inputs = el("ul", {}, calc.inputs.map((input) => inputRow(model, input, onCalcLink)));
    const outputs = el("ul", {}, [
      ...calc.outputs.map((output) => outputRow(model, calc, output, onCalcLink)),
      ...calc.undeclaredOutputIds.map((outputId) => undeclaredOutputRow(model, calc, outputId, onCalcLink)),
    ]);
    panelElement.replaceChildren(
      header(model, calc),
      locationSection(model, calc),
      formulaSection(calc),
      docSection(calc),
      section("inputs", `Inputs (${calc.inputs.length})`, [inputs]),
      section("outputs", `Outputs (${calc.outputs.length})`, [outputs])
    );
    panelElement.dataset.calcNodeId = calc.nodeId;
    panelElement.scrollTop = 0;
  }

  function renderPlaceholder(panelElement) {
    delete panelElement.dataset.calcNodeId;
    panelElement.replaceChildren(el("p", { className: "placeholder", text: "Select a calc in the graph to see its formula, documentation, inputs and outputs." }));
  }

  // A panel-level warning for a link or search whose target is not in the model.
  function renderMissingCalc(panelElement, key) {
    delete panelElement.dataset.calcNodeId;
    panelElement.replaceChildren(el("p", { "data-role": "missing-calc" }, [warning(`No calc ${key} in this snapshot; nothing to show.`)]));
  }

  return { renderPanel, renderPlaceholder, renderMissingCalc };
})();
