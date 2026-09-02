"""WI-037 T-002 final prototype: ash-coupled solve, full radiation, quasi-neutrality.
Levers: n_e0 (peak electron density), p_aux, machine (a,R,V,B,iota). Held sourced:
f_ren=1.0, f_alpha=0.95, tau_ratio=8.0, f_suppr=0.5, f_W=7.76e-6, Z_eff=1.20, Ti/Te=0.95.
Solved: T_i0, n_He0 (ash), n_D0=n_T0 (quasi-neutrality)."""
import math
def sigv_dt(T_keV):
    T=max(T_keV,1e-6)
    theta=T/(1.0-T*(1.51361e-2+T*(4.60643e-3+T*-1.06750e-4))/(1.0+T*(7.51886e-2+T*(1.35000e-2+T*1.36600e-5))))
    xi=((34.3827*34.3827)/(4.0*theta))**(1.0/3.0)
    return 1.17302e-9*theta*math.sqrt(xi/(1124656.0*T*T*T))*math.exp(-3.0*xi)*1e-6
alpha_n=0.33; alpha_T=1.19; alpha_n_e=0.596
V=425.0; a=1.3; R=12.74; E_fus=2.817e-12
f_ren=1.0; f_alpha=0.95; ash_frac=0.2002; Ti_over_Te=0.95
KEV=1.602176634e-16; Z_eff=1.20; f_W=7.76e-6; TAU_RATIO=8.0; F_SUPPR=0.5
WALL_K=3.131234717504045/2748.0568768605704
mu0=1.25663706212e-6
N=400
def prof_int(fn):
    acc=0.0
    for i in range(N+1):
        rho=i/N; u=1.0-rho*rho
        v=fn(u,rho)
        acc+=v if 0<i<N else v/2
    return acc/N
def Lz_W(T):
    T=max(T,0.01)
    if T<0.1: return 5.0e-31*T**-1.0
    if T<1.0: return 1.5e-31*T**0.5
    if T<10.0: return 5.0e-31
    return 5.0e-31*T**-0.5
def p_sync(T_e0,n_e0_20,B):
    R_w=0.6; kappa=1.0; BT=2.0
    p_a0=6.04e3*a*n_e0_20/B
    corr=(1-R_w)**0.62/(1+0.12*T_e0/p_a0**0.41*(1-R_w)**0.41)**1.51
    K=((alpha_n_e+3.87*alpha_T+1.46)**(-0.79)*(1.98+alpha_T)**1.36*BT**2.14*(BT**1.53+1.87*alpha_T-0.16)**(-1.33))
    G=0.93*(1+0.85*math.exp(-0.82*R/a))
    return 3.84e-8*corr*R*a**1.38*kappa**0.79*B**2.62*n_e0_20**0.38*T_e0*(16+T_e0)**2.61*K*G
