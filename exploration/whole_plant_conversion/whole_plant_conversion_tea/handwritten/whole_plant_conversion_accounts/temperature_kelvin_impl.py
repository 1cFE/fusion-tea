"""Exact Celsius offset for the actual endpoint check."""
AUTO_IMPLEMENTED=False
INPUTS=dict(celsius=0.)
OUTPUTS=['value']
def calculate(x):return dict(value=x['celsius']+273.15)

from whole_plant_conversion_tea.modules.whole_plant_conversion_accounts.temperature_kelvin import Temperature_KelvinInput

def _native_result(inputs):
    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})
    return result['value']

def run_temperature_kelvin(inputs: Temperature_KelvinInput) -> float:
    return _native_result(inputs)
