#!/usr/bin/env python3
"""
manuscript_check.py - mechanical pre-edit scan for ACS Sustainable Chem. Eng. drafts.

Usage:
    python manuscript_check.py <manuscript.docx|.md|.txt> [--json]

Stdlib only (reads .docx via zipfile, no python-docx needed). Prints a Markdown
report listing:

  * AI-tell vocabulary and puffery, with line numbers and density per 1000 words
  * Novelty / superlative claims ("novel", "for the first time", "unprecedented")
  * Bare sustainability words ("green", "sustainable") that need a metric behind them
  * ACS unit and number formatting slips ("2g", "100°C", "hrs", "ml", "cm-1")
  * Paragraph-opening connective tics (Furthermore / Moreover / Additionally ...)
  * Journal-required elements that appear to be missing (Synopsis, Keywords, TOC graphic ...)
  * Reference-list style inconsistencies (mixed formats, missing DOIs)

The scan is a starting point for the human/model edit, not a verdict. Every hit
needs judgment: "green chemistry" as a field name is fine; "a green process"
without a metric is not. See references/ai-tells-scientific.md for the reasoning.
"""

import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from xml.etree import ElementTree as ET

# --------------------------------------------------------------------------- #
# Word lists
# --------------------------------------------------------------------------- #

# Words whose frequency in scientific abstracts jumped sharply after 2023
# (Kobak et al. style "excess vocabulary") plus the usual importance-claiming
# vocabulary. Tier 1 is close to diagnostic; tier 2 matters in clusters.
AI_TIER1 = [
    r"\bdelv(e|es|ed|ing)\b", r"\brealm\b", r"\btapestry\b", r"\blandscape\b",
    r"\bpivotal\b", r"\bcrucial\b", r"\bvital\b", r"\bparamount\b",
    r"\bunderscor(e|es|ed|ing)\b", r"\bshowcas(e|es|ed|ing)\b",
    r"\bmeticulous(ly)?\b", r"\bintricate\b", r"\bmultifaceted\b",
    r"\bpav(e|es|ed|ing) the way\b", r"\bholds? great promise\b",
    r"\bgarnered\b", r"\bunlock(s|ed|ing)?\b", r"\bharness(es|ed|ing)?\b",
    r"\bleverag(e|es|ed|ing)\b", r"\bsynerg(y|istic|istically)\b",
    r"\bgame[- ]chang(er|ing)\b", r"\bpromising (candidate|avenue|platform|alternative|solution)\b",
    r"\bvaluable insights?\b", r"\bnew insights? into\b", r"\bshed(s)? (new )?light on\b",
    r"\bin the (context|realm|field) of\b", r"\bplays? an? (crucial|vital|pivotal|key|important|significant) role\b",
    r"\btremendous (attention|interest|potential)\b", r"\bconsiderable attention\b",
    r"\bgreat potential\b", r"\bopens? (up )?(new )?(avenues|opportunities|possibilities)\b",
    r"\bcircular (plastics )?economy\b(?!.*\d)",
]
AI_TIER2 = [
    r"\brobust\b", r"\bcomprehensive(ly)?\b", r"\bholistic\b", r"\bfoster(s|ed|ing)?\b",
    r"\bfacilitat(e|es|ed|ing)\b", r"\butiliz(e|es|ed|ing|ation)\b", r"\bnavigat(e|es|ed|ing)\b",
    r"\bnotably\b", r"\bremarkabl(e|y)\b", r"\bsignificantly enhanc(e|es|ed|ing)\b",
    r"\bhighly (efficient|effective|promising|attractive)\b", r"\bexcellent\b", r"\boutstanding\b",
    r"\bsuperior\b", r"\bdramatic(ally)?\b", r"\bsubstantial(ly)?\b",
    r"\benhanc(e|es|ed|ing|ement)\b", r"\bin order to\b", r"\bit is worth (noting|mentioning)\b",
    r"\bit should be noted\b", r"\bit is (important|noteworthy) to (note|mention)\b",
    r"\bnot only\b.*\bbut also\b", r"\bfurthermore\b", r"\bmoreover\b", r"\badditionally\b",
    r"\bconsequently\b", r"\bin summary\b", r"\bin conclusion\b", r"\bwidely (regarded|believed|recognized|accepted)\b",
    r"\bnumerous studies\b", r"\bvarious (studies|authors|researchers)\b", r"\bextensively studied\b",
    r"\bindispensable\b", r"\bever[- ]increasing\b", r"\burgent need\b", r"\bgrowing (demand|interest|concern)\b",
    r"\baddress(es|ed|ing)? (these|this|the) challenge(s)?\b", r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bcost[- ]effective\b", r"\bversatile\b", r"\btunable\b", r"\benvironmentally (friendly|benign)\b",
    r"\beco[- ]friendly\b", r"\bnon[- ]toxic\b", r"\bbiodegradab(le|ility)\b(?!.*\bISO\b|.*\bASTM\b|.*\d+\s*%)",
]
NOVELTY = [
    r"\bnovel\b", r"\bfor the first time\b", r"\bfirst report\b", r"\bunprecedented\b",
    r"\bto the best of our knowledge\b", r"\bfacile\b", r"\bsuccessfully\b",
    r"\bherein\b", r"\bsystematically (investigated|studied)\b",
]
SUSTAINABILITY_BARE = [
    r"\bgreen\b", r"\bsustainab(le|ility)\b", r"\brenewable\b", r"\bcircular\b",
    r"\bbenign\b", r"\bclean(er)?\b", r"\blow[- ]carbon\b", r"\bcarbon[- ]neutral\b",
]
HEDGE_EMPTY = [
    r"\bit (was|is|can be|has been) (found|observed|shown|demonstrated|noted|seen) that\b",
    r"\bit is (clear|evident|obvious|apparent) that\b", r"\bas (can be|is) (seen|shown|observed)\b",
    r"\bit can be (seen|concluded|observed)\b", r"\bthis (clearly )?(indicates|demonstrates|confirms|suggests) that\b",
    r"\bmay be (due|attributed) to\b", r"\bcan be attributed to\b", r"\bas expected\b",
]

