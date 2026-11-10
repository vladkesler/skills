# Claims and evidence in bio-based and polymer materials papers

Editors and reviewers at Matter, Advanced Functional Materials and Carbohydrate Polymers test every performance claim the same way: what is the number, compared with what, measured how, on how many samples? This file is the editing guide for that test in the fields this skill is used for most: biomass-derived materials, polymers, composites, hydrogels and other soft materials. Section 1 is the rule and applies to every paper. Sections 2–7 list what reviewers in these fields expect to see reported; use them to find gaps and turn each gap into a query for the author.

You are an editor here, and the author is the scientist. When something is missing, ask for it. Do not supply a value, a standard or a method the draft does not contain.

Contents: 1 The rule · 2 The benchmark comparison · 3 Describing the material · 4 Mechanical, thermal and structural data · 5 Functional properties · 6 "Green", "bio-based", "biodegradable" and similar words · 7 Replicates and statistics · 8 Quick definitions

---

## 1. The rule

Every evaluative word in the draft ("strong", "tough", "highly conductive", "excellent stability", "superior", "scalable", "low-cost", "sustainable") stands in for three things. Find them or ask for them:

1. **The number**, with units and conditions (temperature, humidity, strain rate, thickness, cycle count).
2. **The comparator**: the incumbent material, the best published result for the same class, or the authors' own control, with its number and a citation. A control made in the same lab is necessary; on its own it does not show an advance over the field.
3. **The basis**: sample size, what the error value is (SD or SEM), and the method or standard.

When the draft has all three, the edit is to put them in the sentence and delete the adjective. When it does not, rewrite the sentence as the plain fact it can support, and query the rest.

| Draft says | Edit to | Query if missing |
|---|---|---|
| "exhibits excellent mechanical properties" | "reaches a tensile strength of 52 ± 3 MPa and a strain at break of 18 ± 2% (n = 5), compared with 31 ± 2 MPa and 6 ± 1% for the unfilled film" | n, error, test standard, conditioning |
| "enhanced toughness" (only strain at break was measured) | "strain at break rises from 6 to 18%", and "ductile" or "extensible" in place of "tough" | a toughness value with its method, if "tough" is to stay |
| "superior to previously reported materials" | "exceeds the toughness of published cellulose–PVA hydrogels (0.4–2.1 MJ m⁻³; Table 2)" | the comparison table with references |
| "highly sensitive strain sensor" | "gauge factor of 4.2 over 0–150% strain, stable over 1,000 cycles" | range, linearity, cycles, drift |
| "good biocompatibility" | "cell viability above 90% after 72 h (L929 fibroblasts, ISO 10993-5 extract test)" | cell line, assay, standard, controls |
| "outstanding stability" | "retains 91% of its initial conductivity after 30 days at 25 °C and 50% relative humidity" | duration, conditions, what was measured |
| "scalable and low-cost" | "films of 30 × 40 cm were cast (Figure S3)" and delete "low-cost" | scale shown; cost basis if the claim stays |
| "fully bio-based" | "contains 87 wt % bio-based carbon (calculated from the monomer feed)" | which components are fossil-derived |
| "biodegradable" | "lost 68% of its mass after 60 days in soil burial (method in the Experimental Section)" | the test, the conditions, the number; mineralization vs mass loss |
| "for the first time" | delete; state what the nearest prior work did and what differs | the nearest prior reference |

The values in this table are invented to show the form of the edit. Use the author's numbers, never these.

These rules apply to statements about the authors' own material. A general statement in the background ("bio-based polymers are being developed to replace fossil-derived plastics") needs a reference, not a metric.

All three journals want novelty shown, not claimed. Cell Press discourages the words in its guidelines; at AFM the claim is tested against "the latest international research"; Carbohydrate Polymers asks authors to set their hypothesis against the most relevant earlier literature. Novelty is shown by the comparison.

## 2. The benchmark comparison

The single most persuasive element in a materials paper for any of these journals is a direct comparison with recent literature, and it is the one authors most often leave in the Supporting Information or omit.

