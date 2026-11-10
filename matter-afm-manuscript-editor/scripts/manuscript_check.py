#!/usr/bin/env python3
"""
manuscript_check.py - mechanical pre-edit scan for drafts aimed at Matter (Cell Press)
or Advanced Functional Materials (Wiley).

Usage (python3; plain "python" also works where it exists):
    python3 manuscript_check.py <manuscript.docx|.md|.txt> --journal matter|afm [--json]
    python3 manuscript_check.py --count [file]     # characters and words per line (stdin if no file)

Stdlib only (reads .docx through zipfile). The assistant runs this itself when it has a
code tool; the author is never asked to run it. Text pasted into the chat has to be saved
to a temporary .txt file first.

[AUTHOR: ...] markers are left out of every count and check, so the script can be run on
edited text that still contains them. A file that holds only the short pieces (Highlights,
eTOC blurb, Progress and potential, ToC text) is recognised and only those are checked.

What it reports:
  * Counted limits, which are easy to misjudge by eye:
      Matter: title <= 145 characters, Summary <= 150 words, <= 10 keywords, <= 4 Highlights
              of <= 85 characters each, eTOC blurb <= 50 words, Progress and potential
              <= 300 words (and <= 1,000 characters on one of the journal's pages)
      AFM:    abstract <= 200 words, 3-7 keywords, ToC text 50-60 words
  * Journal elements that appear to be missing, split into "needed at first submission"
    and "needed by revision"
  * Journal style slips (citation form, section names, figure callouts, British spelling)
  * AI-tell vocabulary, novelty claims and bare property words, with line numbers
  * Unit slips, statistics markers, reference-list consistency

Run it on the original draft to plan the edit, and again on your edited text (or on a
file holding just the Highlights / eTOC blurb / ToC text you drafted) to confirm the
limits before you deliver. Every hit is a prompt for judgment, not a verdict.
"""

import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from xml.etree import ElementTree as ET

# --------------------------------------------------------------------------- #
# Journal profiles
# --------------------------------------------------------------------------- #

NOW, LATER = "needed at first submission", "needed by revision or acceptance"

PROFILES = {
    "matter": {
        "name": "Matter (Cell Press)",
        "abstract_label": "Summary",
        "abstract_max": 150,
        "keywords": (0, 10),
        "body_typical": (5000, 7000),
        "required": [
            ("Summary (the abstract; one paragraph, 150 words max)", r"^\W*(summary|abstract)\b", NOW),
            ("Corresponding author email ('*Correspondence: name@institution')", r"[\w.+-]+@[\w-]+\.[\w.-]+", NOW),
            ("Methods (enough experimental detail to judge the results)", r"^\W*(\d[\d.]*\s+)?(methods|experimental|materials and methods)\b", NOW),
            ("Progress and potential statement", r"progress and potential", NOW),
            ("Proposed MAP level with a short justification", r"(?-i:\bMAP\b)", NOW),
            ("Declaration of interests section (plus the PDF form)", r"declaration of interests?|competing interests?", NOW),
            ("Keywords (up to 10)", r"^\W*keywords?\b", LATER),
            ("Resource availability: Lead contact", r"lead contact", LATER),
            ("Resource availability: Materials availability", r"materials availability", LATER),
            ("Resource availability: Data and code availability", r"data and code availability", LATER),
            ("Acknowledgments (funding)", r"acknowledge?ments?", LATER),
            ("Author contributions (required)", r"author contributions?", LATER),
            ("Supplemental information index (Document S1 ...)", r"supplemental information|document s1", LATER),
            ("Highlights (up to four, 85 characters each)", r"^\W*highlights\b", LATER),
            ("eTOC blurb / In brief (50 words max)", r"etoc|in brief", LATER),
            ("Graphical abstract", r"graphical abstract", LATER),
            ("References", r"^\W*(\d[\d.]*\s+)?references\b", LATER),
        ],
    },
    "afm": {
        "name": "Advanced Functional Materials (Wiley)",
        "abstract_label": "Abstract",
        "abstract_max": 200,
        "keywords": (3, 7),
        "body_typical": (3000, 8000),
        "required": [
            ("Abstract (200 words max, present tense, impersonal)", r"^\W*(abstract|summary)\b", NOW),
            ("Introduction", r"^\W*(\d[\d.]*\s+)?introduction\b", NOW),
            ("Conclusion", r"^\W*(\d[\d.]*\s+)?conclusions?\b", NOW),
            ("Experimental Section / Methods", r"^\W*(\d[\d.]*\s+)?(experimental|methods|materials and methods)\b", NOW),
            ("Corresponding author's institutional email (and an email for every co-author)", r"[\w.+-]+@[\w-]+\.[\w.-]+", NOW),
            ("Data Availability Statement (required)", r"data availability", NOW),
            ("Conflict of Interest statement", r"conflicts? of interest|competing interests?", NOW),
            ("Funding statement / Acknowledgements", r"acknowledge?ments?|funding|grant", NOW),
            ("References", r"^\W*(\d[\d.]*\s+)?references\b", NOW),
            ("Keywords (3 to 7)", r"^\W*keywords?\b", LATER),
            ("'Statistical Analysis' subsection at the end of the Experimental Section", r"statistical analysis", LATER),
            ("Supporting Information line", r"supporting information", LATER),
            ("Table of Contents text (50-60 words)", r"table of contents|\btoc\b", LATER),
        ],
    },
}

