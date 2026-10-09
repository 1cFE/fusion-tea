"""Reproducible precision receipts for independent WI-097 limiting equations."""
import json
from pathlib import Path

import mpmath as mp
from exploration.exchanger_architecture.thermal_requirements.studies import thermal_oracle as o


def inverse_log(hot, mean, digits):
    with mp.workdps(digits):
        a, target = mp.mpf(hot), mp.mpf(mean)
        lo, hi = mp.mpf(-4096), mp.mpf(4096)
        for _ in range(digits*4+20):
            x = (lo+hi)/2
            lm = a if x == 0 else a*mp.expm1(x)/x
            if lm > target:
                hi = x
            else:
                lo = x
        return float(mp.log(a)+(lo+hi)/2)


def main():
    rows = []
    for ratio in (.1, .99999999999, 1., 1.00000000001, 10.):
        for ua in (.001, 2., 50., 1000.):
            args = (300., ua, 4*ratio, 4.)
            low, high = (o.precise_passive_transfer(*args, digits=d) for d in (80, 160))
            actual = o.passive_transfer(*args)
            assert low == high
            error = abs(actual-high)/max(abs(actual), abs(high))
            assert error < 2e-14
            rows.append(dict(fixture="passive", drive=300., ua=ua, ch=4*ratio, cs=4.,
                value_80_digits=low, value_160_digits=high, binary64=actual, relative_error=error))
    for hot, cold in ((30.,30.), (230.,1e-30), (1e-25,230.)):
        with mp.workdps(160):
            a, b = mp.mpf(hot), mp.mpf(cold)
            mean = float(a if a == b else (a-b)/mp.log(a/b))
        low, high = (inverse_log(hot,mean,d) for d in (80,160))
        _, actual = o.cold_gap_from_lmtd(hot, mean)
        assert low == high
        assert abs(actual-high) < 1e-11
        rows.append(dict(fixture="inverse_LMTD", hot_gap=hot, prescribed_mean=mean,
            log_cold_gap_80_digits=low, log_cold_gap_160_digits=high,
            log_cold_gap_binary64=actual, log_absolute_error=abs(actual-high)))
    log_hot, log_cold = o.passive_log_terminal_gaps(100.,1000.,10.,1.)
    assert log_hot < -800
    result = dict(status="PASS", kind="constructed equation fixtures; not plant candidates",
        precisions_decimal_digits=[80,160], cases=rows,
        sub_float_hot_gap=dict(drive=100., ua=1000., ch=10., cs=1.,
            log_hot_gap=log_hot, log_cold_gap=log_cold, rounded_transferred_heat=100.))
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status="PASS", precision_pairs=len(rows))))


if __name__ == '__main__':
    main()
