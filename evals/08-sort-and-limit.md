# Eval 08: Sort and Limit

## Query
"What is my highest-value deal?"

## Expected Behavior
- Object: deals
- Filter: None — sort by deal value descending, limit 1
- Fields needed: name, deal_value, associated company
- Expected results: Exactly 1 deal — the one with the highest value

## Acceptance Criteria
- [ ] Returns exactly 1 deal (not all deals sorted client-side)
- [ ] The deal returned has the highest value in the workspace
- [ ] Response includes deal name, value, and associated company

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/08-sort-and-limit.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/08-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
