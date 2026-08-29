# Making a sustainability claim this journal will accept

The editors of *ACS Sustainable Chem. Eng.* screen every submission for one thing before anything else: is the sustainability advantage identified, quantified where possible, and compared with what already exists? This file is the editing guide for that question. Section 1 is the general rule; sections 2–6 give the reporting norms by field, drawn from the journal's "Expectations" and "Shaping Effective Practices" editorial series (2020–2026) and standard practice in each field. Read section 1 and the section(s) matching the paper.

Contents: 1 The rule and how to edit toward it · 2 Biomass feedstocks and processing · 3 Bio-based materials and polymers · 4 Life-cycle assessment · 5 Techno-economic analysis · 6 Catalysis, synthesis, solvents, electrochemistry (brief) · 7 Toxicity · 8 Metric definitions

---

## 1. The rule

"A molecule, material, or process is never 'green' in the absolute sense, but it may be 'greener' when compared to what is already known." (Editors, 2024.) Every sustainability word in the draft is therefore a comparative claim and needs three things:

1. **A metric or a specific fact.** E-factor, PMI, atom economy, solvent intensity, energy demand, GHG per functional unit, renewable carbon content, recovery per cycle, TON/TOF, Faradaic efficiency, minimum selling price, or a named property (persistence, toxicity, biodegradation under a named standard).
2. **A comparator.** The incumbent process, the prior best result, or the fossil counterpart, with its number and citation. Self-comparison (this catalyst vs. our own control) is not enough; the editors say so explicitly for durability and performance claims.
3. **A boundary.** What the number includes: gate-to-gate, cradle-to-gate, with or without solvent recovery, with or without water in the E-factor, per kilogram of what.

When the draft has these, the editing job is to state them in the abstract, the last paragraph of the Introduction, and the Conclusions, because the 2026 editorial asks for "explicit statements related to such advances in the abstract, introduction, and conclusion sections," and desk rejections cite sustainability that lives only in the cover letter.

When the draft does not have them, do not manufacture them. Rewrite the sentence as the technical fact it stands for ("recyclable" → "the DES was reused five times with delignification falling from 78 to 72%"), delete the adjective, and put the missing metric at the top of the author queries. The journal's guidance says a full LCA "will be beyond the scope of most manuscripts," but "framing the paper's contribution in the context of product and process life cycles" is expected of every paper, at least qualitatively. A paragraph that says where the process sits in the supply chain, what it replaces, and what the largest remaining burden is (solvent makeup, energy for the 140 °C step, a petroleum-derived reagent) satisfies that in a paper that has no LCA.

### Editing patterns

| Draft says | Edit to | Query if missing |
|---|---|---|
| "a green and sustainable pretreatment" | "a pretreatment that reuses the solvent for five cycles with 91% recovery" | recovery mass balance per cycle |
| "environmentally friendly solvent" | "a solvent with [EHS data: LD₅₀, biodegradability under OECD 301, vapor pressure] compared with [incumbent]" | the EHS data or a solvent-selection-guide ranking (CHEM21, GSK, Pfizer) |
| "renewable feedstock" | "a feedstock with X% biogenic carbon; cultivation and transport emissions of Y kg CO₂e/kg from [source]" | feedstock footprint if the claim is climate-related; "renewable" alone is fine for provenance |
| "biodegradable" | "reached 90% mineralization in 45 days under ISO 14855 industrial composting conditions" | the standard, conditions, and number |
| "low-carbon / carbon-neutral" | "cradle-to-gate GHG of X kg CO₂e per kg product versus Y for the fossil route (same boundary, same LCIA method)" | boundary, method, data year, comparator |
| "cost-effective" | "minimum selling price of $X/kg (2022 USD, 10% IRR) against a market price of $Y" | TEA basis |
| "mild conditions" | "100 °C and atmospheric pressure, versus 170–200 °C and 10–20 bar for organosolv (refs)" | the comparator conditions |
| "atom-economical / waste-free" | "atom economy 87%; E-factor 3.4 (excluding water) / 12 (including water)" | which waste streams are counted |
| "circular" | "X% of the solvent / catalyst / product is recovered and reused; the remainder goes to [fate]" | recovery data |
| "reduces energy consumption" | "a cumulative energy demand of X MJ/kg versus Y" or "eliminates the 180 °C distillation step" | an energy estimate, even a rough one |

Title: the editors discourage "green" and "sustainable" in titles. Move the claim into the abstract as a number.

## 2. Biomass feedstocks and processing