- A **comparison table** in the main text: material, key property values, test conditions, reference. Same units throughout; conditions stated, because a strength measured dry and one measured at 50% relative humidity are different numbers.
- Or a **property chart** (strength against strain at break, conductivity against stretchability, permeability against modulus) placing this work among published points, with the references in the caption or the supplement.
- The comparators must include the best recent results, including those from other groups, and the commercial incumbent where one exists (PET, LDPE, PDMS, a commercial ionogel, a Nafion membrane).
- For AFM, references from the last two to three years are expected; an editor who knows a stronger published result that the paper ignores will decline it.
- If the paper's material is better on one axis and worse on another, say so. A stated trade-off reads as command of the field.
- For Carbohydrate Polymers the comparison that matters most is usually with the same polysaccharide: earlier reports at other molecular weights, degrees of substitution or sources. A table that compares a chitosan film only with polyethylene misses the journal's question.

If the draft has no benchmark, add an `[AUTHOR: ...]` placeholder for the table where it belongs and make it the first item in the to-do list. Do not assemble literature values yourself.

## 3. Describing the material

AFM states that manuscripts "reporting results using undisclosed material compositions may not be considered for publication and may be returned without external review", including commercial and proprietary products. Matter requires enough detail to reproduce the work and structural proof for new compounds. Carbohydrate Polymers goes furthest: its guide says editors are unlikely to send a paper for review when the polysaccharide is not adequately characterized, purchased polysaccharides included, and a separate guideline lists what to report for each polymer. That list is in `carbpol-requirements.md` §5; when the target is Carbohydrate Polymers, work through it for every polysaccharide in the draft and put each missing item in the first group of the to-do list. For all three journals, check for:

- **Every component named and quantified**: supplier and grade, molar mass or viscosity grade for polymers, degree of hydrolysis or substitution where relevant, concentration in wt % or mol %, solvent, pH, and the final composition of the material (not only the feed).
- **Biomass-derived inputs**: species and plant part or organism, source and supplier, the extraction or fractionation method, purity and composition (for lignin: type such as kraft, organosolv or enzymatic, molar mass, hydroxyl content, ash; for cellulose and nanocellulose: source, dimensions with the measuring method, crystallinity with the method, surface charge or degree of substitution; for chitosan: degree of deacetylation and molar mass; for proteins such as silk fibroin or gelatin: source and processing; for starch: amylose content). Biomass varies; reviewers ask whether more than one batch was used.
- **New polymers and compounds**: structure proof (¹H and ¹³C NMR, FTIR), molar mass and dispersity by SEC with the eluent, calibration standards and detector stated, composition of copolymers from NMR compared with the feed, end groups where they matter. Spectra in the supplement.
- **Processing history**, since it sets the properties: casting or printing conditions, drying temperature and time, annealing, crosslinking dose or time, film thickness with its variation, conditioning before testing.
- **Hazards** in the procedure named (AFM: "hazardous chemicals, equipment and techniques must be emphasized").

## 4. Mechanical, thermal and structural data

**Tensile and compression tests.** Standard followed or specimen geometry given (dog-bone type and gauge dimensions, or film strip width and gauge length); crosshead speed or strain rate; temperature and relative humidity during conditioning and testing, which is decisive for hygroscopic bio-based materials and hydrogels; number of specimens (five is the usual minimum); mean ± SD for strength, modulus and strain at break; how the modulus was taken (strain range of the fit); representative stress–strain curves. For hydrogels: water content and whether samples were tested as prepared or swollen to equilibrium.

**Toughness and fracture.** "Toughness" must be defined: work of fracture from the area under the stress–strain curve (MJ m⁻³) is different from fracture energy (J m⁻²) from a notched test (pure shear, single-edge notch, tearing). Name the method. Fatigue or cyclic claims need the number of cycles, the strain amplitude, and the residual strain or hysteresis.

**Self-healing and recovery.** Healing efficiency defined (ratio of which property), healing time, temperature, humidity, whether any stimulus or pressure was applied, and how the cut was made.

**Rheology and dynamic mechanical analysis.** Geometry, strain within the linear range (state how this was checked), frequency, temperature ramp rate; for DMA, how Tg is defined (peak of tan δ or of E″).

**Thermal analysis.** DSC: heating and cooling rates, which scan the values come from, how Tg is taken (midpoint); TGA: atmosphere, heating rate, the temperature at 5% mass loss. Thermal conductivity: the method (laser flash, hot disk, steady state), direction for anisotropic materials, density and specific heat used.

**Structure.** XRD crystallinity with the method named (for cellulose, the Segal index and deconvolution give different values); spectroscopic assignments with references; microscopy with scale bars, representative fields, and low-magnification images accompanying high-magnification ones; particle or fiber dimensions as distributions with the number measured. Carbohydrate Polymers does not accept microscopy, routine FT-IR or UV spectra as proof of a polysaccharide's fine structure (residues, ring size, anomeric configuration), nor DLS size or zeta potential alone as a description of nanocellulose; FT-IR is accepted as qualitative evidence that a modification took place.

