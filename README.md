# BC1 1 L electric kettle: independent factory-gate LCA work

## 1. Study identity and purpose

**Title:** BC1 1 L plastic electric kettle, packaged, factory-gate GWP100. **Public alias:** `bj2345-ai`. **Repository:** https://github.com/bj2345-ai/1. **Run ID:** `independent-001`. **Study date:** 2026-10-08. **Goal:** build and audit a reproducible cradle-to-factory-gate model for one packaged representative kettle, then compare independent class results on a common boundary. This repository is the independent run; no revised run or comparison has been made. Git tag: `independent-001`. The final commit SHA must be taken from Git after committing and entered in the course form; it is deliberately absent here.

## 2. Product, declared unit and system boundary

**Declared unit:** one manufactured and packaged BC1 1 L plastic electric kettle at the factory gate. It is a representative base case, not a named commercial model. The [BOM](data/bom.csv) transcribes the finished masses from the [EU Electric Kettles preparatory study (2020), Task 4, Tables 4-3, 4-4 and 4-8](https://publica-rest.fraunhofer.de/server/api/core/bitstreams/3df3f4d6-3717-4261-99e3-a232323111d6/content). The audit confirms **723 g kettle + 137.8 g packaging = 860.8 g packaged**. Material detail and the pre-calculation hypothesis are in the [system sketch](docs/model.md).

The intended boundary includes raw-material supply, component manufacture, kettle assembly, packaging production/conversion and packing. Customer delivery, use, water heating and end of life are excluded. No cut-off threshold has been adopted; missing flows are listed as gaps. The kettle's manufacturing country and year are unknown. The 2020 date refers to the BOM source, not production. The USLCI candidates are mainly North American or US and are geographical proxies only. No use-phase or end-of-life extension is included.

## 3. Foreground inventory and quantitative assumptions

All 12 material amounts and their sourced/finished-mass status are in [bom.csv](data/bom.csv). The [model file](data/model.json) holds unresolved inputs as `null`, never as zero.

| Parameter | Value and unit | Evidence | Status |
| --- | --- | --- | --- |
| Kettle finished materials | 723 g total | 2020 BOM, 10 rows | Sourced |
| LDPE foil and cardboard finished mass | 6.3 g and 131.5 g | 2020 BOM | Sourced |
| Purchased material yields/losses | Unknown | No procurement or scrap data supplied | Unresolved |
| Nylon grade | Unknown (PA6/PA66 not chosen) | BOM does not specify grade | Unresolved |
| Molding, metal forming, wire, foil and box conversion | Unknown except inspected PP molding candidate | No complete component route supplied | Unresolved |
| Assembly/packing electricity | Unknown kWh per kettle | No factory data supplied | Unresolved |
| Inbound transport | Unknown | No distances or modes supplied | Unresolved |
| Scrap destinations/credits | Unknown | No kettle-specific scrap data supplied | Unresolved |
| Prices | Not applicable | No monetary model selected | Not applicable |

For a material with yield `y`, purchased kg would be `finished_mass_g / 1000 / y`, but no `y` has been assigned. Each process demand must then be divided by its actual reference output amount and converted to the provider's reference unit. The inspected PP molding record consumes **1.034 kg PP resin and 6.444 MJ electricity per kg part** and records scrap; using it as an all-in conversion route requires excluding separate charges for those same inputs. Background processes can include other upstream energy and transport. The audit treats their links as unresolved until provider closure is demonstrated.

## 4. Background data and matching decisions

The downloaded [USLCI 1.2025-06.0 JSON-LD archive](data/manifest.json) was verified by SHA-256 `55437502fc33d193236d50fd87a361880beea82a27139d1803be38ae0f0934b0` on 2026-10-08. The [complete mapping](data/matches.csv) records all 12 BOM materials, selected candidate UUIDs/versions and rejections. [Inspected record metadata](results/dataset_records.csv) gives each named dataset, release, UUID, version, geography, validity dates, reference flow/amount/unit, source URL, archive member, retrieval date and archive hash. The [search log](docs/search-log.md) lists queries, alternatives and rationale.

Six BOM inputs have candidate material processes: stainless 304 coil, PP resin, PVC resin, ABS resin, LDPE resin and corrugated product. They are **unit-process inventory candidates**, not cumulative GWP factors or validated component impacts. Brass, nylon, POM, PC and silicone have no matching process in this inspected release. The copper `USLCI to USEEIO` bridge was rejected because its external USEEIO background is unavailable. No monetary estimates are used. Direct default-provider gaps are in [provider_gaps.json](results/provider_gaps.json); an alternative provider may exist but has not been linked or verified. TianGong search returned `SUPABASE_OAUTH_LOGIN_REQUIRED`; no TianGong record or ID is claimed.

## 5. Calculation and impact-assessment methods

The [strict matrix solver](matrix_solver.py) implements `A s = f`, where diagonal entries are process reference outputs and off-diagonal entries are linked technosphere requirements; `B s` gives elementary inventory and characterization `C(B s)` gives GWP100. It uses NumPy `2.3.5` `numpy.linalg.solve`, checks provider IDs and units, and rejects missing declared climate factors. A [synthetic two-process check](tests/test_matrix_solver.py) exercises upstream scaling; it is **not** a kettle result. The [kettle audit](kettle_lca.py) verifies the real archive, BOM, record identities, direct supplier links and unresolved inputs before any result is claimed.

Allocation/system model: unknown for the full linked model. Candidate USLCI records declare `NO_ALLOCATION` where recorded, but this does not establish a common system model. Kettle scrap recycling, credits and biogenic-carbon treatment: unresolved. **Characterization method and version: not selected; no GWP100 kettle value was calculated.** The downloaded USLCI JSON-LD archive contains no LCIA method records. A method such as IPCC GWP100 must be sourced, versioned and flow-matched before calculation. Uncharacterized climate flows and missing upstream providers must be reported, not assigned zero. The [matrix formulation reference](https://doi.org/10.1065/lca2007.08.360) and [NumPy solve documentation](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html) describe the algorithm, not the missing datasets.

## 6. How to reproduce the analysis

Repository map: [BOM](data/bom.csv), [foreground model](data/model.json), [dataset matches](data/matches.csv), [archive manifest](data/manifest.json), [system sketch](docs/model.md), [search/decision log](docs/search-log.md), [prompt log](docs/decisions.md), [audit program](kettle_lca.py), [matrix solver](matrix_solver.py), [results](results/independent.json), and [tests](tests/test_matrix_solver.py). The verified USLCI ZIP is cached at `cache/uslci_2025_06.zip` and is ignored by Git; the precise public retrieval URL and hash are in the manifest.

Run on Linux with Python 3.12 and NumPy 2.3.5 (the versions used here):

```bash
cd /workspace/1
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python kettle_lca.py retrieve
.venv/bin/python kettle_lca.py audit
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m json.tool results/independent.json
```

For another checkout, replace `/workspace/1` with its repository root. The audit writes `results/independent.json`, `results/dataset_records.csv` and `results/provider_gaps.json`. Open those text/CSV files directly. Retrieval requires HTTPS access to `raw.githubusercontent.com`; no account is required for the public USLCI archive. TianGong's authenticated search requires a usable CLI OAuth session and was unavailable here. Do not add credentials to the repository. No randomness or seed is used. A complete numerical kettle calculation also requires missing foreground choices, background providers and a compatible LCIA method. The [search log](docs/search-log.md) gives the remaining access/manual steps.

## 7. Results, checks and interpretation

The [independent audit result](results/independent.json) has status **blocked: full cradle-to-gate GWP100 cannot be calculated**. GWP100 in kg CO2-eq per packaged kettle is **not calculated**, not `0`. A numerical material/process contribution breakdown and top three contributors are likewise not calculated. The predicted PP contribution in the [system sketch](docs/model.md) is a pre-calculation hypothesis only. No figure is generated because no valid total or ranked contributions exist. There is one independent baseline and no scenario/method comparison.

The mass check passed: 723 g + 137.8 g = 860.8 g. Six of twelve BOM inputs have candidate records; five are missing and copper's only candidate is rejected. Those six candidates themselves have at least one unresolved direct default-provider link each; the detailed examples are in [provider_gaps.json](results/provider_gaps.json). Full upstream supplier closure therefore fails. Reference outputs in the inspected records are 1 kg; purchased masses and per-kettle scaling remain unresolved. A contribution-sum check is not applicable to this kettle because no contributions were calculated. The synthetic solver test does check its own residual and sum. Double counting is prevented conceptually by keeping PP resin and the all-in PP molding alternative mutually exclusive. The current archive, missing materials, production geography, unknown yields/energy and absent LCIA method do not support a product GWP ranking or comparison with classmates.

## 8. Uncertainty and sensitivity

Not calculated: a complete deterministic baseline is not available. No parameter distributions, correlations, Monte Carlo draws, seed, convergence result, mean, median, P05/P95 or conditional central 90% interval exists. Future parameter uncertainty (yields, manufacturing electricity), provider/method scenarios (including nylon grade) and variation between repeated AI-assisted runs must be reported separately. No numerical sensitivity claim is made from this incomplete model.

## 9. Codex and human decisions

Codex model family: GPT-6, as displayed in the session; exact build/version and inference settings are unknown. Work occurred on 2026-10-08. Consequential prompts, assistant choices, one parser correction and independent checks are summarized in the [curated decision log](docs/decisions.md). The student supplied the task, boundary and BOM. The student has not yet chosen manufacturing geography, nylon grade, yields, energy inputs or a licensed additional dataset. All selected/rejected record matches are documented in [matches.csv](data/matches.csv). No external human review or classmate result was used. The generated audit outputs were independently checked against the original BOM and downloaded JSON-LD record IDs/versions.

## 10. Independent and revised runs

`independent-001` is preserved in [independent.json](results/independent.json) and the `independent-001` Git tag; its value is unavailable because the model is incomplete. The full commit SHA is submitted separately and is not embedded in this README. No revised run exists, so prior commit, changed decision, predicted effect, original/revised numeric results and absolute/percentage difference are **not applicable**. A later revision should write a new run file and tag without overwriting this independent record, and distinguish a corrected error from a defensible modeling alternative.

**Unresolved for student review before publication:** confirm manufacturing location/year and nylon grade; provide or authorize an appropriate source for brass, copper, nylon, POM, PC and silicone; decide component routes and sourcing of yields, assembly/packaging energy, transport, scrap treatment and allocation; choose a compatible GWP100 method/version. The present work is an auditable incomplete model, not a finished kettle impact result.
