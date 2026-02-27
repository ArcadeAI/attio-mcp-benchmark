# Linear MCP Toolkit Benchmark

Reproducible benchmark comparing 2 MCP toolkits for Linear: **Arcade** and **Composio**.

**Blog post**: [TBD](https://arcade.dev/blog)

## Results Summary

| Scenario | Arcade | Composio |
|----------|--------|----------|
| List all issues | — | — |
| Issues by state (In Progress) | — | Cannot express |
| Issues by priority (Urgent) | — | Cannot express |
| Issues by label (bug) | — | Cannot express |
| Issues by assignee (me) | — | — |
| Issues by date (last 7 days) | — | Cannot express |
| Compound filter (4 conditions) | — | Cannot express |
| Lean issue detail (no bloat) | — | Cannot control |

*Token counts will be filled after benchmark run.*

## Query Expressiveness

| Capability | Arcade | Composio |
|---|---|---|
| List issues | Yes | Yes |
| Filter by state | Yes (by name) | No |
| Filter by priority | Yes (by name) | No |
| Filter by label | Yes (by name) | No |
| Filter by assignee | Yes (by name or @me) | Yes (by UUID only) |
| Filter by date range | Yes (created_after) | No |
| Compound filters | Yes (8 params combine) | No (max 2: project + assignee) |
| Response pruning | Yes (4 include toggles) | No (always full payload) |
| Name-based lookups | Yes (everywhere) | No (UUIDs required) |
| **Total expressible** | **8/8** | **~2/8** |

## Key Differences

### Name-based vs UUID-based
Arcade accepts human-readable names everywhere — teams, assignees, labels, states, priorities. Composio requires UUIDs, meaning extra lookup calls before you can filter.

### Response control
Arcade's `GetIssue` lets you toggle `include_comments`, `include_attachments`, `include_relations`, `include_children`. Composio always returns the full payload.

### Filter depth
Arcade's `ListIssues` supports 8 combinable filter parameters (keywords, team, state, assignee, priority, label, project, created_after). Composio's supports 2 (project_id, assignee_id).

## Reproduce It

### Option A: Verify token counts only (no API key needed)

```bash
pip install tiktoken
python scripts/count_tokens.py
```

### Option B: Full end-to-end reproduction

```bash
# 1. Have a Linear workspace with issues, labels, priorities, teams

# 2. Connect both MCP toolkits to the workspace:
#    - Arcade: docs.arcade.dev
#    - Composio: mcp.composio.dev/linear

# 3. Run the 8 evals through each toolkit
#    (see evals/ for queries, RUNNER.md for setup)

# 4. Save raw responses to raw/{toolkit}/

# 5. Count tokens
pip install tiktoken
python scripts/count_tokens.py
```

## File Structure

```
linear/
├── README.md                  # You're here
├── RUNNER.md                  # How to run evals per toolkit
├── evals/                     # 8 toolkit-agnostic eval prompts
│   ├── 01-list-all-issues.md
│   ├── 02-issues-by-state.md
│   ├── 03-issues-by-priority.md
│   ├── 04-issues-by-label.md
│   ├── 05-issues-by-assignee.md
│   ├── 06-issues-by-date.md
│   ├── 07-compound-filter.md
│   └── 08-lean-issue-detail.md
├── scripts/
│   └── count_tokens.py        # Standalone token counter
└── raw/
    ├── arcade/                # Raw JSON responses from Arcade
    │   ├── 01-list-all-issues.json
    │   ├── 02-issues-by-state.json
    │   └── ...
    └── composio/              # Raw JSON responses from Composio
        ├── 01-list-all-issues.json
        ├── 02-NOT-EXPRESSIBLE.md
        └── ...
```

## Methodology

- Both toolkits connected to the **same** Linear workspace
- Same queries, same issues, same session
- Token counts via tiktoken `cl100k_base` encoding
- Raw JSON responses saved verbatim (no truncation, no parsing)
- NOT_EXPRESSIBLE scenarios documented with specific tool limitations

### What we measured
- Token counts per toolkit per scenario
- Byte sizes of raw JSON responses
- Query expressiveness (can/cannot express each scenario)
- Number of tool calls required per query

### What we didn't measure
- Tool schema sizes (input tokens)
- API call latency
- GraphQL escape hatch reliability (Composio's fallback)

## Toolkits Tested

| Toolkit | Documentation |
|---|---|
| Arcade | [docs.arcade.dev](https://docs.arcade.dev) |
| Composio | [mcp.composio.dev/linear](https://mcp.composio.dev/linear) |