**Mechanism claims.** A statement that a property arises from hydrogen bonding, dynamic bonds, alignment or phase separation needs evidence in the paper: a control that removes the interaction, a spectroscopic shift, scattering data, or a simulation. Without it, the sentence is a hypothesis and must be worded as one, in the author's own hedged terms. For Matter this is often the heart of the paper: a tested mechanism is a concept; an asserted one is decoration.

## 5. Functional properties

For AFM the function is the paper. For Carbohydrate Polymers a function counts together with what the polysaccharide's structure contributes to it. For each function the draft claims, check that the standard figures of merit are reported with their conditions. Query what is absent; do not add methods.

| Function | What reviewers expect |
|---|---|
| Gas or water-vapor barrier | Transmission rate with film thickness, temperature and relative humidity, and the permeability normalized by thickness; units stated; comparison with PET, EVOH or LDPE; humidity dependence for hydrophilic bio-based films |
| Electronic or ionic conductivity | Method (four-probe, impedance), sample geometry, temperature and humidity; for ionic conductors the water or solvent content; stability over time |
| Strain, pressure or humidity sensing | Sensitivity (gauge factor or equivalent) over a stated range, linearity, detection limit, response and recovery times, hysteresis, cycling stability; for tests on a person, the ethics and consent statements all three journals require |
| Actuation and shape change | Stimulus magnitude, response speed, stroke or curvature, force or work density, cycle life |
| Adhesion | Test type (lap shear, peel, tack) and standard, substrates, cure or contact conditions, failure mode (adhesive or cohesive), wet and dry values if water resistance is claimed |
| Energy storage (supercapacitors, batteries, binders, separators) | Mass loading, values normalized by mass, area and volume as appropriate, rate, cycle life with capacity retention, full-cell data if a device is claimed; the journal's battery or supercapacitor checklist |
| Triboelectric and piezoelectric generators | Output voltage and current with contact area, force and frequency; power density across a load-resistance sweep; durability |
| Antibacterial or antifouling action | Organisms and strains, method (colony counts, zone of inhibition, a named standard), contact time, controls, replicates; leaching versus contact killing |
| Biocompatibility or biomedical use | Cytotoxicity assay and cell line, standard followed, controls; for animal work the approvals; avoid "biocompatible" as a blanket term |
| Flame retardancy | Limiting oxygen index, UL-94 rating with thickness, cone calorimetry values (peak heat release rate, total heat release) |
| Optical properties | Transmittance at a stated wavelength and thickness, haze, refractive index; for structural color or emission, spectra and angles; quantum yield with the method |
| Thermal insulation or management | Thermal conductivity with method and density; for radiative cooling, emissivity and solar reflectance spectra and field-test conditions |
| Adsorption, separation, membranes | Capacity with isotherm and kinetics, selectivity, flux and rejection with pressure, regeneration cycles, tests in realistic mixtures |
| Water or solvent resistance | Swelling ratio, mass loss, wet strength; time and medium; this is the usual weak point of bio-based materials and reviewers look for it |
| Durability | Aging time and conditions (temperature, humidity, UV), property retention; storage stability of hydrogels against drying or freezing if claimed |

A demonstration (lighting an LED, a glove that senses finger bending, a film wrapped around fruit) helps a reader see the function. It does not replace the figures of merit. If the draft has a demonstration and no numbers, query the numbers.

## 6. "Green", "bio-based", "biodegradable" and similar words

None of the three is a sustainability journal, and an environmental benefit will not carry the paper. These words still appear in most bio-based materials papers, and reviewers test them. For each one: attach the fact, or delete the word and query the author.

