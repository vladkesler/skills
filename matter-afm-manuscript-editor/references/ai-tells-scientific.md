# AI-sounding prose in materials papers: what it looks like and what to write instead

Editors at Matter and Advanced Functional Materials read a great many drafts written or "polished" by a language model, and the pattern is easy to recognize. AFM's editors reject at the first screen papers that "need extensive improvement in the language"; Cell Press discourages the words "novel" and "first" in its guidelines. Prose that reads as generated tells an editor that nobody with judgment has gone through the paper, and it usually hides a claim that was never pinned down. This file lists the tells and, more usefully, what a well-written paper does in each place. Use it during the prose pass.

Two principles before the lists:

**Every tell marks the spot where a specific fact is missing.** "This work paves the way for next-generation flexible electronics" appears where the author has not said what the result enables, for which device, under what conditions. "Significantly enhanced" appears where the number and the comparator should be. The fix is never a synonym. It is the fact, taken from the draft, or a query to the author if the draft does not contain it. Swapping "crucial" for "important" makes the paper harder to diagnose and no better.

**Density and clustering matter; single words do not.** People write "crucial" and "comprehensive" too. One instance means nothing. Five importance-claiming words in an abstract, every paragraph opening with "Furthermore" and closing on an "-ing" clause, is a paper an editor will assume is unread. Never tell the author that their draft "looks AI-generated". Edit the prose and list the changes.

Contents: 1 Vocabulary · 2 Sentence patterns · 3 Paragraph and section patterns · 4 Results and Discussion tells · 5 References · 6 What good scientific prose does · 7 Disclosure

---

## 1. Vocabulary

### 1.1 Words whose use in scientific abstracts jumped after 2023

Studies of excess vocabulary in millions of abstracts (Kobak et al., *Science Advances* 2025; Liang et al., 2024) found these far above their earlier trend.

| Word | Replace with |
|---|---|
| delve(s), delving | "examine", "measure", or simply say what was done |
| underscore(s), underscoring | the fact the sentence is underscoring |
| showcase, showcasing | "show", with the number |
| pivotal, crucial, vital, paramount | delete, or give the reason it matters |
| intricate, intricacies | name the structure or interaction |
| meticulous(ly) | delete; describe the procedure |
| realm, landscape | "field", or delete |
| notably, importantly | delete; the sentence should carry its own weight |
| comprehensive(ly), systematically | list what was characterized or varied |
| potential (as noun: "the potential of") | say what it could do, with the number that suggests it |
| additionally, furthermore, moreover | a new sentence, "and", "also", or nothing |
| across ("across various") | be specific |

### 1.2 Importance-claiming and outlook phrases

Delete on sight; if the point is real, replace it with the fact.

plays a (crucial / pivotal / vital / key) role · holds great promise · paves the way (for / toward) · opens (new) avenues · a promising (candidate / alternative / platform / strategy) · offers (valuable / new) insights · sheds (new) light on · has garnered / attracted (tremendous / considerable / increasing) attention · in the (context / realm / landscape) of · is of paramount importance · is highly desirable · is an urgent need · the ever-increasing demand · addresses these challenges · unlock the potential · harness · leverage · synergistic (without a measured synergy) · game-changing · groundbreaking · transformative · next-generation · robust (of a result, without a test) · seamless · state-of-the-art (without a citation to that state of the art) · a new paradigm · bridges the gap

### 1.3 Novelty and evaluation words

novel · new · for the first time · first report · to the best of our knowledge · unprecedented · facile · successfully (before a verb) · herein (as a sentence opener) · remarkable / remarkably · excellent · outstanding · superior (without "to X by Y") · ultra- and super- prefixes without a definition (ultrastrong, supertough) · dramatic · significant(ly) (without a statistical test) · highly efficient · impressive · ideal · optimal (without an optimization) · multifunctional (without the functions measured) · smart

Cell Press: "We discourage novelty claims (e.g., use of the word 'novel' and 'first') because they are overused, tend not to add meaning, and are difficult to verify." Novelty is demonstrated by the comparison with prior work. "Successfully synthesized" says nothing that "synthesized" plus the yield does not. If "ultrastrong" stays, the paper must say what strength qualifies and compared with what.

### 1.4 Bare property and sustainability words

strong · tough · flexible · stretchable · conductive · stable · durable · biocompatible · green · sustainable · eco-friendly · biodegradable · renewable · low-cost · scalable

When one of these describes the authors' own material, it is a claim reviewers test. Attach the number, the conditions and the comparator, or delete. General background statements need a reference, not a metric. The editing patterns are in `materials-claims.md`.

