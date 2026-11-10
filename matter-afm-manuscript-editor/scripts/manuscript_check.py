#!/usr/bin/env python3
"""
manuscript_check.py - mechanical pre-edit scan for drafts aimed at Matter (Cell Press),
Advanced Functional Materials (Wiley) or Carbohydrate Polymers (Elsevier).

Usage (python3; plain "python" also works where it exists):
    python3 manuscript_check.py <manuscript.docx|.md|.txt> --journal matter|afm|carbpol [--json]
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
      Carbohydrate Polymers: abstract <= 200 words, 3-6 keywords, text <= 8,000 words
              excluding references, about 15 figures and tables, optional Highlights
              (3-5 of <= 85 characters each)
  * Journal elements that appear to be missing, split into "needed at first submission"
    and "needed by revision" (Carbohydrate Polymers needs everything at first submission)
  * Journal style slips (citation form, section names, figure callouts, spelling)
  * Carbohydrate Polymers only: a named polysaccharide in the title, scope prompts, the
    characterization the journal's guideline asks for each polysaccharide found in the
    text, and a cross-check of author-year citations against the reference list
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
    "carbpol": {
        "name": "Carbohydrate Polymers (Elsevier)",
        "abstract_label": "Abstract",
        "abstract_max": 200,
        "keywords": (3, 6),
        "body_typical": None,
        "text_max": 8000,       # words of text, excluding references
        "display_max": 15,      # figures + tables, "generally not more than"
        # No free-format first submission: everything is needed at once.
        "required": [
            ("Abstract (200 words max)", r"^\W*abstract\b", NOW),
            ("Keywords (3 to 6)", r"^\W*keywords?\b", NOW),
            ("Introduction (numbered section 1)", r"^\W*(\d[\d.]*\s+)?introduction\b", NOW),
            ("A hypothesis statement (the journal asks for one, normally at the end of the Introduction)",
             r"hypothes[ei]s|hypothesi[sz]ed?", NOW),
            ("Materials and methods, in the main text directly after the Introduction",
             r"^\W*(\d[\d.]*\s+)?(materials? and methods|experimental|methods)\b", NOW),
            ("Conclusions", r"^\W*(\d[\d.]*\s+)?conclusions?\b", NOW),
            ("Corresponding author's email on the title page", r"[\w.+-]+@[\w-]+\.[\w.-]+", NOW),
            ("CRediT authorship contribution statement (required)",
             r"credit author|author(ship)? contributions?|contribution statement", NOW),
            ("Declaration of competing interest (statement from Elsevier's declarations tool)",
             r"declaration of (competing )?interests?|competing interests?|conflicts? of interest", NOW),
            ("Data availability (repository link, or why the data cannot be shared)", r"data availability", NOW),
            ("Funding statement", r"^\W*funding\b|was supported by|grant numbers?|did not receive any specific grant|financial support", NOW),
            ("References", r"^\W*(\d[\d.]*\s+)?references\b", NOW),
        ],
    },
}

JOURNAL_ALIASES = {
    "advanced functional materials": "afm", "adfm": "afm", "adv funct mater": "afm",
    "carbohydrate polymers": "carbpol", "carbohydr polym": "carbpol", "carbohydr. polym.": "carbpol",
    "carbpolym": "carbpol", "cp": "carbpol", "carp": "carbpol",
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
    ("methods", r"experimental(?: section| procedures)?|materials? and methods|methods"),
    ("resource", r"resource availability"),
    ("ack", r"acknowledge?ments?"),
    ("contrib", r"credit authorship contribution statement|author contributions?"),
    ("interests", r"declaration of (?:competing )?interests?|conflicts? of interest|competing interests?"),
    ("ai", r"declaration of generative ai[^\n]*"),
    ("dataavail", r"data availability(?: statement)?|data and code availability"),
    ("funding", r"funding(?: sources?)?"),
    ("si", r"supporting information|supplemental information|supplementary (?:information|materials?|data)"
           r"|appendix a\.? supplementary (?:data|materials?)"),
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

# Carbohydrate Polymers accepts British or American English, not a mixture. Two classes are
# compared separately, because "-ize" with "colour" (Oxford spelling) is consistent British.
SPELL_IZE = {
    "British": [BRITISH[0], BRITISH[1]],
    "American": [r"\b(%s)(e|ed|es|ing|ation|ations|er|ers)\b" % "|".join(st[:-1] + "z" for st in BRITISH_IS.split("|")),
                 r"\b(analyz|catalyz|hydrolyz|paralyz)(e|ed|es|ing|er|ers)\b"],
}
SPELL_OTHER = {
    "British": [r"\bcolour\w*\b", r"\bbehaviour\w*\b", r"\bfavour\w*\b", r"\bvapours?\b", r"\bfibres?\b",
                r"\bcentr(e|es|ed)\b", r"\bmodell(ing|ed)\b", r"\blabell(ing|ed)\b", r"\baluminium\b"],
    "American": [r"\bcolor(?!imet)\w*\b", r"\bbehavior\w*\b", r"\bfavor\w*\b", r"\bvapors?\b", r"\bfibers?\b",
                 r"\bcenter(s|ed)?\b", r"\bmodel(ing|ed)\b", r"\blabel(ing|ed)\b", r"\baluminum\b"],
}

# Named carbohydrate polymers (Carbohydrate Polymers wants one in the title and as the subject).
NAMED_GLYCANS = (
    r"(?:nano|micro)?cellulos\w*|hemicellulos\w*|chitosan\w*|(?:nano)?chitin\w*|starch\w*|amylose|amylopectin|"
    r"alginat\w*|alginic|pectin\w*|(?:arabino)?xylan\w*|xyloglucan\w*|(?:gluco|galacto)?mannan\w*|"
    r"glucan\w*|dextran\w*|(?:cyclo|malto)?dextrin\w*|pullulan\w*|hyaluron\w+|carrageenan\w*|agar|agarose|"
    r"xanthan|gellan|curdlan|scleroglucan|schizophyllan|levan|inulin|fructan\w*|fucoidan\w*|ulvan\w*|"
    r"laminarin\w*|heparin\w*|chondroitin|glycosaminoglycan\w*|guar|konjac|gum arabic|locust bean gum|"
    r"glycogen|(?:arabino)?galactan\w*|lentinan|exopolysaccharide\w*|lipopolysaccharide\w*|peptidoglycan\w*"
)
NAMED_GLYCAN_RE = re.compile(r"\b(?:%s)\b" % NAMED_GLYCANS, re.IGNORECASE)

NANOCELLULOSE = (r"nanocellulose|cellulose nano(?:crystal|fib|whisker)\w*|nanofibrillated cellulose|"
                 r"microfibrillated cellulose|cellulose microfib\w*|(?-i:\bCNCs?\b|\bCNFs?\b|\bMFC\b|\bTOCNs?\b)")
# (polymer label, pattern that shows the polymer is used, pattern that shows the item is reported, the item)
# from the journal's guideline "Characterization of carbohydrates and related products" (26 Aug 2024).
GLYCAN_ITEMS = [
    ("alginate", r"\balginat\w*|\balginic", r"M/G|G/M|guluron|mannuron|(?-i:\bF[_ ]?G\b)|G[- ]block|G residues|G content",
     "the fraction of G residues (F_G) or the M/G ratio"),
    ("pectin", r"\bpectin\w*", r"esterif|methoxyl|(?-i:\bDE\b|\bDM\b)", "the degree of methyl esterification"),
    ("pectin", r"\bpectin\w*", r"galacturonic", "the galacturonic acid content"),
    ("chitosan", r"\bchitosan\w*", r"deacetylat|degree of acetylation|(?-i:\bDDA?\b|\bDA\b|\bF_?A\b)", "the degree of deacetylation"),
    ("xanthan gum", r"\bxanthan", r"pyruv", "the degree of pyruvylation and of acetylation"),
    ("red seaweed galactan (agar, agarose, carrageenan)", r"\bcarrageenan\w*|\bagar\b|\bagarose\b",
     r"anhydrogalactose|sul(?:f|ph)ate content|degree of sul(?:f|ph)ation", "the ratio galactose : 3,6-anhydrogalactose : sulfate"),
    ("sulfated glycan (heparin, chondroitin sulfate, fucoidan, ulvan ...)",
     r"\bheparin\w*|\bchondroitin|\bfucoidan\w*|\bulvan\w*|\bdermatan|\bkeratan|sul(?:f|ph)ated polysaccharide",
     r"degree of sul(?:f|ph)ation|sul(?:f|ph)ate content|sul(?:f|ph)ation degree", "the degree of sulfation"),
    ("nanocellulose", NANOCELLULOSE, r"(?-i:\bAFM\b|\bTEM\b)|atomic force|transmission electron",
     "both lateral and longitudinal dimensions from AFM or TEM (a DLS size is not enough)"),
    ("nanocellulose", NANOCELLULOSE,
     r"charge density|surface charge|conductometric|charge content|carboxyl(?:ate)? content|sul(?:f|ph)ate half[- ]ester|[mµu]mol\s?/?\s?k?g\b|[mµu]mol k?g",
     "the surface charge type and density, or number of charged groups, and the counter-ion (zeta potential alone is not enough)"),
    ("nanochitin", r"nanochitin|chitin nano(?:crystal|fib|whisker)\w*", r"(?-i:\bAFM\b|\bTEM\b)|atomic force|transmission electron",
     "both lateral and longitudinal dimensions from AFM or TEM"),
    ("cellulose derivative (ester or ether)",
     r"carboxymethyl ?cellulose|cellulose acetate|hydroxypropyl ?(?:methyl ?)?cellulose|hydroxyethyl ?cellulose|"
     r"methyl ?cellulose|ethyl ?cellulose|cellulose (?:ether|ester)s?|(?-i:\bCMC\b|\bHPMC\b|\bHPC\b|\bHEC\b)",
     r"degree of substitution|substitution degree|molar substitution|(?-i:\bDS\b|\bMS\b)",
     "the nature and degree of substitution (DS; MS for hydroxyalkyl ethers)"),
    ("starch", r"\bstarch\w*", r"amylose", "the amylose content (with botanical source and purity)"),
]

# Words that can stand before a year without being an author name.
CITE_STOP = {
    "in", "since", "during", "until", "from", "by", "after", "before", "between", "on", "at", "to", "for", "with",
    "and", "the", "of", "about", "around", "circa", "late", "early", "mid", "year", "years", "figure", "fig", "table",
    "scheme", "section", "eq", "equation", "iso", "astm", "tappi", "din", "version", "origin", "matlab", "excel",
    "spss", "office", "windows", "standard", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december", "china", "usa", "germany", "japan", "india",
    "brazil", "france", "sweden", "finland", "canada", "sigma", "aldrich", "merck", "accessed", "retrieved",
    "al", "et", "no", "ca", "model", "type", "grade", "over", "under", "than",
}
AUTHOR_YEAR_RE = re.compile(
    r"(?P<a>[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+)(?:\s+et\s+al\.?|\s+(?:&|and)\s+[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+)?,?\s*\(?(?P<y>(?:19|20)\d{2})[a-z]?\b"
)

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
        if not rest and len(line.strip()) > 90 and key != "ai":
            continue  # too long for a heading (the AI-declaration heading is the one long exception)
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
        elif journal == "carbpol":
            notes = []
            if not NAMED_GLYCAN_RE.search(title):
                if re.search(r"(?i)polysaccharide|carbohydrate|biopolymer|glycan", title):
                    notes.append("the title speaks of a polysaccharide in general terms; the journal wants the carbohydrate polymer named (e.g. chitosan, cellulose nanocrystals)")
                else:
                    notes.append("no named carbohydrate polymer in the title; the journal requires one to be the main focus of the paper and its title")
            abbr = [w for w in re.findall(r"\b[A-Z][A-Z0-9]{1,}s?\b", title) if w not in ("DNA", "RNA", "NMR", "UV", "II", "III", "IV")]
            if abbr and not title.isupper():
                notes.append("abbreviation in the title (%s): avoid unless established and widely understood" % ", ".join(sorted(set(abbr))))
            if re.search(r"[₀-₉]|=|[A-Z][a-z]?\d", title):
                notes.append("formula in the title: avoid where possible")
            if tw > 25:
                notes.append("long: the guide asks for a concise title")
            rows.append(("Title", "%d characters, %d words" % (tc, tw), "concise; names the carbohydrate polymer; no uncommon abbreviations or formulae",
                         "check" if notes else "ok", "; ".join(notes) or title))
            out_scope = re.findall(r"(?i)\blignin\w*|\bpoly\(?lactic acid\)?|\bpolylactide\b|(?-i:\bPLA\b|\bPHAs?\b|\bPHB\b)|\bpolyhydroxy(?:alkanoate|butyrate)s?\b"
                                   r"|\bbiochar\b|\bchars?\b|\bcarboni[sz]ed\b|\bactivated carbon\b|\bcarbon (?:dots?|aerogels?)\b", title)
            if out_scope:
                rows.append(("Title scope", ", ".join(sorted(set(w.lower() for w in out_scope))),
                             "the journal lists polyalkanoates, polylactic acid, lignin and chars as not of interest", "check",
                             "the carbohydrate polymer must be the subject, with these at most in a supporting role"))
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
            rows.append((label + " citations", "contains reference citations",
                         "avoid; if one is essential, give authors and year" if journal == "carbpol" else "none allowed", "FIX", ""))
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
        if journal == "carbpol":
            joined = [k.strip() for k in re.split(r",\s+|;|\n", first_para) if re.search(r"(?i)\b(and|of)\b", k)]
            if joined:
                rows.append(("Keyword form", "%d joined with 'and' or 'of'" % len(joined), "avoid multi-word keywords using 'and' or 'of'",
                             "check", "; ".join(joined)))

    if journal == "carbpol":
        if not pieces_only:
            ts = text_stats(lines, headings)
            rows.append(("Text length", "%d words outside the reference list" % ts["text_words"],
                         "<= %d words excluding references" % prof["text_max"],
                         "OVER" if ts["text_words"] > prof["text_max"] else "ok",
                         "the guide does not say whether abstract, captions and tables count; this count includes them"))
            rows.append(("Figures and tables", "%d numbered items cited" % ts["display_items"],
                         "generally <= %d in total" % prof["display_max"],
                         "check" if ts["display_items"] > prof["display_max"] else "ok",
                         "move the least essential to the supplementary material (not the methods)" if ts["display_items"] > prof["display_max"] else ""))
        hl, _ = section_text(lines, headings, "highlights")
        if hl is not None:
            items = bullets(hl)
            rows.append(("Highlights count (optional piece)", str(len(items)), "3 to 5", "ok" if 3 <= len(items) <= 5 else "FIX", ""))
            for j, it in enumerate(items, 1):
                rows.append(("Highlight %d" % j, "%d characters" % len(it), "<= 85 characters incl. spaces", "ok" if len(it) <= 85 else "OVER", it))
    elif journal == "matter":
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


def display_items(body):
    """Distinct numbered figures, schemes and tables cited (Fig. S1 and Table A.1 do not count)."""
    kinds = set(re.findall(r"\b((?:Figure|Fig\.?|Scheme|Table)\s+\d+)", body))
    return len(set(re.sub(r"\s+", " ", re.sub(r"Fig(?:ure|\.)?", "Figure", k)) for k in kinds))


def body_stats(journal, lines, headings):
    keys = {k: i for i, k, _ in reversed(headings)}
    start = keys.get("introduction", 0)
    end = keys.get("references", len(lines))
    if end <= start:
        end = len(lines)
    body = "\n".join(lines[start:end])
    return {"body_words": n_words(body), "display_items": display_items(body), "typical": PROFILES[journal]["body_typical"]}


def split_references(lines, headings):
    """(text outside the reference list, reference-list text or None)."""
    for idx, (i, k, rest) in enumerate(headings):
        if k == "references":
            end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
            return "\n".join(lines[:i] + lines[end:]), "\n".join(([rest] if rest else []) + lines[i + 1:end])
    return "\n".join(lines), None


def text_stats(lines, headings):
    """Carbohydrate Polymers counts 'words of text (excluding references)'."""
    outside, _ = split_references(lines, headings)
    return {"text_words": n_words(outside), "display_items": display_items(outside)}


def missing_elements(journal, text):
    out = {NOW: [], LATER: []}
    for label, pat, stage in PROFILES[journal]["required"]:
        if not re.search(pat, text, re.IGNORECASE | re.MULTILINE):
            out[stage].append(label)
    return out


def spelling_mix(text):
    """Carbohydrate Polymers: British or American English, not both. Returns a note or None."""
    def hits(patterns):
        found = []
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                if not BRITISH_FALSE.match(m.group(0)):
                    found.append(m.group(0).lower())
        return found
    brit, amer, mixed = [], [], False
    for group in (SPELL_IZE, SPELL_OTHER):
        b, a = hits(group["British"]), hits(group["American"])
        mixed = mixed or bool(b and a)
        brit += b
        amer += a
    if not mixed:
        return None
    note = ("mixed spelling: %d British forms (%s) and %d American forms (%s). The journal accepts either variety, not a mixture; "
            % (len(brit), ", ".join(sorted(set(brit))[:6]), len(amer), ", ".join(sorted(set(amer))[:6])))
    if len(brit) == len(amer):
        return note + "keep the variety the author uses in the rest of the text"
    majority, few = ("British", amer) if len(brit) > len(amer) else ("American", brit)
    return note + "the draft is mostly %s, so change the others (%s)" % (majority, ", ".join(sorted(set(few))[:8]))


def style_checks(journal, text, lines, headings):
    notes = []
    body, _refs = split_references(lines, headings)
    bracket = len(re.findall(r"\[\d+(?:\s?[-–,]\s?\d+)*\]", body))
    author_year = len(re.findall(r"\([A-Z][A-Za-z-]+(?: et al\.| and [A-Z][A-Za-z-]+| & [A-Z][A-Za-z-]+)?,? (?:19|20)\d{2}[a-z]?[;)]", text))
    numbered = [l.strip() for l in lines
                if re.match(r"^\s*(?:#+\s*)?(?:\*\*|__)?\s*\d+(?:\.\d+)*\.?\s+[A-Z][A-Za-z ,&()/-]{2,70}?(?:\*\*|__)?\s*$", l)]
    fig_abbr = len(re.findall(r"\bFigs?\.\s?S?\d", text))
    fig_full = len(re.findall(r"\bFigures?\s+S?\d", text))
    upper_panel = len(re.findall(r"\bFig(?:ure|\.)?\s?\d+[A-H]\b", text))
    lower_panel = len(re.findall(r"\bFig(?:ure|\.)?\s?\d+[a-h]\b", text))
    keys = [k for _, k, _ in headings]
    # recognised section headings that carry a number ("2. Materials and methods"); address lines do not count
    numbered_main = [i for i, _, _ in headings
                     if re.match(r"^\s*(?:#+\s*)?(?:\*\*|__)?\s*\d+(?:\.\d+)*\.?\s+\S", lines[i])]

    if journal == "carbpol":
        if bracket:
            notes.append("%d numbered citations like [12]: the journal uses author–year citations in APA style, e.g. (Surname et al., 2021); "
                         "convert them from the author's own reference list" % bracket)
        if not numbered_main and len(headings) >= 4:
            notes.append("section headings are not numbered: the guide asks for numbered sections (1., 1.1, 1.1.1); the abstract is not numbered")
        first = {}
        for i, k, _ in headings:
            first.setdefault(k, i)
        if "methods" in first:
            after = [k for k in ("results", "conclusion") if k in first and first[k] < first["methods"]]
            if after:
                notes.append("the methods section comes after the %s: the journal wants Materials and methods in the main text "
                             "immediately after the Introduction" % " and ".join("Results" if k == "results" else "Conclusions" for k in after))
        if re.search(r"(?i)(?:method|procedure|protocol|experimental detail)s?[^.\n]{0,60}(?:supplementary|supporting|supplemental)|"
                     r"(?:supplementary|supporting|supplemental)[^.\n]{0,40}(?:method|experimental section)", text):
            notes.append("methods appear to be placed in the supplementary material: the journal wants them in the main body")
        if fig_abbr and fig_full:
            notes.append("mixed callouts: %d 'Fig.' and %d 'Figure'. The guide does not prescribe one; the journal prints 'Fig. 1', so use that throughout"
                         % (fig_abbr, fig_full))
        elif fig_full:
            notes.append("%d callouts written 'Figure': not an error (the guide is silent), but the journal prints 'Fig. 1'" % fig_full)
        if re.search(r"(?i)supporting information|supplemental information", text):
            notes.append("'Supporting/Supplemental Information': Elsevier's term is 'Supplementary material'")
        pdi = re.findall(r"(?i)polydispersity(?: index)?|(?-i:\bPDI\b)", text)
        if pdi:
            notes.append("%d uses of 'polydispersity (index)' or 'PDI': the journal's characterization guideline asks for 'dispersity (Đ)'" % len(pdi))
        interval = re.findall(r"\b\d+(?:[.,]\d+)?\s?(?:–|-|—|to)\s?\d+(?:[.,]\d+)?\s?(?:kDa|kg/mol|kg mol|g/mol|g mol|Da)\b", text)
        if interval:
            notes.append("molecular weight given as an interval (%s): the guideline does not accept intervals; give the value with its method and the type of average"
                         % ", ".join(sorted(set(interval))[:4]))
        mix = spelling_mix(body)
        if mix:
            notes.append(mix)
        if not bracket and not author_year and len(headings) >= 3:
            notes.append("no citations recognised in the text: they are missing, or were superscript numbers lost in pasting")
        scope = []
        if re.search(r"(?i)\bcyclodextrin", text) and re.search(r"(?i)inclusion complex", text):
            scope.append("a drug complexed with a single cyclodextrin is on the not-of-interest list")
        if re.search(r"(?i)\bbiochar\b|\bcarboni[sz]ation\b|\bpyrolys[ei]s\b|\bactivated carbon\b", text):
            scope.append("chars made from polysaccharides are on the not-of-interest list, whatever their application")
        if re.search(r"(?i)\bextraction yield", text) and not re.search(r"(?i)molecular weight|monosaccharide composition", text):
            scope.append("extraction yields without characterization of the extracted polysaccharide are on the not-of-interest list")
        for s in scope:
            notes.append("scope: " + s + " (check the role this plays in the paper)")
    else:
        if author_year:
            notes.append("%d author–year citations: Matter and AFM use numbered citations in order of first appearance" % author_year)
        if fig_abbr:
            notes.append("%d uses of 'Fig.': write 'Figure' in full" % fig_abbr)
    if journal == "matter":
        if bracket:
            notes.append("%d bracketed citations like [12]: Matter uses superscript numbers (keep the numbering, change the form)" % bracket)
        if numbered_main:
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
    elif journal == "afm":
        if not numbered_main and len(headings) >= 4:
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
    if journal != "carbpol" and named and not bracket and not author_year and flat_cite < 2:
        notes.append("%d 'Name et al.' mentions but no reference numbers in the text: citations are missing or were lost in pasting" % named)
    if re.search(r"(?i)\bproprietary\b|\bconfidential\b|\btrade secret\b|\bundisclosed\b", text):
        notes.append("a material is described as proprietary/undisclosed: every composition must be given"
                     + (" (AFM may return such papers without review)" if journal == "afm" else " for the work to be reproducible"))
    if re.search(r"(?i)\bvolunteers?\b|\bparticipants?\b|\bpanell?ists?\b|\bhuman subjects?\b|\bwearer\b|\bon (?:the|a) (?:human )?(?:skin|finger|wrist|throat|arm|hand)\b", text) \
            and not re.search(r"(?i)ethic|informed consent|institutional review|\bIRB\b|helsinki", text):
        notes.append("tests on a person are described but there is no ethics-approval and informed-consent statement (required by all three journals, including for wearable-sensor tests and sensory panels)")

    if journal != "carbpol":
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
            notes.append("%d British spellings (%s): Matter and AFM ask for American English" % (len(brit), ex))
    return notes


def characterization_prompts(text, lines):
    """Carbohydrate Polymers: what the journal's characterization guideline asks for each polysaccharide in the text."""
    def has(pat):
        return re.search(pat, text, re.IGNORECASE) is not None
    out = []
    found = sorted(set(m.group(0).lower() for m in NAMED_GLYCAN_RE.finditer(text)))
    if not found:
        return ["no named carbohydrate polymer recognised in the text: the journal publishes work whose main subject is one"]
    out.append("carbohydrate polymers named in the text: %s" % ", ".join(found[:12]))
    if not has(r"molecular weight|molar mass|(?-i:\bM[wnv]\b)|\bkDa\b|g/mol|g mol|intrinsic viscosity|degree of polymeri[sz]ation"):
        out.append("MISSING? molecular weight: required for every polysaccharide, with the method, the units and the type of average")
    else:
        if not has(r"(?-i:\bM[wnv]\b)|weight[- ]average|number[- ]average|viscosity[- ]average"):
            out.append("molecular weight is mentioned without the type of average (Mw, Mn, Mv)")
        if not has(r"(?-i:\bSEC\b|\bGPC\b|\bMALS\b)|size[- ]exclusion|gel permeation|(?<!dynamic )light scattering|viscomet|intrinsic viscosity|Mark[–-]Houwink|osmomet|MALDI"):
            out.append("molecular weight is mentioned without the method used to determine it")
        if has(r"(?<!dynamic )light scattering|(?-i:\bMALS\b)") and not has(r"dn/dc|refractive index increment"):
            out.append("light scattering is used: give the dn/dc value")
    if not has(r"\bpurity\b|carbohydrate content|ash content|protein content|moisture content"):
        out.append("MISSING? purity (e.g. total carbohydrate content and the share of each monosaccharide residue)")
    if has(r"purchased|obtained from|supplied by|bought from|provided by|procured from|(?-i:Sigma|Aldrich|Merck)") \
            and not has(r"catalog(?:ue)?|cat\. ?no|product (?:no|number|code)|\blot\b|\bbatch\b"):
        out.append("a supplier is named without a catalogue code: required for purchased polysaccharides")
    for label, used, reported, item in GLYCAN_ITEMS:
        if has(used) and not has(reported):
            out.append("MISSING? %s: %s" % (label, item))
    if has(NANOCELLULOSE) and has(r"(?-i:\bDLS\b)|dynamic light scattering|zeta[- ]potential"):
        out.append("nanocellulose with DLS or zeta potential: the journal accepts neither on its own for dimensions or charge")
    weak = []
    for i, line in enumerate(lines, 1):
        if re.search(r"(?i)(?:FT-?IR|infrared|\bUV\b|\bSEM\b|\bTEM\b)[^.]{0,100}(?:confirm|prov|verif|demonstrat|reveal)\w*[^.]{0,60}structure", line):
            weak.append(i)
    if weak:
        out.append("structure claim resting on FT-IR, UV or microscopy at %s: not accepted as proof of fine structure (FT-IR is accepted as qualitative evidence of a modification)"
                   % ", ".join("L%d" % i for i in weak[:6]))
    return out


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


