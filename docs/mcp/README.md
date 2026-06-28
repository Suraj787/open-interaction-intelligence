# Motif MCP Server

Exposes the shared source of truth (registry, findings, policy, memory) to MCP clients such
as Claude Code over JSON-RPC on stdio. Status mirrors
[`docs/reviews/motif-v3-gap-analysis.md`](../reviews/motif-v3-gap-analysis.md) (§19:
**implemented**, stdlib JSON-RPC over stdio; read-only tools + guarded writes; audit log;
dry-run).

## What it does

- Speaks **JSON-RPC over stdio** using only the Python standard library (no extra deps).
- Offers **read tools** (search registry, get source/component/pattern, list findings, read
  memory, read policy) openly.
- Offers **guarded write tools** (record finding, write memory) that **dry-run by default**
  and append to an **audit log**.

## Running it

```bash
motif mcp serve            # start the server on stdio (for an MCP client to spawn)
motif mcp tools            # list the tools the server exposes
motif mcp call <tool> ...  # invoke a tool once for inspection/testing
```

Aliases: `ii mcp`, `oii mcp`.

### Example client config (Claude Code)

```json
{
  "mcpServers": {
    "motif": { "command": "motif", "args": ["mcp", "serve"] }
  }
}
```

## Honest status

| Capability | Status |
|---|---|
| JSON-RPC/stdio server (stdlib only) | implemented |
| Read tools over registry / findings / memory / policy | implemented |
| Guarded write tools (dry-run default, audited) | implemented |
| Audit log | implemented |

## Safety

Reads are side-effect free. Writes are guarded: dry-run unless explicitly confirmed, scoped,
and every call is appended to an audit log. The server reads the one shared registry via
library functions, it never holds a divergent copy.

## See also

- [`docs/atlas/README.md`](../atlas/README.md), the same registry as a static site
- [`docs/memory/README.md`](../memory/README.md), [`docs/policies/README.md`](../policies/README.md)
- [`docs/architecture/motif-v3-live-architecture.md`](../architecture/motif-v3-live-architecture.md) §8
