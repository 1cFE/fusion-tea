exec(open('op_solve_proto4.py').read().split("print(f\"@14.63")[0])
# density scan: scale all species peaks by fd; recompute line-av n19, W, alpha, rad
import math
mu0=1.25663706212e-6
def beta_of(T_i0,fd):
    T_e0=T_i0/Ti_over_Te
    p=KEV*(fd*n_e0*T_e0/(1+alpha_n_e+alpha_T)+fd*(n_D0+n_T0+n_He0)*T_i0/(1+alpha_n+alpha_T))
    return 2*mu0*p/(B*B)
wall_area=940.0*327.0/940.0  # S_lcfs=327 used for wall load? model uses wall_area from radial build; use ratio to current: wall_load = p_fus*(1-ash)/wall_area_model; current: 3.1312 at p_fus 2748
WALL_K=3.131234717504045/2748.0568768605704  # MW/m2 per MW fusion (model's own ratio)
def scan(fd):
    nD,nT,nE,nHe=fd*n_D0,fd*n_T0,fd*n_e0,fd*n_He0
    n19l=nE*prof_int(lambda u,rho:u**alpha_n_e)/1e19
    def pf(T):
        I=prof_int(lambda u,rho:(u**(2*alpha_n))*sigv_dt(T*(u**alpha_T))*2*rho)
        return nD*nT*I*E_fus*V*1e-6
    def W_(T):
        T_e0=T/Ti_over_Te
        p=KEV*(nE*T_e0/(1+alpha_n_e+alpha_T)+(nD+nT+nHe)*T/(1+alpha_n+alpha_T))
        return 1.5*p*V*1e-6
    def rad(T):
        T_e0=T/Ti_over_Te
        Ib=prof_int(lambda u,rho:(u**(2*alpha_n_e))*math.sqrt(max(T_e0*(u**alpha_T),1e-9))*2*rho)
        brems=5.35e-37*Z_eff*(nE**2)*Ib*V*1e-6
        Il=prof_int(lambda u,rho:(u**(2*alpha_n_e))*Lz_W(T_e0*(u**alpha_T))*2*rho)
        line=f_W*(nE**2)*Il*V*1e-6
        sync=p_sync(T_e0,nE/1e20)
        return brems+line+sync
    def g(T,paux):
        W=W_(T)
        return f_alpha*ash_frac*pf(T)+paux-rad(T)-W/tau_E(W,n19l)
    # required sustained aux: max over T of -(g at paux=0) minimized => min aux to open window
    Ts=[8+0.5*i for i in range(45)]
    req=min(-g(T,0.0) for T in Ts)
    # burn point at paux=0 and 50
    out=[f"fd={fd:.2f} n19l={n19l:.1f} aux_req={req:6.1f}"]
    for paux in (0.0,50.0):
        burn=None
        prev=g(Ts[0],paux)
        for T in Ts[1:]:
            cur=g(T,paux)
            if prev>0 and cur<=0:
                lo,hi=T-0.5,T
                for _ in range(50):
                    m=0.5*(lo+hi)
                    if g(m,paux)>0: lo=m
                    else: hi=m
                burn=0.5*(lo+hi)
            prev=cur
        if burn:
            pfb=pf(burn)
            out.append(f"paux={paux:3.0f}: T={burn:5.2f} p_fus={pfb:6.0f} wall={WALL_K*pfb:5.2f}(lim 4.05) beta={beta_of(burn,fd)*100:5.2f}%(lim 5)")
        else:
            out.append(f"paux={paux:3.0f}: no burn")
    print("  ".join(out))
for fd in (1.0,1.05,1.1,1.2,1.3,1.5):
    scan(fd)
