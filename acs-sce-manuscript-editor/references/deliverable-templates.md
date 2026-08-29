# Deliverable templates

Formats for what the skill hands back. Adjust length to the input: a full manuscript gets all four parts; a pasted abstract gets the edited text, three lines of change log, and the author queries.

## 1. Edited manuscript

Return the full text in manuscript order. For a .docx input where file writing is available, write an edited .docx and also show the changed abstract and Synopsis in the reply so the user sees the direction without opening the file. For pasted text, return plain text that pastes cleanly into Word:

```
TITLE
<title>

AUTHORS AND AFFILIATIONS
<unchanged, or [AUTHOR: mark corresponding author with * and give email]>

ABSTRACT
<150–200 words, no citations, key numbers, one sentence stating the benchmarked sustainability advance>

KEYWORDS
<5–8 keywords, some not in the title, or [AUTHOR: confirm keywords]>

INTRODUCTION
...

EXPERIMENTAL SECTION  (or MATERIALS AND METHODS — keep the author's heading; sections are not numbered)
...
<Safety: [AUTHOR: state any unexpected or significant hazards; ACS requires a hazard statement here]>

RESULTS AND DISCUSSION
...

CONCLUSIONS
...

ASSOCIATED CONTENT
Supporting Information: <non-sentence list of contents with file type, e.g. "Composition data, HSQC integration method, DES recovery mass balance, and Figures S1–S4 (PDF)", or [AUTHOR: list SI contents]>
Data Availability Statement: The data underlying this study are available in the published article and its Supporting Information. [AUTHOR: confirm, or give repository and DOI]

AUTHOR INFORMATION
Corresponding Author: *[AUTHOR: name, affiliation, email] (ORCID iDs are linked in the ACS profile, not typed here)
Author Contributions: [AUTHOR: optional; "‡ These authors contributed equally" or a CRediT sentence]
Notes: The authors declare no competing financial interest.  [AUTHOR: confirm]

ACKNOWLEDGMENTS
[AUTHOR: all funding sources for all authors; AI-tool disclosure if any tool was used for text: "Portions of the draft were edited with the assistance of <tool, version>; the authors reviewed and verified all content."]

REFERENCES
<ACS format, numbered in order of first citation, one reference per number, titles and DOIs>

FOR TABLE OF CONTENTS USE ONLY
<TOC graphic 3.33 × 1.875 in., original artwork, not AI-generated — [AUTHOR: supply]>
Synopsis (optional under the Aug 2026 guidelines; was required until 2025): <one sentence, ~20 words, plain language, how the work relates to sustainability>
```

Inline queries use exactly the form `[AUTHOR: ...]` so the author can search for them. Keep them short and specific: `[AUTHOR: dry-basis or as-received?]`, `[AUTHOR: n = ? replicates; report ± SD]`, `[AUTHOR: ref 4 could not be matched to a real article — verify]`.

## 2. Change log

Group by editing pass. One line per substantive change; roll up mechanical ones as counts. Quote original wording when the meaning or emphasis shifted, so the author can veto it.

