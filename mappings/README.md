# Phase 1 mapping governance

Field mappings and state transitions are controlled artifacts, not implementation-local constants. Object ownership remains with the source system; a mapping may define a projection, reference, validation, or event handoff, but it must not transfer fact ownership to the consumer.

The Phase 1 mapping slots reserved by the implementation plan are:

- `crm-spc-order.yaml` — M05 CRM commercial order to M06 SPC delivery order.
- `spc-fac-delivery.yaml` — M06 SPC delivery/material results to M09 FAC inputs.
- `fac-ebms-result.yaml` — M09 FAC verified finance results to M03 EBMS management views.

Each mapping must identify source and target systems, object ownership, field semantics, units/currency, revision and effective-time rules, state transitions, evidence references, and compatibility handling. Changes require review by both the source owner and the consuming owner.
