# Attio Benchmark Runner Prompt

Copy everything below this line and paste into a fresh Claude Code session
with the target toolkit's MCP tools loaded. Run once per toolkit.

---

## Context

You are running the Attio MCP toolkit benchmark. The repo is at:
`~/Desktop/attio-mcp-benchmark`

The Attio sandbox workspace has been seeded with:
- 25 Fortune 100 companies
- Deals across multiple stages (Nurture, Qualified, Closed Won, etc.)
- Categories including "Technology"
- Deal values ranging from <$50k to >$50k

## Toolkit

Determine which toolkit you have available by inspecting your MCP tools:
- **Arcade** → save files to `raw/arcade/`
- **Composio** → save files to `raw/composio/`
- **Attio Official** → save files to `raw/attio-official/`

## Schema Reference (Arcade-specific — adapt field names for other toolkits)

**Companies object:**
- `name` (text)
- `categories` (select) — filter: `{"categories": {"$eq": "Technology"}}`
- `employee_range` (select) — values: "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"
- `domains` (domain)

**Deals object:**
- `name` (text)
- `stage` (status) — filter: `{"stage": {"$eq": "Nurture"}}` ($eq only for status)
- `value` (currency) — filter: `{"value": {"$gt": 50000}}`
- `associated_company` (record-reference)
- `created_at` (timestamp)

Compound filter syntax: `{"$and": [{...}, {...}]}`

## The 8 Queries

For EACH query:
- Save the COMPLETE raw tool response as JSON. Do NOT truncate or summarize.
- If the toolkit **cannot express** the query (missing filter, operator, or parameter),
  create a `raw/{toolkit}/XX-NOT-EXPRESSIBLE.md` file instead, containing:
  - What tool you tried
  - What parameter or operator is missing
  - Why the query cannot be expressed

| # | File | Query |
|---|------|-------|
| 01 | `raw/{toolkit}/01-list-all-companies.json` | List all companies, limit 25, return name |
| 02 | `raw/{toolkit}/02-deals-by-stage.json` | Find all deals in the "Nurture" stage, return name + stage |
| 03 | `raw/{toolkit}/03-deals-over-50k.json` | Show deals worth more than $50,000, return name + value |
| 04 | `raw/{toolkit}/04-companies-name-search.json` | Find companies with "Tech" in their name, return name |
| 05 | `raw/{toolkit}/05-technology-companies.json` | List all Technology companies, return name + categories |
| 06 | `raw/{toolkit}/06-deals-by-close-date.json` | Show deals created before 2026-03-01, return name + created_at + value |
| 07 | `raw/{toolkit}/07-compound-filter.json` | Find Technology companies with 201+ employees, return name + categories + employee_range |
| 08 | `raw/{toolkit}/08-sort-and-limit.json` | Get the single highest-value deal, sort by value desc, limit 1, return name + value + associated_company |

## After All Queries

1. Write `raw/{toolkit}/metadata.json` with:
   - Tool name and exact parameters used for each query
   - Number of records returned
   - EXPRESSIBLE or NOT-EXPRESSIBLE for each query
   - Any errors or notes

2. Run token counter:
```
pip3 install tiktoken
python3 scripts/count_tokens.py
```

3. Print the summary table.

4. Commit and push:
```
cd ~/Desktop/attio-mcp-benchmark
git add -A
git commit -m "Add {toolkit} benchmark results"
git push origin main
```
