# Eval 06: Deals by Close Date

## Query
"Show me deals closing before March 2026"

## Expected Behavior
- Object: deals
- Filter: close date before 2026-03-01
- Fields needed: name, close_date, deal_value
- Expected results: 20+ deals with close dates before March 2026

## Acceptance Criteria
- [ ] Returns only deals with close date before March 2026 (not all deals)
- [ ] Response includes deal names, close dates, and values
- [ ] Every returned deal has a close date before 2026-03-01

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/06-deals-by-close-date.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/06-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
