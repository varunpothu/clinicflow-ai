
# User Journeys

## Journey A: standard request

~~~mermaid
sequenceDiagram
    actor Patient
    participant API
    participant AI
    participant Rules
    participant Staff
    participant Booking

    Patient->>API: Submit natural-language request
    API->>AI: Extract structured scheduling intent
    AI-->>API: Typed intent
    API->>Rules: Validate intent
    Rules-->>API: Valid
    API->>Booking: Search availability
    Booking-->>API: Candidate slots
    API-->>Staff: Proposal in approval queue
    Staff->>API: Approve
    API->>Booking: Revalidate and commit
    Booking-->>API: Appointment confirmed
    API-->>Patient: Confirmation event
~~~

## Journey B: ambiguous request

If required scheduling fields are missing or ambiguous, the workflow enters clarification instead of inventing values.

## Journey C: stale approval

A staff member can approve a proposal after the original slot has been taken. The system must revalidate inside the final booking transaction. A conflict moves the workflow to exception handling and proposes the next valid action.

## Journey D: rejection

A staff member rejects a proposal with an optional reason. The workflow becomes terminal for that proposal, while the original request remains auditable.
