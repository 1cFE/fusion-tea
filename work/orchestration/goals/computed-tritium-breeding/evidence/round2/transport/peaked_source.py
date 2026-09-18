"""Sample the current plant's fusion-emissivity profile with toroidal Jacobian.

Bosch-Hale algebra transcribed from the existing generated dt_fusion_power_impl.py
(commit identity must be recorded by the consuming study). No new fit is used.
"""
import math
from pathlib import Path
import numpy as np
import openmc


def sigv(T):
    T=np.maximum(T,1e-6)
    theta=T/(1-T*(1.51361e-2+T*(4.60643e-3-T*1.06750e-4))/(1+T*(7.51886e-2+T*(1.35000e-2+T*1.36600e-5))))
    xi=(34.3827**2/(4*theta))**(1/3)
    return 1.17302e-9*theta*np.sqrt(xi/(1124656*T**3))*np.exp(-3*xi)*1e-6


def write(path: Path,seed: int,n: int=500_000):
    rng=np.random.default_rng(seed)
    accepted=[]
    total=0
    max_emissivity=float(sigv(14.63))
    while total<n:
        count=500_000
        rho=np.sqrt(rng.random(count))
        theta=rng.uniform(0,2*math.pi,count)
        jac=(1270+130*rho*np.cos(theta))/1400
        u=1-rho*rho
        emissivity=u**.66*sigv(14.63*u**1.19)/max_emissivity
        assert np.max(emissivity)<=1+1e-12
        keep=rng.random(count)<jac*emissivity
        rho,theta=rho[keep],theta[keep]
        count=min(len(rho),n-total)
        accepted.append((rho[:count],theta[:count]));total+=count
    rho=np.concatenate([x[0] for x in accepted]);theta=np.concatenate([x[1] for x in accepted])
    phi=rng.uniform(0,2*math.pi,n)
    r=1270+130*rho*np.cos(theta)
    xyz=np.column_stack((r*np.cos(phi),r*np.sin(phi),130*rho*np.sin(theta)))
    mu=rng.uniform(-1,1,n);angle=rng.uniform(0,2*math.pi,n)
    directions=np.column_stack((np.sqrt(1-mu*mu)*np.cos(angle),np.sqrt(1-mu*mu)*np.sin(angle),mu))
    particles=[openmc.SourceParticle(r=point,u=direction,E=14.06e6,wgt=1) for point,direction in zip(xyz,directions)]
    openmc.write_source_file(particles,path)
    grid=np.linspace(0,1,100001);u=1-grid*grid
    weights=2*grid*u**.66*sigv(14.63*u**1.19)
    expected=float(np.trapezoid(weights*grid**2,grid)/np.trapezoid(weights,grid))
    observed=float(np.mean(rho*rho));se=float(np.std(rho*rho,ddof=1)/math.sqrt(n))
    assert abs(observed-expected)<5*se
    return dict(bank_particles=n,bank_seed=seed,alpha_n=.33,alpha_T=1.19,T_i0_keV=14.63,
                mean_normalized_minor_radius_squared=observed,expected=expected,standard_error=se,
                limitation='finite source bank adds source approximation uncertainty; pilot sensitivity only')