def cross_check(refs, body):
    """Author-year citations against the reference list, both directions (Carbohydrate Polymers)."""
    cited = {}
    for m in AUTHOR_YEAR_RE.finditer(body):
        a, y = m.group("a"), m.group("y")
        if a.lower() in CITE_STOP or len(a) < 2:
            continue
        cited.setdefault((a, y), 0)
        cited[(a, y)] += 1
    if len(cited) < 3:
        return None  # the text does not use author-year citations (yet)
    low = [r.lower() for r in refs]
    not_listed = sorted("%s %s" % (a, y) for (a, y) in cited
                        if not any(a.lower() in r and y in r for r in low))
    not_cited = []
    for r in refs:
        m = re.match(r"\W*(?:\[?\d+[\].)]\s*)?([A-Za-zÀ-ÿ'’\- ]+?),", r)
        y = re.search(r"\(((?:19|20)\d{2})[a-z]?\)", r)
        if not m or not y:
            continue
        tok = m.group(1).split()[-1]
        if not re.search(re.escape(tok) + r"[^;\n]{0,70}?" + y.group(1), body):
            not_cited.append("%s %s" % (m.group(1).strip(), y.group(1)))
    return {"n_citations": len(cited), "not_listed": not_listed, "not_cited": not_cited}


def check_references(lines, headings, journal="matter"):
    text, start = section_text(lines, headings, "references")
    if text is None:
        return {"present": False}
    refs = [l.strip() for l in text.splitlines() if l.strip()]
    extra = {}
    if journal == "carbpol":
        numbered = sum(1 for r in refs if re.match(r"^\[?\d+[\].)]\s", r))
        surnames = []
        for r in refs:
            m = re.match(r"\W*(?:\[?\d+[\].)]\s*)?([A-Za-zÀ-ÿ'’\-]+)", r)
            surnames.append(m.group(1).casefold() if m else "")
        breaks = [(surnames[i - 1], surnames[i]) for i in range(1, len(surnames)) if surnames[i] and surnames[i] < surnames[i - 1]]
        apa_like = sum(1 for r in refs if re.search(r"\((?:19|20)\d{2}[a-z]?\)\.", r))
        if apa_like < len(refs) / 2:
            breaks = []  # entries do not start with the surname, so their order cannot be judged
        body, _ = split_references(lines, headings)
        extra = {"numbered_entries": numbered, "order_breaks": len(breaks),
                 "first_break": "'%s' is listed after '%s'" % (breaks[0][1], breaks[0][0]) if breaks else "",
                 "no_year": sum(1 for r in refs if not re.search(r"\((?:19|20)\d{2}[a-z]?\)", r)),
                 "cross": cross_check(refs, body)}
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
    out = {"present": True, "count": len(refs), "styles": dict(styles), "without_doi": no_doi,
           "compound": compound, "with_et_al": et_al}
    out.update(extra)
    return out


