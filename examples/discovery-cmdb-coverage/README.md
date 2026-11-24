# Discovery-to-CMDB Population Coverage — public example

A synthetic candidate data product comparing generic discovery observations with ServiceNow CMDB configuration items. It contains no organization-specific data, real assets, credentials, actual integrations, or approved operational measures.

- `odps42-product.json`: draft product metadata structured against the Open Data Product Specification (ODPS) 4.2.
- `requirements.json`: non-ODPS architectural requirements and decisions to validate before implementation.

## Business question

For a given eligible asset class and environment, which distinct assets are represented in the CMDB and which require reconciliation?

## Example metric

`100 * represented_eligible_distinct_assets / approved_eligible_distinct_population`

The denominator requires an approved population baseline. Neither discovery alone nor the union of discovery and CMDB records proves complete population coverage. Multiple discovery observations may refer to one asset. An unmatched discovery observation is not necessarily in-scope; a CMDB record lacking current discovery evidence is not necessarily wrong. No thresholds are asserted.

## Lifecycle distinction

ODPS describes the proposed product and commitments; a separate operating model governs how the product is qualified, defined, implemented, assured and improved. No executable workflow is implied.

Specification: https://opendataproducts.org/v4.2/

This is an illustrative public example, not an endorsed ServiceNow integration or production system.


## Use-case context

**Goal:** Determine which eligible assets are represented in the CMDB and which need reconciliation.

**Primary actor:** An illustrative CMDB data steward. The asset population authority resolves scope questions; ambiguous matches require an assigned reviewer. No real ownership assignment is implied.

**Trigger and preconditions:** A steward requests a coverage review for an asset class, environment and measurement time. A usable comparison needs source snapshots, agreed identity rules and an eligible population baseline. These are proposed inputs; none is supplied or approved by this example.

**Main flow:** Select the scope and measurement time; reconcile discovery observations and CMDB representations to distinct eligible assets; review represented, unrepresented and unresolved cases with their provenance; assign follow-up for gaps.

**Alternative outcomes:** Preserve ambiguous matches for review. If a trustworthy population baseline is unavailable, report the comparison and its limitation without claiming complete population coverage. A CMDB-only record can be valid when discovery participation is not required.

**Successful outcome:** The steward can distinguish a representation gap from an identity or evidence gap and determine the next action. Evidence of that outcome must come from later testing and use, not this declaration.

## Development and lifecycle

Follow the [repository lifecycle and change process](../../README.md). The current example is a draft definition with open business decisions. Its schema and product identity can be checked now; reconciliation behavior, pipeline tests, access and runtime assurance remain development work. The requirements companion holds additional rules, a proposed model and open decisions; it is not yet an approved requirements baseline.
