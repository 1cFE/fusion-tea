"""WI-037 T-002 prototype v3: pure python, cached."""
import math
from functools import lru_cache

def sigv_dt(T_keV):
    T = max(T_keV, 1e-6)
    theta = T / (1.0 - T*(1.51361e-2 + T*(4.60643e-3 + T*-1.06750e-4))
                 / (1.0 + T*(7.51886e-2 + T*(1.35000e-2 + T*1.36600e-5))))
    xi = ((34.3827*34.3827)/(4.0*theta))**(1.0/3.0)
    return 1.17302e-9*theta*math.sqrt(xi/(1124656.0*T*T*T))*math.exp(-3.0*xi)*1e-6

n_D0=1.96e20; n_T0=1.96e20; n_e0=5.06e20; n_He0=0.56e20
alpha_n=0.33; alpha_T=1.19; alpha_n_e=0.596
V=425.0; a=1.3; R=12.74; B=9.0; E_fus=2.817e-12
f_ren=1.0; f_alpha=0.95; ash_frac=0.2002
Ti_over_Te=0.95; KEV=1.602176634e-16
Z_eff=1.20; f_W=7.76e-6; iota=0.92
N=400

def prof_int(fn):
    acc=0.0
    for i in range(N+1):
        rho=i/N; u=1.0-rho*rho
        v=fn(u,rho)
        acc += v if 0<i<N else v/2
    return acc/N

# W cooling curve, pure python (radiation.py _COOLING_CURVES["W"])
def Lz_W(T):
    T=max(T,0.01)
    if T<0.1: return 5.0e-31*T**-1.0
    if T<1.0: return 1.5e-31*T**0.5
    if T<10.0: return 5.0e-31
    return 5.0e-31*T**-0.5

def p_sync(T_e0,n_e0_20):
    R_w=0.6; kappa=1.0; BT=2.0
    A_=R/a
    p_a0=6.04e3*a*n_e0_20/B
    corr=(1-R_w)**0.62/(1+0.12*T_e0/p_a0**0.41*(1-R_w)**0.41)**1.51
    K=((alpha_n_e+3.87*alpha_T+1.46)**(-0.79)*(1.98+alpha_T)**1.36*BT**2.14
       *(BT**1.53+1.87*alpha_T-0.16)**(-1.33))
    G=0.93*(1+0.85*math.exp(-0.82*A_))
    return (3.84e-8*corr*R*a**1.38*kappa**0.79*B**2.62*n_e0_20**0.38
            *T_e0*(16+T_e0)**2.61*K*G)

@lru_cache(maxsize=4096)
def p_fus_MW(T_i0):
    I=prof_int(lambda u,rho:(u**(2*alpha_n))*sigv_dt(T_i0*(u**alpha_T))*2*rho)
    return n_D0*n_T0*I*E_fus*V*1e-6

def W_MJ(T_i0):
    T_e0=T_i0/Ti_over_Te
    p=KEV*(n_e0*T_e0/(1+alpha_n_e+alpha_T)+(n_D0+n_T0+n_He0)*T_i0/(1+alpha_n+alpha_T))
    return 1.5*p*V*1e-6

def n19_volav(): return 31.7
def n19_lineav(): return n_e0*prof_int(lambda u,rho:u**alpha_n_e)/1e19

def tau_E(W,n19):
    C=0.134*f_ren*(a**2.28)*(B**0.84)*(iota**0.41)*(n19**0.54)*(R**0.64)
    return (C*(W**-0.61))**(1.0/0.39)

@lru_cache(maxsize=4096)
def p_brems_MW(T_i0):
    T_e0=T_i0/Ti_over_Te
    I=prof_int(lambda u,rho:(u**(2*alpha_n_e))*math.sqrt(max(T_e0*(u**alpha_T),1e-9))*2*rho)
    return 5.35e-37*Z_eff*(n_e0**2)*I*V*1e-6

@lru_cache(maxsize=4096)
def p_line_MW(T_i0):
    T_e0=T_i0/Ti_over_Te
    I=prof_int(lambda u,rho:(u**(2*alpha_n_e))*Lz_W(T_e0*(u**alpha_T))*2*rho)
    return f_W*(n_e0**2)*I*V*1e-6

@lru_cache(maxsize=4096)
def p_sync_MW(T_i0):
    return p_sync(T_i0/Ti_over_Te,n_e0/1e20)

def solve(rad_fn,n19,p_aux=0.0,Tlo=2.0,Thi=60.0,step=0.25):
    def g(T):
        W=W_MJ(T)
        return f_alpha*ash_frac*p_fus_MW(T)+p_aux-rad_fn(T)-W/tau_E(W,n19)
    crossings=[]
    Tprev,gprev=Tlo,g(Tlo)
    T=Tlo+step
    while T<=Thi+1e-9:
        gc=g(T)
        if gprev*gc<=0 and gc!=gprev:
            lo,hi=Tprev,T
            for _ in range(60):
                m=0.5*(lo+hi)
                if g(lo)*g(m)<=0: hi=m
                else: lo=m
            crossings.append((0.5*(lo+hi),"up" if gprev<0 else "down"))
        Tprev,gprev=T,gc
        T+=step
    return crossings

print(f"@14.63: p_fus={p_fus_MW(14.63):.1f} W={W_MJ(14.63):.1f} tauE_volav={tau_E(W_MJ(14.63),31.7):.3f} tauE_lineav={tau_E(W_MJ(14.63),n19_lineav()):.3f}")
print(f"n19 lineav={n19_lineav():.2f}; rad@14.63: brems={p_brems_MW(14.63):.1f} line={p_line_MW(14.63):.1f} sync={p_sync_MW(14.63):.2f} (printed photon 228.9)")
RAD={"brems":lambda T:p_brems_MW(T),
     "brems+line":lambda T:p_brems_MW(T)+p_line_MW(T),
     "b+l+sync":lambda T:p_brems_MW(T)+p_line_MW(T)+p_sync_MW(T)}
for n19name,n19 in (("volav",31.7),("lineav",n19_lineav())):
    for rname,rfn in RAD.items():
        for paux in (0.0,50.0):
            cr=solve(rfn,n19,paux)
            s=" ".join(f"{t:.2f}({d})" for t,d in cr) or "none"
            burn=[t for t,d in cr if d=="down"]
            pf=f" T_burn={burn[-1]:.2f} p_fus={p_fus_MW(burn[-1]):.0f}" if burn else ""
            print(f"n19={n19name:6s} rad={rname:10s} paux={paux:4.0f}: {s}{pf}")
