# Eval 06: Issues by Date Range

## Query
"Show me issues created in the last 7 days"

## Expected Behavior
- Object: issues
- Filter: created after 7 days ago
- Fields needed: title, created date, state
- Expected results: Only issues created within the last week

## Acceptance Criteria
- [ ] Returns only issues created in the last 7 days (not all issues)
- [ ] Response includes issue titles and creation dates
- [ ] Every returned issue was created within the last week

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/06-issues-by-date.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/06-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
