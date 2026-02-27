# Eval 02: Issues by State

## Query
"Find all issues that are In Progress"

## Expected Behavior
- Object: issues
- Filter: state/status equals "In Progress"
- Fields needed: title, state, assignee
- Expected results: Only issues currently in the "In Progress" state

## Acceptance Criteria
- [ ] Returns only issues where state is "In Progress" (not all issues)
- [ ] Response includes issue titles and state values
- [ ] Agent can answer "which issues are in progress?" from the response

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/02-issues-by-state.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/02-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
