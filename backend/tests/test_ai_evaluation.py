from pathlib import Path

from app.ai.evaluate import evaluate


def test_synthetic_dataset_meets_deterministic_release_gate() -> None:
    root = Path(__file__).resolve().parents[2]
    summary = evaluate(root / "data" / "synthetic" / "requests.jsonl")
    assert summary.total == 5
    assert summary.intent_accuracy >= 0.8
    assert summary.clarification_accuracy >= 0.8
