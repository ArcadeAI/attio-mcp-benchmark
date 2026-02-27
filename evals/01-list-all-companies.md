# Eval 01: List All Companies

## Query
"Show me all companies in our CRM"

## Expected Behavior
- Object: companies
- Filter: None (list all, limit 25)
- Fields needed: name (at minimum)
- Expected results: 25 company records with names

## Acceptance Criteria
- [ ] Returns company records (up to 25)
- [ ] Response includes company names
- [ ] Agent can list the companies from the response

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/01-list-all-companies.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/01-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
