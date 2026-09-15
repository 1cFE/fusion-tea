import math,json
from scipy.integrate import quad
coef=[-1.4087,1.3982,.2543,-.6260,.2334,.4256,-.4658,.1650,-.0199]
def k(t):
    x=math.log10(t)
    return 10**sum(c*x**i for i,c in enumerate(coef))
Kc=quad(k,20,77,epsabs=1e-9)[0]; Kw=quad(k,77,300,epsabs=1e-9)[0]
rows=[]
for label,f,e,q,G,eta in [('low',1,.02,.5,.48,.3),('nominal',1.25,.05,1,1.92,.2),('high',1.5,.1,2,7.68,.15)]:
    A=48*25*4*.7; Aw=1.2*A
    lead_c=f*12*50000*math.sqrt(2.45e-8*(77**2-20**2))
    lead_w=f*12*50000*math.sqrt(2.45e-8*(300**2-77**2))
    rad_c=A*e*5.670374419e-8*(77**4-20**4)
    rad_w=Aw*q-rad_c
    support_c=G*Kc; support_w=G*(Kw-Kc)
    cold=lead_c+rad_c+support_c; warm=lead_w+rad_w+support_w
    direct=lead_c+lead_w
    elec=cold*(300-20)/(eta*20)+warm*(300-77)/(eta*77)+direct
    rows.append(dict(case=label,area_cold_m2=A,area_warm_m2=Aw,lead_cold_W=lead_c,lead_warm_W=lead_w,radiation_cold_W=rad_c,radiation_warm_W=rad_w,support_cold_W=support_c,support_warm_W=support_w,total_cold_W=cold,total_warm_W=warm,direct_W=direct,increment_electrical_MW=elec/1e6))
print(json.dumps(dict(K20_77_W_per_m=Kc,K77_300_W_per_m=Kw,scenarios=rows),indent=2))
