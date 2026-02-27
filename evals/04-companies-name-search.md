# Eval 04: Companies Name Search

## Query
"Find companies with 'Tech' in their name"

## Expected Behavior
- Object: companies
- Filter: company name contains "Tech"
- Fields needed: name
- Expected results: ~8 companies with "Tech" somewhere in their name

## Acceptance Criteria
- [ ] Returns only companies whose name contains "Tech" (not all companies)
- [ ] Response includes company names
- [ ] Every returned company has "Tech" in its name (not just in any field)

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/04-companies-name-search.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/04-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
