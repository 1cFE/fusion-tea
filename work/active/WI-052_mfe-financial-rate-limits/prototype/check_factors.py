"""Independent 90-digit references from actual binary64 operands."""
from decimal import Decimal as D, localcontext
import json
import math
from pathlib import Path
from factors import crf, annuity_pv, idc, periodic_pv

rows = []
def check(name, actual, expected, args):
    error = abs(D(actual) - expected) / abs(expected) if expected else abs(D(actual))
    assert error <= D('1e-9'), (name, args, actual, str(expected), str(error))
    rows.append(dict(quantity=name, operands=args, actual=actual, expected=str(expected), error=float(error)))

rates = [0., .02, .08] + [s * 10.**(-p) for p in (4, 8, 12, 16, 18) for s in (-1, 1)]
durations = [.25, .5, 1., math.nextafter(1., 0.), math.nextafter(1., 2.), 8., 8.5, 30., 30.5, 100.5, 200.5]
with localcontext() as ctx:
    ctx.prec = 90
    for n in durations:
        boundary = .125 / max(1., n)
        for i in rates + [s*x for s in (-1,1) for x in (math.nextafter(boundary, 0.), boundary, math.nextafter(boundary, math.inf))]:
            I,N = D(i),D(n)
            expected = D(1)/N if not I else I/(1-(1+I)**(-N))
            check('crf', crf(i,n), expected, [i,n])
            expected = D(0) if not I or N==1 else ((1+I)**N-1)/(I*N)-1
            check('idc', idc(i,n), expected, [i,n])
            for count in (0., 1., 7.):
                expected = sum((D('1e6')/(1+I)**(D(k)*N) for k in range(1,int(count)+1)),D(0))
                check('periodic_pv', periodic_pv(1e6,i,n,count), expected,[i,n,count])
    for n in (30., 30.5, .25, 200.5):
        for t in (8.,8.5,.25,50.5):
            for i in rates + [-.02]:
                for g in rates + [i] + [i+s*10.**(-p) for p in (4,8,12,16,18) for s in (-1,1)]:
                    I,G,N,T = map(D,(i,g,n,t))
                    a1=D('1e6')*(1+G)**T
                    if n.is_integer():
                        pv=sum((a1*(1+G)**(k-1)/(1+I)**k for k in range(1,int(n)+1)),D(0))
                    else:
                        pv=a1*N/(1+I) if I==G else a1*(1-((1+G)/(1+I))**N)/(I-G)
                    check('annuity_pv',annuity_pv(1e6,i,g,n,t),pv,[i,g,n,t])
Path(__file__).with_name('factor-results.json').write_text(json.dumps(dict(count=len(rows),max_error=max(r['error'] for r in rows),rows=rows),indent=2)+'\n')
print('PASS',len(rows),'checks; maximum relative/true-zero absolute error', max(r['error'] for r in rows))