```
CHANGE LOG

Structure and required elements
- Title: "Novel and Green DES Pretreatment ... : A Sustainable Approach" → "Choline Chloride–Lactic Acid Deep Eutectic Solvent Pretreatment of Corn Stover with Five-Cycle Solvent Reuse". Removed evaluative adjectives; named the system and the reuse result.
- Abstract: removed citations [1–3] (ACS abstracts are self-contained); added the recovered-lignin Mw and DES reuse numbers from Section 3.3–3.4.
- Added a one-sentence synopsis with the TOC placeholder (optional under current guidelines; drafted from your numbers, please confirm) and KEYWORDS (placeholder, 5–8).
- Added ASSOCIATED CONTENT (SI description, Data Availability) / AUTHOR INFORMATION / ACKNOWLEDGMENTS blocks with placeholders; removed section numbers (journal style).
- Experimental: added a hazard-statement placeholder (required by ACS).

Sustainability argument
- "green and sustainable strategy" (Conclusions) → replaced with the quantified statement: solvent reused five times with delignification falling from 78.4 to 72.1%. The unquantified claim would draw an editor query.
- Added [AUTHOR] query for DES recovery mass balance (% recovered per cycle) — the reuse claim rests on it.
- Added [AUTHOR] query for a comparison table against prior ChCl–lactic acid pretreatments of corn stover (refs 4, 5 report similar systems).

Prose
- Removed "novel" (5), "for the first time", "to the best of our knowledge", "paves the way" (2), "holds great promise", "delve", "realm", "crucial" (2), "pivotal", "garnered tremendous attention", "valuable insights", "not only ... but also".
- Introduction paragraph 2: "Nevertheless, these methods suffer from various drawbacks such as harsh conditions, high cost, environmental pollution ..." → specific drawbacks per method with the citations the draft already had.
- Section 3.1: "This can be attributed to the optimal balance between the hydrogen bonding ability and viscosity of the DES" → marked as a hypothesis and pointed at the viscosity data if it exists [AUTHOR query].
- Cut 6 sentences that restated the previous sentence or announced the next.

Style (ACS)
- Units: added space before units in 9 places; °C spacing (5); "ml" → "mL" (3); "hrs" → "h"; "minutes" → "min"; "over night" → "overnight"; "40-60 mesh" → "40–60 mesh"; "cm-1" → "cm⁻¹"; "wt%" → "wt %"; "DMSO-d6" → "DMSO-d₆".
- Tense: methods to past tense throughout; "Figure 1 shows" (present) for figure callouts.
- "data was" → "data are" (2). "utilized" → "used" (2). "in order to" → "to" (3).
- References: converted 5 entries to ACS format; all authors listed; DOIs added where I could verify them from the draft's own details — [AUTHOR: verify DOIs].

Consistency
- Glucose yield stated as 84.7% in abstract and 3.1 but "85%" in conclusions → 84.7% throughout.
- Figure 2c,d cited before Figure 2b → reordered callouts.
- Assumed superscripts/subscripts were lost when the text was pasted from Word; restored where inferable.
```

## 3. Author queries

Numbered, most consequential first. Each should be answerable in a sentence or by adding a number, and should say why it matters for this journal.

```
AUTHOR QUERIES (in priority order)

1. Sustainability metric. The paper claims a "green" process but reports no solvent-recovery mass balance, E-factor, or comparison of energy/solvent use with the organosolv or ionic-liquid baselines you cite. ACS SCE editors screen for this. Minimum: % DES recovered per cycle and lignin/sugar losses to the DES; better: PMI or a simple energy estimate for the 140 °C, 3 h step vs. the baseline.
2. Benchmark. Refs 4 and 5 report ChCl–carboxylic-acid DES pretreatment of similar residues. A short table (feedstock, DES, T, t, delignification, glucose yield, reuse cycles) would let reviewers see what is new here. Without it, "first report" claims will be challenged.
3. Replicates and error. No error bars or n are reported for delignification and glucose yield. State n and report ± SD; "significant" is used seven times with no statistical test.
4. Mechanistic attribution in 3.1 ("optimal balance between hydrogen bonding ability and viscosity"). Do you have viscosity or Kamlet–Taft data for the three ratios? If not, present as a hypothesis.
5. Composition basis. Are glucan/xylan/lignin contents on a dry, extractive-free basis (NREL/TP-510-42618)? State it in Methods and Table 1.
6. References. Ref 1 was in Nature style and ref 3 in APA; converted to ACS. Please verify DOIs and page ranges. Ref 5 lacks a full page range.
7. Missing elements: Keywords (5–8), TOC graphic (3.33 × 1.875 in., original, not AI-generated), SI description with file type, Data Availability Statement, corresponding author with email, competing-interest statement, funding, hazard statement. Synopsis drafted (optional) — confirm.
```

## 4. Submission checklist status

