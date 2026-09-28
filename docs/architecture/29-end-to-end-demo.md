# End-to-End Demo Architecture

## Demo sequence

```mermaid
flowchart TD
  A[👤 Patient enters request] --> B[🛡️ Input guardrails]
  B --> C[🤖 AI intent extraction]
  C --> D[✅ Strict schema validation]
  D --> E[🔎 Availability engine]
  E --> F[📝 Appointment proposal]
  F --> G[👩‍💼 Staff approval]
  G --> H[🔐 Idempotency + final revalidation]
  H --> I[📅 Appointment transaction]
  I --> J[🧾 Audit + Outbox]
  J --> K[📨 Notifications]
  J --> L[📊 Analytics]
  H -->|conflict| M[🔴 Operational exception]
  M --> F
```

## What the interviewer should see

The most important demonstration is not the colour or chatbot. It is the boundary between AI and business authority:

- AI interprets unstructured language.
- deterministic services decide whether the request is valid.
- deterministic availability creates candidates.
- staff controls approval.
- the booking service revalidates the slot.
- idempotency prevents duplicate side effects.
- audit and outbox provide traceability and downstream integration.

This creates a concrete FDE narrative from customer problem to production controls.