# Headings the scanner recognises (group 'name' is the canonical key).
HEADING_NAMES = [
    ("abstract", r"abstract|summary"),
    ("keywords", r"keywords?"),
    ("highlights", r"highlights"),
    ("etoc", r"etoc(?: blurb)?|in brief"),
    ("pandp", r"progress and potential"),
    ("toc", r"table of contents(?: text| entry)?|toc(?: text| entry)?"),
    ("title", r"title"),
    ("introduction", r"introduction"),
    ("results", r"results and discussion|results|discussion"),
    ("conclusion", r"conclusions?"),
    ("methods", r"experimental(?: section| procedures)?|materials and methods|methods"),
    ("resource", r"resource availability"),
    ("ack", r"acknowledge?ments?"),
    ("contrib", r"author contributions?"),
    ("interests", r"declaration of interests?|conflicts? of interest|competing interests?"),
    ("ai", r"declaration of generative ai[^\n]*"),
    ("dataavail", r"data availability(?: statement)?|data and code availability"),
    ("si", r"supporting information|supplemental information|supplementary (?:information|material)"),
    ("legends", r"figure (?:titles and )?legends|figure captions"),
    ("references", r"references"),
]
HEADING_RE = re.compile(
    r"^\s*(?:#+\s*)?(?:\*\*|__)?\s*(?:\d+(?:\.\d+)*\.?\s+)?(?P<name>"
    + "|".join("(?P<%s>%s)" % (key, pat) for key, pat in HEADING_NAMES)
    + r")\s*(?:\*\*|__)?\s*(?P<colon>[:.])?\s*(?:\*\*|__)?\s*(?P<rest>.*)$",
    re.IGNORECASE,
)

# --------------------------------------------------------------------------- #
# Word lists (see references/ai-tells-scientific.md for the reasoning)
# --------------------------------------------------------------------------- #

AI_TIER1 = [
    r"\bdelv(e|es|ed|ing)\b", r"\brealm\b", r"\btapestry\b", r"\blandscape\b",
    r"\bpivotal\b", r"\bcrucial\b", r"\bvital\b", r"\bparamount\b",
    r"\bunderscor(e|es|ed|ing)\b", r"\bshowcas(e|es|ed|ing)\b",
    r"\bmeticulous(ly)?\b", r"\bintricate\b", r"\bmultifaceted\b",
    r"\bpav(e|es|ed|ing) the way\b", r"\bholds? great promise\b",
    r"\bgarnered\b", r"\bunlock(s|ed|ing)?\b", r"\bharness(es|ed|ing)?\b",
    r"\bleverag(e|es|ed|ing)\b", r"\bsynerg(y|istic|istically)\b",
    r"\bgame[- ]chang(er|ing)\b", r"\bgroundbreaking\b", r"\bnext[- ]generation\b",
    r"\bpromising (candidate|avenue|platform|alternative|solution|strategy)\b",
    r"\bvaluable insights?\b", r"\bnew insights? into\b", r"\bshed(s)? (new )?light on\b",
    r"\bin the (context|realm|field) of\b",
    r"\bplays? an? (crucial|vital|pivotal|key|important|significant) role\b",
    r"\b(tremendous|considerable|increasing|extensive) (attention|interest)\b",
    r"\bgreat potential\b", r"\bopens? (up )?(new )?(avenues|opportunities|possibilities)\b",
    r"\bbridg(e|es|ing) the gap\b", r"\bnew paradigm\b",
]
AI_TIER2 = [
    r"\brobust\b", r"\bcomprehensive(ly)?\b", r"\bholistic\b", r"\bfoster(s|ed|ing)?\b",
    r"\bfacilitat(e|es|ed|ing)\b", r"\butiliz(e|es|ed|ing|ation)\b",
    r"\bnotably\b", r"\bimportantly\b", r"\binterestingly\b", r"\bremarkabl(e|y)\b",
    r"\bsignificantly (enhanc|improv|increas)\w*\b",
    r"\bhighly (efficient|effective|promising|attractive|desirable)\b",
    r"\bexcellent\b", r"\boutstanding\b", r"\bsuperior\b", r"\bdramatic(ally)?\b",
    r"\bin order to\b", r"\bit is worth (noting|mentioning)\b", r"\bit should be noted\b",
    r"\bnot only\b.*\bbut also\b", r"\bfurthermore\b", r"\bmoreover\b", r"\badditionally\b",
    r"\bwidely (regarded|believed|recognized|accepted|studied)\b",
    r"\bnumerous studies\b", r"\bvarious (studies|strategies|approaches|methods)\b",
    r"\bextensive(ly)? (efforts|studied|investigated)\b",
    r"\bindispensable\b", r"\bever[- ]increasing\b", r"\burgent need\b",
    r"\baddress(es|ed|ing)? (these|this|the) (challenge|issue|problem)s?\b",
    r"\bstate[- ]of[- ]the[- ]art\b", r"\bversatile\b", r"\bmultifunctional\b", r"\bsmart\b",
    r"\bideal candidate\b", r"\bsystematically (investigated|studied)\b",
]
NOVELTY = [
    r"\bnovel\b", r"\bfor the first time\b", r"\bfirst (report|example|demonstration)\b",
    r"\bunprecedented\b", r"\bto the best of our knowledge\b", r"\bfacile\b",
    r"\bsuccessfully\b", r"\bherein\b", r"\bultra[- ]?(strong|tough|stretchable|high|low|fast|thin|light)\w*\b",
    r"\bsuper[- ]?(tough|strong|stretchable|elastic)\w*\b",
]
BARE_CLAIMS = [
    r"\bgreen\b", r"\bsustainab(le|ility)\b", r"\beco[- ]friendly\b",
    r"\benvironmentally (friendly|benign)\b", r"\bbiodegradab(le|ility)\b", r"\bcompostab(le|ility)\b",
    r"\brecyclab(le|ility)\b", r"\bbio[- ]?based\b", r"\brenewable\b", r"\bnon[- ]?toxic\b",
    r"\bbiocompatib(le|ility)\b", r"\blow[- ]cost\b", r"\bcost[- ]effective\b", r"\bscalab(le|ility)\b",
]
EMPTY_FRAMES = [
    r"\bit (was|is|can be|has been) (found|observed|shown|demonstrated|noted|seen) that\b",
    r"\bit is (clear|evident|obvious|apparent|well known) that\b",
    r"\bas (can be|is) (seen|shown|observed)\b", r"\bit can be (seen|concluded|observed)\b",
    r"\bmay be (due|attributed) to\b", r"\bcan be attributed to\b", r"\bas expected\b",
    r"\bas mentioned (above|earlier|before)\b",
]
CHATBOT_STRINGS = [
    r"as an ai language model", r"as of my last (knowledge )?update", r"regenerate response",
    r"\bcertainly[!,] here (is|are)\b", r"i hope this helps",
]

