# Key user prompts (curated excerpts)

These are verbatim excerpts of consequential user requests in this project, in conversation order. They are not a complete chat transcript. The detailed modeling responses and corrections are in [decisions.md](decisions.md). No credentials or personal contact details are included.

## 1. LCA task and boundary

> BUILD YOUR OWN LCA TOOL WITH CODEX
>
> Case: one manufactured and packaged BC1 1 L plastic electric kettle at the factory gate.
> Include raw-material supply, component manufacture, assembly and packaging. Exclude customer delivery, use and end of life.
>
> 1. Define your model. Sketch the system and predict its main contributor before asking Codex to calculate.
> 2. Build your tool with Codex. Search TianGong and USLCI, inspect candidate records, and choose and justify matches. Record dataset IDs, versions, geography and reference units.
> 3. Calculate and check. Report GWP100 in kg CO2-eq per packaged kettle, stating the characterization method and version. Check units, upstream suppliers, missing flows and double counting. Separate sourced values from assumptions.
> 4. Document, publish and compare. Ask Codex to create README.md using all required README fields on this page and the actual files/results in your repository. Review it, publish your own public GitHub repository, and commit the independent result before class comparison. Submit your name, email, repository URL and full commit SHA in the form. Preserve the first result when testing a changed choice.
>
> The BOM contains finished masses, not procurement quantities. Nylon grade, material losses, manufacturing energy and allocation are decisions to investigate; no numerical defaults are supplied. A missing input is not a zero impact.

The sourced 12-row BOM from this prompt is stored without changes in [data/bom.csv](../data/bom.csv).

## 2. README instruction

> Inspect my actual LCA repository: code, input data, dataset matches, assumptions, prompts and generated results. Create README.md so another student or the instructor can interpret and reproduce this analysis.
>
> Use every section below. Give substantive summaries and link detailed tables, logs and figures using relative paths. Use actual values and paths, not illustrative results. Do not invent missing information: mark it unknown, not calculated or not applicable and explain why; ask me where a necessary decision is unresolved. Document the analysis as it exists. Do not change results just to make the README appear complete.
>
> Keep my full name and email in the course submission form only. Do not include credentials, course codes, private messages or restricted database dumps in the public README. The final commit SHA is submitted after committing; do not attempt to embed this README's own future commit hash.

The ten requested README sections are implemented in [README.md](../README.md). This excerpt omits the long field-by-field checklist, which is reflected in those sections.

## 3. Approximation authorization

> 결과를 낼수없으면 appox, assumption으로 해결하고, 언급을 추가해줘

This authorized a **separate assumption-based screening estimate** after the independent audit found that a verified GWP100 could not be calculated. The estimate does not replace the preserved original run.

## 4. Final report request

> 전체 과제를 끝까지 완료하면 report.html로 최종결과를 만들어줘

## 5. Prompt visibility request

> 프롬프트를 볼수있게 만들어줘

This request led to this curated prompt file and an in-page prompt section in [report.html](../report.html).