# Unit / number style slips (ACS: space between number and unit, including °C;
# SI abbreviations; negative exponents preferred; "h" not "hrs")
UNIT_PATTERNS = [
    (r"\b\d+(\.\d+)?(g|mg|kg|mL|ml|L|mol|mmol|µL|uL|nm|µm|um|mm|cm|m|rpm|MPa|kPa|bar|Pa|min|h|s|mV|V|mA|A|W|kW|MJ|kJ|J|wt|vol|ppm|FPU|IU)\b(?!\S)", "missing space between number and unit (ACS: '2 g', '50 mL')"),
    (r"\d\s*°C", None),  # handled specially: need exactly one space before °C
    (r"\b\d+(\.\d+)?\s*ml\b", "'ml' should be 'mL'"),
    (r"\bhrs?\b|\bhours?\b(?= at| of| and)", "'hrs'/'hours' should be 'h' in methods and figure text"),
    (r"\bmins?\b|\bminutes\b", "'min' is the ACS abbreviation for minutes"),
    (r"\bsec\b|\bseconds\b", "'s' is the ACS abbreviation for seconds"),
    (r"\bover night\b", "'overnight' is one word"),
    (r"\bcm-1\b|\bcm\^-1\b", "wavenumber should be 'cm−1' with a superscript minus one (cm⁻¹)"),
    (r"\d\s*%\s*\(?w/w|\bwt\.?%|\bwt%|\bmol%|\bvol%", "ACS style: 'wt %', 'mol %', 'vol %' with a space"),
    (r"\b\d+\s*-\s*\d+\s*(°C|h|min|mesh|%|nm|mL|g|kg|mm|cm)", "ranges take an en dash with no spaces: '40–60 mesh', '1–6 h'"),
    (r"\bmicro[- ]?liter|\bmicroliter", "use µL"),
    (r"\b\d+\s*x\s*\d+", "use the multiplication sign × (e.g. 5 × 10³)"),
    (r"\bg/mol\b", "'g/mol' is acceptable; ACS also accepts 'g mol−1'; be consistent throughout"),
    (r"\b(\d+)(K|k)\b(?!\w)", "check: temperatures in kelvin take a space ('298 K'); thousands use no unit"),
    (r"\bDMSO-d6\b", "isotope descriptor: DMSO-d₆ (subscript 6, italic d)"),
    (r"\b(e\.g\.|i\.e\.)(?!,)", "ACS: follow 'e.g.' and 'i.e.' with a comma"),
    (r"\bvs\b(?!\.)", "ACS: 'vs.' with a period"),
]

