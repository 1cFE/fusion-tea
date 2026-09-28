    calc def 'Operating Heating Power' {
        doc /* Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11 */
        in attribute p_required_in : Real;
        in attribute eta_source_in : Real;
        in attribute eta_couple_in : Real;
        out attribute p_coupled : Real = p_required_in;
        out attribute p_delivered : Real = p_required_in / eta_couple_in;
        out attribute p_wallplug : Real = p_delivered / eta_source_in;
    }
    constraint def 'Heating Efficiency Positive' {
        doc /* Constant conversion efficiency domain. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: source-output and plasma-coupling efficiency definitions **Basis**: positive physical fraction for inverse conversion **Last Updated**: 2026-09-11 */
        in attribute efficiency : Real;
        efficiency > 0.0
    }
    constraint def 'Heating Efficiency Upper' {
        doc /* Constant conversion efficiency domain. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: source-output and plasma-coupling efficiency definitions **Basis**: positive physical fraction for inverse conversion **Last Updated**: 2026-09-11 */
        in attribute efficiency : Real;
        efficiency <= 1.0
    }
