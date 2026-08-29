# AI-generated prose in scientific papers: what it looks like and what to write instead

Editors at ACS journals now read hundreds of drafts a year that were written or "polished" by a language model, and they have learned the tells. This file lists those tells for chemistry and chemical-engineering manuscripts and, more importantly, what a well-written paper does in each place instead. Use it during the prose pass (Pass C in SKILL.md).

Two principles before the lists:

**Every tell marks the spot where a specific fact is missing.** "This work paves the way for sustainable biorefineries" appears where the author has not said what the result enables, for whom, at what scale. "Significantly enhanced" appears where the number and the comparator should be. The fix is never a synonym; it is the fact, pulled from the draft, or a query to the author if the draft does not contain it. If you just swap "crucial" for "important", you have made the paper harder to diagnose and no better.

**Density and clustering, not single words.** Humans write "crucial" and "comprehensive". One instance is nothing. Five importance-claiming words in an abstract, every paragraph opening with "Furthermore" and closing on an "-ing" clause, is a paper an editor will assume nobody with judgment has read. Do not tell the author their draft "looks AI-generated"; edit the prose and list the changes.

Contents: 1 Vocabulary · 2 Sentence patterns · 3 Paragraph and section patterns · 4 Results and Discussion tells · 5 References · 6 What good scientific prose does · 7 Disclosure policy

---

## 1. Vocabulary

### 1.1 Words with measured post-2023 excess in scientific abstracts

From the studies of 15 million PubMed abstracts (Kobak et al., *Sci. Adv.* 2025) and ~1 million arXiv/bioRxiv/Nature papers (Liang et al., 2024–2025). The frequency ratios are 2024 vs. the pre-LLM trend.

| Word | Excess | Replace with |
|---|---|---|
| delve(s)/delving | 28× | "examine", "measure", or just say what was done |
| underscore(s)/underscoring | 14× | state the fact the sentence is underscoring |
| showcase/showcasing | 11× | "show" with the number |
| pivotal, crucial, vital, paramount | large | delete, or give the reason it matters |
| intricate, intricacies | large | name the structure or interaction |
| meticulous(ly) | large | delete; describe the procedure |
| realm | large | "field", or delete |
| notably | large | delete; the sentence should carry its own weight |
| comprehensive(ly) | large | list what was actually characterized |
| potential (as noun: "the potential of") | largest absolute | say what it could do, with the number that suggests it |
| findings ("our findings") | large | "results", or the finding itself |
| additionally, furthermore, moreover | large | new sentence, "and", "also", or nothing |
| across ("across various") | large | be specific |
| grappling | large | delete |

### 1.2 Importance-claiming and outlook phrases

Delete on sight; if the point is real, replace with the fact.

plays a (crucial/pivotal/vital/key/important) role · holds great promise · paves the way (for/toward) · opens (new) avenues · a promising (candidate/alternative/platform/avenue) · offers/provides (valuable/new) insights · sheds (new) light on · has garnered/attracted (tremendous/considerable/significant/increasing) attention · in the (context/realm/landscape) of · is a testament to · marks a (turning point/milestone) · a step toward · is of paramount importance · is highly desirable · is an urgent need · the ever-increasing demand · cannot be overstated · addresses these challenges · unlock the potential · harness · leverage · synergistic (without a measured synergy) · game-changing · groundbreaking · transformative · robust (of a result, without a test) · seamless · state-of-the-art (as adjective without a citation to the state of the art)

### 1.3 Novelty and evaluation words

novel · new · for the first time · first report · to the best of our knowledge · unprecedented · facile · successfully (before a verb) · herein (as sentence opener) · remarkable/remarkably · excellent · outstanding · superior (without "to X by Y") · dramatic · significant(ly) (without a statistical test) · highly efficient · impressive · ideal · optimal (without an optimization)

Novelty is demonstrated by the comparison table against prior work, not by the adjective. Several ACS journals prohibit "novel", "new", "first", "excellent", "outstanding" in titles and abstracts outright. "Successfully synthesized" says nothing that "synthesized" plus the yield does not.

### 1.4 Bare sustainability words (see `sustainability-claims.md` for the fix)

green · sustainable · eco-friendly · environmentally friendly/benign · renewable (of a process, rather than a feedstock) · circular · low-carbon · clean · non-toxic (without a data point) · biodegradable (without a standard and a number)

Each of these is a claim reviewers at this journal test. Attach the metric, the comparator, or delete.

### 1.5 Empty frames the ACS Style Guide itself lists

