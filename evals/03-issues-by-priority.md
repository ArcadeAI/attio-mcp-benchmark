# Eval 03: Issues by Priority

## Query
"Show me all urgent issues"

## Expected Behavior
- Object: issues
- Filter: priority equals "urgent"
- Fields needed: title, priority, state, assignee
- Expected results: Only issues marked as urgent priority

## Acceptance Criteria
- [ ] Returns only issues with urgent priority (not all issues)
- [ ] Response includes issue titles and priority levels
- [ ] Every returned issue has urgent priority

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/03-issues-by-priority.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/03-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
