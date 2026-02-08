---
description: Add a new ADR to the decisions document
---

I need to add a new Architectural Decision Record to @docs/02-decisions.md.

Please guide me through creating this ADR interactively:

1. **Title**: Ask what the decision is about (e.g., "Use Hexagonal Architecture", "Use RabbitMQ for Message Queues")

2. **Context**: Ask what problems or needs led to this decision (will be formatted as bullet points)

3. **Decision**: Ask what was decided and key implementation details (will be formatted as bullet points)

4. **Alternatives considered**: Ask what other options were evaluated and why they were not chosen

5. **Trade-offs**: Ask for pros (+) and cons (−) of the decision

6. **Status**: Ask for the status:
   - Accepted
   - Proposed
   - Deprecated

After gathering all information, determine the next ADR number by counting existing ADRs, then append the new ADR to the file following this format:

## ADR-XXX: [Title]

Context:
- [bullet points]

Decision:
- [bullet points]

Alternatives considered:
- [alternatives with brief reasoning]

Trade-offs:
+ [pros]
− [cons]

Status:
- [Status] (YYYY-MM-DD)