It is interesting to note that · It is worth (noting/mentioning) that · It should be noted that · It has been found that · It was demonstrated that · It has long been known that · As already stated · It may be said that · It is clear/evident/obvious that · As can be seen (from Figure X) · It can be seen that

Cut the frame; start with the content. "As can be seen from Figure 1a, delignification increased with temperature" → "Delignification increased from 45 to 78% between 100 and 140 °C (Figure 1a)".

## 2. Sentence patterns

**Participial closers.** A factual sentence with an "-ing" clause bolted on to assert meaning: "...decreased to 6.9%, highlighting the efficient removal of lignin." "...exhibited a porous morphology, underscoring the disruption of the cell wall." The clause is a narrator asserting significance. Cut it. If the interpretation is real, make it a sentence with its own evidence: "The porous morphology (Figure 2d) is consistent with removal of the lignin–hemicellulose matrix, which the composition data in Table 1 confirm."

**Copula avoidance.** "serves as", "stands as", "represents", "acts as", "functions as", "boasts" in place of "is". "Lignocellulose represents the most abundant renewable resource" → "Lignocellulose is the most abundant renewable carbon source (≈180 Gt/yr)".

**Negative parallelism.** "not only X but also Y", "not just X, it is Y". Two sentences, or "X and Y".

**Rule of three.** "low cost, biodegradability, and tunable properties"; "harsh conditions, high cost, and environmental pollution". Models reach for triples to make a thin point feel complete. Keep only the items that matter to this paper and give each its source or number.

**Vague attribution.** "numerous studies have demonstrated", "it is widely believed", "various authors have argued", "researchers have found", "it is well established". Cite the specific studies, with the numbers they reported, or own the statement.

**Elegant variation.** The pretreated solid becomes "the substrate", "the material", "the sample", "the biomass". Pick one noun per thing and reuse it; readers of a chemistry paper need to know that two names are the same sample, and the varying synonyms are a model artifact from repetition penalties.

**Announcing sentences.** "In this section, the effect of temperature is discussed." "The following paragraphs describe the characterization." Delete; the heading does this.

**Symmetric length.** Every sentence 18–25 words, subject–verb–object. Break long ones, let a short one carry the key number. "At 140 °C the delignification reached 78.4%." is a fine sentence.

**Hedging stacks.** "may potentially be attributed to", "could possibly suggest". One hedge, and name the alternative: "The drop in Mw is consistent with ether cleavage; condensation would give the opposite trend."

**Em dashes** joining clauses. Chemistry papers use commas, parentheses, and periods; ACS reserves em dashes for words that would be misread otherwise.

## 3. Paragraph and section patterns

- **Transition openers.** "Furthermore," "Moreover," "Additionally," "Consequently," "Notably," "Importantly," "Interestingly," starting successive paragraphs or sentences. In a well-argued paper, the logic is carried by content; transitions are rare and mostly "however" and "because". More than one "furthermore/moreover" per section is a tell.
- **Introduction formula.** Paragraph 1: global importance with round numbers ("400 million tons"). Paragraph 2: "various methods have been developed ... however, these suffer from ..." with an undifferentiated triple of drawbacks. Paragraph 3: "X has garnered tremendous attention due to ...". Paragraph 4: "Herein/In this study, we ... To the best of our knowledge, this is the first ... This work not only ... but also ...". Rewrite so that paragraph 2 names the specific prior results and their numbers, paragraph 3 says what is unknown or unsolved, and paragraph 4 says what this paper measured and the answer.
- **Recap conclusions.** A paragraph that restates the abstract, then "paves the way". A Conclusions section states the two or three quantitative findings, the limitation, and what would have to be true for the result to matter at scale.
- **"Challenges and outlook" boilerplate.** "Despite these advances, challenges remain in scaling up ... future work should focus on ...". Either name the specific obstacle with a number (viscosity at 20 wt % loading, cost of DES makeup at 5% loss per cycle) or omit.
- **Uniform paragraph shape.** Claim, explanation, example, transition, repeated. Some paragraphs should be two sentences and a number.
- **Bulleted or bold-headed fragments** in place of argued prose in Results and Discussion.

## 4. Results and Discussion tells

Reviewers of a wholly GPT-generated manuscript (2025 study) who did catch it named "template-like phrasing, superficial discussion, repetitive language". In a chemistry paper that looks like:

