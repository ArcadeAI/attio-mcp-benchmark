# Attio Benchmark Runner Prompt

Copy everything below this line and paste into a fresh Claude Code session
that has the Attio MCP tools loaded.

---

## Context

You are running the Arcade Attio MCP toolkit benchmark. The repo is at:
`~/Desktop/attio-mcp-benchmark`

The Attio sandbox workspace has already been seeded with:
- 25 Fortune 100 companies
- Deals across multiple stages (Nurture, Qualified, Closed Won, etc.)
- Categories including "Technology"
- Deal values ranging from <$50k to >$50k

## Schema Reference

**Companies object** — key attributes:
- `name` (text)
- `categories` (select) — filter with `{"categories": {"$eq": "Technology"}}`
- `employee_range` (select) — options like "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"
- `domains` (domain)

**Deals object** — key attributes:
- `name` (text)
- `stage` (status) — filter with `{"stage": {"$eq": "Nurture"}}` (only `$eq` works for status)
- `value` (currency) — filter with `{"value": {"$gt": 50000}}`
- `associated_company` (record-reference)
- `created_at` (timestamp)

Compound filter syntax: `{"$and": [{...}, {...}]}`

## Task

Run these 8 queries using whatever Attio MCP tools you have available.
For EACH query, save the COMPLETE raw tool response as JSON — do NOT truncate or summarize.
Work in directory: `~/Desktop/attio-mcp-benchmark`

| # | File | Query |
|---|------|-------|
| 01 | raw/arcade/01-list-all-companies.json | List all companies, limit 25, return name |
| 02 | raw/arcade/02-deals-by-stage.json | Find all deals in the "Nurture" stage, return name + stage |
| 03 | raw/arcade/03-deals-over-50k.json | Show deals worth more than $50,000, return name + value |
| 04 | raw/arcade/04-companies-name-search.json | Find companies with "Tech" in their name, return name |
| 05 | raw/arcade/05-technology-companies.json | List all Technology companies, return name + categories |
| 06 | raw/arcade/06-deals-by-close-date.json | Show deals created before 2026-03-01, return name + created_at + value |
| 07 | raw/arcade/07-compound-filter.json | Find Technology companies with employee_range "201-500" or higher, return name + categories + employee_range |
| 08 | raw/arcade/08-sort-and-limit.json | Get the single highest-value deal, sort by value desc, limit 1, return name + value + associated_company |

## After All Queries

1. Write `raw/arcade/metadata.json` with tool name, exact parameters, and record count for each query.

2. Run token counter:
```
pip3 install tiktoken
python3 scripts/count_tokens.py
```

3. Print the summary table.

4. Git add + commit + push everything to:
`https://github.com/ArcadeAI/attio-mcp-benchmark`