- **Bio-based / renewable.** As a description of where a material comes from, "bio-based" or "lignin-derived" may stay in a title or keyword list when the paper states which components are bio-sourced. As a claim of benefit it needs the share. Say which components and what share: wt % of bio-based components in the final material, or biogenic carbon content (ASTM D6866 if measured). "Fully bio-based" fails if the crosslinker, plasticizer or catalyst is fossil-derived. A bio-derivable monomer bought as a petrochemical is "obtainable from renewable sources", not "bio-based".
- **Biodegradable / compostable.** Needs the test, the conditions and the number: the standard or method (for example ISO 14855 or ASTM D5338 for industrial composting, ISO 17556 or ASTM D5988 for soil, ISO 14851 or 14852 for aqueous media), temperature, duration, and percent mineralization or mass loss. Mass loss and disintegration are not biodegradation; if the draft measured mass loss in soil burial, the sentence should say exactly that. Enzymatic degradation in a vial is a different claim again.
- **Recyclable / reprocessable.** Number of cycles and property retention after each; for chemical recycling, monomer yield and purity; for dissolution–recasting, what happens to the properties.
- **Green / sustainable / eco-friendly / environmentally benign.** No absolute meaning. Replace with the specific fact (water as the only solvent, room-temperature processing, no added crosslinker, reuse of the solvent with a stated recovery) or delete. Keep these words out of the title for all three journals. If the paper makes a quantified environmental claim (a carbon footprint, an energy comparison), it needs the functional unit, the system boundary and the data source stated.
- **Non-toxic / safe.** Needs a data point or a citation for the specific substance and exposure.
- **Low-cost / scalable.** "Low-cost" needs a cost basis; usually delete it. "Scalable" is supported by showing scale: the size or quantity made and the process used.
- **Waste-derived / upcycled.** Name the waste stream, its composition and variability, and any pretreatment.

For Matter, the societal relevance of a bio-based material belongs in the Progress and potential statement, where outlook is invited; it still has to rest on the paper's results.

## 7. Replicates and statistics

All three journals ask for this.

- Cell Press: "articles must include replicate results with means and standard deviations"; figure legends state the number of replicates, define the error bars ("Data are represented as mean ± SD") and name any test; plotting individual data points is recommended.
- AFM: a "Statistical Analysis" subsection at the end of the Experimental Section covering pre-processing, data presentation, sample size for each analysis, the tests used and the software; legends repeat *n*, the test and the P value.
- Carbohydrate Polymers: the abstract is to give the main findings with their statistical significance where that applies. The guide has no separate statistics section, so the tests, *n* and the software go in Materials and methods and the figure captions. Mechanical properties need the sample dimensions and the temperature and humidity of the test.

When editing:

- Every key number carries its *n* and what the ± means. If the draft gives a bare value, query it.
- "Significant" and "significantly" are statistical words. If a test was done, name it and give the P value; if not, replace with the plain comparison ("increased from 12 to 31 MPa").
- Distinguish independent samples from repeated measurements on one sample.
- Check that precision matches the method (a tensile strength quoted as 52.37 MPa with an SD of 3 is over-reported; write 52 ± 3 MPa).
- If the draft has no statistics subsection and the target is AFM, add the heading with `[AUTHOR: ...]` prompts for each required item.

## 8. Quick definitions

For consistency checks; use the author's definition if the paper states one.

- **Tensile strength**: maximum engineering stress. **Young's modulus**: slope of the initial linear region; state the strain range.
- **Strain at break** (elongation at break): engineering strain at fracture, in %.
- **Toughness (work of fracture)**: area under the stress–strain curve, MJ m⁻³. **Fracture energy**: energy per unit crack area, J m⁻² or kJ m⁻².
- **Swelling ratio**: (swollen mass − dry mass) / dry mass; state mass or volume basis. **Water content**: water mass / total mass.
- **Gel fraction**: insoluble dry mass / initial dry mass after extraction.
- **Gauge factor**: (ΔR/R₀) / strain.
- **Permeability**: transmission rate × thickness / pressure difference; state units (for oxygen, commonly cm³ µm m⁻² day⁻¹ atm⁻¹, or barrer).
- **Healing efficiency**: healed property / original property × 100, with the property named.
- **Crystallinity index**: state the method (XRD peak-height, deconvolution, DSC enthalpy with the reference enthalpy used).
- **Dispersity (Đ)**: Mw/Mn. Carbohydrate Polymers does not accept "polydispersity index" or "PDI" for this.
- **Degree of substitution (DS)**: average number of substituted hydroxyl groups per sugar unit (0 to 3 for cellulose and starch). **Molar substitution (MS)**: moles of substituent per sugar unit; it can exceed 3 when substituents chain, as in hydroxypropyl ethers.
- **Degree of deacetylation (DD)**, chitosan: share of glucosamine units among all units, in %; state the method (NMR, titration, FT-IR with its calibration).
- **M/G ratio**, alginate: mannuronate to guluronate residues; F_G is the guluronate fraction.
- **Bio-based content**: mass of bio-based components / total mass, or biogenic carbon / total organic carbon; say which.