- **Caption restated as prose.** "Figure 3 shows the HSQC spectrum of the DES lignin." State what the figure demonstrates: "The Aβ/Aα cross-peak ratio (Figure 3) gives 38 β-O-4 linkages per 100 aromatic units, versus 52 in the milled-wood lignin."
- **Generic mechanism.** A paragraph about hydrogen-bond disruption or acid-catalyzed ether cleavage that could be pasted into any DES paper, with no reference to this paper's own control, spectrum, or kinetic data. Either tie it to a measurement in the draft or mark it as a hypothesis and query the author for the supporting data.
- **"As expected" / "consistent with previous reports" on every observation** without which report and which value. Give the citation and the number, or delete.
- **"Can be attributed to" / "may be due to"** as the connective between every result and its explanation, with no evidence offered. Once per section is fine; a chain of them is an unsupported discussion.
- **Superlatives without comparators.** "remarkable improvement", "excellent recyclability", "superior performance". Give the number, the comparator, and the source: "72% delignification after five cycles, versus 58% after three cycles for the ChCl–oxalic acid system in ref 12".
- **"Significant" with no statistics.** Give n, error bars, and a test, or use "the difference (78 vs. 45%) ...".
- **Inconsistent terminology or values** between sections (84.7% in Results, "85%" in Conclusions, "~80%" in the abstract).
- **Numbers that are too clean.** Round improvements ("a 4-fold enhancement") and results with more significant figures than the method supports. Query.
- **Residual chatbot strings.** "As an AI language model", "as of my last knowledge update", "Certainly! Here is", "regenerate response". Search the text for them; they have appeared in published papers.

## 5. References

The most concrete AI tell and the one publishers now check automatically (Science, NEJM, JAMA, and others run reference validators; a 2026 study found one paper in ~280 contains a fabricated citation). Signs:

- Authors who are real but never wrote together; a plausible title that does not exist; a real DOI pointing at a different article; volume and page ranges that do not match the year.
- Citations that support a claim only generically ("DESs are green solvents [3–7]") with five references for a sentence that needs one specific one.
- Mixed citation styles in one list (APA, Nature, ACS) suggest concatenation from several sources without a reference manager; convert and query.

You cannot verify DOIs offline. Do not "correct" a reference into something that looks plausible. Reformat what is given, and query any entry whose details are internally inconsistent or that you suspect does not exist.

## 6. What good scientific prose does

Use this as the target when rewriting.

| Instead of | Write |
|---|---|
| significance adjective | the number, the comparator, and where it came from: "78% delignification (Table 1), compared with 61% for the ChCl–oxalic acid DES under the same conditions¹²" |
| "provides insights into the mechanism" | the specific inference and the evidence: "The 0.9 ppm downfield shift of the Hα signal indicates ..." |
| "various studies have shown" | "Kumar et al. reported 65% delignification of rice straw with a ChCl–lactic acid DES at 120 °C¹⁴" |
| "green solvent" | "a solvent recovered at 91% per cycle with an E-factor of 4.2" |
| "holds promise for scale-up" | the obstacle with a number, and what would resolve it |
| hedged chain | one hedge that names the alternative and how to distinguish it |
| paragraph that ends in "-ing" | paragraph that ends on the number or the limitation |
| recap conclusion | conclusion that states the findings, the limitation, and the condition under which the process matters |

Also:

- One idea per paragraph, topic sentence first, 60–150 words typical; vary length.
- First person plural where it clarifies who did what and prevents dangling modifiers.
- Concessions are credibility: "The five-cycle reuse test does not include DES makeup; a mass balance is in the SI" reads as a scientist writing; "excellent recyclability" reads as a press release.
- Comparisons to prior work are specific and usually tabulated.
- Terminology and sample names fixed at first use and never varied.

## 7. Disclosure policy

ACS Publications policy (2024–2026): AI tools cannot be authors; use of generative AI for text must be disclosed in the Acknowledgments with when and how it was used (substantial use also in Methods); AI use in graphics disclosed in the caption; AI-generated images are not permitted for the TOC graphic; authors are responsible for the accuracy of AI-generated content and references; editors may reject or request revision if AI use is judged excessive. If the user tells you the draft was written with a chatbot, remind them once, in the author queries, that ACS asks for a disclosure sentence and offer the wording: "Portions of the initial draft were edited with the assistance of [tool, version]; all content was reviewed and verified by the authors." Editing for grammar and style with an AI tool is where publishers draw the line for "no declaration needed" (Elsevier, Springer Nature) but ACS's wording is broader; disclosure is the safe default.