BRITISH_IS = ("characteris|optimis|utilis|polymeris|crystallis|functionalis|organis|realis|minimis|"
              "maximis|stabilis|visualis|summaris|normalis|neutralis|oxidis|ionis|localis|immobilis|"
              "emphasis|recognis|generalis|standardis|solubilis|mineralis|plasticis|homogenis|"
              "magnetis|polaris|sensitis|categoris|prioritis|customis|miniaturis|commercialis|"
              "industrialis|valoris|synthesis")
BRITISH = [
    r"\b(%s)(e|ed|es|ing|ation|ations|er|ers)\b" % BRITISH_IS,
    r"\b(analys|catalys|hydrolys|paralys)(e|ed|ing|er|ers)\b",
    r"\bcolour\w*\b", r"\bbehaviour\w*\b", r"\bfavour\w*\b", r"\bvapour\w*\b",
    r"\bfibres?\b", r"\bcentr(e|es|ed)\b", r"\bmodell(ing|ed)\b", r"\blabell(ing|ed)\b",
    r"\bsulph\w+\b", r"\baluminium\b", r"\bgrey\b", r"\bmould\w*\b", r"\bprogramme\b",
    r"\bwhilst\b", r"\bamongst\b", r"\bageing\b", r"\bmetres?\b", r"\blitres?\b",
]
# Words the patterns above could catch that are also correct American English.
BRITISH_FALSE = re.compile(r"^(syntheses|emphases|analyses|hydrolyses)$", re.IGNORECASE)

UNIT_PATTERNS = [
    (r"\b\d+(\.\d+)?(mg|kg|g|mL|ml|µL|uL|L|mmol|mol|nm|µm|um|mm|cm|rpm|MPa|kPa|GPa|Pa|min|h|mV|mA|kW|MJ|kJ|Hz|kHz)\b",
     "space between number and unit ('2 g', '50 mL')"),
    (r"\b\d+(\.\d+)?\s*ml\b", "'ml' should be 'mL'"),
    (r"(?<![A-Za-z])hrs?\b", "'h' is the unit symbol for hours"),
    (r"(?<![A-Za-z])mins\b", "'min' is the unit symbol for minutes"),
    (r"(?<![A-Za-z])secs?\b", "'s' is the unit symbol for seconds"),
    (r"\b(cm|m|g|mol|kg|s|K|L|mL)-[1-3]\b", "flattened exponent: write as a superscript (cm⁻¹, g⁻¹); usually lost when pasting from Word"),
    (r"\b\d+(\.\d+)?\s*-\s*\d+(\.\d+)?\s*(°C|h|min|%|nm|µm|mm|mL|g|kg|MPa|wt)", "ranges take an en dash without spaces ('40–60 °C')"),
    (r"\b\d+\s*x\s*\d+", "use the multiplication sign × ('5 × 10³')"),
]
SLASH_UNITS = re.compile(
    r"(?<![A-Za-z/])(?:µ|u|m|k|M|G|n)?(?:g|L|mol|m|S|A|V|W|J|N|Pa|F|Wh|Ah)\s?/\s?(?:c|m|k|µ|u|n)?(?:g|L|mol|m|s|h|min|K)(?:2|3|²|³)?(?![A-Za-z/])"
)

# [AUTHOR: ...] markers are the editor's queries, not manuscript text (one level of nested [] allowed).
MARKER_RE = re.compile(r"\[AUTHOR\b(?:[^\[\]]|\[[^\[\]]*\])*\]", re.DOTALL)


# --------------------------------------------------------------------------- #
# Input
# --------------------------------------------------------------------------- #

def read_docx(path):
    """Extract paragraphs from a .docx without python-docx."""
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter("{%s}p" % ns):
        paras.append("".join(t.text or "" for t in p.iter("{%s}t" % ns)))
    return "\n".join(paras)


def load_text(path):
    if path.lower().endswith(".docx"):
        return read_docx(path)
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


ORPHAN_PUNCT = re.compile(r"^[.,;:!?()\[\]\"'“”‘’•*#|-]+$")


def n_words(text):
    """Whitespace-separated tokens, as Word counts them ("=" and "%" count; stray punctuation does not)."""
    return len([t for t in text.split() if not ORPHAN_PUNCT.match(t)])


def strip_markers(text):
    """Remove [AUTHOR: ...] markers, keeping line breaks so line numbers stay valid."""
    n = len(MARKER_RE.findall(text))
    cleaned = MARKER_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return cleaned, n