IFUS=lambda T:prof_int(lambda u,rho:(u**(2*alpha_n))*sigv_dt(T*(u**alpha_T))*2*rho)
def state(T,n_e0,p_aux,B,iota):
    """Inner ash fixed point at temperature T. Returns dict or None if collapse."""
    n_He0=0.0
    n19l=n_e0*prof_int(lambda u,rho:u**alpha_n_e)/1e19
    C=0.134*f_ren*(a**2.28)*(B**0.84)*(iota**0.41)*(n19l**0.54)*(R**0.64)
    Ifus=IFUS(T)
    T_e0=T/Ti_over_Te
    for it in range(60):
        n_fuel=n_e0-2.0*n_He0
        if n_fuel<=0: return None
        nD=nT=0.5*n_fuel
        p_fus=nD*nT*Ifus*E_fus*V*1e-6
        p=KEV*(n_e0*T_e0/(1+alpha_n_e+alpha_T)+(nD+nT+n_He0)*T/(1+alpha_n+alpha_T))
        W=1.5*p*V*1e-6
        tauE=(C*(W**-0.61))**(1.0/0.39)
        n_He_new=F_SUPPR*TAU_RATIO*tauE*nD*nT*sigv_dt(T)
        if abs(n_He_new-n_He0)<1e12: n_He0=n_He_new; break
        n_He0=0.5*(n_He0+n_He_new)
    n_fuel=n_e0-2.0*n_He0
    if n_fuel<=0: return None
    nD=nT=0.5*n_fuel
    p_fus=nD*nT*Ifus*E_fus*V*1e-6
    p=KEV*(n_e0*T_e0/(1+alpha_n_e+alpha_T)+(nD+nT+n_He0)*T/(1+alpha_n+alpha_T))
    W=1.5*p*V*1e-6
    tauE=(C*(W**-0.61))**(1.0/0.39)
    Ib=prof_int(lambda u,rho:(u**(2*alpha_n_e))*math.sqrt(max(T_e0*(u**alpha_T),1e-9))*2*rho)
    brems=5.35e-37*Z_eff*(n_e0**2)*Ib*V*1e-6
    Il=prof_int(lambda u,rho:(u**(2*alpha_n_e))*Lz_W(T_e0*(u**alpha_T))*2*rho)
    line=f_W*(n_e0**2)*Il*V*1e-6
    sync=p_sync(T_e0,n_e0/1e20,B)
    rad=brems+line+sync
    g=f_alpha*ash_frac*p_fus+p_aux-rad-W/tauE
    beta=2*mu0*p/(B*B)
    return dict(g=g,p_fus=p_fus,W=W,tauE=tauE,rad=rad,n_He0=n_He0,beta=beta,nD=nD)
def burn(n_e0,p_aux,B,iota=0.92,Tlo=6.0,Thi=60.0,step=0.5):
    prev=None; lastdown=None
    T=Tlo
    while T<=Thi+1e-9:
        s=state(T,n_e0,p_aux,B,iota)
        gc=s["g"] if s else -1e9
        if prev is not None and prev>0 and gc<=0:
            lo,hi=T-step,T
            for _ in range(55):
                m=0.5*(lo+hi)
                sm=state(m,n_e0,p_aux,B,iota)
                if sm and sm["g"]>0: lo=m
                else: hi=m
            lastdown=0.5*(lo+hi)
        prev=gc; T+=step
    return lastdown
# 1) ash chain check at printed point
s=state(14.63,5.06e20,0.0,9.0,0.92)
print(f"@printed T=14.63,n_e0=5.06e20: n_He0={s['n_He0']:.3e} (printed 0.56e20) p_fus={s['p_fus']:.0f} tauE={s['tauE']:.3f} rad={s['rad']:.1f} g={s['g']:.1f}")
# 2) baseline attractor at point-A levers
for paux in (0.0,50.0):
    Tb=burn(5.06e20,paux,9.0)
    if Tb:
        sb=state(Tb,5.06e20,paux,9.0,0.92)
        print(f"pointA levers paux={paux:3.0f}: T_burn={Tb:.2f} p_fus={sb['p_fus']:.0f} wall={WALL_K*sb['p_fus']:.2f} beta={sb['beta']*100:.2f}% ash={sb['n_He0']:.2e} tauE={sb['tauE']:.2f}")
    else:
        print(f"pointA levers paux={paux:3.0f}: no burn")
# 3) field reward scan: B x n_e0, paux=50 — find burn, wall, beta
print("\nfield-reward map (paux=50, iota=0.92): T_burn/p_fus/wall/beta")
for B in (8.0,9.0,10.0,11.0,12.0):
    row=[]
    for nf in (0.7,0.85,1.0,1.15):
        n0=5.06e20*nf
        Tb=burn(n0,50.0,B)
        if Tb:
            sb=state(Tb,n0,50.0,B,0.92)
            ok="OK " if WALL_K*sb['p_fus']<=4.05 and sb['beta']<=0.05 else "VIO"
            row.append(f"n={nf:.2f}:T={Tb:4.1f},P={sb['p_fus']:5.0f},w={WALL_K*sb['p_fus']:4.1f},b={sb['beta']*100:4.2f} {ok}")
        else:
            row.append(f"n={nf:.2f}: no burn                  ")
    print(f"B={B:4.1f}: "+" | ".join(row))