```
SUBMISSION CHECKLIST — ACS Sustainable Chem. Eng. Research Article
[ ] Within 7000 word-equivalents (text + 300–600 per figure/table)
[x] Title specific, no evaluative adjectives, no "green/sustainable"
[x] Abstract self-contained, 150–200 words, no citations, key numbers
[ ] Keywords (5–8)
[x] Sections unnumbered: Introduction / Experimental / Results and Discussion / Conclusions
[ ] Hazard/safety statement in Experimental
[ ] Sustainability advantage quantified and benchmarked; stated in abstract, introduction, conclusions (see query 1)
[ ] Comparison table with prior work
[ ] Error bars / n reported
[ ] Associated Content: SI description with file types; Data Availability Statement
[ ] Corresponding author marked with * and email (≤ 3); ORCIDs linked in ACS profiles
[ ] Competing-interest statement
[ ] Funding in Acknowledgments (and Funder Registry at submission)
[ ] Generative-AI use disclosed in Acknowledgments if applicable
[x] References in ACS format, numbered in citation order, one per number, titles, DOIs
[ ] All figures cited in order; captions self-contained
[ ] TOC graphic 3.33 × 1.875 in., original, labeled, last page, not AI-generated
[~] One-sentence synopsis (optional under 2026 guidelines) — drafted, needs confirmation
[ ] Cover letter with rationale, Green Chemistry/Engineering principles, keywords, author contacts
```

Mark `[x]` present, `[~]` added as placeholder or drafted, `[ ]` missing.

## 5. Synopsis examples

The synopsis is a one-sentence, non-technical statement of how the work relates to sustainability, written for a non-specialist editor. It was mandatory (~20 words, complete sentence, not a description of the TOC graphic) through the June 2025 guidelines and is absent from the Aug 2026 guidelines; it remains the sentence the editor is looking for, so draft it and use it in the abstract and cover letter even if it is not submitted separately. Plain words, one number if possible, no abbreviations, no "novel". About 20–30 words.

- "Replacing the lignin boiler with a lignin-to-polyol product cuts the ethanol selling price by 22% and cradle-to-gate greenhouse-gas emissions by 18% in a corn stover biorefinery."
- "A recyclable choline chloride–lactic acid solvent removes 78% of the lignin from corn stover and is reused five times, reducing solvent consumption in biomass fractionation."
- "Fully bio-based furanic copolyesters reach the toughness of petroleum-based packaging films while keeping the oxygen barrier that makes PEF attractive."

Weak: "This work provides new insights into sustainable biorefineries." (No fact, no number, could describe any paper.)

## 6. Cover letter skeleton

Half a page. Editors read the first paragraph.

```
Dear Dr. [Editor],

We submit "[Title]" for consideration as a Research Article in ACS Sustainable Chemistry & Engineering.

[One paragraph: what was done and the quantitative result. One sentence on the sustainability advance in the same terms as the Synopsis: the metric, the benchmark it beats, and by how much.]

[One paragraph: why this journal. Name the scope area (e.g., Biomass or Wastes as Resources; Life-Cycle Assessment; Green Manufacturing) and which Principles of Green Chemistry / Green Engineering the work demonstrates (the guidelines ask for this explicitly), with one sentence of evidence for each. If genuinely relevant, one or two recent ACS SCE papers this work builds on.]

Keywords: [the same 5–8 as in the manuscript]
Authors and affiliations: [list]
Contact information for all authors: [AUTHOR: mailing address, email, phone where available — the guidelines require this]

[Required statements: original, not under consideration elsewhere; all authors approved; competing interests; preprint server and link if posted, with what changed; word-limit justification if over 7000; previous manuscript ID and changes if resubmitting; safety considerations if any; for a Letter, whether the first author is a doctoral student or postdoc.]

Suggested reviewers (optional): [AUTHOR: 3–5 names with institutional emails, no same-institution or recent coauthors]

Sincerely,
[Corresponding author, affiliation, ORCID]
```
