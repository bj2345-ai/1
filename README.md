# BC1 1 L electric kettle: independent factory-gate LCA work

## 1. Study identity and purpose

**Title:** BC1 1 L plastic electric kettle, packaged, factory-gate GWP100. **Public alias:** `bj2345-ai`. **Repository:** https://github.com/bj2345-ai/1. **Run IDs:** preserved audit `independent-001` and subsequent approximate `screening-001`. **Study date:** 2026-10-08. **Goal:** build and audit a reproducible cradle-to-factory-gate model for one packaged representative kettle, then compare independent class results on a common boundary. The original audit is preserved. The separate screening run uses explicitly assumed factors; no class comparison has been made. Git tag: `independent-001`. The final commit SHA must be taken from Git after committing and entered in the course form; it is deliberately absent here.

## 2. Product, declared unit and system boundary

**Declared unit:** one manufactured and packaged BC1 1 L plastic electric kettle at the factory gate. It is a representative base case, not a named commercial model. The [BOM](data/bom.csv) transcribes the finished masses from the [EU Electric Kettles preparatory study (2020), Task 4, Tables 4-3, 4-4 and 4-8 (printed pp. 26, 27 and 30)](https://publica-rest.fraunhofer.de/server/api/core/bitstreams/3df3f4d6-3717-4261-99e3-a232323111d6/content). The audit confirms **723 g kettle + 137.8 g packaging = 860.8 g packaged**. Material detail and the pre-calculation hypothesis are in the [system sketch](docs/model.md).

The intended boundary includes raw-material supply, component manufacture, kettle assembly, packaging production/conversion and packing. Customer delivery, use, water heating and end of life are excluded. No cut-off threshold has been adopted; missing flows are listed as gaps. The kettle's manufacturing country and year are unknown. The screening run uses an illustrative North American-style 2025 supply scenario, not a claim about the real factory. The 2020 date refers to the BOM source, not production. The USLCI candidates are mainly North American or US and are geographical proxies only. No use-phase or end-of-life extension is included.

## 3. Foreground inventory and quantitative assumptions

The 12 sourced finished masses are in [bom.csv](data/bom.csv); original unresolved inputs are `null` in [model.json](data/model.json). The later approximate run uses the complete per-material [screening input table](data/screening_inputs.csv) and [scenario configuration](data/screening_config.json). No missing input is silently assigned zero.

| Parameter/input | Value and unit | Evidence/source | Status |
| --- | --- | --- | --- |
| Kettle materials | 723 g | 2020 EU study BOM | Sourced |
| LDPE and cardboard packaging | 6.3 g and 131.5 g | 2020 EU study BOM | Sourced |
| Material climate factors | 0.8–6.0 kg CO₂-eq/kg; each listed in input table | Author-chosen illustrative cumulative cradle-to-gate proxies | **All assumed** |
| Procurement yields | Steel 90%; other kettle materials 95%; packaging 98% | No actual kettle factory yields supplied | Assumed |
| PP resin procurement | 1.034 kg/kg finished PP part | USLCI injection molding exchange, UUID `89a2b59a-1ca2-34f5-acc8-a8eaaa6fa870`, version `00.00.014` | Sourced quantity; suitability for kettle assumed |
| Nylon grade | Unfilled PA6 proxy | Grade unspecified in BOM | Assumed |
| Component/packaging conversion electricity | 0.3–1.5 kWh/kg finished by material | Illustrative processing intensities | Assumed |
| PP molding electricity | 6.444 MJ/kg = 1.79 kWh/kg finished PP | Same USLCI exchange, using 3.6 MJ/kWh | Sourced quantity; suitability assumed |
| Assembly and packing | 0.15 kWh/kettle | No factory energy supplied | Assumed |
| Grid intensity | 0.45 kg CO₂-eq/kWh | Illustrative | Assumed |
| Inbound transport | 500 km; 0.10 kg CO₂-eq/tonne-km | No route/mode data supplied | Assumed |
| Scrap treatment | 0.10 kg CO₂-eq/kg loss; no credit | No destination data supplied | Assumed |
| Prices and monetary sectors | Not applicable | No monetary proxy used | Not applicable |

For yield `y`, purchased kg = finished g ÷ 1000 ÷ `y`; PP uses the recorded 1.034 resin-to-part ratio. Scrap kg = purchased − finished. Material reference factors are per purchased kilogram; conversion electricity is per finished kilogram. The PP material factor remains **assumed**, despite the sourced molding quantities. Screening counts resin supply and electricity once and does not separately add a complete PP molding process impact. Other molding inputs, such as auxiliary fuels, are omitted. No recycling credit is claimed. A future fully linked process calculation must normalize demands by each provider reference amount/unit and examine which energy and transport burdens background records already include.

## 4. Background data and matching decisions

The downloaded [USLCI 1.2025-06.0 JSON-LD archive](data/manifest.json) was verified by SHA-256 `55437502fc33d193236d50fd87a361880beea82a27139d1803be38ae0f0934b0` on 2026-10-08. The [complete mapping](data/matches.csv) records all 12 BOM materials, selected candidate UUIDs/versions and rejections. [Inspected record metadata](results/dataset_records.csv) gives candidate names, releases, UUIDs, versions, geography, validity dates, reference flows/amounts/units, source URL, archive member, retrieval date and archive hash. The [screening source record](data/screening_sources.json) supplies the same metadata for the PP molding quantity used in the estimate. The [search log](docs/search-log.md) lists queries, alternatives and rationale.

Six BOM inputs have candidate material processes: stainless 304 coil, PP resin, PVC resin, ABS resin, LDPE resin and corrugated product. They are **unit-process inventory candidates**, not cumulative GWP factors or validated component impacts. Brass, nylon, POM, PC and silicone have no matching process in this inspected USLCI release. The copper `USLCI to USEEIO` bridge was rejected because its external USEEIO background is unavailable. No monetary estimates are used. Direct default-provider gaps are in [provider_gaps.json](results/provider_gaps.json); an alternative provider may exist but has not been linked or verified. The authenticated TianGong CLI search returned `SUPABASE_OAUTH_LOGIN_REQUIRED`. A later search of the [public historical TianGong tree](docs/tiangong-public.md) found a copper candidate, but the brass and stainless records have zero input exchanges and were rejected as standalone material backgrounds. Nylon-yarn and silicone-monomer proxies were also rejected; no POM or PC production process was found. These historical records were **not applied** to the preserved independent audit.

## 5. Calculation and impact-assessment methods

The [strict matrix solver](matrix_solver.py) implements `A s = f`, `g = B s`, `h = C g` with NumPy `2.3.5` `numpy.linalg.solve`, including provider/unit and characterization checks. [Synthetic tests](tests/test_matrix_solver.py) verify the algorithm. It has **not** produced a full kettle result because real provider links and LCIA characterization are incomplete. The [archive audit](kettle_lca.py) checks record identities, references and direct provider gaps.

The separate [screening calculator](screening.py) uses, per material `i`, `purchased_i × assumed cumulative material factor_i + finished_i × conversion kWh/kg_i × assumed grid factor + scrap_i × assumed disposal factor`. It then adds assembly electricity × grid factor and purchased tonnes × inbound km × truck factor. The nominal time horizon is 100 years; **a formal GWP100 characterization method, version and flow mapping are unknown**. The title “GWP100 screening” is a proxy convention, not an application of a named LCIA method. All factor values and their status are in the input table. No unit-process supplier links are solved in this screening run.

Allocation and system model for a full linked model remain unknown; inspected USLCI records may declare `NO_ALLOCATION`, which does not define the whole model. Screening assumes no recycling credit, models scrap disposal with a proxy and does not model biogenic-carbon flows separately. Uncharacterized flows and missing upstream providers are unresolved, not zero. The [closure assessment](results/closure_assessment.json) and [provider-gap file](results/provider_gaps.json) document these gaps. The [matrix reference](https://doi.org/10.1065/lca2007.08.360) and [NumPy documentation](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html) describe the strict formulation.

## 6. How to reproduce the analysis

Repository map: [BOM](data/bom.csv), [foreground model](data/model.json), [dataset matches](data/matches.csv), [archive manifest](data/manifest.json), [system sketch](docs/model.md), [search/decision log](docs/search-log.md), [prompt log](docs/decisions.md), [audit program](kettle_lca.py), [matrix solver](matrix_solver.py), [independent result](results/independent.json), [screening code](screening.py), [report generator](report.py), [HTML report](report.html), and [tests](tests/test_screening.py). The verified USLCI ZIP is cached at `cache/uslci_2025_06.zip` and is ignored by Git; the precise public retrieval URL and hash are in the manifest.

The optional login-free historical TianGong inspection is documented in [tiangong-public.md](docs/tiangong-public.md), with its [Git commit manifest](data/tiangong_manifest.json) and [candidate table](results/tiangong_candidates.csv). It requires a separate public Git clone and does not change the tagged independent result.

Run on Linux with Python 3.12 and NumPy 2.3.5 (the versions used here):

```bash
cd /workspace/1
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python kettle_lca.py retrieve
.venv/bin/python kettle_lca.py audit
.venv/bin/python screening.py
.venv/bin/python report.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m json.tool results/independent.json
```

For another checkout, replace `/workspace/1` with its repository root. The audit writes `results/independent.json`, `results/dataset_records.csv` and `results/provider_gaps.json`. The screening run writes `results/screening-001.json` and `results/screening_contributions.csv`; `report.py` writes the standalone [report.html](report.html), which can be opened in a browser. Open the JSON/CSV files directly for full precision. Retrieval requires HTTPS access to `raw.githubusercontent.com`; no account is required for the public USLCI archive. TianGong's current-platform search requires a usable CLI OAuth session; a [historical public dataset search](docs/tiangong-public.md) needs no account. Do not add credentials to the repository. No randomness or seed is used. A complete **verified** kettle calculation still requires measured foreground choices, background providers and a compatible LCIA method. The approximate screening run needs no account beyond downloading the public archive. The [search log](docs/search-log.md) gives the remaining access/manual steps.

## 7. Results, checks and interpretation

The preserved [independent audit](results/independent.json) has **no calculable full-LCA GWP100 value**. In response to the student's request for an approximate result, the separate [screening run](results/screening-001.json) estimates **3.486 kg CO₂-eq per packaged kettle** in its central assumed scenario. This is an illustrative, assumption-based GWP100-style estimate, **not a verified full LCA or a value characterized with a named method/version**. See the [HTML report](report.html) and [complete contribution CSV](results/screening_contributions.csv).

| Central stage | kg CO₂-eq/kettle |
| --- | ---: |
| Assumed material supply | 2.8676 |
| Component and packaging conversion electricity | 0.5007 |
| Assembly and packing electricity | 0.0675 |
| Assumed inbound transport | 0.0453 |
| Assumed scrap disposal | 0.0045 |
| **Total** | **3.4856** |

The top three material-row subtotals are stainless steel **1.3258**, PP **1.0076** and nylon/assumed PA6 **0.2942** kg CO₂-eq. The predicted PP lead in the [pre-calculation sketch](docs/model.md) did not hold under these assumptions: stainless leads because its assumed factor is high. This ranking is sensitive to unverified material factors. Every material row and its material, conversion and scrap components is in the CSV; assembly and inbound transport are allocated only at stage level.

The sourced finished-mass check passes: 0.7230 kg kettle + 0.1378 kg packaging = 0.8608 kg. Assumed purchased mass is 0.9060 kg, with 0.0452 kg modeled losses. Screening mass and stage-contribution residuals are zero at reported precision. Units convert grams to kg, MJ to kWh and kg to tonnes for transport. The six USLCI material candidate processes all have unresolved direct provider links, and no appropriate complete background exists for several materials; **full upstream supplier closure fails**. The assumed cumulative factors mask upstream detail and cannot cure this failure. The PP conversion calculation charges its recorded resin and electricity once each, but omitted auxiliary inputs and possible factor-boundary overlap remain a double-counting/omission risk. Production geography, year, grade, yields, grid, energy and material factors are unknown for the actual kettle. The result cannot establish a product-specific footprint or a sound comparison with classmates' characterized LCAs.

## 8. Uncertainty and sensitivity

Statistical uncertainty was **not calculated**: no defensible parameter distributions, correlations or primary-data ranges are available. Therefore there is no Monte Carlo method, draw count, seed, convergence test, mean, median, P05/P95 or conditional central 90% interval. The [configuration](data/screening_config.json) instead defines deterministic joint-assumption scenarios: **2.224 kg CO₂-eq low**, **3.486 central**, and **5.149 high** per kettle. Low/high simultaneously vary material-factor multipliers (0.70/1.30), conversion-energy multipliers (0.50/1.50), grid intensity (0.30/0.70 kg CO₂-eq/kWh), and inbound distance (250/1000 km). These are deliberately chosen stress cases, **not confidence bounds**. Provider/method alternatives and variation between repeated AI runs were not quantified; no class comparison has occurred.

## 9. Codex and human decisions

Codex model family: GPT-6, as displayed in the session; exact build/version and inference settings are unknown. Work occurred on 2026-10-08. Consequential prompts, assistant choices, one parser correction and independent checks are summarized in the [curated decision log](docs/decisions.md). The student supplied the task, boundary and BOM. The student authorized approximate assumptions when a full result could not be obtained. Codex selected the provisional North American-style context, PA6 proxy, yields, energy and cumulative factors; the student has not confirmed them as real-world values. The independent USLCI choices are in [matches.csv](data/matches.csv); subsequent historical TianGong candidates are in [tiangong_candidates.csv](results/tiangong_candidates.csv). No external human review or classmate result was used. The generated audit outputs were independently checked against the original BOM and downloaded JSON-LD record IDs/versions.

## 10. Independent and revised runs

The original `independent-001` audit is preserved in [independent.json](results/independent.json) and the `independent-001` Git tag. Its full cradle-to-gate GWP100 is unavailable. The later `screening-001` [result](results/screening-001.json) is a separately labeled approximation made after the student authorized assumptions. It does **not** overwrite or retrospectively convert the original audit into a numerical independent LCA. No class comparison or single-choice revision has occurred. Thus a prior numerical class-comparison result, one changed decision, revised numerical result, absolute/percentage change and explanatory comparison are **not applicable**. When a genuine revision is made, preserve both runs and identify its prior commit and one changed choice. Submit the final 40-character independent commit SHA separately in the course form.

**Unresolved for student review:** actual manufacturing country/year, nylon grade, material-factor sources and formal LCIA method/version, supplier closure, measured yields/conversion/assembly energy, transport and scrap management. The course form also needs the student's full name, email and instructor-provided submission password; these are not stored in this public repository. The present numerical result is approximate and must be labeled as such wherever quoted.
