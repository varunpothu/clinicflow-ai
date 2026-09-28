# Waitlist Workflow

A waitlist entry is a deterministic administrative preference:

patient + appointment type + optional clinician + acceptable time window.

When a slot becomes available, the matching engine selects eligible entries in created order. It does not make a clinical priority decision.

Future production flow:

Cancelled appointment -> availability event -> waitlist matcher -> candidate notification -> human approval -> booking.
