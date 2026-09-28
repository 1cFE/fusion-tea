"""Conservative propagation of the model's existing numerical-definedness guards."""
from collections import deque

P = 'stellarator_09__stellaris__'
GUARDS = {
    P + 'blanket__breeding__defined_flag': None,
    P + 'breeding_adequacy__defined_flag': None,
    P + 'fuel_cycle__inventory__defined_flag': None,
    P + 'fuel_cycle__processing_cost__defined_flag': None,
    P + 'turbine__matched_cycle__main_UA_available': P + 'turbine__matched_cycle__main_UA_MW_K',
    P + 'turbine__matched_cycle__reheat_UA_available': P + 'turbine__matched_cycle__reheat_UA_MW_K',
}


def state(flags):
    if not flags:
        return 'no_guard_in_scope'
    if any(type(v) not in (bool, int, float) or v not in (0, 1) for v in flags.values()):
        return 'unknown'
    return 'defined' if all(flags.values()) else 'undefined'


def assess_definedness(graph, document):
    pubs = document['publications']
    guards_by_publication = {key: {} for key in pubs}
    for flag, target in GUARDS.items():
        if flag not in pubs:
            raise ValueError('missing pinned model guard: ' + flag)
        record = pubs[flag]
        owner = record['producer']
        if owner not in graph.spec.modules or graph.channel_providers.get(record['channel']) != owner:
            raise ValueError('guard producer mismatch: ' + flag)
        if target is None:
            # A defined_flag covers this module; broad propagation is intentional.
            direct = {key for key, p in pubs.items() if p['producer'] == owner and key != flag}
            starts = set(graph.adjacency[owner])
        else:
            if target not in pubs or pubs[target]['producer'] != owner:
                raise ValueError('guarded target mismatch: ' + target)
            direct = {target}
            target_channel = pubs[target]['channel']
            starts = {key for key, spec in graph.spec.modules.items()
                      if not spec.is_exit and any(b.channel_name == target_channel for b in spec.inputs.values())}
        paths = {key: [owner, key] for key in starts}
        queue = deque(starts)
        while queue:
            key = queue.popleft()
            for child in graph.adjacency[key]:
                if child not in paths:
                    paths[child] = paths[key] + [child]
                    queue.append(child)
        value = document['numeric_outputs'].get(flag)
        for key, publication in pubs.items():
            if key in direct or publication['producer'] in paths:
                guards_by_publication[key][flag] = {
                    'value': value, 'path': [owner] if key in direct else paths[publication['producer']]}
    return {'schema_version': 'model-definedness/v1',
            'scope': 'Six existing declared guard outputs only; absence of a tracked guard does not establish scientific support.',
            'granularity': 'Module-conservative downstream; matched-cycle guards start at their specific UA outputs.',
            'publications': {key: {'model_definedness': state({f: r['value'] for f, r in flags.items()}),
                                   'guards': flags} for key, flags in guards_by_publication.items()}}