The editors' Biomass Expectations (2020) and the biomass metrics editorial (2021) set these expectations; the rest is the reporting reviewers in this field demand.

**Feedstock.** Species, cultivar or source, location and harvest, storage, particle size, moisture. Composition by a named method (NREL LAP TP-510-42618 for structural carbohydrates and lignin; state whether extractives were removed first), with the basis stated: dry, extractive-free. "Corn stover contained 35.6% glucan" is incomplete without "on a dry, extractive-free basis" and a replicate count.

**Yields and mass balances.** Every yield needs its basis and denominator. Delignification as % of initial lignin; glucose yield as % of theoretical from the glucan in the raw or the pretreated solid (say which; they differ by the solid recovery). Report solid recovery after pretreatment; a 78% delignification with 45% solid loss is a different result from one with 85% solid recovery. A mass balance closure (sugars + lignin + losses ≈ 100%) is the most convincing single table in a pretreatment paper. Sugar and lignin losses to the liquor and to degradation products (furfural, HMF, formic and acetic acids) should be measured or acknowledged.

**Solvent and reagent burden.** Solid loading (wt %), solvent-to-biomass ratio, reagent consumption per kg dry biomass, and recovery per cycle with a mass balance (makeup fraction). "The solvent could be recycled five times with negligible loss" needs the numbers per cycle and the fate of the accumulated solutes. The Solvents Expectations editorial does not outlaw ionic liquids or DES but expects toxicity, biodegradability, and EHS evidence rather than the label "green solvent."

**Energy.** Temperature, time, and heating method are not an energy estimate. A rough process energy (heating the solvent mass through ΔT, plus solvent recovery by evaporation, per kg dry biomass) compared with the incumbent (dilute acid at 160–190 °C, steam explosion, organosolv) is what "mild conditions" needs to mean anything. A cumulative energy demand or a simple heat balance in the SI is enough.

**Benchmark.** A table of prior pretreatments of the same or similar feedstock: solvent system, T, t, loading, delignification, sugar yield, reuse cycles, reference. The editors' Introduction guidance specifically asks for this. "Numerous studies have shown DESs remove lignin" is the vague statement they say is "not useful."

**Lignin as product.** If lignin valorization is claimed: yield on initial lignin, purity (Klason lignin, ash, residual sugars), Mw/Mn by a stated GPC method (calibration, solvent, acetylation), β-O-4 content per 100 aromatic units from HSQC with the integration method stated, and a comparison with the reference lignin (milled-wood or the incumbent process lignin). A lignin with "high β-O-4 content" is a claim about downstream depolymerization; if no depolymerization was done, say what the number implies and stop.

**Feedstock is not sustainability.** "The replacement of fossil resources to produce chemicals is not an automatic guarantee of sustainability. Instead, a quantitative measure of the net CO₂ footprint of the feedstock during cultivation, harvesting, and transportation must be accounted for." (Catalysis practices editorial, 2021.) Cite a feedstock footprint (GREET, ecoinvent, or a published LCA) when the paper's claim is climate-related.

**Statistics.** Replicates (n), mean ± SD, and a test if "significant" is used. Reviewers in this field ask for it on every yield.

## 3. Bio-based materials and polymers

The Sustainable Materials (2020), Biomaterials practices (2021), and Polymer Science (2025) editorials are blunt: a bio-based monomer does not make a sustainable polymer. What meets expectations:

- **Property parity or better** against the incumbent, in a table with the incumbent's numbers and citations (Tg, Tm, modulus, elongation, barrier, etc.). "Manuscripts that incorporate sustainable materials without improving efficiency or stability compared with the benchmark reports do not meet the technical scope."
- **Route burden.** The E-factor (mass of waste per mass of product) is "strongly encouraged for all submitted manuscripts" in this area; extend it over multistep routes; state whether water and solvent recovery are included. A bio-based route with a toxic catalyst, a chlorinated solvent, or more waste than the petroleum route "would not meet journal expectations."
- **Renewable carbon content** (mol % or wt % biogenic carbon, or ASTM D6866 if measured) rather than "fully bio-based" when a comonomer or catalyst is fossil-derived.
- **End of life** with a named standard and conditions: ISO 14855 / ASTM D5338 (industrial compost), ISO 14851/14852 (aqueous), ASTM D5988 (soil), marine tests; percent mineralization and time; disintegration vs. biodegradation distinguished. "Compostable" without a standard is a query. Recyclability: number of reprocessing cycles with property retention, or chemical recycling yield and purity.
- **Toxicity** of monomers, catalysts, additives, and solvents disclosed and justified (Polymer editorial 2025; Toxicity editorial 2026). Sb, Sn, and Ti catalysts, isocyanates, phenol, and halogenated solvents draw reviewer attention.
- **Incremental advances** named by the editors as likely out of scope: blends of established polymers with biomass, well-known renewable monomers used conventionally, minor variations of known syntheses. If the paper is in that territory, the sustainability case has to be explicit and quantified or the editor will not send it out.
- **Application-phase framing**: what the material replaces, at what scale, and the largest life-cycle burden (a petroleum-derived comonomer at 34% of emissions, for instance).

