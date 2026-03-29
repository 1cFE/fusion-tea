---
source_url: "https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion"
access_date: "2026-03-28T21:54:08.564386+00:00"
content_hash_sha256: "1a29b7997a009ea16ea9b4d23d035b909e8dceff7b5b9468f8985016a0479cc7"
title: "Fusion Startup Spotlight: Realta Fusion"
author: "Fusion Hub"
extraction_tool: "trafilatura 2.0.0"
---

# Fusion Startup Spotlight: Realta Fusion

### A deep dive into the new fusion startup applying high temperature superconducting magnets to the magnetic mirror

High temperature superconducting (HTS) rare earth barium copper oxide (REBCO) magnets are revolutionizing magnetic fusion energy and may be the key to commercializing fusion.

The pitch is that REBCO magnets enable much smaller (i.e. cheaper) magnetic fusion reactors than was previously required for net power generation.

But even with the REBCO revolution, the fusion industry still has a looming threat on the horizon.

Assume all the physics challenges are solved.

Assume all the engineering challenges are solved.

Most, if not all, fusion reactors will be incredibly complex and expensive machines.[1](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-1-135385038)

Even today there are big uncertainties around fusion power plant necessities, like the details of fusion fuel cycles. And fusion reactors will still generate radioactive waste and pose a concern for proliferation of nuclear weapons.

So, **the question every fusion startup needs to answer is how will their fusion concept compete economically with natural gas, wind, solar, and even nuclear fission.**

Maybe the scheme that is arguably the closest to putting power on the grid — the tokamak — will simply not be able to compete with other energy sources.

Or maybe no fusion scheme at all will be able to provide electricity cheaply enough, and have to pivot to other markets instead.

This is a potential future that Realta Fusion is well positioned for.

Rather than a tokamak or a stellarator, Realta is applying HTS magnets to arguably the simplest MCF scheme: the magnetic mirror. And unlike most other fusion startups, they are not aiming for electricity production, but industrial process heat, a necessity for the production of steel, cement, petrochemicals, etc.

Before getting to the magnetic mirror and Realta Fusion, let’s quickly review the tokamak approach to fusion. A plasma, consisting of electrons and ions (which includes the fusion fuel, such as deuterium (D) and tritium (T)), goes around in a torus (i.e. a donut) and is held in by magnetic fields. Stronger magnetic fields means stronger plasma confinement, which means more fusion reactions.

And if the magnetic field is strong enough (for example from HTS REBCO magnets) you get a net power producing fusion reactor. That’s the approach that MIT spin-off, Commonwealth Fusion Systems (CFS), is taking, with $2 billion+ in funding to make it happen.

But tokamaks aren’t the only MCF scheme. Rather than a toroidal shape, magnetic mirrors are cylindrical. Their magnetic field is strongest at the ends, where plasma particles reflect off, return to the center of the plasma, and reflect off the other end like a game of Pong. But the reflection isn’t perfect. Some particles leak out the ends, which is bad if you want a lot of particles fusing. But, like tokamaks, stronger magnetic fields means better confinement.

**Like CFS, Realta Fusion is applying HTS magnets to the magnetic mirror concept to build a commercially viable fusion reactor**. And, if they succeed, they will have a much simpler reactor geometry (cylindrical instead of toroidal) than a tokamak, which means cheaper construction, cheaper operations and maintenance, and cheaper energy.

Pair that with a prudent choice of first market — industrial heat — and they might just pull off a fusion reactor that can generate energy for a profit.

At least that’s the pitch.

Realta Fusion was spun-out from UW Madison in 2022. Their experimental timeline consists of 3 devices:

Planned experimental devices

WHAM: simple mirror

[2](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-2-135385038)to validate improvements from high fieldWHAM++: simple mirror to demonstrate scientific breakeven

HAMMIR: tandem mirror designed for industrial heat production



$10 million from ARPA-E is funding WHAM, but the next devices will cost even more to build and operate ($50 million in REBCO tape alone for WHAM++, although that is expected to be the majority of the cost). So they will need to secure more funding, achieving investor-mandated milestones along the way like any fusion startup.

WHAM is in the final stages of construction, and may have already had first plasma.

With that out of the way, let’s dig into the physics, engineering, and economics of Realta’s fusion reactor design. We’ll cover:

**Basic Physics of the Magnetic Mirror****Challenges for Realta’s Fusion Reactor Design****Realta’s Go-to-Market Strategy**

### Basic Physics of the Magnetic Mirror

#### The Simple Mirror

Before diving further into Realta’s planned machines and the solutions they have proposed to solve the historical problems with magnetic mirrors, let’s review some basic mirror machine physics.

The simplest kind of magnetic mirror consists of two strong magnetic field coils, with (optionally) lower field coils in between, all arranged in a cylindrical geometry.