# --------------------------------------------------------------------------- #
# Structure
# --------------------------------------------------------------------------- #

def find_headings(lines):
    """Return [(line_index, key, inline_rest)] for lines that look like section headings."""
    out = []
    for i, line in enumerate(lines):
        if not line.strip() or len(line) > 4000:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        rest = (m.group("rest") or "").strip()
        key = next(k for k, _ in HEADING_NAMES if m.group(k))
        if rest and not m.group("colon"):
            continue  # "Results show that ..." is a sentence, not a heading
        if not rest and len(line.strip()) > 90:
            continue
        if key == "title" and not rest:
            continue  # a bare "Title" line tells us nothing
        out.append((i, key, rest))
    return out


def section_text(lines, headings, key):
    """Text of the first section with this key (inline remainder + following lines)."""
    for idx, (i, k, rest) in enumerate(headings):
        if k != key:
            continue
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        body = [rest] if rest else []
        body += [l for l in lines[i + 1:end]]
        return "\n".join(body).strip(), i
    return None, None


def detect_title(lines, headings):
    t, _ = section_text(lines, headings, "title")
    if t:
        return t.splitlines()[0].strip()
    first_heading = headings[0][0] if headings else len(lines)
    candidates = [l.strip() for l in lines[:first_heading] if l.strip()]
    # the first line before the abstract that is not a chat message, an author line or an address
    for c in candidates:
        if not 15 <= len(c) <= 300 or c.endswith("?") or "@" in c:
            continue
        if re.match(r"(?i)^\W*(hi|hello|hey|dear|please|here|this is|can you|could you|i |correspond)", c):
            continue
        return re.sub(r"^[#*\s]+|[*\s]+$", "", c)
    return ""


def bullets(text):
    items = []
    for l in text.splitlines():
        s = re.sub(r"^\s*(?:[-•*–·]|\d+[.)])\s*", "", l).strip()
        if s:
            items.append(s)
    return items


# Case-sensitive on purpose: "US" and "(i)" are not first-person words.
FIRST_PERSON = re.compile(r"\b(?:We|we|Our|our|ours|us)\b")


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def find_all(patterns, lines, flags=re.IGNORECASE):
    """Return {matched text (lower case): [(line, text), ...]}; overlapping matches count once (longest wins)."""
    hits = defaultdict(list)
    for i, line in enumerate(lines, 1):
        found = []
        for pat in patterns:
            for m in re.finditer(pat, line, flags):
                found.append((m.start(), m.end(), m.group(0)))
        taken = []
        for start, end, text in sorted(found, key=lambda f: (f[0] - f[1], f[0])):
            if any(start < e and end > s for s, e in taken):
                continue
            taken.append((start, end))
            hits[re.sub(r"\s+", " ", text.lower())].append((i, text))
    return hits


