---
source: "https://www.avalanchefusion.com/blog/cwfest2023"
source_type: "url"
extracted_at: "2026-03-29T19:17:28.435214+00:00"
content_hash_sha256: "24fff2fa63ff13f983e0ee6656db1139fe9ca9de8c479126434c879232427d3c"
backend: "trafilatura"
title: "Avalanche | Behind the Scenes of Our Compact Fusion Machines"
---

Fusion plasma conditions are notoriously difficult to create and harder yet to maintain. One commonality between most attempts, is that the fusion cores are huge, and the infrastructure to feed them is massive. Avalanche’s compact fusion machine is markedly different here; its fusion core can be held in your hands, and fully integrated could fit in a pickup bed.

This year at the Canadian Workshop on Fusion Energy Science and Technology (CWFEST-2023), [ Robin Langtry](https://avalanchefusion.com/about/team/robin-langtry/), co-founder and CEO of Avalanche Energy peeled back the curtain on Avalanche’s compact fusion machine:

Robin Langtry is an entrepreneur and scientist leading Avalanche Energy and the development of the Orbitron. In 2020 Dr. Langtry invented the Orbitron electrostatic fusion reactor concept and much of his experience with computational fluid dynamics, massively parallel cloud simulations, acoustics and hydrodynamic stability were pivotal to the ideas that led to that discovery. Today, in addition to his role at Avalanche as CEO he also leads the scientific team developing the science of Orbitons via theory, simulation and experimental test programs.

**Peter Schwanke:** We will then move next to our next presenter here, this is Robin Langry from Avalanche Energy and providing a presentation on Electrostatic Orbitron Fusion Reactor overview of scientific program at Avalanche Energy. So with that, please proceed.

**Robin Langtry:** Thank you very much. I'm really happy to be here. Super cool talks. Thank you very much for holding this. It sounds like this WebEx is being hosted in Ottawa. So it's, it's cool to be back in my hometown, virtually.

I grew up in Ottawa, did a master's in in aerospace at Carleton University, and then went to Germany to do a PhD in turbulence modeling, which brought me to Seattle and Boeing and then ultimately to Blue Origin, designing rockets that fly backwards through their plumes. And you talked about fusion being hard. That was a hard one to more recently, I founded a fusion company a couple years ago.

And so that's what we're going to be talking about today, Avalanche Energy.

So we're developing what we call the world's smallest fusion reactor. So I think the previous talk was talking about what are the biggest fusion reactor concepts I've seen? And so I'm gonna take sort of the contrarian view and say, small could be really cool, too.

And so I'll start with sort of a question, what is an important truth? What important truth the very few people agree with you on? And so this is a really famous question in the startup world, from Peter Thiel, from his book Zero to One notes on startups and how to build a future.

A lot of really impactful startups and technologies started with an answer to this question. SpaceX, for example, Tesla.

So what I'm here to tell you today is that fusion reactors do not need to be large billion dollar machines. Small fusion power can be mobile, distributed and mass produced at scale, kind of like a Tesla battery pack.

So we're talking about doing electrostatic fusion here, using very high voltages in a very small compact form factor. So 10s of centimeters in diameter is the plasma core we're talking about. People have proposed electrostatics machines before. We'll talk about this a lot over the course of the talk, is electrons, co rotating with ions, in what are called E Cross B fields, is the key to unlocking small scale fusion.

The electrons do two things. The first thing is they help mitigate what's called space charge effects, which is something you have to worry about in electrostatic fusion machines. The electrons mitigate space charge and help you get to really high plasma densities. The second thing electrons do is their co-rotating with the ions. And so we have to worry about ion thermalization, right. And so electrons are light, they travel really fast. If they're co-rotating with the ions, you can think of them almost like a tailwind at the back of the ions. And if we can get the right tail wind force, we can actually have the ions burn longer long enough to fuse significantly.

So that's like the two things that we're trying to do that are really kind of novel that I don't think have ever been attempted before. And certainly not at the scale for an electrostatic shooting machine.

So the other thing is, the previous talk was talking about bigger is better? Well, fusion reactor size really determines the capital, the headcount and the development time- the speed that you're working with, right. So if you know a lot of fusion companies are targeting grid scale electricity, most of those approaches are thermo nucular in nature.

Your reactor size is anywhere from the size of a house to a warehouse. And so those are going to have capital costs to commercial operation- like first commercial operations, probably in a billion dollars or more, those companies are probably going to be headcounts of hundreds to 1000s of people when you're there. And the first commercial operations are probably more than six years out.

If you can do a small fusion reactor, you can build them in weeks, instead of years. Your iteration time on that machine is days instead of sort of months. And then in terms of scaling into the markets and trying to really help decarbonize the economy. Large scale fusion is pretty much going to be like a civil engineering project.

Whereas if you have a small fusion reactor, you can sort of mass produce those in a factory, kind of like almost like automotive manufacturing. So that's the really interesting thing. At Avalanche, we are trying to develop a compact fusion machine that's targeted more at mobility and distributed energy applications.

So think about like, micro grids up in the Arctic, things that could power sort of long haul trucking, aviation maritime shipping, we're trying to do that with capital costs to first come up commercial operations is less than a billion dollars. Nomily, I hope that company is less than 200 people in headcount. And we're trying to do that really fast.

So in under six years, if possible, you can see a picture of the plasma core we're talking about to the right here. It's called an Orbitron. And so what is an Orbitron. So an Orbitron is kind of a mix of two different plasma devices, combining orbitrap and magnetron Orbitron. Both of these devices exist.

An orbitrap is used in mass spectrometers, it's a purely electrostatic device. And so the way it works is you have this cathode, this rod at negative voltage, and then a specially shaped anode at ground around it. And you shoot an ion beam into the orbitrap, to give it an azimuthal velocity component. And if that beam has the right energy matched to the cathode voltage, the ions will go into orbits around the cathode, just like a satellite orbiting the Earth, if you will.

And then the ends of the device are pinched, so that if the ions get near the end, they see an X axial reflecting electrostatic force. So you can think of this. It's very analogous to a magnetic bottle, except it's using electrostatics to create that bottle shaped field. Orbit traps are really good at confining ions for long periods of time. That's why they're used in mass spectrometers. It's electrostatic in nature.

So it's pretty straightforward to show that you can scale this thing up in terms of size and voltage, and start confining those ions at really high fusion energies like 60 KV or greater. The main problem that orbit traps have is space charge. So you you're loading ions, and you get to this point where there's so many positively charged ions in there, that the trap is full, if you try and add more to leak out the sides, you basically hit the space charge limit. So you need to confine electrons with those ions. And that's sort of the key innovation that we came up with a couple of years ago. And what essentially we're doing is we're combining an orbitrap with a device called a magnetron.

So magnetrons were invented in the 30s, some of the first radar devices were based on them, there's a picture of one in the middle here. magnetrons are coaxial devices. So you have a cathode rod in the middle at negative voltage, you have an anode at ground around it, electrons are emitted from that cathode. And because it's negatively charged, they want to accelerate away and hit the anode. So you have current running between your cathode and your anode. And what you do is you add an axial magnetic field, that's just strong enough to bend the trajectory of the electrons back towards the cathode.

That's called the hole cut off condition and magnetron science. And what happens is your current drops to almost zero. And so now you have electrons confined in the space between the cathode and the anode. And as you increase that magnetic field further, the gyro radius of the electrons shrinks, they see less of the full potential gradient, and so their temperature drops as well. And so what we're basically doing is combining these two devices to try and offset space charge effects.

So that cathod of the Orbitron is this figure on the right. So you have ions that are in elliptical orbits around this cathode, where those elliptical orbits cross the crossing at Fusion type centres of mass energies. And then you have electrons being emitted from the cathode, doing their EEG Crosby orbits, and everything is co-rotating in the same direction in the figure, it's counterclockwise.

And that's a very important reason for that, which comes back to coulomb collisions, and I'll get into more in the talk. So that's what an Orbitron is. So where does the Orbitron fit in sort of the taxonomy of different fusion confinement schemes? Right, so this is a chart from Derek Sutherland at zap energy. So you can think of the Orbitron it's down here below underneath inertial electrostatic confinement. You can think of it as kind of a cousin of the magnetic mirror approaches.

So in the Orbitron, the electrons are magnetised. So they're combined like E cross BB like a like in the mirror like in CML, CMF X or wham or routa. But the ions are not magnetised. They're confined electrostatically around that cathode. So all the force that's confining them comes from the electrostatic gradient. It doesn't come from the magnetic field.

So as a result, we have relatively low magnetic fields point six Tesla. Very compact diameters, so like 10s of centimetres, but we have very high voltages like hundreds of kilovolts in this 10 centimetre diameter package.

So we have to get very good at vacuum high voltage to operate these devices. Okay, fusion rate scaling. So we've looked at a lot of particle and cell simulations to try and understand how the Orbitron will scale as a function of voltage and magnetic field. That's illustrated in these contour plots here. So the x-axis is the cathode voltage, you can think of that like fusion energy, and then the y axis is the magnetic field you can think of that like fusion density.

The contour plot on the left is for a deuterium deuterium neutron source with a six centimetre radius, so 12 centimetre diameter, so it's about this big. And the contour plot on the right is for deuterium tritium in kilowatts. So the really interesting plasma parameter space is sort of 300 kilovolts point for Tesla. That's where you have sort of the optimum conditions, which are for deuterium tritium.

And so that would be making sort of mid to high 10 to the 11 neutrons per second, which is a really interesting neutron source. And then if you're operating with deuterium tritium, that would be about a kilowatt. And so if our cathode is consuming 600 Watts and our iron guns are consuming 400 Watts, that is essentially like a huge sigh of something like one in that device.

So that's where we're ultimately trying to go. And we're trying to understand sort of how to devise scale Orbitron or non thermal plasmas, so the ions are on magnetised and the electrons are confined via e Crosby. The other interesting thing about Orbitron is that the ions you can vary the ion collisional energy via voltage and beam energy independently from the electron energy which is basically controlled via the magnetic field in that magnetron mode.

So that makes them really interesting devices for exploring different fusion plasma parameter spaces you can control the electron temperature independently from the ions which I think is pretty unique as plasma confinement devices go alright. Okay, so, electrostatic and non thermal fusion plasmas are controversial in Fusion sciences. So in 1995, Todd Ryder published his thesis, where he looked at the recirculating power and the power balance for a range of non thermal or non Maxwellian fusion machines. And he concluded that for all possible types of fusion reactors, if the major particle species are significantly non Maxwellian, or radically different energies, the recirculating power will always substantially exceed the fusion power. And so, in 2003, Ross Docker and co workers at trial published sort of a rebuttal of that. They said the large recirculating power that Ryder attained was a consequence of assumptions in particle disk distribution functions in this reduced order model that he was solving that simplify the calculations but have no physical basis.

So if I'm using a hockey term, this is like plasma physicists like dropping the gloves going at it. I think the easier thing to grok is really the critique of lab fee and Mannheimer from NRL in 1998. So they said that the coulomb collision rate through 90 degrees of scattering for PB 11 is 37 times faster than fusion.

So I'm paraphrasing here, but for DT it's 25 times faster. And so colliding beam fusion is not feasible, because the particle loss and energy energy dissipation rates are orders of magnitude faster than fusion. That is a very good argument. And that is the one that we're going to have to address if we're ever going to get to an energy fusion machine with a non Maxwellian plasma.

So, at a high level, a lot has been written about electrostatic fusion and non Maxwellian plasmas, I think you can really summarise it as two key points, electrostatic approaches to Fusion cannot achieve high ion densities due to space charge effects, and electrostatic or non thermal approaches to fusion and cannot achieve net energy due to excessive coulomb coalition losses. Those are like the two major arguments against what we're doing here.

Much of this controversy stems from modelling assumptions in these sort of reduced order models that people work with to try and understand the viability of a fusion concept. And the real fusion, the real confinement physics are super complicated. And you can't always capture all those physics in a reduced order model. So we do find these two high level critiques space charge and coulomb collisions are valid.

And the Orbitron has unique aspects that address both issues. So the way we're approaching this as we're developing first order models to try and understand the high level Orbitron physics. We're developing particle and cell simulations to incorporate that more complicated, complicated physics that you can't actually include in a reduced order model. And then ultimately, we're building experimental prototypes to anchor our first order models and our simulations.

And that's actually how you're going to really demonstrate it. So the first critique space charge density, so let's get into it. So this is that you can achieve high densities in electrostatic fusions. So remember, we're confining electrons, that's really key to offset in that space charge. This is a particle cell simulation demonstrating that. So basically, what we're doing is we're loading ions and electrons into the Orbitron. Electrons are the orange curve, ions or the blue curve, and you can see the ion density on the left over here, the electron density on the right over here.

So initially, they're uncoupled, right, they have their own confinement physics, they're not really interacting, so maybe for the odd collision, and then what happens is you get to the electron space charge limit first. And so the electrons start to couple with the ions by a space charge. So where you see a high population density of ions, you start to see a high population density of electrons to make the plasma quasi neutral. And then as you go, you keep going up, you see that you're basically blowing up this really nice, well confined plasma bubble, where you have quasi neutrality being enforced via space charge coupling between the ions and the electrons. So that's the simulation.

This is well past the space charge limit that you could achieve if you didn't have electron confinement alone. And then here's a sort of movie of this thing. So we're loading ions in on the left electrons in the right, we're going to mess with the timescale so you can kind of see what's going on. So you'll see that the ions look frozen, they're not, it's just we've slowed down time. So you can kind of see what the electrons are doing on the right. And then we're going to speed up time again, and continue to load ions on the left and electrons on the right. And you can see, as you get to these higher densities, they start to couple via space charge, where you have space charge mismatches, the plasma will oscillate that does work on the electrons and pulls them off their field lines to the regions where you have high ion density. And then once you've neutralised, the plasma ion space charge at the plasma kind of settles down and continues to load up.

You can see sort of an axial mode developing here, as they're kind of loading up and then we slow time down again, and look at the the behaviour of the electrons on the right, in that, timescale the ions look really slow, and then we speed time up again and keep going.

So this loaded up way past the space charge limit that you could ever achieve via electrostatic confinement alone. So that's a really interesting thing that kind of addresses the first critique of electrostatic fusion. And now we gotta go prove this experimentally. The other critique so that non thermal approaches to Fusion cannot achieve net energy due to excessive coulomb losses. We're attempting to do that with a first order model and also with simulation.

So we've kind of gone through using collision frequencies from NRL plasma formula and build sort of a first order model of coulomb collision transport for the Orbitron. So basically, what we're doing is we're summing all the different coulomb collision processes in terms of whether they cause the ions to lose energy, and spiral down into the cathode or gain energy and spiral up into the anode. Electrons always lose energy to ions and basically spiral from cathode to anode.

That's sort of how the physics works. So we sum all those currents for the different processes, we convert them to power based on the energy of the particles when they hit the walls. And then we develop this very simple equation for for Q plasma, which is basically the fusion rate on the numerator, divided by a sum of all of these different collisional, processes that down, scatter things to the cathode up, scatter them up to the anode, and then bremsstrahlung X rays. And so we sum all that up. And then what we do is we sweep the centre of mass energy of those ions, we sweep the electron temperature and we look at that plasma like, is there something interesting there from a queue? And sure enough, there is. Once you get to sort of 63 KV centre of mass, you see a peak makes sense. That's what sort of the peak fusion rate cross section for DT.

What is interesting is at low electron temperatures, the queue is really low. And then you hit this sort of peak, and then you go to the right, it drops off again. So like what's going on there? The best way to kind of understand that is to look at the currents of the different particles from this 1d model. So we have deuterium tritium electrons. Positive means the particles being up scattered to the anode negative means on the wire just means the particles being down scattered to the cathode.

And then we've got electron temperature on the x axis. So at low electron temperatures, everything's getting up scattered to the anode. Basically, the electrons are colliding with the part of the ions, transferring energy to them, they're basically all getting up scattered to the anode. The really interesting thing is around 15 KV electron temperature. That's where the deuterium tritium collision term.

So deuterium slowing down on tritium, is balanced by deuterium being sped up by electrons. So those two collision frequencies are approximately similar magnitude. And that's causing basically a low current of electrons. So basically, the deuterium is not speeding it up, and it's not slowing down. As you go to the right, now your electron collision frequencies drop. And so the deuterium starts to fall into the cathode, because it's basically slowing down on tritium, and the scattering of the tritium from the electrons is starting to diminish. So around 10 to 20 ke V, electron temperature seems like this really interesting, potentially low loss plasma.

Let's go to simulations and see if you know that shows up. So we're doing a bunch of coulomb scattering simulations in a code called warp x. That's being developed by Lawrence Berkeley National Lab, so I'll show a movie in a second. So what we're doing is we're injecting ions into these elliptic orbits, electrons are born from the cathode magnetron style. And then we're looking at the plasma as these things thermalize, there's a couple caveats here, the time step is set by the electrons. So in the thermalization, time per lampion, manheimer is about point o-five seconds, so we can't possibly simulate that at the densities we're talking about.

So what we do is we actually run the simulation at much, much higher densities, and then we density scale the results back down to something that's more real realistic to what the Orbitron could actually achieve. So let's see it.

So this is, loading the ions in on the left, electrons are being loaded from the cathode on the right. So right, now collisions are off, we're just basically loading the particles in. After that, we're going to stop the loading, turn on collisions and just run the plasma and watch it thermalize, you can see the ion beams on the left that are thermalized on each other.

Super cool.

We're going to speed up time in a second to try and get to the end part. And you can see these are thermal lysing on each other, they're going into rotation, you can see the other really cool thing, as you can see this ring of electrons, as they transfer their energy to the ions, the electrons lose energy, and so they start to orbit higher and higher away from the cathode.

And so they start to diffuse towards the anode. So per rider and Lampe and Manheimer, those reduced order models would say that, after point o five seconds, all of the particles should have scattered outside of the trap, or the ones that are left should have thermalized. So there's no collision, you just have solid body rotation. And that's not what we're seeing in the simulation.

So the density scale is results to about point oh, from where they were wrong to like the actual density that we're interested in. It's about point of five 2.8 seconds. So well past, the thermalization time predicted by Lampe and Mannheimer, we still see significant particle density, we still see fusion rates that are significant in the sim.

So I think there's really an interesting plasma parameter space between pure beam beam fusion and pure non Maxwellian fusion that we're observing here. And it's, I think that's going to be like a really interesting thing going forward in terms of plasma densities and, and collisions and energies and stuff. And there may be a really interesting way to run these devices that is efficient. Okay, so that's the coulomb coalition part. So getting into the experimental program.

So this is our lab in Seattle, Washington. It's 15,000 square feet. We have two fusion prototypes. Right now we have Neo which is in the foreground, that's the first fusion prototype we ever built. And then we have Marty in the background that's in a sort of concrete castle for X ray shielding and neutron shielding. This whole thing is designed to eventually get to 10 V 11 neutrons someday.

And then we also have a bunch of high voltage and iron testing and a material science lab. It's called channel Fs.

This is a picture of Neo upfront, so you've got the ion gun, creating the beam, you've got the Anza lens that focuses and steers the beam, the Orbitron is in the middle here. You've got a high voltage feed through that we've designed for bringing in the high voltage. And then Neo is operating with permanent magnets and about point O five Tesla, so pretty weak magnetic field, and then it's got a bunch of diagnostics.

So in terms of our diagnostics capability, we have scintillators with pulse shape discrimination. We have helium three and neutron counters, we do argon spectroscopy be X ray spectroscopy. And we also have a neutron camera which has sort of a restricted field of view that's looking at different positions inside the Orbitron. And trying to discern what is the Beam Target fusion.

So from ions crashing into the cathode, versus the beam beam fusion from this actual like coupling that we're trying to predict. This is pulse shape discrimination. On the left is just sort of background. And on the right is when the Orbitron is running. So basically, the cathode is energized ions are shooting in and going into orbits, you see, we make a lot more neutrons that are approximately two and a half MeV. So they're in the right energy range for fusion.

This is the second prototype, Marty. So this thing is designed to go to 300 kilovolts. We've gotten up past 200 kilovolt, so it might be the highest voltage electrostatic fusion machine anyone's ever built. It's basically incorporating a lot of our learnings from Neo.

In terms of the the second time you build something you always kind of get a little bit better in terms of our experimental program current status.

So Neo is operating about point 0-five Tesla 100 kilovolts. Marty has hit 200 kilovolts. We have superconducting magnets that are supposed to show up in January. So that's good to sort of uncap the magnetic fields that we can operate in. And then we're trying really, really hard to get Marty up to 300 kilovolts. And eventually, we want to get to 300 kilovolts. Point three Tessa so making about mid 2011 neutrons per second. That's the kind of plasma conditions where it makes sense for us to operate with tritium. And so if you go across, operating with tritium that would be about a kilowatt of fusion power.

And basically operating there we're gonna go explore trying to find these really efficient plasmas where the coulomb collisions are minimized, and hopefully we can get to like a Q greater than one condition operating with deuterium tritium. If we can do that, the next step is you scale up in terms of voltage and magnetic field, you start making, five kilowatts, 10 kilowatts. Now you start to have a really interesting small scale fusion machine.

In terms of the team, we're at 33 People now 13 PhDs, supported by major investors, lower carbon offenders fund, and it's hard to believe, but we're probably the largest, most well rare resource team that's ever attempted electrostatic fusion, you know, very high level summary.

There's these two critiques out there for electrostatic fusion, we've addressed the density one, I think pretty well by a pic. And we're very close to demonstrating experimentally on Neo, the coulomb collision one is going to be a longer term thing. We think there's a really interesting plasma out there that will be efficient and basically demonstrating this experimentally with deuterium tritium fusion is ultimately how we intend to develop a queue greater than one small fusion reactor.

So I'm finished.

Now I will leave you with this final sort of movie of what we hope to get to someday, with a very small compact fusion reactor. The plasma is based on our particle simulations. So it's not artistic license is really what we think the plasma beams are going to look like when we're there.

Thank you very much.