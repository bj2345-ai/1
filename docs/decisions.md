# Curated prompts and decision log

Date: 2026-10-08. Assistant: Codex (GPT-6 family); exact displayed model build, reasoning setting, temperature and seed are unavailable.

1. **Student brief:** Build a BC1 1 L packaged electric-kettle factory-gate LCA tool; use the stated 12-line finished-mass BOM; investigate grade, losses, manufacturing energy and allocation; search TianGong and USLCI; report GWP100 only after unit, provider, missing-flow and double-counting checks. Preserve an independent result before class comparison.
2. **README direction:** Use ten sections covering study identity, product and boundary, inventory, background matching, calculation, reproduction, results, uncertainty, Codex and human decisions, and independent/revised runs. Use actual files and values; label unavailable items rather than inventing them. Keep full name and email out of public README.
3. **Assistant decision:** Select the USLCI June 2025 JSON-LD ZIP for reproducible record inspection after finding that the September 2026 `.zolca` is an openLCA archive. Verify its SHA-256 before reading. Do not mix releases in one calculation.
4. **Assistant decision:** Keep all unprovided yields, conversion services, assembly electricity, transport, scrap treatment, allocation and LCIA method unresolved. The student's repeated BOM did not specify a nylon grade or production geography. Do not infer those from a database's geography.
5. **Assistant decision:** Reject the copper USEEIO bridge as a self-contained copper inventory. Keep PP resin as a candidate; log PP injection molding as an alternative that already includes resin and electricity. Reject recycled cardboard as a baseline because recycled content is unknown.
6. **Error correction:** The first audit rejected the copper bridge's reference-flow name because it differs from its process name. The parser was corrected to accept a sole product output, while keeping that record marked rejected for the kettle model. The audit then completed.
7. **Independent verification:** The code checks the BOM mass sum, real process UUID/version/reference exchanges, direct default-provider links and unresolved fields. The generic matrix solver is tested on a synthetic two-process inventory. No kettle GWP result has passed full-supply-chain checks.

No classmate result, comparison answer, private correspondence, account credential or manually edited impact figure has been used. Human confirmation of manufacturing geography and nylon grade is pending; no material-match choice has yet been accepted by the student.