def limits(journal, lines, headings):
    """Counted limits. Returns list of (item, measured, limit, status, note)."""
    prof = PROFILES[journal]
    rows = []
    keys = set(k for _, k, _ in headings)
    pieces_only = not keys & {"abstract", "introduction", "results", "methods", "title"} and bool(keys & {"highlights", "etoc", "pandp", "toc"})

    title = "" if pieces_only else detect_title(lines, headings)
    if pieces_only:
        pass
    elif title:
        tw, tc = n_words(title), len(title)
        if journal == "matter":
            status = "OVER" if tc > 145 else ("long" if tw > 14 else "ok")
            rows.append(("Title", "%d characters, %d words" % (tc, tw), "<= 145 characters; about 10-12 words", status, title))
        else:
            notes = []
            if tw > 20:
                notes.append("long for a descriptive title")
            if re.search(r"[A-Za-z]\d|[₀-₉]|=", title):
                notes.append("avoid formulae in the title (database indexing)")
            rows.append(("Title", "%d characters, %d words" % (tc, tw), "descriptive keywords, Title Case, no formulae", "check" if notes else "ok", "; ".join(notes) or title))
        if re.search(r"(?i)\b(novel|facile|green|sustainable|highly|efficient|enhanced|superior|excellent|first|new)\b", title):
            rows.append(("Title wording", "evaluative word in title", "state what was made or found", "check", title))
    else:
        rows.append(("Title", "not detected", "", "check", ""))

    abstract, _ = section_text(lines, headings, "abstract")
    label = prof["abstract_label"]
    if pieces_only:
        pass
    elif abstract is None:
        rows.append((label, "heading not found", "<= %d words" % prof["abstract_max"], "MISSING", ""))
    else:
        aw = n_words(abstract)
        status = "OVER" if aw > prof["abstract_max"] else "ok"
        rows.append((label, "%d words" % aw, "<= %d words" % prof["abstract_max"], status, ""))
        if re.search(r"\[\d+(?:[-–,]\s?\d+)*\]|\(\w+ et al\.,? \d{4}\)", abstract):
            rows.append((label + " citations", "contains reference citations", "none allowed", "FIX", ""))
        if not re.search(r"\d", abstract):
            rows.append((label + " numbers", "no numbers", "state the key quantitative result", "check", ""))
        if journal == "afm":
            fp = FIRST_PERSON.findall(abstract)
            if fp:
                rows.append(("Abstract voice", "%d first-person words (we/our)" % len(fp), "impersonal, present tense", "FIX", ""))
            past = re.findall(r"\b(?:was|were|exhibited|showed|demonstrated|achieved|reached|found|fabricated|prepared|"
                              r"synthesized|synthesised|developed|displayed|revealed|obtained|increased|decreased|improved|"
                              r"investigated|studied|observed|enabled|retained|maintained)\b", abstract, re.IGNORECASE)
            if len(past) >= 2:
                rows.append(("Abstract tense", "%d past-tense verbs (%s)" % (len(past), ", ".join(sorted(set(w.lower() for w in past))[:5])),
                             "present tense", "check", ""))
        if journal == "matter":
            nov = re.findall(r"(?i)\bnovel\b|\bfirst\b|\bunprecedented\b", abstract)
            if nov:
                rows.append(("Summary novelty claims", ", ".join(sorted(set(w.lower() for w in nov))), "Cell Press discourages 'novel' and 'first'", "FIX", ""))
            if abstract.count("\n\n") >= 1:
                rows.append(("Summary paragraphs", "more than one paragraph", "a single paragraph", "FIX", ""))

    kw, _ = section_text(lines, headings, "keywords")
    lo, hi = prof["keywords"]
    want = "up to %d" % hi if lo == 0 else "%d to %d" % (lo, hi)
    if kw is None and pieces_only:
        pass
    elif kw is None:
        rows.append(("Keywords", "not found", want, "MISSING", ""))
    else:
        first_para = kw.split("\n\n")[0]
        n = len([k for k in re.split(r",\s+|;|\n", first_para) if k.strip()])  # "1,4-butanediol" stays whole
        rows.append(("Keywords", str(n), want, "ok" if lo <= n <= hi else "FIX", ""))

    if journal == "matter":
        hl, _ = section_text(lines, headings, "highlights")
        if hl is not None:
            items = bullets(hl)
            rows.append(("Highlights count", str(len(items)), "<= 4", "ok" if len(items) <= 4 else "OVER", ""))
            for j, it in enumerate(items, 1):
                st = "ok" if len(it) <= 85 else "OVER"
                note = it
                if re.search(r"\b[A-Z]{2,}\b", it):
                    note += "   [possible abbreviation; Highlights should avoid them]"
                rows.append(("Highlight %d" % j, "%d characters" % len(it), "<= 85 characters incl. spaces", st, note))
        et, _ = section_text(lines, headings, "etoc")
        if et is not None:
            w = n_words(et)
            protected = re.sub(r"\b(et al|e\.g|i\.e|vs|ca|Fig|Dr|Prof)\.", r"\1", et.strip())
            sents = len([s for s in re.split(r"(?<=[.!?])\s+", protected) if s.strip()])
            rows.append(("eTOC blurb", "%d words, %d sentences" % (w, sents), "<= 50 words, 2 sentences", "ok" if w <= 50 else "OVER", ""))
            if FIRST_PERSON.search(et):
                rows.append(("eTOC voice", "first person found", "third person (no we/I)", "FIX", ""))
        pp, _ = section_text(lines, headings, "pandp")
        if pp is not None:
            flat = re.sub(r"\s+", " ", pp).strip()
            w, c = n_words(flat), len(flat)
            st = "OVER" if w > 300 else ("over 1,000 chars" if c > 1000 else "ok")
            rows.append(("Progress and potential", "%d words, %d characters" % (w, c),
                         "<= 300 words; one journal page adds <= 1,000 characters incl. spaces", st, ""))
    else:
        toc, _ = section_text(lines, headings, "toc")
        if toc is not None:
            w = n_words(toc)
            rows.append(("ToC text", "%d words" % w, "50 to 60 words", "ok" if 50 <= w <= 60 else "FIX", ""))
            if FIRST_PERSON.search(toc):
                rows.append(("ToC voice", "first person found", "third person, general audience", "FIX", ""))
    return rows


def body_stats(journal, lines, headings):
    keys = {k: i for i, k, _ in reversed(headings)}
    start = keys.get("introduction", 0)
    end = keys.get("references", len(lines))
    if end <= start:
        end = len(lines)
    body = "\n".join(lines[start:end])
    kinds = set(re.findall(r"\b((?:Figure|Fig\.?|Scheme|Table)\s+\d+)", body))
    kinds = set(re.sub(r"Fig\.?", "Figure", k) for k in kinds)
    return {"body_words": n_words(body), "display_items": len(kinds), "typical": PROFILES[journal]["body_typical"]}


def missing_elements(journal, text):
    out = {NOW: [], LATER: []}
    for label, pat, stage in PROFILES[journal]["required"]:
        if not re.search(pat, text, re.IGNORECASE | re.MULTILINE):
            out[stage].append(label)
    return out


