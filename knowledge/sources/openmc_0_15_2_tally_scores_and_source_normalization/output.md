---
source: "https://docs.openmc.org/en/v0.15.2/usersguide/tallies.html"
source_type: "url"
extracted_at: "2026-09-18T20:54:57.858576+00:00"
content_hash_sha256: "672e30ffc6e6847901a505e4a979338b6e1f2932448cb3d05e083098d19b58a1"
backend: "trafilatura"
title: "8. Specifying Tallies¶"
---

# 8. Specifying Tallies[¶](https://docs.openmc.org#specifying-tallies)

In order to obtain estimates of physical quantities in your simulation, you need
to create one or more tallies using the [ openmc.Tally](https://docs.openmc.org/pythonapi/generated/openmc.Tally.html#openmc.Tally) class. As
explained in detail in the

[theory manual](https://docs.openmc.org/methods/tallies.html#methods-tallies), tallies provide estimates of a scoring function times the flux integrated over some region of phase space, as in:

Thus, to specify a tally, we need to specify what regions of phase space should
be included when deciding whether to score an event as well as what the scoring
function (\(f\) in the above equation) should be used. The regions of phase
space are generally called *filters* and the scoring functions are simply
called *scores*.

The only cases when filters do not correspond directly with the regions of phase space are when expansion functions are applied in the integrand, such as for Legendre expansions of the scattering kernel.

## 8.1. Filters[¶](https://docs.openmc.org#filters)

To specify the regions of phase space, one must create a
[ openmc.Filter](https://docs.openmc.org/pythonapi/generated/openmc.Filter.html#openmc.Filter). Since

[is an abstract class, you actually need to instantiate one of its sub-classes (for a full listing, see](https://docs.openmc.org/pythonapi/generated/openmc.Filter.html#openmc.Filter)

`openmc.Filter`

[Constructing Tallies](https://docs.openmc.org/pythonapi/base.html#pythonapi-tallies)). For example, to indicate that events that occur in a given cell should score to the tally, we would create a

[:](https://docs.openmc.org/pythonapi/generated/openmc.CellFilter.html#openmc.CellFilter)

`openmc.CellFilter`

```
cell_filter = openmc.CellFilter([fuel.id, moderator.id, reflector.id])
```

Another commonly used filter is [ openmc.EnergyFilter](https://docs.openmc.org/pythonapi/generated/openmc.EnergyFilter.html#openmc.EnergyFilter), which specifies
multiple energy bins over which events should be scored. Thus, if we wanted to
tally events where the incident particle has an energy in the ranges [0 eV, 4
eV] and [4 eV, 1 MeV], we would do the following:

```
energy_filter = openmc.EnergyFilter([0.0, 4.0, 1.0e6])
```

Energies are specified in eV and need to be monotonically increasing.

Caution

An energy bin between zero and the lowest energy specified is not included by default as it is in MCNP.

Once you have created a filter, it should be assigned to a [ openmc.Tally](https://docs.openmc.org/pythonapi/generated/openmc.Tally.html#openmc.Tally)
instance through the

`Tally.filters`

attribute:```
tally.filters.append(cell_filter)
tally.filters.append(energy_filter)
# This is equivalent
tally.filters = [cell_filter, energy_filter]
```

Note

You are actually not required to assign any filters to a tally. If you create a tally with no filters, all events will score to the tally. This can be useful if you want to know, for example, a reaction rate over your entire model.

## 8.2. Scores[¶](https://docs.openmc.org#scores)

To specify the scoring functions, a list of strings needs to be given to the
`Tally.scores`

attribute. You can score the flux (‘flux’), or a reaction
rate (‘total’, ‘fission’, etc.). For example, to tally the elastic scattering
rate and the fission neutron production, you’d assign:

```
tally.scores = ['elastic', 'nu-fission']
```

With no further specification, you will get the total elastic scattering rate
and the total fission neutron production. If you want reaction rates for a
particular nuclide or set of nuclides, you can set the `Tally.nuclides`

attribute to a list of strings indicating which nuclides. The nuclide names
should follow the same [naming convention](https://docs.openmc.org/materials.html#usersguide-naming) as that used
for material specification. If we wanted the reaction rates only for U235 and
U238 (separately), we’d set:

```
tally.nuclides = ['U235', 'U238']
```

You can also list ‘all’ as a nuclide which will give you a separate reaction rate for every nuclide in the model.

The following tables show all valid scores:

Score |
Description |
|---|---|
flux |
Total flux. |

Score |
Description |
|---|---|
absorption |
Total absorption rate. For incident neutrons, this accounts for all reactions that do not produce secondary neutrons as well as fission. For incident photons, this includes photoelectric and pair production. |
elastic |
Elastic scattering reaction rate. |
fission |
Total fission reaction rate. |
scatter |
Total scattering rate. |
total |
Total reaction rate. |
(n,2nd) |
(n,2nd) reaction rate. |
(n,2n) |
(n,2n) reaction rate. |
(n,3n) |
(n,3n) reaction rate. |
(n,na) |
(n,n\(\alpha\)) reaction rate. |
(n,n3a) |
(n,n3\(\alpha\)) reaction rate. |
(n,2na) |
(n,2n\(\alpha\)) reaction rate. |
(n,3na) |
(n,3n\(\alpha\)) reaction rate. |
(n,np) |
(n,np) reaction rate. |
(n,n2a) |
(n,n2\(\alpha\)) reaction rate. |
(n,2n2a) |
(n,2n2\(\alpha\)) reaction rate. |
(n,nd) |
(n,nd) reaction rate. |
(n,nt) |
(n,nt) reaction rate. |
(n,n3He) |
(n,n |
(n,nd2a) |
(n,nd2\(\alpha\)) reaction rate. |
(n,nt2a) |
(n,nt2\(\alpha\)) reaction rate. |
(n,4n) |
(n,4n) reaction rate. |
(n,2np) |
(n,2np) reaction rate. |
(n,3np) |
(n,3np) reaction rate. |
(n,n2p) |
(n,n2p) reaction rate. |
(n,n*X*) |
Level inelastic scattering reaction rate. The |
(n,nc) |
Continuum level inelastic scattering reaction rate. |
(n,gamma) |
Radiative capture reaction rate. |
(n,p) |
(n,p) reaction rate. |
(n,d) |
(n,d) reaction rate. |
(n,t) |
(n,t) reaction rate. |
(n,3He) |
(n, |
(n,a) |
(n,\(\alpha\)) reaction rate. |
(n,2a) |
(n,2\(\alpha\)) reaction rate. |
(n,3a) |
(n,3\(\alpha\)) reaction rate. |
(n,2p) |
(n,2p) reaction rate. |
(n,pa) |
(n,p\(\alpha\)) reaction rate. |
(n,t2a) |
(n,t2\(\alpha\)) reaction rate. |
(n,d2a) |
(n,d2\(\alpha\)) reaction rate. |
(n,pd) |
(n,pd) reaction rate. |
(n,pt) |
(n,pt) reaction rate. |
(n,da) |
(n,d\(\alpha\)) reaction rate. |
coherent-scatter |
Coherent (Rayleigh) scattering reaction rate. |
incoherent-scatter |
Incoherent (Compton) scattering reaction rate. |
photoelectric |
Photoelectric absorption reaction rate. |
pair-production |
Pair production reaction rate. |
|
An arbitrary integer is interpreted to mean the reaction rate for a reaction with a given ENDF MT number. |

Score |
Description |
|---|---|
delayed-nu-fission |
Total production of delayed neutrons due to fission. |
prompt-nu-fission |
Total production of prompt neutrons due to fission. |
nu-fission |
Total production of neutrons due to fission. |
nu-scatter |
This score is similar in functionality to the
|
H1-production |
Total production of H1. |
H2-production |
Total production of H2 (deuterium). |
H3-production |
Total production of H3 (tritium). |
He3-production |
Total production of He3. |
He4-production |
Total production of He4 (alpha particles). |

Score |
Description |
|---|---|
current |
Used in combination with a meshsurface filter: Partial currents on the boundaries of each cell in a mesh. It may not be used in conjunction with any other score. Only energy and mesh filters may be used. Used in combination with a surface filter: Net currents on any surface previously defined in the geometry. It may be used along with any other filter, except meshsurface filters. Surfaces can alternatively be defined with cell from and cell filters thereby resulting in tallying partial currents. Units are particles per source particle. |
events |
Number of scoring events. Units are events per source particle. |
inverse-velocity |
The flux-weighted inverse velocity where the velocity is in units of centimeters per second. |
heating |
Total nuclear heating in units of eV per source
particle. For neutrons, this corresponds to MT=301
produced by NJOY’s HEATR module while for photons,
this is tallied from direct photon energy
deposition. See |
heating-local |
Total nuclear heating in units of eV per source
particle assuming energy from secondary photons is
deposited locally. Note that this score should only
be used for incident neutrons. See
|
kappa-fission |
The recoverable energy production rate due to fission. The recoverable energy is defined as the fission product kinetic energy, prompt and delayed neutron kinetic energies, prompt and delayed \(\gamma\)-ray total energies, and the total energy released by the delayed \(\beta\) particles. The neutrino energy does not contribute to this response. The prompt and delayed \(\gamma\)-rays are assumed to deposit their energy locally. Units are eV per source particle. |
fission-q-prompt |
The prompt fission energy production rate. This energy comes in the form of fission fragment nuclei, prompt neutrons, and prompt \(\gamma\)-rays. This value depends on the incident energy and it requires that the nuclear data library contains the optional fission energy release data. Energy is assumed to be deposited locally. Units are eV per source particle. |
fission-q-recoverable |
The recoverable fission energy production rate. This energy comes in the form of fission fragment nuclei, prompt and delayed neutrons, prompt and delayed \(\gamma\)-rays, and delayed \(\beta\)-rays. This tally differs from the kappa-fission tally in that it is dependent on incident neutron energy and it requires that the nuclear data library contains the optional fission energy release data. Energy is assumed to be deposited locally. Units are eV per source paticle. |
decay-rate |
The delayed-nu-fission-weighted decay rate where the decay rate is in units of inverse seconds. |
damage-energy |
Damage energy production in units of eV per source particle. This corresponds to MT=444 produced by NJOY’s HEATR module. |
pulse-height |
The energy deposited by an entire photon’s history (including its progeny). Units are eV per source particle. Note that this score can only be combined with a cell filter and an energy filter. |

## 8.3. Normalization of Tally Results[¶](https://docs.openmc.org#normalization-of-tally-results)

As described in [Scores](https://docs.openmc.org#usersguide-scores), all tally scores are normalized per
source particle simulated. However, for analysis of a given system, we usually
want tally scores in a more natural unit. For example, neutron flux is often
reported in units of particles/cm2-s. For a fixed source simulation,
it is usually straightforward to convert units if the source rate is known. For
example, if the system being modeled includes a source that is emitting 104 neutrons per second, the tally results just need to be multipled by 104. This can either be done manually or using the
`openmc.SourceBase.strength`

attribute.

For a \(k\)-eigenvalue calculation, normalizing tally results is not as
simple because the source rate is not actually known. Instead, we typically know
the system power, \(P\), which represents how much energy is deposited per
unit time. Most of this energy originates from fission, but a small percentage
also results from other reactions (e.g., photons emitted from \((n,\gamma)\)
reactions). The most rigorous method to normalize tally results is to run a
coupled neutron-photon calculation and tally the `heating`

score over the
entire system. This score provides the heating rate in units of [eV/source],
which we’ll denote \(H\). Then, calculate the heating rate in J/source as

Dividing the power by the observed heating rate then gives us a normalization factor that can be applied to other tallies:

Multiplying by the normalization factor and dividing by volume, we can then get the flux in typical units:

There are several slight variations on this procedure:

Run a neutron-only calculation and estimate the total heating using the

`heating-local`

score (this requires that your nuclear data has local heating data available, such as in the official data library at[https://openmc.org](https://openmc.org). See[Heating and Energy Deposition](https://docs.openmc.org/methods/energy_deposition.html#methods-heating)for more information.)Run a neutron-only calculation and use the

`kappa-fission`

or`fission-q-recoverable`

scores along with an estimate of the extra heating due to neutron capture reactions.Calculate the overall fission rate and then used a fixed Q value to estimate the heating rate.


Note that the only difference between these and the above procedures is in how \(H'\) is estimated.