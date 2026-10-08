"""Auditable BC1 foreground inventory and USLCI record checker.

The tool refuses to report GWP while required foreground data, providers,
or a characterization method are missing. No missing quantity is set to zero.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
import zipfile
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "data/manifest.json"
BOM = ROOT / "data/bom.csv"
MATCHES = ROOT / "data/matches.csv"
MODEL = ROOT / "data/model.json"
OUT = ROOT / "results"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def retrieve() -> Path:
    manifest = json.loads(MANIFEST.read_text())
    path = ROOT / manifest["local_cache"]
    path.parent.mkdir(exist_ok=True)
    if path.exists() and sha256(path) == manifest["sha256"]:
        return path
    temporary = path.with_suffix(".partial")
    try:
        urllib.request.urlretrieve(manifest["url"], temporary)
        actual = sha256(temporary)
        if actual != manifest["sha256"]:
            raise ValueError(f"USLCI download hash mismatch: {actual}")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def reference_exchange(process: dict) -> dict:
    product_outputs = [
        exchange
        for exchange in process["exchanges"]
        if not exchange["isInput"]
        and exchange["flow"]["flowType"] == "PRODUCT_FLOW"
    ]
    outputs = [exchange for exchange in product_outputs if exchange["flow"]["name"] == process["name"]]
    if not outputs and len(product_outputs) == 1:
        outputs = product_outputs
    if len(outputs) != 1:
        raise ValueError(f"ambiguous reference output: {process['@id']}")
    return outputs[0]


def inspect(archive: Path) -> dict:
    manifest = json.loads(MANIFEST.read_text())
    actual_hash = sha256(archive)
    if actual_hash != manifest["sha256"]:
        raise ValueError(f"USLCI archive hash mismatch: {actual_hash}")
    model = json.loads(MODEL.read_text())
    bom = read_csv(BOM)
    matches = read_csv(MATCHES)
    lookup = {row["material"]: row for row in matches}
    if len(lookup) != len(matches) or set(lookup) != {row["material"] for row in bom}:
        raise ValueError("BOM and mapping must have exactly one matching row per material")

    masses = defaultdict(Decimal)
    for row in bom:
        amount = Decimal(row["finished_mass_g"])
        if amount <= 0 or row["scope"] not in {"Kettle", "Packaging"}:
            raise ValueError(f"invalid BOM row: {row}")
        masses[row["scope"]] += amount
    mass_check = {
        "product_g": str(masses["Kettle"]),
        "packaging_g": str(masses["Packaging"]),
        "packaged_g": str(sum(masses.values())),
        "passed": masses["Kettle"] == 723 and masses["Packaging"] == Decimal("137.8"),
    }

    records = []
    issues = []
    with zipfile.ZipFile(archive) as zipped:
        known_ids = {
            path.removeprefix("processes/").removesuffix(".json")
            for path in zipped.namelist()
            if path.startswith("processes/") and path.endswith(".json")
        }
        for row in bom:
            match = lookup[row["material"]]
            process_id = match["dataset_id"]
            if match["status"] != "candidate":
                issues.append(f"{row['material']}: {match['status']} background match")
            if not process_id:
                continue
            if process_id not in known_ids:
                raise ValueError(f"dataset absent from archive: {process_id}")
            process = json.loads(zipped.read(f"processes/{process_id}.json"))
            if process["version"] != match["dataset_version"]:
                raise ValueError(f"version mismatch for {process_id}")
            reference = reference_exchange(process)
            missing_direct_providers = []
            for exchange in process["exchanges"]:
                if not exchange["isInput"] or exchange["flow"]["flowType"] != "PRODUCT_FLOW":
                    continue
                provider = exchange.get("defaultProvider") or {}
                if provider.get("@id") not in known_ids:
                    missing_direct_providers.append(exchange["flow"]["name"])
            if missing_direct_providers:
                issues.append(
                    f"{row['material']}: {len(missing_direct_providers)} direct upstream supplier(s) unavailable"
                )
            documentation = process.get("processDocumentation") or {}
            records.append(
                {
                    "material": row["material"],
                    "status": match["status"],
                    "database_release": match["database_release"],
                    "dataset_name": process["name"],
                    "dataset_id": process_id,
                    "dataset_version": process["version"],
                    "geography": (process.get("location") or {}).get("name", "unknown"),
                    "valid_from": documentation.get("validFrom") or "unknown",
                    "valid_until": documentation.get("validUntil") or "unknown",
                    "reference_flow": reference["flow"]["name"],
                    "reference_amount": reference["amount"],
                    "reference_unit": reference["unit"]["name"],
                    "process_type": process.get("processType", "unknown"),
                    "allocation": process.get("defaultAllocationMethod") or "unknown",
                    "missing_direct_provider_count": len(missing_direct_providers),
                    "missing_direct_provider_examples": missing_direct_providers[:8],
                    "source_url": manifest["url"],
                    "archive_member": f"processes/{process_id}.json",
                    "retrieved_date": manifest["retrieved_date"],
                    "archive_sha256": actual_hash,
                }
            )

    for field in (
        "nylon_grade", "material_yields", "component_conversion",
        "assembly_electricity_kwh", "packaging_conversion", "scrap_treatment",
        "allocation", "characterization_method", "transport",
    ):
        if model[field] is None:
            issues.append(f"foreground or method input unresolved: {field}")

    result = {
        "run_id": model["run_id"],
        "study_date": model["study_date"],
        "declared_unit": model["declared_unit"],
        "calculation_status": "blocked: full cradle-to-gate GWP100 cannot be calculated",
        "gwp100_kg_co2e_per_packaged_kettle": None,
        "characterization_method": model["characterization_method"],
        "mass_check": mass_check,
        "candidate_record_count": sum(record["status"] == "candidate" for record in records),
        "missing_or_rejected_material_count": sum(
            lookup[row["material"]]["status"] != "candidate" for row in bom
        ),
        "issues": issues,
        "notes": "A missing supplier, yield, energy input, or LCIA method is not a zero impact. Candidate records alone do not establish a valid total.",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "independent.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with (OUT / "dataset_records.csv").open("w", newline="", encoding="utf-8") as stream:
        columns = [key for key in records[0] if key != "missing_direct_provider_examples"]
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow({key: record[key] for key in columns})
    (OUT / "provider_gaps.json").write_text(
        json.dumps(
            {record["material"]: record["missing_direct_provider_examples"] for record in records},
            indent=2,
        ) + "\n"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["retrieve", "audit"])
    args = parser.parse_args()
    archive = retrieve()
    if args.command == "retrieve":
        print(f"Verified {archive.relative_to(ROOT)} against data/manifest.json")
        return
    result = inspect(archive)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
