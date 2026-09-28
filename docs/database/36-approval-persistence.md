# Persistent Approval Contract

The approval record is created from a server-owned proposal. A staff client submits only:

- proposal ID
- expected proposal version
- decision
- optional reason

The server retrieves the proposal and checks status, version and expiry before changing the approval state.

This prevents stale UI state or manipulated client payloads from changing the underlying appointment details.
