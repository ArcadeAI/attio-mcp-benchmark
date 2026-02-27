# Benchmark Runner Guide

How to run the 8 evals across 2 toolkits. Each toolkit gets its own Claude Code window.

## Prerequisites

1. A Linear workspace with issues, labels (including "bug"), priorities, and at least one team.
2. Both MCP toolkits connected to the same Linear workspace.

## Window Setup

### Window 1: Arcade
- **MCP server**: Arcade Linear toolkit (`Linear.*` tools)
- **Save files to**: `raw/arcade/`
- **Docs**: [docs.arcade.dev](https://docs.arcade.dev)

### Window 2: Composio
- **MCP server**: Composio Linear toolkit (`LINEAR_*` tools)
- **Save files to**: `raw/composio/`
- **Docs**: [mcp.composio.dev/linear](https://mcp.composio.dev/linear)

## Run Order

In each window, execute the 8 evals sequentially:

```
evals/01-list-all-issues.md
evals/02-issues-by-state.md
evals/03-issues-by-priority.md
evals/04-issues-by-label.md
evals/05-issues-by-assignee.md
evals/06-issues-by-date.md
evals/07-compound-filter.md
evals/08-lean-issue-detail.md
```

For each eval, paste the **Query** into the chat and instruct the agent to:
1. Answer the query using its available tools
2. Save the complete raw response as JSON to the correct `raw/{toolkit}/` path
3. If the query can't be expressed, create a `NOT-EXPRESSIBLE.md` instead

## After All Evals

1. **Save metadata** — In each window, have the agent write `raw/{toolkit}/metadata.json` with:
   - Tool name and exact parameters for each eval
   - Number of records returned
   - Any errors or notes

2. **Count tokens** — Run the token counter across all raw data:
   ```bash
   pip install tiktoken
   python scripts/count_tokens.py
   ```

3. **Verify** — Spot-check that:
   - Arcade has 8 JSON files (all expressible)
   - Composio has JSON for expressible queries + NOT-EXPRESSIBLE.md for the rest

## Expected Expressiveness

| Eval | Arcade | Composio |
|------|--------|----------|
| 01 - List all issues | Yes | Yes |
| 02 - Issues by state | Yes | No (no state filter) |
| 03 - Issues by priority | Yes | No (no priority filter) |
| 04 - Issues by label | Yes | No (no label filter) |
| 05 - Issues by assignee | Yes | Yes (by UUID) |
| 06 - Issues by date | Yes | No (no date filter) |
| 07 - Compound filter | Yes | No (max 2 filters) |
| 08 - Lean issue detail | Yes (toggles) | No (always full payload) |
| **Total** | **8/8** | **~2/8** |

## File Output Structure

After a complete run:

```
raw/
├── arcade/
│   ├── 01-list-all-issues.json
│   ├── 02-issues-by-state.json
│   ├── ...
│   ├── 08-lean-issue-detail.json
│   └── metadata.json
└── composio/
    ├── 01-list-all-issues.json
    ├── 02-NOT-EXPRESSIBLE.md
    ├── ...
    └── metadata.json
```
