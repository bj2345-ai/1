"""Explicitly assumed, non-LCIA screening estimate for a packaged BC1 kettle.

This calculation is separate from the preserved independent LCA audit. Every
numeric proxy is tagged in data/screening_inputs.csv and screening_config.json.
"""

from __future__ import annotations

import csv
import json
import zipfile
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from kettle_lca import BOM, ROOT, read_csv, retrieve

INPUTS = ROOT / "data/screening_inputs.csv"
CONFIG = ROOT / "data/screening_config.json"
PP_MOLDING_ID = "89a2b59a-1ca2-34f5-acc8-a8eaaa6fa870"


def dec(value: str | int | float) -> Decimal:
    return Decimal(str(value))


def verify_pp_exchange() -> None:
    archive = retrieve()
    with zipfile.ZipFile(archive) as zipped:
        process = json.loads(zipped.read(f"processes/{PP_MOLDING_ID}.json"))
    inputs = [exchange for exchange in process["exchanges"] if exchange["isInput"]]
    resin = [e for e in inputs if e["flow"]["name"] == "Polypropylene, PP, virgin resin, at plant"]
    electricity = [e for e in inputs if e["flow"]["name"] == "Electricity, AC, 120 V"]
    if len(resin) != 1 or len(electricity) != 1:
        raise ValueError("USLCI PP molding reference exchanges changed")
    if (dec(resin[0]["amount"]), resin[0]["unit"]["name"]) != (dec("1.034"), "kg"):
        raise ValueError("USLCI PP resin ratio changed")
    if (dec(electricity[0]["amount"]), electricity[0]["unit"]["name"]) != (dec("6.444"), "MJ"):
        raise ValueError("USLCI PP molding electricity changed")


def calculate(scenario_name: str, bom: list[dict], inputs: list[dict], config: dict) -> dict:
    scenario = config["scenarios"][scenario_name]
    by_material = {row["material"]: row for row in inputs}
    if len(by_material) != len(inputs) or set(by_material) != {row["material"] for row in bom}:
        raise ValueError("screening table must contain every BOM material exactly once")
    if not all(row["factor_status"] == "assumed" for row in inputs):
        raise ValueError("factor status must truthfully mark all unsourced proxy values")
    grid = dec(scenario["grid_kgco2e_per_kwh"])
    factor_multiplier = dec(scenario["material_factor_multiplier"])
    energy_multiplier = dec(scenario["conversion_energy_multiplier"])
    material_sum = conversion_sum = scrap_sum = Decimal(0)
    procured_sum = Decimal(0)
    breakdown = []
    masses = defaultdict(Decimal)
    for item in bom:
        row = by_material[item["material"]]
        finished_kg = dec(item["finished_mass_g"]) / 1000
        ratio = dec(row["procurement_ratio"])
        if finished_kg <= 0 or ratio < 1:
            raise ValueError(f"invalid mass or procurement ratio for {item['material']}")
        if abs(dec(row["yield"]) * ratio - 1) > dec("0.000000001"):
            raise ValueError(f"yield/ratio mismatch for {item['material']}")
        factor = dec(row["material_kgco2e_per_kg"])
        conversion_kwh = dec(row["conversion_kwh_per_kg_finished"]) * finished_kg * energy_multiplier
        if factor < 0 or conversion_kwh < 0:
            raise ValueError(f"negative factor or energy for {item['material']}")
        purchased_kg = finished_kg * ratio
        scrap_kg = purchased_kg - finished_kg
        material = purchased_kg * factor * factor_multiplier
        conversion = conversion_kwh * grid
        scrap = scrap_kg * dec(config["scrap_disposal_kgco2e_per_kg_loss"])
        material_sum += material
        conversion_sum += conversion
        scrap_sum += scrap
        procured_sum += purchased_kg
        masses[item["scope"]] += finished_kg
        breakdown.append({
            "material": item["material"], "scope": item["scope"],
            "finished_kg": float(finished_kg), "purchased_kg": float(purchased_kg),
            "scrap_kg": float(scrap_kg), "material_kgco2e": float(material),
            "conversion_kwh": float(conversion_kwh), "conversion_kgco2e": float(conversion),
            "scrap_kgco2e": float(scrap),
            "subtotal_kgco2e": float(material + conversion + scrap),
        })
    if masses["Kettle"] != dec("0.723") or masses["Packaging"] != dec("0.1378"):
        raise ValueError("finished BOM mass check failed")
    assembly_kwh = dec(config["assembly_and_packing_kwh_per_kettle"]) * energy_multiplier
    assembly = assembly_kwh * grid
    transport = (procured_sum / 1000) * dec(scenario["inbound_distance_km"]) * dec(config["inbound_truck_kgco2e_per_tonne_km"])
    stages = {
        "assumed_material_supply_kgco2e": float(material_sum),
        "component_and_packaging_conversion_kgco2e": float(conversion_sum),
        "assembly_and_packing_kgco2e": float(assembly),
        "assumed_inbound_transport_kgco2e": float(transport),
        "assumed_scrap_disposal_kgco2e": float(scrap_sum),
    }
    total = sum(map(dec, stages.values()))
    return {
        "scenario": scenario_name,
        "screening_gwp100_kgco2e_per_packaged_kettle": float(total),
        "stage_contributions": stages,
        "material_breakdown": breakdown,
        "top_three_material_rows": [x["material"] for x in sorted(breakdown, key=lambda x: x["subtotal_kgco2e"], reverse=True)[:3]],
        "checks": {
            "finished_mass_kg": float(sum(masses.values())),
            "purchased_mass_kg": float(procured_sum),
            "mass_balance_kg": float(procured_sum - sum(masses.values()) - sum(dec(x["scrap_kg"]) for x in breakdown)),
            "contribution_sum_residual_kgco2e": float(total - sum(map(dec, stages.values()))),
            "upstream_supplier_closure": "not demonstrated; cumulative material factors are assumed proxies",
            "formal_lcia_method": "unknown; screening proxy convention only",
        },
    }


