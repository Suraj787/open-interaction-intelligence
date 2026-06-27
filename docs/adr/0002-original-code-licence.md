# ADR 0002, Original code licence: MIT

- Status: Accepted
- Date: 2026-06-27

## Context

The project distributes original skill logic, scanners, schemas, CLI code and
clean-room recipe implementations. We need a permissive licence that maximises adoption
by other AI coding agents and frontend teams while never overriding third-party terms.

## Decision

Original Motif code is licensed **MIT**. We chose MIT over Apache-2.0 for minimal friction
and because Motif does not ship a patent-sensitive surface that warrants Apache's patent
grant complexity for v0.1.0.

## Non-negotiable boundary

The project licence governs **only original Motif code**. Every third-party source keeps
its own licence and obligations, recorded per record in `registry/` and summarised in
`THIRD_PARTY_SOURCES.md`. The MIT licence never relaxes a source-available, Commons-Clause,
attribution or non-redistribution obligation.