### 1.5 Empty frames

It is interesting to note that · It is worth (noting / mentioning) that · It should be noted that · It has been found that · It was demonstrated that · It is well known that · As mentioned above · It is clear / evident / obvious that · As can be seen (from Figure X) · It can be seen that

Cut the frame and start with the content. "As can be seen from Figure 2a, the tensile strength increased with lignin content" becomes "Tensile strength rose from 21 to 52 MPa as the lignin content increased from 0 to 15 wt % (Figure 2a)".

## 2. Sentence patterns

**Participial closers.** A factual sentence with an "-ing" clause bolted on to assert meaning: "...retained 91% of its conductivity after 1,000 cycles, highlighting its excellent durability." "...showed a porous morphology, underscoring the effectiveness of the freeze-casting strategy." The clause is a narrator asserting significance. Cut it. If the interpretation is real, give it its own sentence with its own evidence.

**Copula avoidance.** "serves as", "stands as", "represents", "acts as", "functions as", "boasts" in place of "is" or "has". "Cellulose represents the most abundant biopolymer" becomes "Cellulose is the most abundant biopolymer".

**Negative parallelism.** "not only X but also Y", "not just X, it is Y". Write two sentences, or "X and Y".

**Rule of three.** "lightweight, flexible, and biodegradable"; "high cost, poor stability, and complex processing". Models reach for triples to make a thin point feel complete. Keep only the items that matter to this paper and give each its number or source.

**Vague attribution.** "numerous studies have demonstrated", "it is widely recognized", "researchers have found", "extensive efforts have been devoted". Cite the specific studies with the values they reported, or own the statement.

**Elegant variation.** The hydrogel becomes "the gel", "the network", "the material", "the sample", "the as-prepared composite". Pick one name per thing and keep it; a reader needs to know that two names are the same sample.

**Announcing sentences.** "In this section, the mechanical properties are discussed." "The following describes the characterization." Delete; the heading does this.

**Symmetric length.** Every sentence 18–25 words, subject–verb–object. Break long ones and let a short one carry the key number. "The film stretches to 40%." is a fine sentence.

**Hedging stacks.** "may potentially be attributed to", "could possibly suggest". One hedge, and name the alternative: "The lower modulus is consistent with plasticization by residual water; reduced crystallinity would have the same effect and is not excluded by the XRD data."

**Em dashes** joining clauses. Research papers use commas, parentheses and periods.

## 3. Paragraph and section patterns

- **Transition openers.** "Furthermore," "Moreover," "Additionally," "Consequently," "Notably," "Interestingly," beginning successive sentences or paragraphs. In a well-argued paper the logic is carried by the content; transitions are rare and mostly "however" and "because". More than one "furthermore" or "moreover" in a section is a tell.
- **Introduction formula.** Paragraph 1: global importance with round numbers ("over 400 million tons of plastic"). Paragraph 2: "various strategies have been developed ... however, these suffer from ..." with an undifferentiated triple of drawbacks. Paragraph 3: "X has attracted tremendous attention owing to ...". Paragraph 4: "Herein, we report a novel ... To the best of our knowledge, this is the first ... This work not only ... but also provides new insights ...". Rewrite so that paragraph 2 names the specific prior results with their numbers, paragraph 3 says what is unknown or unsolved, and the last paragraph says what this paper did and found, with the key number. Both journals want the introduction to end on what was achieved.
- **Recap conclusions.** A paragraph that restates the abstract and ends on "paves the way". A conclusion states the two or three quantitative findings, what they mean, the main limitation, and what would have to be shown next.
- **Challenges-and-outlook boilerplate.** "Despite these advances, challenges remain in scaling up ... future work should focus on ...". Name the specific obstacle with a number (the modulus halves above 70% relative humidity; the monomer costs ten times the petrochemical one) or omit.
- **Uniform paragraph shape.** Claim, explanation, example, transition, repeated. Some paragraphs should be two sentences and a number.
- **Bulleted or bold-headed fragments** in place of argued prose in Results and Discussion.

## 4. Results and Discussion tells