def style_checks(journal, text, lines, headings):
    notes = []
    bracket = len(re.findall(r"\[\d+(?:\s?[-–,]\s?\d+)*\]", text))
    author_year = len(re.findall(r"\([A-Z][A-Za-z-]+(?: et al\.| and [A-Z][A-Za-z-]+)?,? (?:19|20)\d{2}[a-z]?\)", text))
    numbered = [l.strip() for l in lines
                if re.match(r"^\s*(?:#+\s*)?(?:\*\*|__)?\s*\d+(?:\.\d+)*\.?\s+[A-Z][A-Za-z ,&()/-]{2,70}?(?:\*\*|__)?\s*$", l)]
    fig_abbr = len(re.findall(r"\bFigs?\.\s?S?\d", text))
    upper_panel = len(re.findall(r"\bFig(?:ure|\.)?\s?\d+[A-H]\b", text))
    lower_panel = len(re.findall(r"\bFig(?:ure|\.)?\s?\d+[a-h]\b", text))
    keys = [k for _, k, _ in headings]

    if author_year:
        notes.append("%d author–year citations: both journals use numbered citations in order of first appearance" % author_year)
    if fig_abbr:
        notes.append("%d uses of 'Fig.': write 'Figure' in full" % fig_abbr)
    if journal == "matter":
        if bracket:
            notes.append("%d bracketed citations like [12]: Matter uses superscript numbers (keep the numbering, change the form)" % bracket)
        if numbered:
            notes.append("%d numbered section headings: Matter headings are not numbered" % len(numbered))
        if "conclusion" in keys:
            notes.append("a 'Conclusion' section: Matter's order is Introduction, Results, Discussion, Methods; fold the conclusions into the end of the Discussion")
        if re.search(r"(?i)supporting information|supplementary (information|material)", text):
            notes.append("'Supporting/Supplementary Information': the Cell Press term is 'supplemental information' (Figure S1, Document S1)")
        if re.search(r"(?im)^\W*(\d[\d.]*\s+)?experimental section\b", text):
            notes.append("'Experimental Section' heading: Matter calls it 'Methods'")
        if lower_panel and lower_panel >= upper_panel:
            notes.append("%d lower-case panel callouts (Figure 2a): Cell Press figures use capital panel letters (Figure 2A)" % lower_panel)
        if re.search(r"(?i)\backnowledgements\b", text):
            notes.append("'Acknowledgements': US spelling 'Acknowledgments' at Cell Press")
    else:
        if not numbered and len(headings) >= 4:
            notes.append("section headings are not numbered: the AFM template numbers them (1. Introduction, 2. Results and Discussion, 3. Conclusion, 4. Experimental Section)")
        if re.search(r"(?i)supplemental information|supplementary information", text):
            notes.append("'Supplemental/Supplementary Information': the Wiley term is 'Supporting Information'")
        if upper_panel and upper_panel > lower_panel:
            notes.append("%d capital panel callouts (Figure 2A): AFM labels panels with lower-case letters (Figure 2a)" % upper_panel)
        slash = SLASH_UNITS.findall(text)
        if slash:
            ex = ", ".join(sorted(set(s.strip() for s in slash))[:6])
            notes.append("%d units written with a slash (%s): the guide asks for negative exponents (mg mL⁻¹, S cm⁻¹)" % (len(slash), ex))
        if re.search(r"(?i)statistical analysis", text) is None and re.search(r"(?i)\bsignificant", text):
            notes.append("'significant' is used but there is no 'Statistical Analysis' subsection")

    flat_formula = re.findall(r"\b(?:CO2|O2|H2O2?|N2|H2|NH3|CH4|SO2|NO2|H2SO4|HNO3|H3PO4|TiO2|SiO2|Al2O3|Fe3O4|Fe2O3|"
                              r"CaCO3|Na2SO4|NaHCO3|K2CO3|MoS2|CaCl2|ZnCl2|FeCl3|D2O|CDCl3)\b", text)
    flat_exp = re.findall(r"(?<![A-Za-z])(?:mm|cm|µm|nm|m)[23]\b", text)
    if flat_formula or flat_exp:
        ex = ", ".join(sorted(set(flat_formula + flat_exp))[:8])
        notes.append("%d formulae or units with plain digits (%s): subscripts and superscripts were probably lost in pasting; restore them (CO₂, m³)"
                     % (len(flat_formula) + len(flat_exp), ex))
    named = len(re.findall(r"\b[A-Z][a-z]+ et al\.", text))
    flat_cite = len(re.findall(r"[a-z]{3,}[.,]?\d{1,3}(?:[,–-]\d{1,3})*(?=[\s.,;)]|$)", text))
    if named and not bracket and not author_year and flat_cite < 2:
        notes.append("%d 'Name et al.' mentions but no reference numbers in the text: citations are missing or were lost in pasting" % named)
    if re.search(r"(?i)\bproprietary\b|\bconfidential\b|\btrade secret\b|\bundisclosed\b", text):
        notes.append("a material is described as proprietary/undisclosed: every composition must be given"
                     + (" (AFM may return such papers without review)" if journal == "afm" else " for the work to be reproducible"))
    if re.search(r"(?i)\bvolunteers?\b|\bparticipants?\b|\bhuman subjects?\b|\bwearer\b|\bon (?:the|a) (?:human )?(?:skin|finger|wrist|throat|arm|hand)\b", text) \
            and not re.search(r"(?i)ethic|informed consent|institutional review|\bIRB\b|helsinki", text):
        notes.append("tests on a person are described but there is no ethics-approval and informed-consent statement (required by both journals, including for wearable-sensor tests)")

    brit = []
    for i, line in enumerate(lines, 1):
        for pat in BRITISH:
            for m in re.finditer(pat, line, re.IGNORECASE):
                w = m.group(0)
                if BRITISH_FALSE.match(w):
                    continue
                brit.append((i, w))
    if brit:
        ex = ", ".join(sorted(set(w.lower() for _, w in brit))[:10])
        notes.append("%d British spellings (%s): both journals ask for American English" % (len(brit), ex))
    return notes


def unit_checks(lines):
    out = []
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"(\d+(?:\.\d+)?)(\s*)°\s?C", line):
            if m.group(2) != " ":
                out.append((i, m.group(0), "one space between number and °C ('100 °C')"))
        for pat, msg in UNIT_PATTERNS:
            for m in re.finditer(pat, line):
                out.append((i, m.group(0), msg))
    return out