## 4. Life-cycle assessment

Papers with LCA as a primary contribution "are expected to address quantitative environmental impact assessment of a process using appropriate metrics" (Process Systems Expectations, 2026). Reviewers check the ISO 14040/14044 elements; a missing one is the "LCA-lite" desk-reject pattern. Check the draft for each and query what is absent:

1. **Goal and scope**: attributional or consequential; intended application; audience.
2. **Functional unit**, stated once and used throughout: "1 kg of polyol at the plant gate", "1 MJ of ethanol delivered", "1 m² of packaging film with equal oxygen barrier". Results "per kg of product" without a stated functional unit is the most common gap.
3. **System boundary** named (cradle-to-gate, cradle-to-grave, gate-to-gate) and drawn (a figure), with what is excluded (capital goods, infrastructure, end of life) and why.
4. **Multifunctionality**: how co-products were handled: system expansion / substitution (what was displaced, and with what data), or allocation (mass, energy, economic) — and a sensitivity on the choice, because in biorefinery LCAs the allocation choice often changes the sign of the result. An electricity export credit is a substitution and needs the grid mix and year stated.
5. **Inventory data sources and years**: foreground from process models (Aspen, mass and energy balances in SI); background database with version (ecoinvent 3.8, 3.9, 3.10; GREET 2022/2023); geography; the year of the data. "Ecoinvent" with no version is a query.
6. **Impact assessment method** with version: IPCC 2021 GWP100 (or 2013), ReCiPe 2016 (H/E/I), TRACI 2.1, EF 3.1, CML-IA. GWP only is acceptable for a screening LCA if stated as such; multi-category results are expected for a "detailed sustainability assessment."
7. **Biogenic carbon** accounting stated (neutral, or tracked as uptake and release); land-use change included or excluded and why.
8. **Uncertainty and sensitivity**: parameter ranges, Monte Carlo or at least a one-at-a-time sensitivity on the parameters that drive the result; scenario analysis on allocation, grid mix, and displaced product. The 2019 editorial names "inadequate error and uncertainty analyses" and "inadequate validation or sensitivity analyses of computational work" as desk-reject reasons.
9. **Comparator** with the same functional unit, boundary, method, and data vintage; the fossil incumbent's number and source. Comparing to a literature value computed with a different method is a query.
10. **Interpretation** with hot-spot identification (which stage or input dominates) and the conditions under which the conclusion flips.
11. **Prospective/low-TRL** processes: say so, state the scale-up assumptions, and treat lab-scale inventory (excess solvent, no heat integration) as an upper bound.

Language: "reduces GHG emissions by 18%" must carry the boundary and the functional unit in the same sentence in the abstract. Do not let "sustainable" or "green" summarize an LCA result; the number does that.

## 5. Techno-economic analysis

Reviewers of biorefinery TEAs expect the NREL-style reporting basis. Check the draft for:

