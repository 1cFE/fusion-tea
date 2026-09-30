"""Declare every WI-099 study case and write cases.json next to this file.

Run from the repository root:
    .codex-test/run python exploration/magnet_materials/studies/declare_cases.py

Grid (contract sections 2-8):
  - anchors D (EU DEMO TF) and S (Stellaris); fields 8-13 T on both, and 14, 16, 18, 20 T on
    anchor D (REBCO-only extension; Nb3Sn still evaluated so its status is recorded);
  - pairings common-P, native, common-C; rule families reference, both-temperature, both-fraction;
  - per (anchor, field, pairing, family): the reference offer, the insufficient element offer
    floor(0.9 n), the generous element offer ceil(1.2 n), and the reference elements with the
    insufficient (next lower listed) refrigerator;
  - one-at-a-time variants (offer_policy.VARIANTS) at the reference rule family and the common-P
    and native pairings only: the reference offer re-evaluated unchanged under the variant
    (offer_kind "reference") and the policy's variant offer (offer_kind "variant-offer").
Each case stores every design section-6 input, so it is evaluable without the policy.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import importlib.util
import sys

_HERE = Path(__file__).resolve()
_spec = importlib.util.spec_from_file_location("magnet_materials_offer_policy", _HERE.with_name("offer_policy.py"))
op = importlib.util.module_from_spec(_spec)
sys.modules["magnet_materials_offer_policy"] = op
_spec.loader.exec_module(op)

FIELDS = {"D": [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 16.0, 18.0, 20.0],
          "S": [8.0, 9.0, 10.0, 11.0, 12.0, 13.0]}
BASE_PAIRINGS = ("common-P", "native", "common-C")
BASE_FAMILIES = ("reference", "both-temperature", "both-fraction")
VARIANT_PAIRINGS = ("common-P", "native")
VARIANT_FAMILY = "reference"
OUT = _HERE.with_name("cases.json")


def point_class(B: float) -> str:
    if B <= 12.0:
        return "matched"
    if B <= 13.0:
        return "edge"
    return "extension"


def _label(anchor, B, pairing, family, variant, offer_kind, fridge):
    return dict(anchor=anchor, B_peak=B, point_class=point_class(B), pairing=pairing,
                rule_family=family, variant=variant, offer_kind=offer_kind, refrigerator_kind=fridge)


def _case_id(lb):
    return (f"{lb['anchor']}-{lb['B_peak']:g}T-{lb['pairing']}-{lb['rule_family']}-{lb['variant']}-"
            f"{lb['offer_kind']}-{lb['refrigerator_kind']}")


def _record(asm, offers, labels, policy):
    case = op.assemble_case(asm, offers)
    rec = dict(case_id=_case_id(labels), labels=labels)
    rec.update(case)
    rec["policy"] = policy
    return rec


def declare():
    cases = []
    for anchor, fields in FIELDS.items():
        for B in fields:
            ref_offers = {}
            for pairing in BASE_PAIRINGS:
                for family in BASE_FAMILIES:
                    asm = op.assumptions(anchor, B, pairing, family)
                    prop = op.propose_offer(asm)
                    if any(prop[m]["offer"] is None for m in prop):
                        raise RuntimeError(f"no reference offer at {anchor} {B} {pairing} {family}")
                    ref_offers[(pairing, family)] = prop
                    offers = {m: prop[m]["offer"] for m in prop}
                    base_policy = {m: dict(offer_basis="reference-assumptions",
                                           n_reference=prop[m]["offer"]["n_elements"],
                                           trace=prop[m]["trace"]) for m in prop}
                    cases.append(_record(asm, offers, _label(anchor, B, pairing, family, "none", "reference", "reference"),
                                         base_policy))
                    for kind, fn in (("insufficient", op.insufficient_n), ("generous", op.generous_n)):
                        o2 = {m: dict(offers[m], n_elements=float(fn(int(offers[m]["n_elements"])))) for m in offers}
                        cases.append(_record(asm, o2, _label(anchor, B, pairing, family, "none", kind, "reference"),
                                             base_policy))
                    o3 = {m: dict(offers[m], rating_cold=prop[m]["trace"]["insufficient_rating"]) for m in offers}
                    cases.append(_record(asm, o3, _label(anchor, B, pairing, family, "none", "reference", "insufficient"),
                                         base_policy))
            for variant in op.VARIANTS:
                only = op.ANCHOR_ONLY_VARIANTS.get(variant)
                if only is not None and only != anchor:
                    continue
                for pairing in VARIANT_PAIRINGS:
                    asm_v = op.assumptions(anchor, B, pairing, VARIANT_FAMILY, variant)
                    prop_ref = ref_offers[(pairing, VARIANT_FAMILY)]
                    ref_o = {m: prop_ref[m]["offer"] for m in prop_ref}
                    pol_re = {m: dict(offer_basis="reference-assumptions",
                                      n_reference=ref_o[m]["n_elements"], trace=prop_ref[m]["trace"])
                              for m in prop_ref}
                    cases.append(_record(asm_v, ref_o,
                                         _label(anchor, B, pairing, VARIANT_FAMILY, variant, "reference", "reference"),
                                         pol_re))
                    prop_v = op.propose_offer(asm_v)
                    var_o, pol_v = {}, {}
                    for m in prop_v:
                        if prop_v[m]["offer"] is None:
                            var_o[m] = ref_o[m]
                            pol_v[m] = dict(offer_basis="carried-reference", n_reference=ref_o[m]["n_elements"],
                                            trace=prop_v[m]["trace"],
                                            note="no integer element count meets the rule under this variant "
                                                 "(critical current is zero at the rule point); reference offer carried")
                        else:
                            var_o[m] = prop_v[m]["offer"]
                            pol_v[m] = dict(offer_basis="variant-assumptions", n_reference=var_o[m]["n_elements"],
                                            trace=prop_v[m]["trace"])
                        pol_v[m]["identical_to_reference_offer"] = var_o[m] == ref_o[m]
                    cases.append(_record(asm_v, var_o,
                                         _label(anchor, B, pairing, VARIANT_FAMILY, variant, "variant-offer", "reference"),
                                         pol_v))
    return cases


def counts(cases):
    by = {}
    for key in ("anchor", "B_peak", "point_class", "pairing", "rule_family", "offer_kind", "refrigerator_kind"):
        by[key] = dict(sorted(Counter(str(c["labels"][key]) for c in cases).items()))
    by["variant"] = dict(sorted(Counter(c["labels"]["variant"] for c in cases).items()))
    by["offer_kind_x_refrigerator_kind"] = dict(sorted(Counter(
        f"{c['labels']['offer_kind']}|{c['labels']['refrigerator_kind']}" for c in cases).items()))
    by["variant_offer_identical_to_reference"] = sum(
        1 for c in cases if c["labels"]["offer_kind"] == "variant-offer"
        and all(c["policy"][m].get("identical_to_reference_offer") for m in ("nb3sn", "rebco")))
    by["carried_reference_offers"] = sum(
        1 for c in cases for m in ("nb3sn", "rebco") if c["policy"][m]["offer_basis"] == "carried-reference")
    return by


def write(cases):
    ids = [c["case_id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    header = dict(
        schema="wi099-cases-v1",
        generated_by="exploration/magnet_materials/studies/declare_cases.py",
        policy="exploration/magnet_materials/studies/offer_policy.py",
        oracle="exploration/magnet_materials/oracle.py",
        contract="work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md (r3)",
        design="work/active/WI-099_magnet-conductor-alternatives/design.md (sections 2, 5 D1, 6)",
        notes="exploration/magnet_materials/studies/oracle-notes.md",
        layout="each case: case_id, labels, duty, economics, nb3sn, rebco (all design section-6 inputs), policy (trace, not a model input)",
        n_cases=len(cases),
        counts=counts(cases),
    )
    lines = ["{", f' "header": {json.dumps(header, sort_keys=True)},', ' "cases": [']
    for i, c in enumerate(cases):
        lines.append("  " + json.dumps(c, sort_keys=False) + ("," if i < len(cases) - 1 else ""))
    lines += [" ]", "}"]
    OUT.write_text("\n".join(lines) + "\n")
    return header


if __name__ == "__main__":
    cs = declare()
    h = write(cs)
    print(json.dumps(dict(n_cases=h["n_cases"], counts=h["counts"]), indent=1))
    print("wrote", OUT, OUT.stat().st_size, "bytes")
