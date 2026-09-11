# Radius meaning: parent source check

[AGENT] Parent assessment for T-021, 2026-09-11. This checks the existing model's intended reference quantity. It does not infer exact modular-coil geometry or approve a new source/relation.

## Source observations

The parent directly viewed Table 2 in both the original extraction companion and the registered KIT mirror's image set in the primary checkout. Both images label **Major plasma radius [m] = 12.7** and **Minor plasma radius [m] = 1.3**. The registered mirror image is copied as `stellaris-table2.png`, SHA256 `433306f0a4522a08a1889d8c76a3de64b51b73d148e61c33a0261c89b66eae73`. Original read location: `/home/reid/1cfe/fusion-tea/knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/images/page_002_table_0.png`. The primary checkout was read only.

The corresponding raw PDF SHA256 is `7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865`, matching `knowledge/SOURCE_INDEX.md`'s registered Stellaris Design Paper. The PDF was hashed, not newly extracted or read in full. The original iter-01 image SHA256 is `a54b61528687bb4554d2c6ff9d02bb6b8486ece711004faf5de182da54d9d102`; the two differently encoded images show the same relevant table values. The older text extraction's corrupted table is not quantitative authority.

## Model and existing source interpretation

`models/library/analyses/mfe_magnet_field.sysml:9–29` explicitly uses the same Table 2 major radius for the coil-set axis-field calculation and its axis-linkage calibration. `models/library/cost_structure/mfe_power_core.sysml:65–85` defines `R0` as major radius and separately defines `r_coil` as coil-bore radius. The two quantities must not be conflated.

The existing model's reference `/home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py:273–281` calls `R0` the toroidal major radius and `r_coil` the coil-bore radius derived from the vessel outer radius. The file is clean at repository revision `02543850089be175ea7c28b92a8b2a4184e1637e`, SHA256 `66e8102965cab6cc6673eb6f4fed9fee817c962884b243faf5e6ad026cb89f10`. This is a current reference-code observation, not a fresh execution or new source approval. The historical WI-032 spec (`work/completed/20260827_WI-032_cold-volume-basis/spec.md:32–46`) interprets `2*pi*R0*B/mu0` as current linking the magnetic axis and distinguishes the coil-bore proxy length. That historical interpretation is supporting model-intent evidence, not an independent physical measurement.

## Assessment

[AGENT] The present supported toroidal plant uses one major plasma/axis scale. Its existing sources and documentation do not declare a second independently variable magnet major-radius surface or an offset relation. The independent `magnet.R0` literal therefore represents duplicate ownership of the intended plant quantity. Binding the supported plant's magnet major-radius input to its authoritative plant radius would express that existing intent. Standalone reusable magnet calculations may still accept their own radius inputs; the caller inventory must determine the correct binding location.

This conclusion does not equate all real stellarator geometric surfaces. It does not source a radius operating envelope, repair broader algebraic domains or certify magnet/plasma physics. The ordinary baseline remains the already sourced 12.7 m; no new baseline value is proposed.
