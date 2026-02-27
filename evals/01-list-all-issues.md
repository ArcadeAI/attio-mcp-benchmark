# Eval 01: List All Issues

## Query
"Show me all open issues"

## Expected Behavior
- Object: issues
- Filter: None (list recent issues, limit 25)
- Fields needed: title, state, assignee
- Expected results: Up to 25 issues

## Acceptance Criteria
- [ ] Returns issues (up to 25)
- [ ] Response includes issue titles and states
- [ ] Agent can list the issues from the response

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/01-list-all-issues.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/01-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