Particles move along the field lines, reflecting back once they reach a high field end, hence the “mirror” in magnetic mirror. One way to understand this is the conservation of magnetic moment (which I explore in the tweet thread linked in the image). But, in short, it is this reflection and continuous back and forth which provides the magnetic confinement.

The primary metric to describe the characteristic strength of the magnetic confinement is the **mirror ratio, the ratio between the maximum and minimum magnetic field strengths**:

The high field provided by HTS magnets significantly increases the mirror ratio compared to previous mirror devices. And **a high mirror ratio greatly improves particle confinement in the magnetic mirror**.

The improvement is so great that you should no longer need various engineering features and structures (e.g. minimum B magnets like yin-yang coils, thermal barriers) that were historically seen as necessities, but made mirrors increasingly complex and, hence, expensive.

#### Ion Confinement

The first order of business is assessing how well the ions are confined. If you lose too many ions then you won’t get enough fusion reactions. So good ion confinement is essential.

A fundamental property of the mirror is the loss cone. Let’s think back to our picture of particles reflecting off the high field regions. If a particle is moving too fast along the field line (i.e. too high parallel velocity), then it will simply stream out the end and be lost. This threshold parallel velocity for loss of ions defines a **loss cone** in velocity space.

Put simply, if an ion’s velocity is inside a loss cone, it will be lost by leaking out of the central cell. However, **higher mirror ratio narrows the loss cone**, so it will take a larger parallel velocity to stream out.

This is one of the big reasons why higher field strengths, provided by HTS magnets, is so beneficial.

Besides the loss cone at high parallel velocities, there is another hole in velocity space: the **ambipolar hole**.

In the central cell of the mirror, electrons leak out the ends more quickly than ions (since the electrons are much lighter), generating a positive electric potential (more ions (positive charge) than electrons (negative charge)) in the center relative to the ends. The excess positive charge will then push some ions out. This ends up generating another hole in velocity space, at low velocities.

Like the loss cone, any ion whose velocity is in this ambipolar hole will be lost.[3](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-3-135385038)

But, also like the loss cone, **high mirror ratio narrows the ambipolar hole**.

The size of the ambipolar hole in velocity space, characterized by a critical perpendicular velocity is shown above.

To summarize what we’ve learned so far:

**HTS REBCO magnets → higher magnetic fields at mirror ends → higher mirror ratio → smaller loss cone and ambipolar hole → better ion confinement **

So HTS magnets improve on a critical issue for magnetic mirrors. But the loss cone and ambipolar hole will still need to be seriously addressed by Realta Fusion, because these holes in velocity space can be a nasty source of kinetic instabilities (which we’ll discuss when we get to their plasma stability challenges).

These relations have been validated experimentally (and of course much theory has been developed) to show that the ion confinement time does indeed scale with the mirror ratio.

#### Direct Energy Conversion

Losing ions from the central cell isn’t all bad however.

Since lost ions emerge from the central cell as a directed beam of positive charge, it can be converted into an electrical current to power the reactor subsystems, improving the balance of plant. Realta has discussed plans to implement direct energy conversion via axisymmetric ferromagnetic venetian blinds.

#### Scaling to Scientific Breakeven and Beyond

For a fusion device to be economically viable (for most applications at least), it needs to produce more energy than it consumes.

For the magnetic mirror, we can see how the plasma performance scales with mirror parameters, like the mirror ratio and average ion energy, to figure out what device parameters we need for scientific breakeven. The plot below shows the performance of past magnetic mirror devices and how Realta’s machines (green ovals for WHAM and WHAM++) compare.

Realta is predicting breakeven with their second experimental device: WHAM++.[4](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-4-135385038)

We can doubt the validity of extrapolating that far in parameter space, while being slightly more assured with simulation results, but of course scientific breakeven can only really be demonstrated experimentally.[5](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-5-135385038)

With that in mind, we can make a few observations from these scaling curves:

A mirror ratio of 2 (which was the historically the maximum that could be achieved while maintaining MHD stability) could not achieve breakeven. Now,

**with mirror ratios of 10 or more, breakeven and beyond is feasible**.There is good agreement between the theoretical scaling and the experimental data.


#### Tandem Mirror

So far we’ve talked about the simple mirror. Again, that’s just 2 high field coils at each end of a central cell containing the bulk of the plasma.

But Realta is building towards what is called a **tandem mirror**.

Like the simple mirror, it has a central cell where most of the fusion reactions will still be happening. But it adds on two more mirror cells, one between the central cell and each expander region (furthest-out regions of plasma, one on each end), referred to as end plugs. The **end plugs are designed to prevent leakage out of the central cell**.

Neutral beam injectors (NBI) increase the density of these end plugs over the central cell, setting up an even higher electrical potential (even more positive charge) than we discussed earlier for the central cell. So, any ions that leak out the central cell will encounter a substantially higher potential that will repel them, keeping them in the central cell where we want them.

