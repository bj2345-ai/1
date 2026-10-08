"""Render the assumption-based screening run as a portable HTML report."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def esc(value):
    return html.escape(str(value))


def number(value, digits=3):
    return f"{value:,.{digits}f}"


def main():
    run = json.loads((ROOT / "results/screening-001.json").read_text())
    central = run["central"]
    stages = central["stage_contributions"]
    material_rows = "\n".join(
        f"<tr><td>{esc(row['material'])}</td><td>{number(row['finished_kg'] * 1000, 2)}</td>"
        f"<td>{number(row['purchased_kg'] * 1000, 2)}</td><td>{number(row['material_kgco2e'])}</td>"
        f"<td>{number(row['conversion_kgco2e'])}</td><td>{number(row['subtotal_kgco2e'])}</td></tr>"
        for row in central["material_breakdown"]
    )
    stage_rows = "\n".join(
        f"<tr><td>{esc(key.replace('_kgco2e', '').replace('_', ' ').title())}</td><td>{number(value, 4)}</td></tr>"
        for key, value in stages.items()
    )
    total = central["screening_gwp100_kgco2e_per_packaged_kettle"]
    low, high = run["scenario_range_kgco2e"]
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BC1 kettle | LCA screening report</title>
<style>
body{{font:16px/1.55 system-ui,sans-serif;max-width:1000px;margin:0 auto;padding:2rem;color:#173044;background:#f8fafb}}
h1,h2{{line-height:1.2}}h1{{margin-bottom:.3rem}}.lead{{font-size:1.2rem}}
.card{{background:white;border:1px solid #d5dfe4;border-radius:10px;padding:1.3rem;margin:1.2rem 0}}
.number{{font-size:2.4rem;font-weight:750;color:#006b70}}.caution{{border-left:5px solid #c77816;padding:1rem;background:#fff7e8}}
table{{border-collapse:collapse;width:100%;font-size:.9rem}}th,td{{border-bottom:1px solid #d5dfe4;padding:.5rem;text-align:left}}th{{background:#eaf1f5}}
td:not(:first-child),th:not(:first-child){{text-align:right}}.scroll{{overflow-x:auto}}a{{color:#006b70}}
</style></head><body>
<h1>BC1 1 L packaged electric kettle</h1><p class="lead">Factory-gate climate-impact screening · run screening-001 · 8 October 2026</p>
<div class="card"><div>Approximate central result per packaged kettle</div><div class="number">{number(total, 3)} kg CO₂-eq</div>
<div>Assumption stress scenarios: {number(low, 3)}–{number(high, 3)} kg CO₂-eq. This is not a confidence interval.</div></div>
<div class="caution"><strong>Interpretation:</strong> All 12 material climate factors and most manufacturing parameters are illustrative assumptions. A named, versioned LCIA characterization method was not applied. Upstream supplier closure has not been demonstrated. This figure is an approximate screening estimate, not a verified full LCA result or a defensible class comparison benchmark.</div>
<section class="card"><h2>Product and boundary</h2><p>One manufactured and packaged representative BC1 1 L plastic kettle at the factory gate. The sourced 2020 EU preparatory-study BOM contains 723.0 g of kettle materials and 137.8 g of packaging: 860.8 g finished total. Included: assumed material supply, component conversion, assembly and packing, inbound transport and scrap disposal. Excluded: customer delivery, use and end of life. Manufacturing location and year are unknown; the North American-style 2025 context is illustrative.</p><p><a href="data/bom.csv">BOM</a> · <a href="docs/model.md">System sketch and prediction</a></p></section>
<section class="card"><h2>Contributions</h2><p>Stages sum to {number(total, 4)} kg CO₂-eq per packaged kettle. Top material rows: {', '.join(esc(x) for x in central['top_three_material_rows'])}.</p><div class="scroll"><table><thead><tr><th>Stage</th><th>kg CO₂-eq</th></tr></thead><tbody>{stage_rows}</tbody></table></div>
<h3>Material rows</h3><div class="scroll"><table><thead><tr><th>Material</th><th>Finished g</th><th>Purchased g</th><th>Assumed supply kg CO₂-eq</th><th>Conversion kg CO₂-eq</th><th>Subtotal kg CO₂-eq</th></tr></thead><tbody>{material_rows}</tbody></table></div><p>Material subtotals also contain small scrap-disposal terms; assembly and inbound transport are stage totals outside the material rows.</p></section>
<section class="card"><h2>Method and evidence</h2><p>Each material row uses purchased mass × assumed cumulative material factor, plus finished mass × conversion electricity intensity × assumed grid factor, plus scrap-disposal proxy. Assembly adds 0.15 kWh × 0.45 kg CO₂-eq/kWh. Inbound transport assumes 500 km and 0.10 kg CO₂-eq per tonne-km. The nominal horizon is 100 years, but formal LCIA source and version are unknown. No matrix inventory result is claimed for this screening calculation.</p><p>The BOM masses are sourced. The PP molding record from USLCI 1.2025-06.0 (UUID 89a2b59a-1ca2-34f5-acc8-a8eaaa6fa870, version 00.00.014) supplies 1.034 kg resin and 6.444 MJ electricity per kg molded part. PP resin's climate factor remains assumed. Other direct molding inputs are omitted. All other numerical burden factors and process parameters are assumptions. <a href="data/screening_inputs.csv">Factor, yield and energy table</a> · <a href="data/screening_config.json">Scenario settings</a> · <a href="data/matches.csv">Dataset matches</a> · <a href="data/manifest.json">USLCI source manifest</a></p></section>
<section class="card"><h2>Checks and limits</h2><p>Finished mass: {number(central['checks']['finished_mass_kg'], 4)} kg. Assumed purchased mass: {number(central['checks']['purchased_mass_kg'], 4)} kg. Mass-balance and stage-sum residuals: {number(central['checks']['mass_balance_kg'], 8)} kg and {number(central['checks']['contribution_sum_residual_kgco2e'], 8)} kg CO₂-eq. Unresolved provider links and missing compatible characterization factors prevented a verified cradle-to-gate inventory calculation. The preserved independent audit therefore has no numerical GWP100 value. The 2.224–5.149 range varies chosen assumptions together and is not parameter uncertainty or a P05–P95 interval.</p><p><a href="results/independent.json">Preserved independent audit</a> · <a href="results/closure_assessment.json">Closure assessment</a> · <a href="results/screening-001.json">Full screening results</a> · <a href="results/screening_contributions.csv">Contribution CSV</a> · <a href="README.md">Full study and reproduction README</a></p></section>
<section class="card"><h2>Reproduce</h2><p>Install <code>requirements.txt</code>, then run <code>python kettle_lca.py retrieve</code>, <code>python kettle_lca.py audit</code>, <code>python screening.py</code>, and <code>python report.py</code>. The public USLCI archive is fetched and hash-checked; TianGong historical search details and unresolved alternatives are documented in the README. This report is generated from <code>results/screening-001.json</code>.</p></section>
</body></html>"""
    (ROOT / "report.html").write_text(page, encoding="utf-8")
    print(ROOT / "report.html")


if __name__ == "__main__":
    main()
