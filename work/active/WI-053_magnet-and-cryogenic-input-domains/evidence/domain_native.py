"""Run invalid plant cases through the existing native PreparedEvaluator."""
from pathlib import Path
import native_probe
P=native_probe.P
native_probe.CASES={
 'ordinary': {},
 'live_negative': {P+'coil_t':20.},
 'live_equal': {P+'coil_t':19.4},
 'reference_negative': {P+'magnet__a_coil_ref':13.},
 'reference_equal': {P+'magnet__a_coil_ref':12.7},
 **{name:{P+'T_cold_cryo':cold,P+'T_amb_cryo':ambient} for name,cold,ambient in [('cold_zero',0.,300.),('cold_negative',-1.,300.),('temperature_equal',300.,300.),('temperature_reversed',301.,300.),('ambient_zero',20.,0.),('ambient_negative',20.,-1.)]}
}
if __name__=='__main__':
    root=Path(__file__).resolve().parents[4]
    native_probe.run(root/'exploration/stellarator_e2e/generated',Path(__file__).resolve().parent/'domain-native.json')