REQUIRED_ELEMENTS = {
    "One-sentence sustainability synopsis (optional since Aug 2026 guidelines; still what editors screen for)": r"\bsynopsis\b",
    "Keywords (5–8 required)": r"\bkeywords?\b",
    "TOC / abstract graphic mention": r"\b(TOC|table of contents|abstract) graphic\b|\bgraphical abstract\b",
    "Supporting Information / ASSOCIATED CONTENT": r"\bsupporting information\b|\bassociated content\b",
    "Corresponding author marked": r"\*\s*(corresponding|e-?mail)|\bcorresponding author\b",
    "Author contributions (optional)": r"\bauthor contributions?\b|\bCRediT\b",
    "Hazard / safety statement in Experimental (required by ACS)": r"\b(hazard|hazardous|caution|safety|toxic|flammable|corrosive)\b",
    "Conflict of interest / Notes": r"\bconflict(s)? of interest\b|\bcompeting (financial )?interests?\b|\bnotes\b",
    "Acknowledgments": r"\backnowledg(e)?ments?\b",
    "Data Availability Statement (Associated Content)": r"\bdata availability\b|\bdata are available\b|\bdata is available\b",
    "Experimental / Methods section": r"\b(experimental|materials and methods|methods|methodology)\b",
    "Conclusions section": r"\bconclusions?\b",
}