### Challenges for Realta’s Fusion Reactor Design

We have a good sense now of basic magnetic mirror physics and the benefits of higher magnetic field strengths for confinement. But the picture presented so far has neglected a lot of the challenges that were faced by previous research mirror researchers, and that Realta will need to solve.

Fortunately for Realta, they are not just building off the advances in the US mirror program mostly in the 70’s and 80’s. This program had important achievements, but also yielded very large machines with beautifully complex, but expensive, magnet geometries.

Mirror research has also been going on outside the US, notably in Japan with the Gamma-10 machine, and Russia with the Gas Dynamic Trap (GDT) mirror machine. The GDT in particular achieved several impressive results like sufficient magneto-hydrodynamic (MHD) stability, high electron temperatures (~ 1 keV), and mitigation of kinetic instabilities (all discussed below). And this was all accomplished in axisymmetric mirrors i.e. no complex magnets like yin-yang coils.

The challenge for Realta will be integrating these more recent achievements in their new devices along with HTS magnets.

One big part of that challenge, like almost every fusion concept, is stability. Generally speaking, if your plasma goes unstable, you lose confinement of heat and particles, quenching your fusion reactions. For mirrors, there are two classes of instabilities to be worried about: kinetic and MHD.

#### Kinetic Stability

Kinetic instabilities emerge from holes in velocity space.

For magnetic mirrors, these come from the loss cone and the ambipolar hole, which we already discussed. So, besides the ion leakage they cause, they can also drive kinetic instabilities. And this problem doesn’t magically go away with the higher mirror ratios that Realta is planning on.

Important kinetic instabilities, or “micro-instabilities,” of concern here are the **drift cyclotron loss cone (DCLC) instability** and **Alfven Ion Cyclotron (AIC) instability**. **Realta is proposing to use “sloshing ions” to help stabilize such micro-instabilities.**

Skewed neutral beam injectors will inject ions into the plasma that “slosh” back and forth between the mirror turning points. Since their axial velocity is zero at the turning points (i.e. where they reflect), the sloshing ion density is highest at these turning points, establishing positive potential peaks there. These potential peaks then confine the ions that would otherwise leave due to the ambipolar hole. Therefore, these sloshing ions serve to fill in the ambipolar hole, and thus stabilize kinetic instabilities.

#### MHD Stability

MHD instabilities can arise when a machine has “**bad curvature**.”

Whether you have good or bad curvature depends on the curvature of the field lines relative to regions of higher pressure (i.e. the hot plasma).

Mirrors have bad curvature in the central cell, which can lead to MHD instabilities like the interchange instability. Picture the cylindrically shaped plasma in the central cell as a greek column developing flutes that grow exponentially in time. Such an instability would be devastating for plasma confinement.

Realta is proposing to use **vortex stabilization to mitigate MHD instability**. This would involve inducing (via an electric field) sheared azimuthal flows (like swirling water around in a cup), up to the edge of the plasma. With a sufficient sheared flow, the flutes of the interchange instability don’t have enough time to grow in place.

Besides vortex stabilization in the central cell, **Realta is also exploiting the good curvature in the expander regions to improve the averaged field curvature**.

#### Electron Temperature

Magnetic mirrors have historically had low electron temperatures, which is bad because collisions between high temperature ions and colder electrons will cool the ions.

Fortunately, more recent experiments like the GDT have demonstrated higher electron temperatures (~ 1 keV) simply by applying electron cyclotron heating (ECH) to heat up the electrons. An additional advantage of ECH, particularly in the end plugs, is higher end plug potentials since they scale with the electron temperature. Higher potentials in the end plugs then improve the ion confinement.

#### Engineering Challenges

Realta will also face engineering challenges on top of the physics challenges. Important concerns will include plasma material interactions (PMI), blanket engineering, neutron shielding of the HTS magnets, and many more. Many of these are common to other MCF reactor concepts like tokamaks and stellarators.

One notable difference is different behavior of impurities in mirrors compared to toroidal magnetic fusion devices. Impurities are any elements that end up in your plasma (for example from sputtering) that are not your fusion fuel. For example, tungsten from the first wall would be an impurity in plasma consisting of deuterium and tritium fuel ions. Impurities can be a big issue, especially if they’re high Z, meaning they have many electrons and so can massively increase the radiation (bremsstrahlung) losses, cooling down the plasma.

In simple mirrors, impurities are actually not much of an issue because of the ambipolar potential, which will pull out the high Z ions from the central cell even better than it does the fusion fuel ions.

However, impurities stick around longer in tandem mirrors because of the high potential end plugs. It remains to be seen how big of an issue this will be for Realta’s tandem mirror design.

### Realta’s Go-to-Market Strategy

#### Target Markets

