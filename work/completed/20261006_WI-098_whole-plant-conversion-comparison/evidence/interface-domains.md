# New calculation domains and diagnostic conventions

Implementation interface supplement to accepted design; domain handling does not resize equipment. Real outputs are finite on admitted calculation domains. A domain refusal is a failed evaluation and cannot rank. Finite outputs with a zero support flag remain failed cases. The native interface defines names in `models/library/analyses/whole_plant_conversion_accounts.sysml`; common station assumptions are owned by steam_operating and gas_operating binds them, without giving steam a different reactor.

| Calculation | Algebra refusal | Finite support predicate |
|---|---|---|
| Supplied Source Basis | Nonpositive heating efficiency, reference fusion or divertor area denominator | Positive calculated fusion, efficiencies in(0,1], positive hot multiplier; separate heating/divertor/source-ceiling margins enforce capacities |
| Captured Reactor Offer | None for finite capture discriminator | Discriminator48001; immutable fixed outputs; field/current/fit/strain/stress and cryo margins calculated from capture values, not writable pass bits |
| Fuel Supply Accounts | Burn fraction outside(0,1], nonpositive masses/reaction energy conversion | Availability in(0,1], recycle in[0,1], extraction in(0,1], nonnegative selected stock/TBR/prices; separate stock and processing margins |
| Whole Plant Capital Accounts | None for finite amounts | All input amounts/rates nonnegative; branch discriminator exactly0 or1 |
| Whole Plant Operating Ledger | None for finite amounts | Availability in(0,1], conditional auxiliary water25C, every electrical demand nonnegative, primary motor loss>=−1e−10MW arithmetic tolerance; separate auxiliary/net/annual-net margins |
| Whole Plant Lifecycle Ledger | Positive integer operating horizon, rate>=0, availability in(0,1], positive wall load and material/magnet/primary lives required | Nonnegative construction duration, initial capital, routine-service fraction and terminal fractions; economic_defined additionally requires positive discounted export and annual net-grid energy; failed economics returns finite zero LCOE plus flag0 and cannot rank |
| Conditional Cryogenic Demand | Nonfinite or negative q_nuc/extra_cold demand; nonpositive volume/COP fraction or temperatures outside0<Tcold,Tintercept<Tambient | Nonnegative operands and Carnot fractions<=1; cold/intercept capacity margins consume independently selected offer ratings; capacity failure remains finite |
| Actual Exchanger Approaches | None for finite temperatures | Both actual terminal gaps strictly positive, no30K replacement threshold |
| Temperature Kelvin | None for finite Celsius input | Unit conversion only; consumers own thermal domain |
| Supplied Primary Capacity | None for finite pressure inputs | Selected pressure, total electric and per-path flow minus demand>=0; path count exactly14 for the retained installed primary inventory |

Fuel fields ending `_atom_residual` are normalized dimensionless conservation residuals. For annual productive reactions R and loss factor `(1-b)/b*(1-rho)`, D uses `(D_purchased_atoms-R-R*loss_factor)/max(R,1)`. T uses `(external_kg+usable_kg-need_kg-surplus_kg)/max(need_kg,1)`. Li6 uses `(Li6_purchased_atoms-R*TBR)/max(R,1)`. These definitions avoid judging cancellation of approximately1e28 atoms by an absolute one-atom tolerance. Independent checks should use1e−12 dimensionless tolerance and also compare every mass/flow individually. Cost and power residuals retain USD2025 and MW units, respectively; use1e−4USD and1e−9MW absolute cancellation tolerances plus independent component equality checks.

Steam purchased salt stock is conversion `capital_2`; its explicit secondary spare is inside `capital_1`. Gas transport `capital_9` includes inseparable stock within the reviewed installed-cost proxy. No stock is added to that gas aggregate a second time.

The captured stress margin uses the native selected casing allowable800MPa.650MPa is the old winding-stress calibration reference and is not an allowable. The first development run and its independent finding are retained; the corrected final run has a different executable identity.
