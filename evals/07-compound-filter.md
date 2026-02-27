# Eval 07: Compound Filter

## Query
"Find high priority bugs assigned to me that are in progress"

## Expected Behavior
- Object: issues
- Filter: priority = "high" AND label = "bug" AND assignee = me AND state = "In Progress"
- Fields needed: title, priority, labels, assignee, state
- Expected results: Only issues matching ALL four conditions

## Acceptance Criteria
- [ ] Returns only issues matching all conditions simultaneously
- [ ] Response includes titles, priority, labels, assignee, and state
- [ ] No returned issue is missing any of the four filter criteria

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/07-compound-filter.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/07-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
