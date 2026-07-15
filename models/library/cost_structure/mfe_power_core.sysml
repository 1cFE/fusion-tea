package mfe_power_core {
    private import ScalarValues::*;
    private import cas_hierarchy::'CAS22 Power Core';
    private import economic_parameter::'CAS Scope';

    // =========================================================================
    // MFE-divergent CAS22 sub-account TYPES
    //
    // CAS22 (Power Core) is the IFE/MFE divergence point (DI-002). Sub-accounts
    // 22.1.3 (magnets), 22.1.4 (heating & current drive), and 22.1.8 (divertor)
    // have completely different cost structures by confinement approach; each is
    // tagged `mfe_divergent` here, mirroring the IFE side. These are concept-
    // agnostic TYPES — no tokamak/stellarator values (MR-WI009-8); WI-011 sets
    // concept values on the costed components below.
    // =========================================================================

    part def 'CAS22.1.3 Magnet System' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.3 (MFE): Magnet System. The MFE analogue of the IFE
        driver — the dominant MFE power-core cost driver (RQ-1). Superconducting
        or resistive confinement coils (TF/CS/PF for tokamaks, modular coils for
        stellarators).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:271-444 (C220103 coil costing)
        **Basis**: DI-002 — CAS22.1.3 is MFE-divergent; coils replace the IFE driver
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    part def 'CAS22.1.4 Heating and Current Drive' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.4 (MFE): Supplementary Heating and Current Drive
        (NBI, ICRF, ECRH, LHCD). The MFE analogue of IFE ignition/target energy.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:446-459 (C220104 supplementary heating, per-MW costs)
        **Basis**: DI-002 — CAS22.1.4 is MFE-divergent (heating vs ignition)
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    part def 'CAS22.1.8 Divertor' :> 'CAS22 Power Core' {
        doc /*
        CAS Account 22.1.8 (MFE): Divertor (W monoblock cassettes on CuCrZr heat
        sinks). The MFE analogue of the IFE target factory.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:556-570 (C220108 divertor, power-scaled)
        **Basis**: DI-002 — CAS22.1.8 is MFE-divergent (divertor vs target factory)
        */
        :>> scope = 'CAS Scope'::mfe_divergent;
    }

    // =========================================================================
    // Concept-agnostic costed components
    //
    // Specialization chain (SV-022):
    //   'Magnet System' -> 'CAS22.1.3 Magnet System' -> 'CAS22 Power Core'
    //     -> 'CAS Account' -> 'Costed Component'
    // 'Costed Component' provides capital_cost + cas_code; 'CAS Account' adds
    // account_name + scope.
    // =========================================================================

    part def 'Magnet System' :> 'CAS22.1.3 Magnet System' {
        doc /*
        Concept-agnostic magnet/coil system carrying the coil-cost parameters
        for the bilinear toroidal conductor model. All parameters are inputs —
        WI-011 binds tokamak/stellarator values. `capital_cost` is populated by
        the 'Magnet Coil Cost' calc (mfe_magnet_cost.sysml).

        Parameters (all concept-set, MR-WI009-8):
          B            — field at the loop center (axis) [T]
          R0           — major radius [m]
          r_coil       — coil-bore radius [m]
          G            — geometry factor (tokamak 4*pi^2, stellarator 8*pi^2)
          coil_markup  — conductor -> installed magnet manufacturing markup
          cost_per_kAm — conductor cost [$/kA-m], by coil material

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:427 (total_kAm), cas22.py:440-444 (SC coil cost)
        **Basis**: MFE coil conductor-quantity model; parameterized for any MFE concept
        */

        attribute B : Real;
        attribute R0 : Real;
        attribute r_coil : Real;
        attribute G : Real;
        attribute coil_markup : Real;
        attribute cost_per_kAm : Real;
    }

    part def 'Heating and CD' :> 'CAS22.1.4 Heating and Current Drive' {
        doc /*
        Concept-agnostic supplementary heating / current-drive costed component.
        Carries `capital_cost` (inherited from 'Costed Component'); the per-MW
        heating mix and its cost are set per concept in WI-011.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:453-459 (C220104 per-MW heating costs)
        **Basis**: MFE heating/current-drive account; concept-agnostic carrier
        */
    }

    part def 'Divertor' :> 'CAS22.1.8 Divertor' {
        doc /*
        Concept-agnostic divertor costed component. Carries `capital_cost`
        (inherited from 'Costed Component'); the power-scaled divertor cost is
        set per concept in WI-011.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:570 (C220108 divertor, power-scaled)
        **Basis**: MFE divertor account; concept-agnostic carrier
        */
    }
}
