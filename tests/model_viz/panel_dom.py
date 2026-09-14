"""Read the rendered detail panel's DOM into plain data for comparison with the raw snapshot.

Reads only DOM hooks (data-* attributes and textContent), never the viewer's model.
"""

_PANEL_DUMP_JS = """
() => {
  const panel = document.querySelector('[data-role=panel]');
  const section = (name) => panel.querySelector(`[data-section=${name}]`);
  const text = (el) => (el === null ? null : el.textContent);
  const formula = section('formula');
  const doc = section('doc');
  const inputs = section('inputs');
  const outputs = section('outputs');
  const location = section('location');
  return {
    nodeId: panel.dataset.calcNodeId ?? null,
    header: text(panel.querySelector('[data-role=calc-name]')),
    sections: [...panel.querySelectorAll('[data-section]')].map(s => s.dataset.section),
    sectionText: Object.fromEntries(
      [...panel.querySelectorAll('[data-section]')].map(s => [s.dataset.section, s.textContent])),
    location: location && {
      text: text(location.querySelector('[data-role=location-text]')),
      hash: text(location.querySelector('[data-role=file-hash]')),
      hashTitle: location.querySelector('[data-role=file-hash]')?.title ?? null,
    },
    formulaEntries: formula === null ? [] : [...formula.querySelectorAll('li[data-formula-index]')]
      .map(li => ({
        index: Number(li.dataset.formulaIndex),
        text: text(li.querySelector('.formula-text')),
        repeat: li.hasAttribute('data-doc-repeat'),
      })),
    provenance: formula === null
      ? null : text(formula.querySelector('[data-role=formula-provenance]')),
    derived: formula === null ? null : text(formula.querySelector('[data-role=derived-formula]')),
    docText: doc === null ? null : text(doc.querySelector('.doc-text')),
    docAbsent: doc !== null && doc.hasAttribute('data-doc-absent'),
    inputs: inputs === null ? [] : [...inputs.querySelectorAll('[data-input-kind]')].map(row => ({
      kind: row.dataset.inputKind,
      name: row.dataset.inputName,
      producerNodeId: row.dataset.producerNodeId ?? null,
      outputId: row.dataset.outputId ?? null,
      unresolved: row.hasAttribute('data-unresolved'),
      value: row.dataset.value ?? null,
      linkKey: row.querySelector('[data-calc-key]')?.dataset.calcKey ?? null,
      hasWarning: row.querySelector('.warning') !== null,
      text: row.textContent,
    })),
    outputs: outputs === null ? [] : [...outputs.querySelectorAll('li[data-output-id]')]
      .map(row => ({
        outputId: row.dataset.outputId,
        name: row.dataset.outputName ?? null,
        undeclared: row.hasAttribute('data-undeclared-output'),
        noConsumer: row.hasAttribute('data-no-consumer'),
        consumers: [...row.querySelectorAll('[data-consumer-node-id]')].map(link => ({
          nodeId: link.dataset.consumerNodeId,
          inputName: link.dataset.inputName,
          key: link.dataset.calcKey ?? null,
        })),
      })),
  };
}
"""


def panel_dump(page) -> dict:
    return page.evaluate(_PANEL_DUMP_JS)
