# Eval 08: Lean Issue Detail

## Query
"Get me the details of issue ENG-1, just the core info — no comments or attachments"

## Expected Behavior
- Object: single issue
- Filter: issue identifier = "ENG-1" (or equivalent first issue)
- Fields needed: title, description, state, priority, assignee
- Expected results: 1 issue with core fields only — no comments, attachments, or relations bloating the response

## Acceptance Criteria
- [ ] Returns exactly 1 issue
- [ ] Response includes core issue fields (title, description, state, priority)
- [ ] Response does NOT include unnecessary bulk data (comments, attachments, sub-issues) — OR if it does, note that the toolkit cannot control this

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/08-lean-issue-detail.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/08-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Whether comments/attachments/relations were included in the response
- Token count of the response
- Any errors or unexpected behavior
