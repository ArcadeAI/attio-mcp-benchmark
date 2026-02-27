# Eval 07: Compound Filter

## Query
"Find Technology companies with more than 100 employees"

## Expected Behavior
- Object: companies
- Filter: industry/category equals "Technology" AND employee count greater than 100
- Fields needed: name, industry/category, employee_count
- Expected results: 10+ companies matching both conditions

## Acceptance Criteria
- [ ] Returns only companies that are BOTH in Technology AND have 100+ employees
- [ ] Response includes company names, categories, and employee counts
- [ ] No returned company is outside Technology or has fewer than 100 employees

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
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
