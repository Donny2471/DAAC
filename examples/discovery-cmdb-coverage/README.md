# Discovery-to-CMDB Population Coverage — public example

A synthetic candidate data product comparing generic discovery observations with ServiceNow CMDB configuration items. It contains no organization-specific data, real assets, credentials, actual integrations, or approved operational measures.

- `odps42-product.json`: draft product metadata structured against the Open Data Product Specification (ODPS) 4.2.
- `architecture-companion.json`: non-ODPS architectural requirements and decisions to validate before implementation.

## Business question

For a given eligible asset class and environment, which distinct assets are represented in the CMDB and which require reconciliation?

## Example metric

`100 * represented_eligible_distinct_assets / approved_eligible_distinct_population`

The denominator requires an approved population baseline. Neither discovery alone nor the union of discovery and CMDB records proves complete population coverage. Multiple discovery observations may refer to one asset. An unmatched discovery observation is not necessarily in-scope; a CMDB record lacking current discovery evidence is not necessarily wrong. No thresholds are asserted.

## Lifecycle distinction

ODPS describes the proposed product and commitments; a separate operating model governs how the product is qualified, defined, implemented, assured and improved. No executable workflow is implied.

Specification: https://opendataproducts.org/v4.2/

This is an illustrative public example, not an endorsed ServiceNow integration or production system.