- **Caption restated as prose.** "Figure 3 shows the SEM images of the aerogel." State what the figure demonstrates: "Freeze casting aligns the pore walls along the growth direction, with a wall spacing of 20–40 µm (Figure 3a,b)."
- **Generic mechanism.** A paragraph about hydrogen bonding, π–π stacking or chain entanglement that could be pasted into any paper on the material class, with no reference to this paper's own control, spectrum or model. Tie it to a measurement in the draft, or mark it as a hypothesis and query the author for the supporting data.
- **"As expected" and "consistent with previous reports"** on every observation, without saying which report and which value. Give the citation and the number, or delete.
- **"Can be attributed to" / "may be due to"** as the connective between every result and its explanation, with no evidence offered. Once in a section is fine; a chain of them is an unsupported discussion.
- **Superlatives without comparators.** "remarkable improvement", "excellent cycling stability", "superior to most reported materials". Give the number, the comparator and the source.
- **"Significant" with no statistics.** Give *n*, error bars and a test, or write "the difference (52 vs 21 MPa)".
- **Characterization as a checklist.** FTIR, XRD, XPS, TGA and SEM each given a paragraph that confirms what the previous one confirmed. Keep what the argument needs; move the rest to the supplement.
- **Inconsistent values or names** between sections (41% in the Results, "about 40%" in the conclusion, "~45%" in the abstract).
- **Numbers that are too clean.** Round improvements ("a 5-fold enhancement") and results with more significant figures than the method supports. Query.
- **Residual chatbot strings.** "As an AI language model", "as of my last knowledge update", "Certainly! Here is", "regenerate response", "I hope this helps". Search the text for them; they have appeared in published papers.

## 5. References

Fabricated references are the most concrete sign of unchecked AI use, and publishers now screen for them. Signs:

- Authors who are real but never wrote together; a plausible title that does not exist; a DOI that points to a different article; a volume and page range that do not match the year.
- Citations that support a claim only generically ("hydrogels have been widely studied [3–9]") with seven references for a sentence that needs one specific one.
- Mixed citation styles in one list, which suggests entries pasted from several sources.

You usually cannot verify a reference from inside a chat. Do not "correct" a reference into something that looks plausible. Reformat what is given, and query any entry whose details are internally inconsistent or that you suspect does not exist: `[AUTHOR: reference 14: please check that this article exists and that the details are right]`.

## 6. What good scientific prose does

Use this as the target when rewriting. The values are invented to show the form; use the author's numbers, never these.

| Instead of | Write |
|---|---|
| a significance adjective | the number, the comparator and where it came from: "a toughness of 3.2 MJ m⁻³, twice that of the lignin-free network (Figure 2c)" |
| "provides insights into the mechanism" | the specific inference and its evidence: "Methylating the phenolic hydroxyls removes the toughening (Figure 4b), which identifies lignin–PVA hydrogen bonds as the dissipating units" |
| "various studies have shown" | "Li et al. reported a cellulose nanofiber film with a tensile strength of 210 MPa" with the citation |
| "eco-friendly film" | "a film cast from water with no added crosslinker" |
| "holds promise for wearable electronics" | what was shown and what remains: "The sensor tracks finger bending for 1,000 cycles; operation above 70% relative humidity remains untested" |
| a hedged chain | one hedge that names the alternative and how to tell them apart |
| a paragraph that ends in "-ing" | a paragraph that ends on the number or the limitation |
| a recap conclusion | the findings, what they mean, the limitation, the next step |

Also:

- One idea per paragraph, topic sentence first, 60–150 words typical; vary the length.
- First person plural is fine in the main text of both journals where it clarifies who did what. The AFM abstract is the exception: impersonal, present tense.
- Concessions add credibility: "The films lose half their modulus at 80% relative humidity" reads as a scientist writing; "excellent stability" reads as a press release.
- Comparisons with prior work are specific and usually tabulated.
- Sample names are fixed at first use and never varied, and they are readable: "PVA–lignin-15" tells the reader more than "sample S3".

## 7. Disclosure

Both journals require authors to disclose the use of generative AI in preparing the manuscript, and both hold the authors responsible for every sentence and reference.

- **Matter (Cell Press, Elsevier policy):** a section titled "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process", placed after the Declaration of interests, included when the paper is first submitted. Wording: "During the preparation of this work, the author(s) used [NAME TOOL / SERVICE] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article." Basic grammar, spelling and reference checkers are exempt.
- **AFM (Wiley):** "If an author has used a GenAI tool to develop any portion of a manuscript, its use must be described, transparently and in detail, in the Methods section (or via a disclosure or within the Acknowledgements section, as applicable)."

An author whose paper was edited with this skill has used such a tool. Add the statement as a placeholder for the author to complete and confirm, say so in the to-do list, and do not treat it as optional. Removing AI-sounding prose is about making the paper say something specific; it is not a way around disclosure.