- **Scale and basis**: feed rate (dry t/day), operating hours per year (e.g., 8410 h), plant location, nth-plant vs. pioneer plant assumptions.
- **Capital cost method**: equipment costs from what (Aspen Process Economic Analyzer, vendor quotes, literature) scaled how (six-tenths rule, with exponents), installation factors, indirect costs, contingency, and the cost year and index used (CEPCI). Total capital investment reported.
- **Operating costs**: feedstock price and basis (delivered, dry), enzyme and chemical prices with sources, utilities, labor, maintenance; co-product prices and their sources and years.
- **Financial assumptions**: cost year for all dollars; discount rate / IRR (10% is the NREL convention); plant life (20 or 30 years); depreciation; tax rate; financing (equity fraction); construction period; working capital. State them in one table.
- **Output metric**: minimum selling price (MSP/MESP), net present value, payback, or levelized cost, defined; unit consistent with the market comparator ($/gal, $/kg, $/GGE).
- **Sensitivity**: tornado plot on capital, feedstock, yield, co-product price, discount rate; scenario analysis; where the result crosses the market price. Uncertainty stated (±30% class-4 estimate is typical and should be said).
- **Comparator**: base case with the same assumptions (the paper's own base case is fine for TEA, unlike for durability claims), and the published benchmark (Humbird 2011 / Davis 2018 NREL designs) with a reconciliation if the base-case MSP differs.
- **Consistency**: the same yields, energy balance, and co-product flows in the TEA and the LCA; the same cost year in text, tables, and figures; MSP quoted identically in abstract, results, and conclusions.
- **Integration**: energy balance closure when a fuel or lignin is diverted from the boiler; makeup natural gas or biomass quantified.

## 6. Catalysis, synthesis, solvents, electrochemistry (brief)

For papers outside the user's main fields, the editors' expectations in one paragraph each. Query what is missing.

**Catalysis and synthesis** (Catalysis practices 2021; Organic Synthesis 2025): TON and TOF, not only conversion and yield; recyclability tested at < 50% of equilibrium conversion with initial rates, procedure per cycle, and leaching by ICP; maximum TON; solvent and auxiliary reduction discussed with CHEM21 metrics (atom economy, PMI, reaction mass efficiency, optimum efficiency, solvent EHS ranking); catalyst preparation burden counted; a "greener" preparation must show equal performance; photochemistry reports quantum yield; a greener catalyst is compared with the incumbent's metrics, not only with the authors' own control. Biocatalysis: specific activity, volumetric productivity, cofactor regeneration, complete E-factor including water or solvent intensity; dilute unisolated products reported only chromatographically are "premature."

**Solvents** (2020): ionic liquids and DES are not disqualified, but "green solvent" requires toxicity, biodegradability, and EHS evidence or a solvent-selection-guide ranking, plus recovery data.

**Electrochemistry** (2025): Faradaic efficiency toward the desired product is a fit criterion; current-density targets approach 500 mA cm⁻² (alkaline electrolyzers), 1 A cm⁻² (PEM/AEM), several hundred mA cm⁻² (CO₂ conversion); durability compared with benchmark reports rather than self-comparison; renewable electricity does not excuse energy or materials inefficiency; LCA/TEA encouraged.

**Nanomaterials** (2020/2021): not characterization alone; a scientific advance plus an attempt to evaluate the sustainability impact; routine characterization of known materials to SI.

## 7. Toxicity

From the 2026 editorial, which applies to every field: disclose toxic compounds used as solvents, reactants, reagents, catalysts, additives, or products; justify why they remain unavoidable; combine (eco)toxicity evaluation with metrics (E-factor, PMI, cumulative energy demand); benchmark against state of the art; state the advance in abstract, introduction, and conclusions. A process with increased toxicity relative to comparators is out of scope even if other metrics improve; managing toxicity by containment rather than benign design is out of scope. When editing, add a sentence in the Experimental section that names hazards (ACS requires a hazard statement anyway) and, if the paper's reagents are the toxic part of the route (isocyanates, propylene oxide, chlorinated solvents, heavy-metal catalysts), make sure the Discussion says so and says what it would take to replace them.

## 8. Metric definitions (for consistency checks)

- **Atom economy (AE)** = MW of product / Σ MW of reactants × 100 (stoichiometric, theoretical).
- **E-factor** = kg waste / kg product; state whether water and recovered solvent are excluded (simple E-factor) or included (complete E-factor, cEF).
- **Process mass intensity (PMI)** = total mass in (including water and solvents) / mass of product; PMI = E-factor + 1 when the same boundary is used.
- **Reaction mass efficiency (RME)** = mass product / mass of reactants × 100.
- **Carbon efficiency** = carbon in product / carbon in reactants × 100.
- **Solvent intensity** = kg solvent / kg product.
- **Cumulative energy demand (CED)** = MJ primary energy per functional unit.
- **TON** = mol product / mol catalyst (active sites); **TOF** = TON per unit time, at stated conversion (initial rate preferred).
- **Faradaic efficiency** = charge to product / total charge × 100.
- **Delignification** = (lignin in raw − lignin in pretreated solid × solid recovery) / lignin in raw × 100.
- **Glucose yield** = glucose released / theoretical glucose from glucan (× 1.111 hydration factor) in the stated basis × 100.
- **MSP/MESP** = selling price giving NPV = 0 at the stated IRR over the plant life, in the stated cost year.
- **GWP100** per functional unit, kg CO₂e, with the IPCC assessment report version.

When a paper defines a non-standard metric, the guidelines require the calculation method in the paper or SI; check that it is there.
