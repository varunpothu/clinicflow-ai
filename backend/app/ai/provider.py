import time
from dataclasses import dataclass
from typing import Protocol

from pydantic import ValidationError

from app.ai.contracts import AppointmentIntent
from app.ai.guardrails import validate_user_text
from app.ai.prompts import PROMPT_VERSION, SYSTEM_PROMPT


@dataclass(frozen=True)
class ExtractedIntent:
    appointment_type: str | None
    preferred_time_text: str | None
    clarification_required: bool
    clarification_question: str | None
    rationale: str


class AIProvider(Protocol):
    def extract_intent(self, text: str) -> ExtractedIntent: ...


class MockAIProvider:
    """Deterministic local adapter; no network calls and no model authority."""

    def extract_intent(self, text: str) -> ExtractedIntent:
        normalized = validate_user_text(text)
        return ExtractedIntent(
            appointment_type="routine_consultation",
            preferred_time_text=normalized,
            clarification_required=False,
            clarification_question=None,
            rationale="Deterministic local fixture used for development and tests.",
        )


class BedrockAIProvider:
    """AWS adapter using Bedrock Converse and a constrained extraction tool."""

    def __init__(
        self,
        *,
        model_id: str,
        region_name: str,
        guardrail_identifier: str | None = None,
        guardrail_version: str | None = None,
    ) -> None:
        import boto3

        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.guardrail_identifier = guardrail_identifier
        self.guardrail_version = guardrail_version

    def extract_intent(self, text: str) -> ExtractedIntent:
        user_text = validate_user_text(text)
        started = time.perf_counter()
        response = self.client.converse(
            modelId=self.model_id,
            system=[{"text": SYSTEM_PROMPT}],
            messages=[{"role": "user", "content": [{"text": user_text}]}],
            toolConfig={
                "tools": [{
                    "toolSpec": {
                        "name": "extract_appointment_intent",
                        "description": "Extract administrative appointment scheduling intent only.",
                        "inputSchema": {
                            "json": {
                                "type": "object",
                                "properties": {
                                    "intent": {"type": "string", "enum": ["BOOK_APPOINTMENT", "CANCEL_APPOINTMENT", "RESCHEDULE_APPOINTMENT", "UNKNOWN"]},
                                    "appointment_type": {"type": ["string", "null"]},
                                    "preferred_date": {"type": ["string", "null"]},
                                    "preferred_date_end": {"type": ["string", "null"]},
                                    "preferred_after": {"type": ["string", "null"]},
                                    "preferred_before": {"type": ["string", "null"]},
                                    "clinician_preference": {"type": ["string", "null"]},
                                    "clarification_required": {"type": "boolean"},
                                    "clarification_question": {"type": ["string", "null"]},
                                    "rationale": {"type": "string"}
                                },
                                "required": ["intent", "appointment_type", "preferred_date", "preferred_date_end", "preferred_after", "preferred_before", "clinician_preference", "clarification_required", "clarification_question", "rationale"]
                            }
                        }
                    }
                }],
                "toolChoice": {"tool": {"name": "extract_appointment_intent"}},
            },
            inferenceConfig={"temperature": 0, "maxTokens": 600},
            **self._guardrail_kwargs(),
        )
        _latency_ms = int((time.perf_counter() - started) * 1000)
        del _latency_ms
        tool_input = self._extract_tool_input(response)
        try:
            intent = AppointmentIntent.model_validate(tool_input)
        except ValidationError as exc:
            raise ValueError("AI_SCHEMA_INVALID") from exc
        return ExtractedIntent(
            appointment_type=intent.appointment_type,
            preferred_time_text=self._format_preference(intent),
            clarification_required=intent.clarification_required,
            clarification_question=intent.clarification_question,
            rationale=intent.rationale,
        )

    def _guardrail_kwargs(self) -> dict[str, object]:
        if not (self.guardrail_identifier and self.guardrail_version):
            return {}
        return {"guardrailConfig": {"guardrailIdentifier": self.guardrail_identifier, "guardrailVersion": self.guardrail_version, "trace": "enabled"}}

    @staticmethod
    def _extract_tool_input(response: dict[str, object]) -> dict[str, object]:
        output = response.get("output", {})
        if not isinstance(output, dict):
            raise ValueError("AI_RESPONSE_INVALID")
        message = output.get("message", {})
        if not isinstance(message, dict):
            raise ValueError("AI_RESPONSE_INVALID")
        content = message.get("content", [])
        if not isinstance(content, list):
            raise ValueError("AI_RESPONSE_INVALID")
        for block in content:
            if not isinstance(block, dict):
                continue
            tool_use = block.get("toolUse")
            if not isinstance(tool_use, dict):
                continue
            if tool_use.get("name") == "extract_appointment_intent":
                tool_input = tool_use.get("input")
                if isinstance(tool_input, dict):
                    return tool_input
        raise ValueError("AI_TOOL_OUTPUT_MISSING")

    @staticmethod
    def _format_preference(intent: AppointmentIntent) -> str | None:
        values = [
            intent.preferred_date.isoformat() if intent.preferred_date else None,
            intent.preferred_date_end.isoformat() if intent.preferred_date_end else None,
            intent.preferred_after.isoformat() if intent.preferred_after else None,
            intent.preferred_before.isoformat() if intent.preferred_before else None,
        ]
        compact = [value for value in values if value]
        return " to ".join(compact) or None