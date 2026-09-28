"""Exact Celsius offset for the actual endpoint check."""
AUTO_IMPLEMENTED=False
INPUTS=dict(celsius=0.)
OUTPUTS=['value']
def calculate(x):return dict(value=x['celsius']+273.15)
