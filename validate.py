"""Validate the repository's draft product definitions; this is not a release gate."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

from jsonschema import Draft202012Validator, FormatChecker

UPSTREAM_REVISION = "d3142fc1e4960ec7639e4d55bd056f8db698ff80"
SCHEMA_URL = (
    "https://raw.githubusercontent.com/Open-Data-Product-Initiative/v4.2/"
    + UPSTREAM_REVISION
    + "/source/schema/odps.json"
)
SCHEMA_SHA256 = "c34b7f0f6083384c1fd461649b31b7330504cbce97915f5bb820a5ebe37aee19"
SCHEMA_DECLARATION = "https://opendataproducts.org/v4.2/schema/odps.json"


def load_schema(path=None):
    if path is not None:
        data = Path(path).read_bytes()
    else:
        with urlopen(SCHEMA_URL, timeout=30) as response:
            data = response.read()
    if hashlib.sha256(data).hexdigest() != SCHEMA_SHA256:
        raise ValueError("ODPS schema checksum mismatch; review an upstream update explicitly")
    schema = json.loads(data)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_repository(root, schema):
    errors = []
    products = sorted((root / "examples").glob("*/odps42-product.json"))
    if not products:
        errors.append("No product specifications found under examples/*/odps42-product.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    seen_ids = set()
    for path in products:
        relative = str(path.relative_to(root))
        try:
            product = json.loads(path.read_text(encoding="utf-8"))
            product_errors = sorted(validator.iter_errors(product), key=lambda e: str(list(e.path)))
            for error in product_errors:
                location = "/".join(str(part) for part in error.path) or "<root>"
                errors.append(f"{relative}:{location}: {error.message}")
            if product_errors:
                continue
            if product.get("version") != "4.2" or product.get("schema") != SCHEMA_DECLARATION:
                errors.append(f"{relative}: expected the ODPS 4.2 JSON Schema declaration")
            details = product.get("product", {}).get("details", {})
            ids = {
                block.get("productID")
                for block in details.values()
                if isinstance(block, dict)
            }
            if len(ids) != 1 or not all(isinstance(value, str) and value.strip() for value in ids):
                errors.append(f"{relative}: language blocks must share one nonempty productID")
                continue
            product_id = next(iter(ids))
            if product_id in seen_ids:
                errors.append(f"{relative}: duplicate productID {product_id}")
            seen_ids.add(product_id)
            companion = json.loads((path.parent / "requirements.json").read_text(encoding="utf-8"))
            if not isinstance(companion, dict) or companion.get("productID") != product_id:
                errors.append(f"{relative}: requirements.json must identify the same product")
            readme = path.parent / "README.md"
            if not readme.is_file() or not readme.read_text(encoding="utf-8").strip():
                errors.append(f"{relative}: missing or empty product README")
        except (OSError, ValueError, TypeError) as error:
            errors.append(f"{relative}: {error}")
    return len(products), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, help="Offline copy of the pinned official schema")
    parser.add_argument("--report", type=Path, help="Write a JSON build validation report")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    count = 0
    try:
        schema = load_schema(args.schema)
        count, errors = validate_repository(root, schema)
    except Exception as error:
        errors = [f"Validation could not complete: {error}"]
    report = {
        "check": "product-definition-validation",
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "repositoryRevision": revision,
        "schemaSource": SCHEMA_URL,
        "schemaSha256": SCHEMA_SHA256,
        "productsChecked": count,
        "passed": not errors,
        "errors": errors,
        "scope": "ODPS schema and local repository integrity; no runtime or release assurance",
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{'FAIL' if errors else 'PASS'}: {count} product definition(s) checked")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
