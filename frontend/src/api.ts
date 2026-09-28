import { getAuthHeaders } from "./auth";
export type AppointmentRequest = {
  patient_id: string;
  appointment_type: string;
  natural_language?: string;
};

export type IntakeResponse = {
  request_id: string;
  status: string;
  next_state: string;
  ai_intent?: {
    appointment_type?: string;
    preferred_time_text?: string;
    clarification_required: boolean;
    clarification_question?: string;
    rationale: string;
  };
  validation_errors: string[];
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function createAppointmentRequest(
  request: AppointmentRequest,
): Promise<IntakeResponse> {
  const response = await fetch(`${API_BASE}/api/v1/appointment-requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Idempotency-Key": crypto.randomUUID(),
      ...(await getAuthHeaders()),
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Unable to create appointment request");
  }

  return response.json() as Promise<IntakeResponse>;
}
