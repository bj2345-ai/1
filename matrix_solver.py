"""Strict unit-process GWP solver for a fully linked, normalized inventory.

Input quantities must already use each provider's reference unit. The solver
rejects missing providers and missing factors for declared climate flows.
"""

from __future__ import annotations

import numpy as np


def solve(model: dict) -> dict:
    processes = model["processes"]
    names = [process["id"] for process in processes]
    if len(names) != len(set(names)):
        raise ValueError("duplicate process id")
    index = {name: position for position, name in enumerate(names)}
    n = len(processes)
    technology = np.zeros((n, n), dtype=float)
    demand = np.zeros(n, dtype=float)
    for item in model["demand"]:
        if item["process_id"] not in index:
            raise ValueError(f"missing demand process: {item['process_id']}")
        demand[index[item["process_id"]]] += float(item["amount"])

    factors = model["characterization_factors"]
    for flow in model["climate_flows"]:
        if flow not in factors:
            raise ValueError(f"missing characterization factor: {flow}")
    local_impacts = np.zeros(n, dtype=float)
    for col, process in enumerate(processes):
        reference = float(process["reference_amount"])
        if reference <= 0:
            raise ValueError(f"invalid reference amount: {process['id']}")
        technology[col, col] += reference
        for item in process["inputs"]:
            provider = item.get("provider_id")
            if provider not in index:
                raise ValueError(f"missing upstream provider: {process['id']} -> {provider}")
            if item["unit"] != processes[index[provider]]["reference_unit"]:
                raise ValueError(f"unit mismatch: {process['id']} -> {provider}")
            technology[index[provider], col] -= float(item["amount"])
        for emission in process["emissions"]:
            if emission["flow_id"] in model["climate_flows"]:
                if emission["unit"] != "kg":
                    raise ValueError(f"emission unit mismatch: {emission['flow_id']}")
                local_impacts[col] += float(emission["amount"]) * float(factors[emission["flow_id"]])

    scaling = np.linalg.solve(technology, demand)
    if np.any(scaling < -1e-10):
        raise ValueError("negative process scaling; check linking or allocation")
    contributions = {name: float(scaling[i] * local_impacts[i]) for i, name in enumerate(names)}
    total = float(sum(contributions.values()))
    return {
        "gwp100_kg_co2e": total,
        "contributions_kg_co2e": contributions,
        "process_scaling": {name: float(scaling[i]) for i, name in enumerate(names)},
        "technology_residual_max": float(np.max(np.abs(technology @ scaling - demand))),
        "contribution_residual": float(total - sum(contributions.values())),
    }
