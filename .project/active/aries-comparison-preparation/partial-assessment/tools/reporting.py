"""Pure reporting of partial arithmetic; never creates a completed comparison."""
from collections import Counter
import math

from qualification import combine_qualifications


def flag_state(values):
    if any(type(v) not in (float, int, bool) or v not in (0, 1) for v in values.values()):
        return 'unknown'
    return 'defined' if all(values.values()) else 'undefined'


def build_report(diagnostic, qualifications, selection, manifest, overlay, observations, contract, definedness):
    numbers = diagnostic['numeric_outputs']
    inputs = selection['effective_inputs']
    values = inputs | numbers
    predicates = {}
    for entry in contract['constraint_catalog']['concrete_entries']:
        key, channel = entry['constraint_id'], entry['evaluation_channel']
        publication = diagnostic['publications'].get(channel, {})
        native = publication.get('structured_value', {})
        status = native.get('status') if publication.get('status') == 'available_structured' else 'unavailable'
        if status not in ('satisfied', 'violated', 'indeterminate', 'unavailable'):
            raise ValueError('unknown predicate vocabulary: ' + repr(status))
        predicates[key] = {'native_status': status, 'native_evaluation': native,
                           'qualification': qualifications['predicates'][key],
                           'model_definedness': definedness['publications'][channel],
                           'engineering_acceptance': False}
        if status in ('satisfied', 'violated'):
            values[channel] = status == 'satisfied'

    rows = []
    for quantity in manifest['quantities']:
        key = quantity['id']
        producers = overlay['producer_overrides'].get(key, quantity['producers'])
        flags = set(overlay.get('defined_when', {}).get(key, []))
        for producer in producers:
            flags.update(definedness['publications'].get(producer, {}).get('guards', {}))
        flags = sorted(flags)
        deps = producers + flags
        records = []
        for producer in deps:
            if producer in qualifications['publications']:
                records.append(qualifications['publications'][producer])
            elif producer in inputs:
                records.append({'field_applicability': 'unaffected_by_field_finding', 'causes': []})
            elif producer not in inputs:
                # A missing dependency cannot be advertised as independent.
                records.append({'field_applicability': 'unknown_unqualified', 'causes': [
                    {'root': 'missing_publication', 'path': [], 'publication': producer}]})
        qualification = combine_qualifications(records) if records else {
            'field_applicability': 'unknown_unqualified', 'causes': [
                {'root': 'structural_evidence_required', 'path': []}]}
        raw = None
        availability = 'available'
        if not producers:
            availability = 'structural_evidence_required'
        elif any(p not in values for p in producers):
            availability = 'unavailable_dependency'
        elif len(producers) == 1:
            raw = values[producers[0]]
        elif quantity['calculation'] == 'sum of producers in cumulative radial order':
            raw = sum(values[p] for p in producers)
        elif quantity['calculation'] == 'producer[0] - producer[1]' and len(producers) == 2:
            raw = values[producers[0]] - values[producers[1]]
        else:
            raise ValueError('unsupported row calculation: ' + key)
        if raw is not None and (type(raw) not in (int, float, bool) or not math.isfinite(raw)):
            raise ValueError('invalid retained arithmetic: ' + key)
        modes = quantity.get('availability_when', [])
        applicability = 'unknown' if any(c['input'] not in inputs for c in modes) else (
            'active' if all(inputs[c['input']] == c['equals'] for c in modes) else 'inactive')
        flag_values = {flag: numbers.get(flag) for flag in flags}
        defined_state = flag_state(flag_values) if flags else 'no_guard_in_scope'
        role = selection['input_roles'][producers[0]] if len(producers) == 1 and producers[0] in inputs and producers[0] not in numbers else 'calculated'
        # Raw numbers remain inspectable even when a model-defined guard suppresses interpretation.
        diagnostic_value = raw if availability == 'available' and applicability == 'active' and defined_state in ('defined', 'no_guard_in_scope') else None
        reference = observations['quantities'].get(key, {})
        rows.append({'id': key, 'unit': quantity['unit'], 'axis': quantity['axis'],
                     'role': role, 'producers': producers, 'raw_arithmetic': raw,
                     'diagnostic_value': diagnostic_value, 'numerical_availability': availability,
                     'mode_applicability': applicability, 'model_definedness': defined_state,
                     'definedness_flags': flag_values, 'field_qualification': qualification,
                     'supported_prediction': None, 'independent_prediction_credit': False,
                     'reference': reference.get('reference'),
                     'historical_correspondence_evidence': reference.get('applicability_evidence'),
                     'comparison_status': 'not_established', 'comparison_ratio': None,
                     'comparison_reason': 'Conditional transfer with held equipment; source definition, technology and accounting correspondence is not established.'})
    assert len({r['id'] for r in rows}) == len(rows)
    return {'schema_version': 'partial-assessment/v1', 'report_kind': 'post_reveal_partial_diagnostic',
            'blind': False, 'publication_ready': False, 'engineering_acceptance': False,
            'supported_lcoe': None, 'state': diagnostic['state'],
            'qualification': 'Diagnostic arithmetic only. Unaffected by the field finding does not certify other model assumptions. No supported prediction or same-design comparison is established here.',
            'predicate_counts': dict(Counter(p['native_status'] for p in predicates.values())),
            'row_counts': dict(Counter(r['numerical_availability'] for r in rows)),
            'field_row_counts': dict(Counter(r['field_qualification']['field_applicability'] for r in rows)),
            'numeric_output_count': len(numbers), 'predicate_count': len(predicates),
            'row_count': len(rows), 'predicates': predicates, 'rows': rows}
