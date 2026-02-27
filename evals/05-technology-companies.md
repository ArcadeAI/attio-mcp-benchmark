# Eval 05: Technology Companies

## Query
"List all Technology companies"

## Expected Behavior
- Object: companies
- Filter: industry/category equals "Technology"
- Fields needed: name, industry/category
- Expected results: ~23 companies categorized as Technology

## Acceptance Criteria
- [ ] Returns only companies in the Technology category (not all companies)
- [ ] Response includes company names and their category/industry
- [ ] Agent can answer "which companies are in Technology?" from the response

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/05-technology-companies.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/05-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
