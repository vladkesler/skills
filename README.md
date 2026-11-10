# skills

Agent Skills for preparing research papers for specific journals. Each folder is a self-contained skill: a `SKILL.md` with the workflow, `references/` with the journal requirements and editing guides, and an optional `scripts/` checker that the assistant runs by itself.

| Skill | For |
|---|---|
| [`matter-afm-manuscript-editor`](matter-afm-manuscript-editor/) | *Matter* (Cell Press) and *Advanced Functional Materials* (Wiley). Fit verdict, edited manuscript in the journal's layout, the journal's short pieces (Highlights, eTOC blurb, Progress and potential, MAP level; ToC text), cover letter, to-do list, checklist. |
| [`acs-sce-manuscript-editor`](acs-sce-manuscript-editor/) | *ACS Sustainable Chemistry & Engineering*. Edited manuscript in ACS style, sustainability-claim check, change log, author queries. |

## Using a skill

Once installed, open a chat, attach the paper as a Word file or paste its text, and write what you want in plain words, for example:

> Get this paper ready for Matter.

> Is this ready for Advanced Functional Materials? Fix what you can.

> Which suits this paper better, Matter or AFM?

Nothing else needs to be set up, and you never need to run anything yourself. The reply starts with a verdict and a numbered list of what is still needed from you, followed by the edited paper.

## Install in Claude (claude.ai or the desktop app)

1. Make a zip of the skill folder: download this repository (green **Code** button, **Download ZIP**), unzip it, then zip the single folder `matter-afm-manuscript-editor` so that the folder itself is the top level of the zip.
2. In Claude, open **Settings**, find **Skills** (under Capabilities or Customize, depending on the version), and upload the zip.
3. Make sure code execution and file creation are switched on in the same settings area, so Claude can run the checker and hand back a Word file.

In Claude Code, copy the folder into `~/.claude/skills/`.

## Install in ChatGPT

**If your workspace has Skills** (a beta feature that reads the same `SKILL.md` format): upload the same zip where ChatGPT lets you add a skill.

**Otherwise, as a custom GPT or a Project:**

1. Create a GPT (**Explore GPTs → Create → Configure**) or a Project.
2. Paste the whole of [`matter-afm-manuscript-editor/chatgpt/instructions.md`](matter-afm-manuscript-editor/chatgpt/instructions.md) into the **Instructions** box. It is under the 8,000-character limit for GPTs.
3. Upload these as knowledge or project files: the six files in `matter-afm-manuscript-editor/references/` and `matter-afm-manuscript-editor/scripts/manuscript_check.py`.
4. Switch on **Code Interpreter & Data Analysis** so it can count lengths and produce a Word file.

## Keeping the journal rules current

The requirements in each skill are dated and quote the journals' own author guidelines. Journals revise these pages. Each skill tells the author to look at the live page before submitting; if you notice a rule has changed, update the `references/*-requirements.md` file and its date.
