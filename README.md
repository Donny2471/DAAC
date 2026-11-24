# DAAC — Data Architecture as Code

A working home for defining, developing, reviewing and maintaining data products. The first example compares generic discovery observations with ServiceNow CMDB representation.

The intent is to keep the business need, product commitments, implementation changes and evidence connected throughout the product lifecycle. ODPS is the product specification within that chain.

## Start here

- [Discovery-to-CMDB example](examples/discovery-cmdb-coverage/README.md)
- [Product specification](examples/discovery-cmdb-coverage/odps42-product.json)
- [Requirements and open decisions](examples/discovery-cmdb-coverage/requirements.json)
- [Validation workflow](.github/workflows/validate.yml)

## Current working baseline

The repository contains a synthetic draft product, its requirements companion, a documented use case, a validation command and CI checks. It does not yet contain a reconciliation pipeline, live connections, approved service targets or runtime assurance evidence. Publication in GitHub is publication of the example; it is not a production release of a data service.

## What belongs where

| Artifact | Responsibility |
| --- | --- |
| Example README | Explain the use case, scope, current state and how to work with the product. |
| ODPS JSON | Authoritative product metadata and the commitments expressible in ODPS. |
| requirements.json | Additional business rules, evidence needs, proposed model and unresolved decisions. This draft is not an approved requirements baseline. |
| Pipeline code and tests, when implemented | Acquire, reconcile and produce the defined output; verify behavior using synthetic fixtures. Keep them beside their product. |
| Pull request | Explain a proposed change, its rationale, impact and evidence. |
| Release record | Identify the accepted product and code versions, evidence, accountable decision and consumer impact. |
| Runtime evidence | Record observations tied to the product version, code revision, measurement time and source provenance. |

Keep each definition authoritative in one place and link to it elsewhere. Do not duplicate ODPS fields into a parallel specification. A separate usecase.json can be introduced if the use case needs independent reuse or management; the example README carries the initial scenario.

## Working lifecycle

These are repository practices adopted for this pilot, not additional requirements imposed by ODPS. ODPS supplies the status vocabulary; the promotion evidence below is our local working profile. The same review loop applies to later changes.

| ODPS status | Work and decision | Evidence needed to progress |
| --- | --- | --- |
| draft | Describe the need, consumer, intended decision, proposed owner and scope. Decide whether to create, reuse or extend a product. | Use case, open decisions and a reviewed product direction. |
| development | Agree applicable requirements and implement the data pipeline. | Source mappings, identity and population rules, code, synthetic fixtures and test results. |
| testing | Verify behavior and product commitments. | Matching, duplicate, ambiguous identity, stale evidence, exclusion and denominator test results; specification checks. |
| acceptance | Have accountable product and consumer representatives review fitness for use. | Recorded acceptance, resolved release blockers, support ownership and operational readiness. |
| production | Release the accepted version and observe its operation and use. | Release identifier, access and support instructions, quality and service observations, adoption and outcome review. |
| sunset | Notify affected consumers and manage replacement or migration. | Impact review, notice, transition plan and retirement decision. |
| retired | Withdraw the service and preserve its decision history. | Retirement record and evidence retained under the applicable retention policy. |

An announcement may precede a draft where useful. CI success does not approve a status transition. Reviewers must distinguish a proposed target from an observed result and an unassigned role from an accountable owner.

## Change and release process

1. Open an issue or describe the need in the pull request. Link the affected use case and product.
2. Update the authoritative specification, requirements and implementation together as applicable.
3. Run the checks below and include relevant pipeline test evidence when pipeline code exists.
4. Obtain review appropriate to the change. Scope, denominator, matching rules and commitments require business or domain review as well as technical review.
5. Merge the accepted change. For a product release, update productVersion and versionNotes, record the Git revision and identify the matching code version. A documentation-only change need not imply a new data-service release.
6. Review runtime findings and consumer outcomes; create the next improvement or retirement decision.

Breaking changes need an explicit consumer impact and migration decision. Credentials, operational asset records and private evidence stay in approved operational systems; this public example uses synthetic material and references only.

## Run the checks

Use Python 3.12 and install jsonschema 4.26.0: `python -m pip install jsonschema==4.26.0`.

Run `python validate.py --report validation-report.json` from the repository root. The command exits with a nonzero status if a check fails.

The validator downloads the official ODPS 4.2 JSON Schema from the exact upstream revision recorded in validate.py and verifies its SHA-256. It checks the ODPS document, parses the companion JSON and checks product identity consistency and required documentation. It does not validate the companion against an invented ODPS schema or claim that a schema pass proves business completeness, pipeline correctness or operational readiness.

For an offline run, supply an already downloaded copy of that same schema: `python validate.py --schema /path/to/odps.json --report validation-report.json`. The checksum check also applies offline. Network or schema retrieval failures fail validation rather than count as a pass.

GitHub Actions runs the same command on pull requests, pushes to main and manual requests. It retains a validation report as a workflow artifact for 30 days. The report is build evidence, not runtime data quality evidence; retain release evidence separately for as long as needed. The workflow checks changes but does not configure branch protection, approve releases or deploy a data service.

## Next development work for the example

1. Confirm the population baseline, identity matching rules and handling of stale observations.
2. Turn the relevant draft statements into agreed, verifiable product requirements and acceptance examples.
3. Implement reconciliation against synthetic discovery, CMDB and population fixtures; preserve unresolved identity cases.
4. Add behavioral tests, source-to-output lineage and a reproducible measurement report.
5. Establish ownership, consumption, support and runtime evidence before considering an operational release.

## Published foundations

- [ODPS 4.2](https://opendataproducts.org/v4.2/): product metadata, status values, references, contracts, quality, service and access definitions. Its brief, definition and operating-model templates describe increasing completeness; minimum schema conformance is not a complete product definition.
- [Data Product Operating Framework](https://opendataproducts.org/framework/): draft v0.2.0 guidance for direction, definition, operation and assurance. We use it as guidance and do not claim adoption or conformance.
- [Open Data Products SDK](https://opendataproducts.org/sdk/): optional tooling for standards-aware validation and related workflows. This initial repository uses a small JSON Schema check; it does not require the SDK.

The repository structure, review process and CI implementation are local choices. Reassess them as the pilot produces evidence rather than adding every specification or framework artifact in advance.
