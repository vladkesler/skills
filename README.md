# skills

Agent Skills for preparing research papers for specific journals. Each folder is a self-contained skill: a `SKILL.md` with the workflow, `references/` with the journal requirements and editing guides, and an optional `scripts/` checker that the assistant runs by itself.

| Skill | For |
|---|---|
| [`matter-advmat-afm-carbpol-manuscript-editor`](matter-advmat-afm-carbpol-manuscript-editor/) | Four journals: *Matter* (Cell Press), *Advanced Materials* and *Advanced Functional Materials* (Wiley), and *Carbohydrate Polymers* (Elsevier). Fit verdict, edited manuscript in the journal's layout, the journal's own pieces (Matter: Highlights, eTOC blurb, Progress and potential, MAP level; Advanced Materials and AFM: ToC text; Carbohydrate Polymers: hypothesis statement, polysaccharide characterization check, graphical-abstract layout), cover letter, to-do list, checklist. |
| [`acs-sce-manuscript-editor`](acs-sce-manuscript-editor/) | *ACS Sustainable Chemistry & Engineering*. Edited manuscript in ACS style, sustainability-claim check, change log, author queries. |

The folder name lists the journals a skill covers: `matter` = Matter, `advmat` = Advanced Materials, `afm` = Advanced Functional Materials, `carbpol` = Carbohydrate Polymers, `acs-sce` = ACS Sustainable Chemistry & Engineering. The four-journal skill was called `matter-afm-manuscript-editor` before Advanced Materials was added; if you installed it under that name, remove it and install this one.

## Using a skill

Once installed, open a chat, attach the paper as a Word file or paste its text, and write what you want in plain words, for example:

> Get this paper ready for Matter.

> Get this paper ready for Advanced Materials.

> Is this ready for Advanced Functional Materials? Fix what you can.

> Make this paper ready for Carbohydrate Polymers.

> Which suits this paper best: Matter, Advanced Materials, AFM or Carbohydrate Polymers?

Nothing else needs to be set up, and you never need to run anything yourself. The reply starts with a verdict and a numbered list of what is still needed from you, followed by the edited paper.

## Install in Claude (claude.ai or the desktop app)

1. Make a zip of the skill folder: download this repository (green **Code** button, **Download ZIP**), unzip it, then zip the single folder `matter-advmat-afm-carbpol-manuscript-editor` so that the folder itself is the top level of the zip.
2. In Claude, open **Settings**, find **Skills** (under Capabilities or Customize, depending on the version), and upload the zip.
3. Make sure code execution and file creation are switched on in the same settings area, so Claude can run the checker and hand back a Word file.

In Claude Code, copy the folder into `~/.claude/skills/`.

## Install in ChatGPT (website or desktop app)

Checked against OpenAI's help pages on 15 Nov 2026. The desktop app has the same menus as the website; if a step looks different there, do the setup once at chatgpt.com, and the project then appears in the desktop app as well.

**As a Project** (every plan):

1. In the sidebar choose **New project** and give it a name, for example "Journal paper editor".
2. Open the project's **•••** menu, choose **Project settings**, and paste the whole of [`matter-advmat-afm-carbpol-manuscript-editor/chatgpt/instructions.md`](matter-advmat-afm-carbpol-manuscript-editor/chatgpt/instructions.md) into the instructions box. The file is kept under 8,000 characters.
3. Add these eight files to the project: the seven files in `matter-advmat-afm-carbpol-manuscript-editor/references/` and `matter-advmat-afm-carbpol-manuscript-editor/scripts/manuscript_check.py`. If ChatGPT will not take the `.py` file, leave it out; the assistant then does the same checks by reading.
4. For each paper, start a new chat inside the project, attach the Word file or paste the text, and say which journal.

On the Free plan a project holds five files. Upload `audience-and-fit.md`, `deliverable-templates.md`, `materials-claims.md`, `ai-tells-scientific.md` and the one requirements file for your journal (`matter-requirements.md`, `wiley-advanced-requirements.md` for Advanced Materials and AFM, or `carbpol-requirements.md`).

**As a Skill** (ChatGPT Business, Enterprise, Edu and Healthcare workspaces, where the administrator allows skill uploads): in the sidebar choose **Plugins**, open the **Skills** tab, choose **Create**, then **Upload from your computer**, and pick the same zip as for Claude. ChatGPT scans the upload before it becomes available. If the upload is refused, use a Project.

**Not as a custom GPT.** OpenAI retires custom GPTs on 11 Dec 2026. If you already built one for an earlier version of this skill, move it into a Project as above.

## Keeping the journal rules current

The requirements in each skill are dated and quote the journals' own author guidelines. Journals revise these pages. Each skill tells the author to look at the live page before submitting; if you notice a rule has changed, update the `references/*-requirements.md` file and its date.