def check_references(lines, headings):
    text, start = section_text(lines, headings, "references")
    if text is None:
        return {"present": False}
    refs = [l.strip() for l in text.splitlines() if l.strip()]
    styles = Counter()
    no_doi = compound = et_al = 0
    for r in refs:
        if re.search(r"no\. \d+ \((?:19|20)\d{2}\):|\((?:19|20)\d{2}\): ?\w+", r):
            styles["journal vol, no. n (year): pages  [Chicago-like, as in the Wiley guide]"] += 1
        elif re.search(r"\d+, \w+[-–]?\w* \((?:19|20)\d{2}\)", r):
            styles["journal vol, pages (year)  [Nature-like]"] += 1
        elif re.search(r"(?:19|20)\d{2}, \d+, \w+", r):
            styles["journal year, vol, page  [ACS / older Wiley-like]"] += 1
        elif re.search(r"(?:19|20)\d{2};\d+", r):
            styles["journal. year;vol:pages  [Vancouver-like]"] += 1
        elif re.search(r"\((?:19|20)\d{2}[a-z]?\)\.\s+\S", r):
            styles["author (year). title. journal vol, pages  [Cell Press / APA-like]"] += 1
        else:
            styles["unclassified"] += 1
        if not re.search(r"doi|10\.\d{4,}/", r, re.IGNORECASE):
            no_doi += 1
        if re.search(r"(?:^|[\s\]])(?:\(?[ab]\))\s", r):
            compound += 1
        if re.search(r"\bet al\b", r):
            et_al += 1
    return {"present": True, "count": len(refs), "styles": dict(styles), "without_doi": no_doi,
            "compound": compound, "with_et_al": et_al}


def analyse(text, journal):
    text, n_markers = strip_markers(text)
    lines = text.splitlines()
    headings = find_headings(lines)
    total = max(1, n_words(text))
    t1, t2 = find_all(AI_TIER1, lines), find_all(AI_TIER2, lines)
    n1 = sum(len(v) for v in t1.values())
    n2 = sum(len(v) for v in t2.values())
    openers = Counter()
    paras = [p.strip() for p in re.split(r"\n", text) if len(p.strip()) > 120]
    for p in paras:
        m = re.match(r"([A-Za-z]+)", p)
        if m and m.group(1).lower() in {"furthermore", "moreover", "additionally", "consequently", "notably",
                                         "importantly", "interestingly", "herein", "overall", "nevertheless"}:
            openers[m.group(1).lower()] += 1
    return {
        "journal": PROFILES[journal]["name"],
        "n_markers": n_markers,
        "n_words": total,
        "sections": sorted(set(k for _, k, _ in headings)),
        "pieces_only": not set(k for _, k, _ in headings) & {"abstract", "introduction", "results", "methods", "title"}
                       and bool(set(k for _, k, _ in headings) & {"highlights", "etoc", "pandp", "toc"}),
        "limits": limits(journal, lines, headings),
        "body": body_stats(journal, lines, headings),
        "missing": missing_elements(journal, text),
        "style": style_checks(journal, text, lines, headings),
        "tier1": t1, "tier2": t2,
        "novelty": find_all(NOVELTY, lines),
        "bare": find_all(BARE_CLAIMS, lines),
        "frames": find_all(EMPTY_FRAMES, lines),
        "chatbot": find_all(CHATBOT_STRINGS, lines),
        "n_t1": n1, "n_t2": n2,
        "density": 1000.0 * (n1 + n2) / total,
        "em_dashes": text.count("—"),
        "significant": len(re.findall(r"\bsignificant(ly)?\b", text, re.IGNORECASE)),
        "stats_markers": len(re.findall(r"\b[pP]\s*[<=>]\s*0?\.\d+|\bANOVA\b|\bt[- ]test\b|standard deviation|±|\bn\s*=\s*\d", text)),
        "openers": dict(openers), "n_paras": len(paras),
        "units": unit_checks(lines),
        "refs": check_references(lines, headings),
    }


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def fmt_hits(hits, limit=6):
    rows = []
    for label, occ in sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        locs = ", ".join("L%d" % ln for ln, _ in occ[:limit])
        more = " (+%d more)" % (len(occ) - limit) if len(occ) > limit else ""
        rows.append("- **%s** ×%d: %s%s" % (label, len(occ), locs, more))
    return "\n".join(rows) if rows else "- none"