SECTION_HEADINGS = re.compile(
    r"^\s*(\d+(\.\d+)*\.?\s+)?(abstract|introduction|experimental( section)?|materials and methods|methods|"
    r"results and discussion|results|discussion|conclusions?|references|acknowledg(e)?ments?|"
    r"supporting information|associated content|author information|keywords?|synopsis)\b.*$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------- #
# Input handling
# --------------------------------------------------------------------------- #

def read_docx(path):
    """Extract paragraphs from a .docx without python-docx."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter("{%s}p" % ns["w"]):
        texts = [t.text or "" for t in p.iter("{%s}t" % ns["w"])]
        paras.append("".join(texts))
    return "\n".join(paras)


def load_text(path):
    if path.lower().endswith(".docx"):
        return read_docx(path)
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #

def find_all(patterns, lines, flags=re.IGNORECASE):
    hits = defaultdict(list)  # pattern -> [(lineno, snippet)]
    for i, line in enumerate(lines, 1):
        for pat in patterns:
            for m in re.finditer(pat, line, flags):
                start = max(0, m.start() - 40)
                end = min(len(line), m.end() + 40)
                snippet = line[start:end].strip()
                hits[pat].append((i, m.group(0), snippet))
    return hits


def locate_sections(lines):
    """Return {heading_lower: line_index} for recognisable section headings."""
    found = {}
    for i, line in enumerate(lines):
        m = SECTION_HEADINGS.match(line)
        if m and len(line.strip()) < 60:
            found.setdefault(m.group(3).lower(), i)
    return found


def abstract_block(lines, sections):
    if "abstract" not in sections:
        return None
    start = sections["abstract"]
    # abstract ends at next heading
    ends = [v for k, v in sections.items() if v > start]
    end = min(ends) if ends else min(start + 15, len(lines))
    return "\n".join(lines[start:end])


def paragraph_openers(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if len(p.strip()) > 120]
    openers = Counter()
    for p in paras:
        first = re.match(r"([A-Za-z]+)", p)
        if first:
            w = first.group(1).lower()
            if w in {"furthermore", "moreover", "additionally", "however", "therefore", "consequently",
                     "nevertheless", "notably", "importantly", "interestingly", "in", "herein", "overall"}:
                openers[w] += 1
    return openers, len(paras)


def check_references(lines, sections):
    if "references" not in sections:
        return {"present": False}
    refs = [l.strip() for l in lines[sections["references"] + 1:] if l.strip()]
    styles = Counter()
    no_doi = 0
    for r in refs:
        if re.search(r"\(\d{4}\)\.", r) or re.search(r", \d{4}\)\.", r):
            styles["APA-like (Author (2011). Title.)"] += 1
        elif re.search(r"\d{4}, \d+, \d+", r) or re.search(r"\*\*\d{4}\*\*", r):
            styles["ACS-like (Journal Year, Vol, Pages)"] += 1
        elif re.search(r"\d+, \d+[-–]\d+ \(\d{4}\)", r):
            styles["Nature-like (Journal Vol, Pages (Year))"] += 1
        elif re.search(r"\d{4};\d+:", r):
            styles["Vancouver-like (Journal. Year;Vol:Pages)"] += 1
        else:
            styles["unclassified"] += 1
        if not re.search(r"doi|10\.\d{4,}/", r, re.IGNORECASE):
            no_doi += 1
    et_al = sum(1 for r in refs if re.search(r"\bet al\b", r))
    return {
        "present": True,
        "count": len(refs),
        "styles": dict(styles),
        "without_doi": no_doi,
        "with_et_al": et_al,
    }


def unit_checks(lines):
    out = []
    for i, line in enumerate(lines, 1):
        # °C spacing: require exactly one space between digit and °C
        for m in re.finditer(r"(\d+)(\s*)°\s*C", line):
            if m.group(2) != " ":
                out.append((i, m.group(0), "ACS: one space between number and °C ('100 °C')"))
        for pat, msg in UNIT_PATTERNS:
            if msg is None:
                continue
            for m in re.finditer(pat, line):
                out.append((i, m.group(0), msg))
    return out


def analyse(text):
    lines = text.splitlines()
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    n_words = max(1, len(words))
    sections = locate_sections(lines)

    tier1 = find_all(AI_TIER1, lines)
    tier2 = find_all(AI_TIER2, lines)
    novelty = find_all(NOVELTY, lines)
    sustain = find_all(SUSTAINABILITY_BARE, lines)
    hedges = find_all(HEDGE_EMPTY, lines)

    n_t1 = sum(len(v) for v in tier1.values())
    n_t2 = sum(len(v) for v in tier2.values())
    em_dashes = text.count("—")
    respectively = len(re.findall(r"\brespectively\b", text, re.IGNORECASE))
    significant = len(re.findall(r"\bsignificant(ly)?\b", text, re.IGNORECASE))
    stats_words = len(re.findall(r"\bp\s*[<=>]\s*0\.\d+|\bANOVA\b|\bt-test\b|\bstandard deviation\b|\b±\b|\bn\s*=\s*\d", text))

    openers, n_paras = paragraph_openers(text)

    abstract = abstract_block(lines, sections)
    abstract_issues = []
    if abstract:
        aw = len(re.findall(r"[A-Za-z][A-Za-z'-]*", abstract))
        if re.search(r"\[\d+([-–,]\d+)*\]|\(\w+ et al\.,? \d{4}\)|\^\d", abstract):
            abstract_issues.append("abstract contains citations (ACS abstracts must be self-contained; no references)")
        if aw > 200:
            abstract_issues.append(f"abstract is {aw} words; ACS SCE requires 150–200 words")
        elif aw < 120:
            abstract_issues.append(f"abstract is {aw} words; ACS SCE requires 150–200 words")
        if not re.search(r"\d", abstract):
            abstract_issues.append("abstract contains no numbers; state the key quantitative results")
    else:
        abstract_issues.append("no 'Abstract' heading found")

    missing = []
    for name, pat in REQUIRED_ELEMENTS.items():
        if not re.search(pat, text, re.IGNORECASE):
            missing.append(name)

    refs = check_references(lines, sections)
    units = unit_checks(lines)

    numbered_headings = [l.strip() for l in lines if re.match(r"^\s*\d+(\.\d+)*\.?\s+[A-Z][A-Za-z ]{2,40}$", l)]
    if numbered_headings:
        missing.append(f"(style) {len(numbered_headings)} numbered section headings found — ACS SCE does not number sections")

    title = next((l.strip() for l in lines if l.strip()), "")
    title_issues = []
    if title:
        tw = len(title.split())
        if tw > 15:
            title_issues.append(f"title has {tw} words; the guidelines call 20 too long — aim for ≤ 15 and drop adjectives")
        if re.search(r"\bnovel\b|\bfacile\b|\bhighly\b|\befficient\b|\bgreen\b|\bsustainable\b|\bapproach\b|\bstrategy\b|\benhanced\b", title, re.IGNORECASE):
            title_issues.append("title contains evaluative adjectives (novel/facile/highly efficient/green/sustainable) — replace with what was done and the key number or system")
        if title.count(":") >= 1 and re.search(r":\s*(a|an|towards?)\s", title, re.IGNORECASE):
            title_issues.append("colon subtitle of the form ': A Sustainable/Novel Approach' adds no information")

    return {
        "n_words": n_words,
        "sections": sections,
        "tier1": tier1, "tier2": tier2, "novelty": novelty, "sustain": sustain, "hedges": hedges,
        "n_t1": n_t1, "n_t2": n_t2,
        "density_t1": 1000 * n_t1 / n_words, "density_all": 1000 * (n_t1 + n_t2) / n_words,
        "em_dashes": em_dashes, "respectively": respectively,
        "significant": significant, "stats_words": stats_words,
        "openers": openers, "n_paras": n_paras,
        "abstract_issues": abstract_issues, "missing": missing,
        "refs": refs, "units": units, "title": title, "title_issues": title_issues,
    }


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def fmt_hits(hits, limit=6):
    lines = []
    items = sorted(hits.items(), key=lambda kv: -len(kv[1]))
    for pat, occ in items:
        label = occ[0][1]
        locs = ", ".join(f"L{ln}" for ln, _, _ in occ[:limit])
        more = f" (+{len(occ) - limit} more)" if len(occ) > limit else ""
        lines.append(f"- **{label}** ×{len(occ)} — {locs}{more}")
    return "\n".join(lines) if lines else "- none"


def report(a):
    out = []
    out.append("# Manuscript pre-edit scan\n")
    out.append(f"Words: {a['n_words']} · paragraphs ≥120 chars: {a['n_paras']} · "
               f"sections detected: {', '.join(sorted(a['sections'])) or 'none'}\n")

    verdict = ("full rewrite of prose likely" if a["density_all"] > 12 else
               "substantial editing" if a["density_all"] > 6 else
               "light editing")
    out.append(f"## AI-tell density\n")
    out.append(f"- Tier-1 tells: {a['n_t1']} ({a['density_t1']:.1f}/1000 words)")
    out.append(f"- All tells: {a['n_t1'] + a['n_t2']} ({a['density_all']:.1f}/1000 words) → **{verdict}**")
    out.append(f"- Em dashes: {a['em_dashes']} · 'respectively': {a['respectively']} · "
               f"'significant(ly)': {a['significant']} with {a['stats_words']} statistical markers in the text")
    if a["openers"]:
        op = ", ".join(f"{k} ×{v}" for k, v in a["openers"].most_common())
        out.append(f"- Paragraph openers: {op} (of {a['n_paras']} paragraphs)")
    out.append("")

    out.append("## Title\n")
    out.append(f"> {a['title']}\n")
    out.extend(f"- {t}" for t in a["title_issues"]) if a["title_issues"] else out.append("- no mechanical issues")
    out.append("")

    out.append("## Abstract\n")
    out.extend(f"- {t}" for t in a["abstract_issues"]) if a["abstract_issues"] else out.append("- no mechanical issues")
    out.append("")

    out.append("## Journal-required elements not found\n")
    out.extend(f"- {m}" for m in a["missing"]) if a["missing"] else out.append("- all present")
    out.append("")

    out.append("## Novelty and superlative claims (delete or replace with the specific advance)\n")
    out.append(fmt_hits(a["novelty"]))
    out.append("")
    out.append("## Bare sustainability words (each needs a metric, a comparison, or deletion)\n")
    out.append(fmt_hits(a["sustain"]))
    out.append("")
    out.append("## Tier-1 AI vocabulary\n")
    out.append(fmt_hits(a["tier1"]))
    out.append("")
    out.append("## Tier-2 vocabulary (fine in isolation, a problem in clusters)\n")
    out.append(fmt_hits(a["tier2"], limit=4))
    out.append("")
    out.append("## Empty framing / hedging\n")
    out.append(fmt_hits(a["hedges"]))
    out.append("")

    out.append("## Units and number style\n")
    if a["units"]:
        seen = set()
        for ln, tok, msg in a["units"]:
            key = (tok, msg)
            if key in seen:
                continue
            seen.add(key)
            out.append(f"- L{ln} `{tok}` → {msg}")
    else:
        out.append("- none detected")
    out.append("")

    out.append("## References\n")
    r = a["refs"]
    if not r.get("present"):
        out.append("- no References section found")
    else:
        out.append(f"- {r['count']} entries · styles detected: {r['styles']}")
        if len([k for k in r["styles"] if k != "unclassified"]) > 1:
            out.append("- **mixed citation styles** — convert all to ACS format (see references/acs-style.md)")
        out.append(f"- entries without DOI: {r['without_doi']} (ACS asks for DOIs where they exist)")
        if r["with_et_al"]:
            out.append(f"- entries using 'et al.': {r['with_et_al']} (ACS lists all authors; 'et al.' only after 10 if the journal allows)")
    out.append("")
    out.append("_Hits are prompts for judgment, not errors. Check each in context._")
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    text = load_text(path)
    a = analyse(text)
    if "--json" in sys.argv:
        serialisable = {k: v for k, v in a.items() if k not in {"tier1", "tier2", "novelty", "sustain", "hedges"}}
        serialisable["openers"] = dict(a["openers"])
        for k in ("tier1", "tier2", "novelty", "sustain", "hedges"):
            serialisable[k] = {pat: [(ln, tok) for ln, tok, _ in occ] for pat, occ in a[k].items()}
        print(json.dumps(serialisable, indent=2, default=str))
    else:
        print(report(a))


if __name__ == "__main__":
    main()
