import { FormEvent, useState } from "react";
import { createAppointmentRequest, IntakeResponse } from "./api";

export default function PatientRequest() {
  const [text, setText] = useState(
    "I need a routine consultation next week after 4pm, preferably Tuesday or Wednesday.",
  );
  const [result, setResult] = useState<IntakeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await createAppointmentRequest({
        patient_id: "00000000-0000-4000-8000-000000000001",
        appointment_type: "routine_consultation",
        natural_language: text,
      });
      setResult(response);
    } catch {
      setError("Demo API is not available. Start the FastAPI service to run this flow.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="request-card">
      <div className="request-intro">
        <span className="demo-label">PATIENT DEMO</span>
        <h2>Tell us when you need your appointment</h2>
        <p>
          Write naturally. ClinicFlow will extract scheduling intent, validate it,
          and keep booking authority with staff.
        </p>
      </div>

      <form onSubmit={submit}>
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          rows={5}
          aria-label="Appointment request"
        />
        <div className="request-footer">
          <span>AI output is advisory until deterministic validation and human approval.</span>
          <button className="button submit-request" type="submit" disabled={loading}>
            {loading ? "Analysing..." : "Analyse request →"}
          </button>
        </div>
      </form>

      {error && <div className="request-error">{error}</div>}

      {result && (
        <div className="intent-result">
          <div>
            <span className="result-label">WORKFLOW STATE</span>
            <strong>{result.next_state}</strong>
          </div>
          <div>
            <span className="result-label">AI APPOINTMENT TYPE</span>
            <strong>{result.ai_intent?.appointment_type ?? "Not identified"}</strong>
          </div>
          <div>
            <span className="result-label">TIME PREFERENCE</span>
            <strong>{result.ai_intent?.preferred_time_text ?? "Clarification required"}</strong>
          </div>
          <p>{result.ai_intent?.rationale}</p>
        </div>
      )}
    </section>
  );
}
