# Eval 02: Deals by Stage

## Query
"Find all deals in the Nurture stage"

## Expected Behavior
- Object: deals
- Filter: stage equals "Nurture"
- Fields needed: name, stage
- Expected results: ~22 deals all with stage = Nurture

## Acceptance Criteria
- [ ] Returns only deals where stage is "Nurture" (not all deals)
- [ ] Response includes deal names and stage values
- [ ] Agent can answer "which deals are in Nurture?" from the response

## Instructions
1. Using whatever Attio MCP tools you have available, answer the query above
2. Save the COMPLETE raw tool response as JSON to: `raw/{toolkit}/02-deals-by-stage.json`
3. If your toolkit cannot express this query, create `raw/{toolkit}/02-NOT-EXPRESSIBLE.md` explaining:
   - What tool you tried
   - What parameter or operator is missing
   - Link to the tool's documentation/schema

## Metadata
After running, record:
- Tool name and exact parameters used
- Number of records returned
- Any errors or unexpected behavior
