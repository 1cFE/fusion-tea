"""`StudyRunner`: the one fixed order — validate/canonicalize -> (bridge ->)
evaluate -> assess -> stage durably -> atomically commit -> advance feedback.

Failure-routing switch (design.md#implementation-notes) written against the
full four-phase `EvaluationPhase` enum, not "two phases": `ENTRY_VALIDATION`
is a bridge defect (loud, `StudyBridgeDefect`, never a case); `PREPARATION`
is a startup fault (re-raised, not a case — unreachable per-case under
`PreparedEvaluator`, B4); `MODULE_EXECUTION` (today) / `OUTPUT_WRITE`
(a future persisting backend) is terminal -> an `execution_failed` case.
"""
from __future__ import annotations

from typing import Mapping

from simkit.evaluation.evaluator import Evaluator
from simkit.evaluation.evidence import ModelEvidence
from simkit.evaluation.failure import EvaluationFailed, EvaluationFailure, EvaluationPhase

from .bridge import CandidateBridge
from .crash import NO_CRASH, CrashController
from .definition import StudyDefinition
from .evidence_io import encode_evidence
from .failures import RetryableStoreError, StudyBridgeDefect
from .identity import mint_attempt_id, mint_candidate_id
from .policy import AssessmentFailed
from .store import StudyStore


class StudyRunner:
    RETRY_LIMIT = 3

    def __init__(
        self,
        store: StudyStore,
        definition: StudyDefinition,
        evaluator: Evaluator,
        crash: CrashController = NO_CRASH,
    ) -> None:
        self.store = store
        self.definition = definition
        self.evaluator = evaluator
        self.bridge = CandidateBridge(definition.entry_models)
        self.crash = crash

    def run(self) -> None:
        study_id = self.store.study_id
        for index, (proposal_id, raw) in enumerate(self.definition.strategy.propose(study_id)):
            canonical = self.definition.validate_proposal(raw)
            if canonical is None:
                # Invalid proposal: a ProposalRecord, never a candidate/case.
                self.store.record_proposal(
                    proposal_id, raw, valid=False, candidate_id=None,
                    reason="failed validation/domain",
                )
                continue

            candidate_id = mint_candidate_id(study_id, index)
            self.store.record_proposal(
                proposal_id, raw, valid=True, candidate_id=candidate_id, reason=None,
            )

            if self.store.has_case(candidate_id):
                continue  # resume idempotency, scoped to (study_id, candidate_id)

            self._evaluate_candidate(candidate_id, proposal_id, canonical)
            self.definition.strategy.observe(feedback=None)

    def _evaluate_candidate(
        self, candidate_id: str, proposal_id: str, canonical_inputs: Mapping,
    ) -> None:
        for _ in range(self.RETRY_LIMIT):
            attempt_number = self.store.next_attempt_number(candidate_id)
            attempt_id = mint_attempt_id(candidate_id, attempt_number)
            try:
                self._run_attempt(
                    candidate_id, proposal_id, attempt_id, attempt_number, canonical_inputs,
                )
            except RetryableStoreError:
                self._record_transition_best_effort(
                    attempt_id, candidate_id, proposal_id, attempt_number, "retryable_failed",
                )
                continue
            return
        raise RuntimeError(f"retry limit exhausted for {candidate_id}")

    def _run_attempt(
        self, candidate_id: str, proposal_id: str, attempt_id: str, attempt_number: int,
        canonical_inputs: Mapping,
    ) -> None:
        self.store.record_transition(
            attempt_id=attempt_id, candidate_id=candidate_id, proposal_id=proposal_id,
            attempt_number=attempt_number, state="started",
        )
        try:
            # bridge.build is inside the failure switch (Item 9 R1): a
            # field-level bridge failure (unknown/malformed) raises
            # EvaluationFailed(ENTRY_VALIDATION) and is recorded as a
            # StudyBridgeDefect, not an uncaught crash.
            typed_inputs = self.bridge.build(canonical_inputs)
            evidence = self.evaluator.evaluate(typed_inputs)
        except EvaluationFailed as error:
            self._commit_execution_failure(
                error.failure, candidate_id, proposal_id, attempt_id, attempt_number,
                canonical_inputs,
            )
            return
        self._assess_and_commit(
            evidence, candidate_id, proposal_id, attempt_id, attempt_number, canonical_inputs,
        )

    def _commit_execution_failure(
        self, failure: EvaluationFailure, candidate_id: str, proposal_id: str, attempt_id: str,
        attempt_number: int, canonical_inputs: Mapping,
    ) -> None:
        if failure.phase == EvaluationPhase.ENTRY_VALIDATION:
            raise StudyBridgeDefect(failure)
        if failure.phase == EvaluationPhase.PREPARATION:
            raise EvaluationFailed(failure)
        # MODULE_EXECUTION (today) / OUTPUT_WRITE (future persisting backend).
        self.store.commit_case(
            candidate_id=candidate_id, proposal_id=proposal_id, attempt_id=attempt_id,
            state="execution_failed", inputs=canonical_inputs, evidence_json=None,
            failure_json=failure.model_dump(mode="json"), crash=self.crash,
        )
        self.store.record_transition(
            attempt_id=attempt_id, candidate_id=candidate_id, proposal_id=proposal_id,
            attempt_number=attempt_number, state="execution_failed",
        )

    def _assess_and_commit(
        self, evidence: ModelEvidence, candidate_id: str, proposal_id: str, attempt_id: str,
        attempt_number: int, canonical_inputs: Mapping,
    ) -> None:
        # `evidence` is immutable (D2), so policy cannot corrupt it — the old
        # "encode before assess to protect the persisted copy" ordering is no
        # longer load-bearing and is deleted (design m2). `encode_evidence` now
        # sits next to each commit. Crash-safety is unchanged: the atomic
        # durability seam is `store.commit_case(..., crash=self.crash)`.
        try:
            assessment = self.definition.policy.assess(evidence, candidate_id=candidate_id)
        except AssessmentFailed as error:
            self.store.commit_case(
                candidate_id=candidate_id, proposal_id=proposal_id, attempt_id=attempt_id,
                state="assessment_failed", inputs=canonical_inputs,
                evidence_json=encode_evidence(evidence),
                assessment_json={"failure": str(error)}, crash=self.crash,
            )
            self.store.record_transition(
                attempt_id=attempt_id, candidate_id=candidate_id, proposal_id=proposal_id,
                attempt_number=attempt_number, state="assessment_failed",
            )
            return

        self.store.commit_case(
            candidate_id=candidate_id, proposal_id=proposal_id, attempt_id=attempt_id,
            state="completed", inputs=canonical_inputs, evidence_json=encode_evidence(evidence),
            assessment_json=assessment, crash=self.crash,
        )
        self.store.record_transition(
            attempt_id=attempt_id, candidate_id=candidate_id, proposal_id=proposal_id,
            attempt_number=attempt_number, state="committed",
        )

    def _record_transition_best_effort(
        self, attempt_id: str, candidate_id: str, proposal_id: str, attempt_number: int,
        state: str,
    ) -> None:
        try:
            self.store.record_transition(
                attempt_id=attempt_id, candidate_id=candidate_id, proposal_id=proposal_id,
                attempt_number=attempt_number, state=state,
            )
        except RetryableStoreError:
            pass  # forensics only; the retry loop proceeds regardless