def analyse(text, journal):
    text, n_markers = strip_markers(text)
    lines = text.splitlines()
    headings = find_headings(lines)
    total = max(1, n_words(text))
    # The AI-use declaration is the publisher's fixed sentence: leave it out of the prose scan.
    prose = list(lines)
    empty = []
    labels = {"methods": "Methods", "ack": "Acknowledgements", "contrib": "Author contributions / CRediT statement",
              "interests": "Declaration of interests", "dataavail": "Data availability", "funding": "Funding",
              "resource": "Resource availability", "si": "Supplementary / supporting information",
              "toc": "Table of Contents text", "abstract": "Abstract", "keywords": "Keywords"}
    for idx, (i, k, rest) in enumerate(headings):
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        if k == "ai":
            for j in range(i, end):
                prose[j] = ""
        elif k in labels and not rest.strip() and not "".join(lines[i + 1:end]).strip() and labels[k] not in empty:
            empty.append(labels[k])
    t1, t2 = find_all(AI_TIER1, prose), find_all(AI_TIER2, prose)
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
        "key": journal,
        "charact": characterization_prompts(split_references(lines, headings)[0], lines) if journal == "carbpol" else [],
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
        "novelty": find_all(NOVELTY, prose),
        "bare": find_all(BARE_CLAIMS, prose),
        "frames": find_all(EMPTY_FRAMES, prose),
        "chatbot": find_all(CHATBOT_STRINGS, prose),
        "n_t1": n1, "n_t2": n2,
        "density": 1000.0 * (n1 + n2) / total,
        "em_dashes": text.count("—"),
        "significant": len(re.findall(r"\bsignificant(ly)?\b", text, re.IGNORECASE)),
        "stats_markers": len(re.findall(r"\b[pP]\s*[<=>]\s*0?\.\d+|\bANOVA\b|\bt[- ]test\b|standard deviation|±|\bn\s*=\s*\d", text)),
        "openers": dict(openers), "n_paras": len(paras),
        "empty_sections": empty,
        "units": unit_checks(lines),
        "refs": check_references(lines, headings, journal),
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
    o.append("# Manuscript scan for %s\n" % a["journal"])
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
    carb = a["key"] == "carbpol"
    if carb:
        o.append("\n- This journal has no free-format first submission: the limits above apply to the first version.")
    else:
        o.append("\n- Main text (Introduction to References): about %d words, %d numbered display items cited. Typical for this journal: %d–%d words%s. No hard limit; length must be justified by the science."
                 % (b["body_words"], b["display_items"], b["typical"][0], b["typical"][1],
                    ", 3–8 display items" if a["key"] == "afm" else ""))
    o.append("")

    o.append("## Elements not found\n")
    o.append("_If you were given only part of a paper, ignore the items that belong to sections you have not seen._\n")
    for stage in (NOW, LATER):
        if carb and stage == LATER:
            continue  # everything is needed at first submission
        o.append("**%s:**" % stage.capitalize())
        o.extend("- %s" % m for m in a["missing"][stage]) if a["missing"][stage] else o.append("- all found")
        o.append("")
    if a["empty_sections"]:
        o.append("**Headings present but empty apart from [AUTHOR: ...] markers (still to be filled in):** %s\n" % "; ".join(a["empty_sections"]))
    if carb:
        o.append("**Cannot be seen in the text; remind the author:** page numbers and continuous line numbers; the graphical abstract "
                 "(separate file, required at submission); each figure also as a separate file; the Word file from Elsevier's declarations tool; "
                 "data deposited in a repository.\n")
        o.append("## Polysaccharide characterization (the journal's guideline; editors may not send the paper to review without it)\n")
        o.extend("- %s" % c for c in a["charact"])
        o.append("- _'MISSING?' means the usual words for the item were not found; confirm by reading the Materials section. Never supply a value yourself._")
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
        if a["key"] == "matter":
            o.append("- Matter format: Surname, I., and Surname, I. (Year). Title. J. Abbrev. vol, pages. DOI — 'et al.' only after 10 authors")
        elif a["key"] == "afm":
            o.append("- AFM accepts any one consistent style at submission; every entry needs the article title")
        else:
            o.append("- Carbohydrate Polymers format (APA 7th): Surname, A. B., & Surname, C. D. (Year). Title. Full Journal Name, volume, pages. https://doi.org/... — alphabetical by first author, not numbered")
            if r["numbered_entries"] > r["count"] / 2:
                o.append("- **the list is numbered** (%d entries): APA lists are alphabetical and unnumbered; convert the in-text numbers to author and year first" % r["numbered_entries"])
            if r["order_breaks"]:
                o.append("- **not in alphabetical order** at %d places; first: %s" % (r["order_breaks"], r["first_break"]))
            if r["no_year"]:
                o.append("- entries not in the APA form 'Surname, A. B. (Year). Title ...': %d" % r["no_year"])
            x = r["cross"]
            if x is None:
                o.append("- fewer than three author–year citations recognised in the text, so citations and list were not cross-checked")
            else:
                o.append("- %d distinct author–year citations recognised in the text" % x["n_citations"])
                if x["not_listed"]:
                    o.append("- **cited in the text but not found in the list** (%d): %s" % (len(x["not_listed"]), "; ".join(x["not_listed"][:10])))
                if x["not_cited"]:
                    o.append("- **in the list but not found cited in the text** (%d): %s" % (len(x["not_cited"]), "; ".join(x["not_cited"][:10])))
                if not x["not_listed"] and not x["not_cited"]:
                    o.append("- every citation has a list entry and every entry is cited")
        o.append("- entries without a DOI: %d" % r["without_doi"])
        if r["compound"] and a["key"] != "carbpol":
            o.append("- %d entries look like compound references (a, b ...): one work per number at Matter and AFM" % r["compound"])
        if r["with_et_al"]:
            rule = {"matter": "Matter lists up to 10 authors before 'et al.'",
                    "afm": "the AFM guide lists all authors, or three then 'et al.' when there are more than six",
                    "carbpol": "APA lists up to 20 authors"}[a["key"]]
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
    journal = JOURNAL_ALIASES.get(journal, journal)
    if journal not in PROFILES:
        print("Give the target journal: --journal matter | afm | carbpol", file=sys.stderr)
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
