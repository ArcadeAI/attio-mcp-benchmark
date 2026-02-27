# Eval 03: Deals Over $50K

## Query
"Show me deals worth more than $50,000"

## Expected Behavior
- Object: deals
- Filter: deal value greater than 50000
- Fields needed: name, deal_value
- Expected results: 25+ deals all with value > $50K

## Acceptance Criteria
- [ ] Returns only deals where value exceeds $50,000 (not all deals)
- [ ] Response includes deal names and values
- [ ] Every returned deal has a value > $50,000

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/03-deals-over-50k.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/03-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
