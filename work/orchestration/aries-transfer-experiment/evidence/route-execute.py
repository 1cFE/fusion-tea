"""Native route smoke probe; numeric inputs are synthetic, not ARIES data."""
import json
from pathlib import Path
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader

root = Path('/tmp/aries-native-route')
package = root / 'route_tea'
module, fingerprint = ProvisionalPackageLoader(package_dir=package, package_name='route_tea', link_root=root / 'link').load()
result = execute_pipeline(package / 'pipelines/pipeline.yaml', root / 'run', registry=module.create_route_tea_registry(), custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
expected = {'p_wallplug_total': 10.0, 'p_delivered': 5.0, 'p_coupled': 4.0, 'eta_pin_eff': 0.4}
for name, value in expected.items():
    assert result.outputs['route_probe__probe__heating__' + name] == value
print(json.dumps({'fingerprint': str(fingerprint), 'outputs': result.outputs, 'synthetic_tooling_probe': True}, indent=2, default=str))