def main() -> None:
    verify_pp_exchange()
    config = json.loads(CONFIG.read_text())
    bom, inputs = read_csv(BOM), read_csv(INPUTS)
    runs = {name: calculate(name, bom, inputs, config) for name in ("low", "central", "high")}
    central = runs["central"]
    if not runs["low"]["screening_gwp100_kgco2e_per_packaged_kettle"] < central["screening_gwp100_kgco2e_per_packaged_kettle"] < runs["high"]["screening_gwp100_kgco2e_per_packaged_kettle"]:
        raise ValueError("scenario ordering failed")
    output = {
        "run_id": config["run_id"], "declared_unit": config["declared_unit"],
        "calculation_status": "illustrative assumption-based screening estimate; not a verified full LCA",
        "method": config["method"],
        "central": central,
        "scenario_range_kgco2e": [runs["low"]["screening_gwp100_kgco2e_per_packaged_kettle"], runs["high"]["screening_gwp100_kgco2e_per_packaged_kettle"]],
        "scenarios": runs,
        "provenance": "BOM is sourced; PP material ratio and electricity are sourced from USLCI molding exchange; all other numeric burden factors and operating parameters are explicit assumptions.",
        "limitations": ["No complete supplier closure", "No verified material-factor LCIA method/version", "Illustrative geographic/year scenario", "Omitted auxiliary fuels and other conversion inputs", "Low/high scenarios are not a statistical interval"],
    }
    result_dir = ROOT / "results"
    result_dir.mkdir(exist_ok=True)
    (result_dir / "screening-001.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    with (result_dir / "screening_contributions.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(central["material_breakdown"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(central["material_breakdown"])
    print(json.dumps({"run_id": output["run_id"], "central_kgco2e": central["screening_gwp100_kgco2e_per_packaged_kettle"], "scenario_range_kgco2e": output["scenario_range_kgco2e"]}, indent=2))


if __name__ == "__main__":
    main()
