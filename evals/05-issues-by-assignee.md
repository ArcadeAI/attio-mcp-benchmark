# Eval 05: Issues by Assignee

## Query
"Show me all issues assigned to me"

## Expected Behavior
- Object: issues
- Filter: assignee equals current user
- Fields needed: title, assignee, state, priority
- Expected results: Only issues assigned to the authenticated user

## Acceptance Criteria
- [ ] Returns only issues assigned to the current user (not all issues)
- [ ] Response includes issue titles and assignee info
- [ ] Agent can answer "what's on my plate?" from the response

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/05-issues-by-assignee.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/05-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
