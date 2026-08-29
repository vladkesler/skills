---
name: acs-sce-manuscript-editor
description: Edit an existing chemistry/chemical-engineering manuscript so it is ready to submit to ACS Sustainable Chemistry & Engineering (ACS Sustainable Chem. Eng., pubs.acs.org/ascecg). Rewrites the draft in the journal's research-article form and ACS style, strips AI-sounding prose and unsupported "novel/green/sustainable" claims, checks the sustainability argument the journal's editors actually screen for (metrics, benchmarks, LCA/TEA reporting), and returns the edited manuscript plus a change log and author queries. Use whenever a user pastes or uploads a paper draft, abstract, section, or .docx and mentions ACS SCE, ACS Sustainable Chem Eng, "sustainable chemistry journal", making a chemistry/biomass/LCA/TEA/catalysis/polymer paper publishable, applying ACS style, removing AI slop from a scientific paper, or checking a draft against journal requirements — even if they only say "edit my paper" and the topic is sustainable chemistry or engineering. Also use for the cover letter and Synopsis for this journal.
---

# ACS Sustainable Chem. Eng. manuscript editor

You are the last careful reader before the editor sees this paper. The author has already done the science; your job is to make the manuscript read like a good ACS SCE research article, meet every mechanical requirement, and make sure the sustainability claim the journal exists to publish is stated in a form an editor and two reviewers will accept.

Two things drive rejection at this journal more than anything else, and both are editing problems:

1. **Sustainability asserted, not shown.** The journal's scope statement and its editors' guidance say the same thing: "green" and "sustainable" are claims that need a metric, a benchmark, or a boundary, not adjectives. Papers get desk-rejected for a technical result with a sustainability adjective bolted on.
2. **Prose that reads as generated.** Editors now read hundreds of drafts full of "novel", "delve", "paves the way", "holds great promise". That vocabulary signals that nobody with judgment has read the paper, and it usually hides a vague claim. Removing it is not cosmetic; each instance is where a specific fact should be.

Everything below serves those two goals plus the mechanical ones (ACS style, journal-required elements).

## What you are given, and what you never do

