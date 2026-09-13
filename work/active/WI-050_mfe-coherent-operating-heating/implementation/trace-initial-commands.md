# Initial native trace calls

These commands executed successfully before `trace_commands.py`; the resulting rows are in `data/traceability_matrix.csv`. All used the `.codex-test/run` launcher and native `agentic-mbse pm trace-element` operation.

```bash
.codex-test/run agentic-mbse pm trace-element --element 'Operating Heating Power' --file models/library/analyses/mfe_heating_chain.sysml --type 'calc def' --source-type codebase --source-doc 'Two-stage heating identities' --source-location 'models/library/analyses/mfe_heating_chain.sysml:4' --confidence Medium --assumptions 'Constant efficiencies; signed diagnostic outside burn hold. MR-WI050-1/2/9.'
.codex-test/run agentic-mbse pm trace-element --element 'Heating Efficiency Positive' --file models/library/analyses/mfe_heating_chain.sysml --type 'constraint def' --source-type codebase --source-doc 'Two-stage heating efficiency domain' --source-location 'models/library/analyses/mfe_heating_chain.sysml:4' --confidence Medium --assumptions 'Dimensionless positive conversion fraction. MR-WI050-2/9.'
.codex-test/run agentic-mbse pm trace-element --element 'Heating Efficiency Upper' --file models/library/analyses/mfe_heating_chain.sysml --type 'constraint def' --source-type codebase --source-doc 'Two-stage heating efficiency domain' --source-location 'models/library/analyses/mfe_heating_chain.sysml:4' --confidence Medium --assumptions 'Dimensionless fraction no greater than one. MR-WI050-2/9.'
```
