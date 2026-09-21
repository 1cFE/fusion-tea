"""Exact normalized algebra counterexample; no plant or reference evaluation.

Demonstrates what one calibration can and cannot determine in Lion Eq.39.
The two positive coefficient pairs below are illustrative, not fitted values,
physical bounds, priors or estimates for any particular coil configuration.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def full_relative(current, size, bore, pack_side, fraction):
    """Ratios to a synthetic reference R=1, a_coil=1/4, pack side=1/10."""
    reference_clearance = F(3, 4)
    clearance = size - bore
    bracket = 1 - fraction + fraction * size * F(1, 10) / pack_side
    return current * reference_clearance / clearance * bracket


def omitted_term_relative(current, size, bore):
    return current * F(3, 4) / (size - bore)


def run():
    fractions = [F(1, 4), F(3, 4)]
    tests = []
    for current in [F(1, 2), F(1), F(2)]:
        predictions = [full_relative(current, F(1), F(1, 4), F(1, 10), f) for f in fractions]
        assert predictions == [current, current]
        tests.append({'case': 'fixed_geometry_proportional_current', 'current_ratio': str(current),
                      'relative_fields': list(map(str, predictions))})
    for scale in [F(1, 2), F(1), F(2)]:
        predictions = [full_relative(F(1), scale, scale / 4, scale / 10, f) for f in fractions]
        assert predictions == [1 / scale, 1 / scale]
        assert omitted_term_relative(F(1), scale, scale / 4) == 1 / scale
        tests.append({'case': 'homothetic_geometry_including_pack', 'length_ratio': str(scale),
                      'relative_fields': list(map(str, predictions))})
    pack_changed = [full_relative(F(1), F(1), F(1, 4), F(1, 5), f) for f in fractions]
    assert pack_changed == [F(7, 8), F(5, 8)]
    assert omitted_term_relative(F(1), F(1), F(1, 4)) == 1
    tests.append({'case': 'pack_side_doubled_at_fixed_coil_centreline_and_current',
                  'relative_fields': list(map(str, pack_changed)), 'omitted_term_prediction': '1'})
    held_pack = [full_relative(F(1), F(2), F(1, 2), F(1, 10), f) for f in fractions]
    assert held_pack == [F(5, 8), F(7, 8)]
    tests.append({'case': 'coil_centreline_scaled_but_pack_held',
                  'relative_fields': list(map(str, held_pack)), 'omitted_term_prediction': '1/2'})
    sources = [
        'knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md',
        'knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/images/lion_2021_nf_stellarator_process.pdf-0009-19.png',
        'knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md',
        'knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0067-03.png',
        'knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0067-05.png',
    ]
    return {'schema_version': 'field-identifiability-proof/v1', 'arithmetic': 'exact rational',
            'scope': 'Synthetic normalized algebra only; no physical calibration or geometry qualification',
            'source_equation': 'Lion2021 Eq39; thesis2023 Eqs2.65/2.66 establish axis convention and scaling',
            'illustrative_reference_second_term_fractions': list(map(str, fractions)),
            'checks': tests, 'all_checks_pass': True,
            'conclusion': 'One normalized reference value cannot identify two positive coefficients. Current scaling and full geometric similarity remove that ambiguity in relative response; independent pack or non-similar geometry changes do not.',
            'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    result = run()
    with (HERE / 'identifiability.json').open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print('Eight exact rational checks passed; no plant calculation or fitted coefficients')