Unlike many other fusion startups, **Realta Fusion is targeting industrial heat, rather than electricity production, as their initial market**.

This seems prudent, considering the huge difficulty fusion will have competing with other sources of electricity like solar, wind, and natural gas. Wind and solar (besides solar thermal) are not well-suited to industrial heat, since they produce energy directly in the form of electricity.

Fusion reactors with DT fuel cycles will produce 80% of their output energy in the form of neutrons which then produce heat energy via their collisions in the reactor blanket. This is often seen as a downside considering the conversion losses in going from heat to electricity (not to mention all the materials challenges), but that’s no longer an issue for a fusion reactor that produces heat directly for industrial processes.

The choice of initial customers is important for any startup, and as Cary Forest (CSO and CTO of Realta Fusion) has mentioned, partnering with customers of process heat (e.g. petrochemical manufacturers) is likely to be more profitable than grid utilities, especially for any first-of-a-kind plant. Customers of industrial heat will generally have more cash on hand to help finance the capital intensive projects that Realta’s reactors will be. In addition, industrial heat provided by fusion, rather than fossil fuels, would be attractive to such industries as they seek to decarbonize.

Besides providing process heat, Realta’s reactor can also serve as a volumetric neutron source (VNS). Interested customers include government contractors in space and defense, and DARPA.

The DOE has even expressed interest in funding a Realta reactor as a fusion component testing facility where various materials and components could be tested under neutron irradiation. Even today, there is not a facility that can generate the required neutron fluxes to replicate a fusion reactor. So, such a facility made by Realta would be very valuable to fusion research as a whole, including all the other fusion startups.

#### Outlook on Realta Fusion

Compared with other MCF schemes, the mirror has several advantages:

simplest magnet geometry out of any MCF scheme → simpler construction and maintenance

no internal plasma current → no current-driven instabilities (e.g. disruptions)

power and particle exhaust are handled in large expander regions, far away from the expensive HTS magnets


At the same time, mirror physics is arguably less well-proven compared to other MCF schemes like tokamaks. Realta also faces substantial risk in integrating all those advancements in mirror physics mentioned above (and many more) into one device. And extrapolating fusion performance to higher levels rarely goes as planned.

It may be surprising to hear that Realta Fusion is actually collaborating with Commonwealth Fusion Systems (CFS) to manufacture Realta’s HTS magnets. It’s less suprising when you consider that CFS is really a magnet company first, and a tokamak company second.

One can envision a world where CFS succeeds no matter which fusion concept ends up providing the cheapest energy. There’s a big market for HTS magnets, not just in fusion coming ahead, but MRI machines, particle accelerators, and much more.

In the nearer term, both companies have something to gain from this collaboration, including physics knowledge and fusion engineering know-how.

Considering some of the questionable fusion startups out there, it’s worth taking a look at the Realta team itself and the strategic choices they’ve made. First of all, the team has extensive plasma physics and fusion experience.

Meanwhile, the wider WHAM collaboration includes MIT and CFS, others at UW Madison, and General Atomics. Realta has also reassuringly had fairly open engagement with the rest of the scientific and fusion community, including presentations and journal articles describing their plan ahead and in-depth physics.

Also, Realta Fusion is one of the winners of the DOE Milestone-Based Fusion Development Program. Much better funded fusion startups also almost certainly applied but did not win one of these awards. This is a big endorsement from the DOE. When presented with more physics and engineering details than we are privy to, and their plans for a pilot plant, the DOE selected Realta Fusion over other, better funded fusion startups.

Of course, it remains to be seen if Realta can successfully apply HTS magnets to mirrors as well implement all their physics strategies into their upcoming experimental devices. But Realta clearly has a compelling case in both their reactor design and go-to-market strategy.

If they succeed, they will probably have one of the cheaper fusion reactor designs thanks to HTS magnets applied to the simple, axisymmetric, cylindrical geometry of the mirror.

[1](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-anchor-1-135385038)

Ironically, for magnetic fusion reactors that’s largely thanks to those fancy HTS magnets.

[2](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-anchor-2-135385038)

Technically it will be an end cell. End cells are used on tandem mirrors, explained a few paragraphs down.

[3](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-anchor-3-135385038)

Some tricks can be played to avoid this, like streaming in a warm gas to fill in the ambipolar hole. This was successfully done on some of the the mirror machines at Lawrence Livermore National Laboratory.

[4](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-anchor-4-135385038)

It is not entirely clear whether this refers to scientific or engineering breakeven. But, in any case, scientific and engineering breakeven are generally pretty similar for magnetic confinement fusion devices (unlike laser-driven inertial confinement fusion).

[5](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion#footnote-anchor-5-135385038)

A general lesson we can draw from the history of fusion research: it’s easy to draw a line up to breakeven and beyond. It’s far harder (as the 10+ year effort for ignition on NIF showed) to demonstrate it in reality.