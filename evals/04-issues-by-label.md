# Eval 04: Issues by Label

## Query
"Find all issues labeled 'bug'"

## Expected Behavior
- Object: issues
- Filter: label equals "bug"
- Fields needed: title, labels, state
- Expected results: Only issues that have the "bug" label applied

## Acceptance Criteria
- [ ] Returns only issues with the "bug" label (not all issues)
- [ ] Response includes issue titles and labels
- [ ] Every returned issue has "bug" as one of its labels

## Instructions
1. Using whatever Linear MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/04-issues-by-label.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/04-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