def report(a):
    o = []
    o.append("# Pre-edit scan for %s\n" % a["journal"])
    o.append("Words in file: %d · sections recognised: %s" % (a["n_words"], ", ".join(a["sections"]) or "none"))
    o.append("[AUTHOR: ...] markers: %d (left out of every count and check below)\n" % a["n_markers"])

    o.append("## Counted limits\n")
    o.append("| Item | Measured | Limit | Status |")
    o.append("|---|---|---|---|")
    for item, measured, limit, status, note in a["limits"]:
        o.append("| %s | %s | %s | %s |" % (item, measured, limit, status))
    notes = [(i, n) for i, _, _, s, n in a["limits"] if n and s != "ok"]
    for item, note in notes:
        o.append("\n- %s: %s" % (item, note))
    if a["pieces_only"]:
        o.append("\n_This file holds only the journal's short pieces, so nothing else was checked._")
        return "\n".join(o)
    b = a["body"]
    o.append("\n- Main text (Introduction to References): about %d words, %d numbered display items cited. Typical for this journal: %d–%d words%s. No hard limit; length must be justified by the science."
             % (b["body_words"], b["display_items"], b["typical"][0], b["typical"][1],
                ", 3–8 display items" if "Advanced" in a["journal"] else ""))
    o.append("")

    o.append("## Elements not found\n")
    o.append("_If you were given only part of a paper, ignore the items that belong to sections you have not seen._\n")
    for stage in (NOW, LATER):
        o.append("**%s:**" % stage.capitalize())
        o.extend("- %s" % m for m in a["missing"][stage]) if a["missing"][stage] else o.append("- all found")
        o.append("")

    o.append("## Journal style\n")
    o.extend("- %s" % s for s in a["style"]) if a["style"] else o.append("- nothing flagged")
    o.append("")

    verdict = ("heavy rewrite of the prose" if a["density"] > 12 else
               "substantial editing" if a["density"] > 6 else "light editing")
    o.append("## Prose\n")
    o.append("- AI-tell density: %d tier-1 + %d tier-2 hits = %.1f per 1000 words → **%s**" % (a["n_t1"], a["n_t2"], a["density"], verdict))
    o.append("- Em dashes: %d · 'significant(ly)': %d, with %d statistical markers (P values, ±, n =) in the text"
             % (a["em_dashes"], a["significant"], a["stats_markers"]))
    if a["openers"]:
        o.append("- Paragraph openers: %s (of %d paragraphs)" % (", ".join("%s ×%d" % kv for kv in a["openers"].items()), a["n_paras"]))
    if a["chatbot"]:
        o.append("- **Leftover chatbot text found — remove:**\n" + fmt_hits(a["chatbot"]))
    o.append("\n### Novelty and superlative claims (delete, or replace with the comparison)\n" + fmt_hits(a["novelty"]))
    o.append("\n### Bare property and sustainability words (each needs a number, a comparator, or deletion)\n" + fmt_hits(a["bare"]))
    o.append("\n### Tier-1 AI vocabulary\n" + fmt_hits(a["tier1"]))
    o.append("\n### Tier-2 vocabulary (fine alone, a problem in clusters)\n" + fmt_hits(a["tier2"], limit=4))
    o.append("\n### Empty frames\n" + fmt_hits(a["frames"]))
    o.append("")

    o.append("## Units and numbers\n")
    if a["units"]:
        seen = set()
        for ln, tok, msg in a["units"]:
            if (tok, msg) in seen:
                continue
            seen.add((tok, msg))
            o.append("- L%d `%s` → %s" % (ln, tok, msg))
    else:
        o.append("- nothing flagged")
    o.append("")

    o.append("## References\n")
    r = a["refs"]
    if not r.get("present"):
        o.append("- no References section found")
    else:
        o.append("- %d entries · styles detected: %s" % (r["count"], r["styles"]))
        if len([k for k in r["styles"] if k != "unclassified"]) > 1:
            o.append("- **mixed reference styles** — make the list consistent")
        if "Matter" in a["journal"]:
            o.append("- Matter format: Surname, I., and Surname, I. (Year). Title. J. Abbrev. vol, pages. DOI — 'et al.' only after 10 authors")
        else:
            o.append("- AFM accepts any one consistent style at submission; every entry needs the article title")
        o.append("- entries without a DOI: %d" % r["without_doi"])
        if r["compound"]:
            o.append("- %d entries look like compound references (a, b ...): one work per number in both journals" % r["compound"])
        if r["with_et_al"]:
            rule = "Matter lists up to 10 authors before 'et al.'" if "Matter" in a["journal"] else "the AFM guide lists all authors, or three then 'et al.' when there are more than six"
            o.append("- entries using 'et al.': %d (%s; do not add names from memory, ask the author)" % (r["with_et_al"], rule))
    o.append("")
    o.append("_Hits are prompts for judgment, not errors. Check each in context._")
    return "\n".join(o)


def count_mode(text):
    text, n_markers = strip_markers(text)
    rows = ["chars | words | text", "---|---|---"]
    tc = tw = 0
    for line in text.splitlines():
        s = re.sub(r"^\s*(?:[-•*–·]|\d+[.)])\s*", "", line).strip()
        if not s:
            continue
        c, w = len(s), n_words(s)
        tc += c
        tw += w
        rows.append("%d | %d | %s" % (c, w, s if len(s) <= 90 else s[:87] + "..."))
    flat = re.sub(r"\s+", " ", text).strip()
    rows.append("\nWhole text as one paragraph: %d characters (with spaces), %d words" % (len(flat), n_words(flat)))
    if n_markers:
        rows.append("(%d [AUTHOR: ...] markers were left out of the counts)" % n_markers)
    return "\n".join(rows)


def main():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        sys.exit(0 if args else 1)
    if "--count" in args:
        rest = [x for x in args if x != "--count"]
        text = load_text(rest[0]) if rest else sys.stdin.read()
        print(count_mode(text))
        return
    journal = None
    if "--journal" in args:
        i = args.index("--journal")
        if i + 1 < len(args):
            journal = args[i + 1].lower()
            del args[i:i + 2]
    if journal in ("advanced functional materials", "adfm", "adv funct mater"):
        journal = "afm"
    if journal not in PROFILES:
        print("Give the target journal: --journal matter   or   --journal afm", file=sys.stderr)
        sys.exit(2)
    paths = [x for x in args if not x.startswith("--")]
    if not paths:
        print("No manuscript file given.", file=sys.stderr)
        sys.exit(2)
    a = analyse(load_text(paths[0]), journal)
    if "--json" in args:
        for k in ("tier1", "tier2", "novelty", "bare", "frames", "chatbot"):
            a[k] = {label: [ln for ln, _ in occ] for label, occ in a[k].items()}
        print(json.dumps(a, indent=2, default=str, ensure_ascii=False))
    else:
        print(report(a))


if __name__ == "__main__":
    main()
