import json
from dataclasses import dataclass
from pathlib import Path

from app.ai.provider import MockAIProvider


@dataclass(frozen=True)
class EvaluationSummary:
    total: int
    intent_correct: int
    appointment_type_correct: int
    clarification_correct: int

    @property
    def intent_accuracy(self) -> float:
        return self.intent_correct / self.total if self.total else 0.0

    @property
    def appointment_type_accuracy(self) -> float:
        return self.appointment_type_correct / self.total if self.total else 0.0

    @property
    def clarification_accuracy(self) -> float:
        return self.clarification_correct / self.total if self.total else 0.0


def evaluate(dataset_path: Path) -> EvaluationSummary:
    provider = MockAIProvider()
    total = 0
    intent_correct = 0
    appointment_type_correct = 0
    clarification_correct = 0

    for raw in dataset_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        case = json.loads(raw)
        total += 1
        result = provider.extract_intent(case["text"])
        expected_intent = case["expected_intent"]
        actual_intent = (
            "BOOK_APPOINTMENT"
            if result.appointment_type == "routine_consultation"
            and "cancel" not in case["text"].lower()
            and "reschedule" not in case["text"].lower()
            and result.clarification_required is False
            else "CANCEL_APPOINTMENT"
            if "cancel" in case["text"].lower()
            else "RESCHEDULE_APPOINTMENT"
            if "reschedule" in case["text"].lower()
            else "UNKNOWN"
        )
        intent_correct += int(actual_intent == expected_intent)
        appointment_type_correct += int(
            result.appointment_type == case["expected_appointment_type"]
        )
        clarification_correct += int(
            result.clarification_required == case["expected_clarification"]
        )

    return EvaluationSummary(
        total=total,
        intent_correct=intent_correct,
        appointment_type_correct=appointment_type_correct,
        clarification_correct=clarification_correct,
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    summary = evaluate(root / "data" / "synthetic" / "requests.jsonl")
    payload = {
        "total": summary.total,
        "intent_accuracy": summary.intent_accuracy,
        "appointment_type_accuracy": summary.appointment_type_accuracy,
        "clarification_accuracy": summary.clarification_accuracy,
    }
    print(json.dumps(payload, indent=2))
