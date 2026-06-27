# Personas — Interface Intelligence OS

IIOS serves one **primary** user (the AI coding agent) and four **human** stakeholders who
direct, consume, or extend its output. Designing for all five keeps the system both
agent-native and accountable to people.

---

## 1. The AI coding agent — *primary user*

**Who.** A coding agent (e.g. Claude Code with skills/subagents) building or modifying a UI
on a human's behalf.

**Goals.** Produce interfaces that are correct, complete, accessible, performant, and
on-brand the first time; avoid generating something that a reviewer will reject; stay
coherent across a long session.

**Pain without IIOS.** Defaults to generic high-fidelity output; skips states; misses
accessibility/performance bars; copies licence-encumbered code; drifts over a long horizon;
can't explain *why* it chose something.

**What IIOS gives it.** An orchestrator skill + bounded specialist subagents, deterministic
tools it can call for validation/scanning/ranking, a state matrix it must satisfy, and a
ledger to record decisions. The agent does judgment; the tools do the safety-critical,
repeatable work.

**Success.** Output passes assurance, looks intentional, and is fully auditable.

---

## 2. The frontend developer

**Who.** An engineer using an IIOS-equipped agent, or IIOS directly, in their own repo.

**Goals.** Ship features fast *without* inheriting inaccessible, slow, or licence-risky
code; keep ownership of the source; integrate with their framework (incl. Vue/Frappe-Vue).

**Pain without IIOS.** Cleaning up generic AI output, retrofitting states and a11y, auditing
copied snippets for licences, fighting design drift in long sessions.

**What IIOS gives them.** Own-your-source implementations, framework-neutral output, a
licence/security gate before code lands, assurance evidence they can trust, and a decision
ledger they can review in a PR.

**Success.** Less rework; UI they'd have written themselves, but faster and provably sound.

---

## 3. The design-system owner

**Who.** The person responsible for a team's tokens, components, patterns, and brand.

**Goals.** Ensure agent-generated UI conforms to *their* system; prevent one-off divergence
and duplicate components; keep accessibility and motion standards enforced.

**Pain without IIOS.** Agents ignore the system, invent components, and erode coherence;
no mechanism to enforce tokens/patterns or detect drift.

**What IIOS gives them.** DTCG token interop, design-intelligence data they can shape,
originality/drift auditing that flags divergence from recorded decisions, and a governance
loop that maintains coherence.

**Success.** Agent output strengthens the system instead of fragmenting it.

---

## 4. The enterprise buyer / engineering leader

**Who.** A decision-maker evaluating IIOS for an organisation.

**Goals.** Adopt AI UI generation **without** taking on accessibility liability,
supply-chain risk, licence violations, or unauditable decisions; satisfy compliance.

**Pain without IIOS.** AI output is a legal/quality risk surface (WebAIM Million: 94.8% of
pages fail WCAG — see [problem P4](../research/problem-evidence.md)); no audit trail; opaque
third-party code.

**What IIOS gives them.** A documented security model, a licence gate, accessibility/
performance assurance with honest coverage statements, an auditable decision ledger, and an
open, self-hostable, dependency-free core they can inspect.

**Success.** A defensible, auditable, lower-risk path to agent-built interfaces.

---

## 5. The open-source contributor

**Who.** A developer extending IIOS — adding sources, design data, specialist agents,
adapters, or assurance checks.

**Goals.** Contribute confidently within clear contracts; have changes validated
automatically; understand what is implemented vs experimental vs planned.

**Pain without IIOS.** Ambiguous scope, no validation gate, unclear honesty standards.

**What IIOS gives them.** Machine-readable schemas, a dependency-free `make check` gate,
authoring guides, the research methodology (don't fabricate), and a capability matrix that
makes the honest state of every feature explicit.

**Success.** Smooth, validated contributions that uphold the honesty and safety standards.

---

## Persona → engine map

| Persona | Most relevant engines |
|---------|-----------------------|
| AI coding agent | All six (via orchestrator + tools) |
| Frontend developer | Implementation, Assurance, Interaction |
| Design-system owner | Design Intelligence, Governance |
| Enterprise buyer | Assurance, Governance, Secure supply chain |
| OSS contributor | All (via schemas + `make check`) |