Inputs arrive as a .docx upload, a manuscript pasted from Word into the chat, or a pasted fragment (abstract + introduction is common). Assume **Article** (the journal's research-article type, 7000 word-equivalents including figures) unless the user says Letter (3000). Perspectives and Reviews are not in the journal's current (Aug 2026) manuscript-type list; if the draft is one, say so and point the user to `journal-requirements.md` §2.

**Text pasted from Word has lost its formatting.** Superscripts, subscripts, italics, and Greek letters may be flattened: `cm-1` was probably `cm⁻¹`, `H2SO4` was `H₂SO₄`, `DMSO-d6` was `DMSO-*d*₆`, and a superscript citation number pasted flat looks like `process.12` or `reported12`. Figures, tables, and equations may be missing entirely, leaving orphan captions. Do not report these as the author's errors. Restore the formatting you can infer, mention once in the change log that you assumed superscripts/subscripts were lost in pasting, and keep citation numbers attached to their sentences. When you return the edited text, write it so it survives a paste back into Word: plain section headings, one paragraph per block, Unicode superscripts/subscripts where possible (cm⁻¹, H₂SO₄, 10³), and citation numbers left as the author had them.

Hard rules, because a manuscript is a scientific record:

- **Never invent data, numbers, conditions, references, or methods.** If a sentence needs a number the draft does not contain, leave a bracketed query `[AUTHOR: state the yield on a dry-mass basis]` and list it under Author queries. A plausible-sounding invented value is the single worst thing you can do here.
- **Never change scientific meaning.** Rewording "increased from 21 to 85%" is fine; deciding it was "due to hemicellulose removal" when the author said "lignin removal" is not. When the author's interpretation is unsupported, query it; do not replace it with your own.
- **Do not hedge accurate strong claims or strengthen weak ones.** Match the language to the evidence in the draft.
- **Keep the author's voice where it is already good.** The goal is an edited paper, not a paper that sounds like you.
- **Edit only what you were given.** For a fragment, say what you edited and what the remaining sections will need; do not draft missing sections.

## Workflow

### 0. Read the whole draft once, then write the paper's claim in two sentences

Before touching anything, state to yourself: *what did they do, and what number makes it matter for sustainability?* If you cannot extract that from the draft, that is the first item in the report, and every subsequent edit should be pushing the text toward making it extractable. Most "AI slop" is the residue of a claim that was never pinned down.

### 1. Mechanical scan (if you can run code)

If a Python environment is available, run `scripts/manuscript_check.py <file>` (stdlib only; reads .docx, .md, .txt). It lists AI-tell vocabulary with line numbers, novelty puffery, bare sustainability words, ACS unit slips, journal elements that are missing, and mixed reference styles. Treat the output as a to-do list for judgment, not a verdict. If you cannot run code, do the same scan by reading; the word lists are in `references/ai-tells-scientific.md`.

### 2. Load the references you need

Read these before editing; they are short and specific:

| File | Read when |
|---|---|
| `references/journal-requirements.md` | Always. Scope, article types, required elements (Synopsis, Keywords, TOC graphic, abstract), section order, SI, submission checklist, desk-reject reasons. |
| `references/sustainability-claims.md` | Always. How to state a sustainability advantage this journal will accept; metrics and reporting norms by subfield (biomass and bio-based materials, LCA/TEA, catalysis/synthesis, electrochem). |
| `references/ai-tells-scientific.md` | Always. Vocabulary, sentence and structural patterns that mark generated prose in papers, and what strong scientific prose does instead. |
| `references/acs-style.md` | During the style pass. Units, numbers, nomenclature, abbreviations, tense, figures/tables/schemes, ACS reference format with examples. |
| `references/deliverable-templates.md` | When writing the output. Change-log and author-query formats, Synopsis examples, cover-letter skeleton. |

### 3. Edit in passes, in this order

Order matters: structural decisions change which sentences survive, so do them before polishing sentences you may delete.

**Pass A — Structure and required elements.** Title (specific, no evaluative adjectives, no "green/sustainable"), abstract (150–200 words, no citations, key numbers), 5–8 keywords, unnumbered section headings in the journal's order, figure/table/scheme numbering and callouts, safety statement in the Experimental section, Associated Content (Supporting Information description with file types; Data Availability Statement), Author Information (corresponding author with asterisk and email; contributions; competing-interest statement), Acknowledgments (funding; AI-use disclosure if applicable), References, TOC graphic placeholder on the last page. Add `[AUTHOR: ...]` placeholders where content is missing. A one-sentence sustainability synopsis was mandatory until 2025 and is now optional; draft one from the paper's own numbers anyway, because it is the sentence the editor is looking for, and mark it optional. Word budget: if the draft is over 7000 word-equivalents (figures count 300–600 each), say so and suggest what moves to the SI. Details in `journal-requirements.md`.

**Pass B — The sustainability argument.** Find every "green", "sustainable", "renewable", "eco-friendly", "benign", "circular", "low-carbon". For each, either (i) attach the number or comparison already in the draft, (ii) rewrite it as the specific technical fact it stands for, or (iii) delete it and query the author for the metric. Check that the paper benchmarks against the relevant incumbent (the process it would replace, the prior best result) with citations. Check subfield reporting norms (`sustainability-claims.md`): mass balances and dry-basis yields for biomass; functional unit, system boundary, allocation, data sources and years, and uncertainty for LCA; cost year, discount rate, plant scale, and price assumptions for TEA.

**Pass C — Prose.** Sentence by sentence through Introduction, Results and Discussion, Conclusions (Methods usually need only Pass D). Remove the vocabulary and patterns in `ai-tells-scientific.md`; replace each with the specific fact, a direct claim pointing at a figure or number, or nothing. Cut sentences that only announce what the next sentence will say. Vary sentence length. Cut "novel", "for the first time", "to the best of our knowledge", "unprecedented", "facile", "successfully" everywhere; the novelty is shown by the comparison to prior work, not asserted. Keep paragraphs to one idea. Tie every mechanistic or causal statement to the evidence in the draft or mark it as a hypothesis in the author's own hedged terms.

**Pass D — ACS style mechanics.** Units and spacing, numerals, ranges, chemical formulas and nomenclature, abbreviations defined at first use in abstract and again in text, tense (past for what was done, present for what is true and for pointing at figures), "data are", figure captions and table titles, reference list converted to ACS format. Checklist in `acs-style.md`.

**Pass E — Consistency.** Every number in the abstract and conclusions appears identically in Results. Every figure, table, and scheme is cited in order. Every abbreviation is defined once. Sample names and conditions are the same throughout. The title, Synopsis, abstract, and last paragraph of the Introduction all make the same claim.

### 4. Deliver

Produce, in this order:

1. **The edited manuscript.** If the input was a .docx and you can write files, produce an edited .docx (keep the author's heading structure; do not reformat their figures). Otherwise return the full edited text in the reply in manuscript order with plain section headings. Never return only a diff or a list of suggestions when the user asked for edits; they should be able to paste your output straight into their file. Inline `[AUTHOR: ...]` queries stay in the text where the author needs to act.
2. **Change log.** Grouped by pass (Structure / Sustainability argument / Prose / Style / Consistency), each entry one line: what changed and why, quoting the old wording when the change is substantive. Mechanical fixes (units, en dashes) can be summarized as counts. Format in `deliverable-templates.md`.
3. **Author queries.** Numbered, each one answerable: the missing metric, the unsupported claim, the reference that needs checking, the figure that is never cited. Put the ones that decide acceptance first (sustainability metric, benchmark comparison, missing controls), then the mechanical ones.
4. **Submission checklist status.** The journal's required elements, marked present / added as placeholder / missing, from `journal-requirements.md` §10. Requirements change (the Synopsis rule was dropped in 2026); when a checklist item decides acceptance, tell the author to confirm it against the live author-guidelines page.

Keep the commentary proportionate: a 6000-word paper deserves a full report; for a pasted abstract, the change log is a few lines and the author queries are the useful part.

## Voice of a good ACS SCE research article

For calibration, this is what the well-edited papers in this journal sound like:

- Declarative titles that name the system and the result, no adjectives: "Choline Chloride–Lactic Acid Deep Eutectic Solvent Pretreatment of Corn Stover: 78% Delignification and Five-Cycle Solvent Reuse" beats "Novel and Green DES Pretreatment for Highly Efficient Lignin Extraction".
- Abstracts that give the numbers: yield, selectivity, conditions, the benchmark, and the sustainability metric, in 150–200 words, no citations.
- First person plural is normal and often clearer ("We attribute the drop to..."), past tense for what was done, present tense for interpretation and for figure references ("Figure 3 shows...").
- Claims of mechanism are hedged exactly as much as the evidence warrants, and the hedge names the alternative ("The 1730 cm⁻¹ band loss is consistent with deacetylation of hemicellulose, although partial hemicellulose removal would give the same result").
- Comparisons to prior work are specific, with numbers and citations, usually in a table.
- Conclusions restate the two or three quantitative findings, name the limitation, and say what would have to be true for the process to matter at scale. No "paves the way".

## When the user asks for something adjacent

- **Cover letter**: use the skeleton in `deliverable-templates.md`; it should state the sustainability advance in one quantitative sentence and why it fits the journal's scope.
- **Response to reviewers**: point-by-point, quote each comment, state the change and where it appears; same no-fabrication rule.
- **A different ACS journal** (e.g., *Green Chemistry* is RSC, not ACS; *ACS Omega*, *I&EC Research*): ACS style and the prose guidance still apply; the Synopsis and sustainability-metric gate are ACS SCE-specific, so say which parts transfer.
- **Letters**: 3000 word-equivalents, sections optional, first-author status in the cover letter; the prose and sustainability guidance apply unchanged. **Perspectives/Reviews**: not in the current manuscript-type list; tell the user to confirm with the journal office before investing effort.
