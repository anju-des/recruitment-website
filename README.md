# Recruitment website

The Mira / Wisemonk Recruit marketing page — a single scroll-driven page.

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8080
```

## What's on the page

The page is one long scroll. Every change of ground is driven by the same
scroll-linked "sky" ramp rather than per-section backgrounds, so the
transitions never show a seam:

| | |
|---|---|
| **Hero** | heading, subcopy and the portal's "describe a role" composer |
| **Statement** | three lines that whiten one at a time while the screen holds still |
| **Logos** | eight glass tiles that drift in and then fall toward the chat |
| **Mira at work** | a black chat window that centres, plays its thread, then is joined by two more |
| **Stages** | Screening · Interview · Scorecard · Offer, on a rail; the frame pins and the scroll changes the stage |
| **Close** | a sphere of light opens on the Mira mark, the loop unwinds, three lines land |

## Testing environment

Pages serves one branch from one root, so the test environment is a folder on
the same site rather than a second deployment:

| | |
|---|---|
| live | https://anju-des.github.io/recruitment-website/ |
| preview | https://anju-des.github.io/recruitment-website/preview/ |

```bash
python build/publish.py ../EOR/docs --preview   # put a draft in preview/
python build/publish.py --promote               # preview/ -> live
python build/publish.py ../EOR/docs             # straight to live
```

The preview is a self-contained copy, not a page sharing the parent's assets —
git stores identical blobs once, and a copy cannot break on a path rewrite the
way a shared one can. It carries a small fixed "Preview" marker in the corner
so a tab is never mistaken for the live one; `--promote` strips it.

## How to change it

**Don't hand-edit `index.html`** — it is generated, and it's 150KB of one file.

`build/build_recruitment_page.py` is the source of truth. It holds the markup
(`CONTENT`) and the styles (`EXTRA_CSS`), and writes the page out. Edit the
builder, run it, copy the result over `index.html`.

`build/patches/` holds the 95 scripts the builder was changed by, one per
revision. Each one asserts on the text it expects to find before replacing it,
so a patch applied against a builder that has moved on fails loudly rather than
corrupting it. They are history, not a pipeline — you don't re-run them.

Two notes on the builder:

- Its output path is absolute to the machine it was written on
  (`…/MCP/EOR/docs/recruitment-copy.html`). Point it wherever you like.
- The page was built by patching the builder with small guarded scripts rather
  than editing it by hand, which is why the comments read the way they do.

## Conventions worth knowing before you touch the scroll code

- **Measure progress from normal-flow geometry only** — never from an element
  that is itself pinned or transformed. Three separate bugs came from that.
- `html, body { overflow-x: clip }`, not `hidden`. `hidden` creates a scroll
  container and breaks every `position: sticky` section on the page.
- Bands are plain `clamp((scroll − start) / span)` ramps written into CSS
  custom properties from one `requestAnimationFrame`-batched scroll handler.

## Design system

This page deliberately sits **outside** the Wisemonk product design system: it
uses Geist rather than Satoshi, and a violet palette rather than the portal
blue. The shared `wisemonk-ui.js` is included for the composer's behaviour
only. The linter will flag the fonts and colours here; that is expected.

## Assets

`assets-source/mira-mark.svg` is the Mira mark the closing animation is drawn
from. The page inlines it as a data URI inside the SVG that masks the metallic
gradient, so the file is kept here as the source it came from rather than as
something the page fetches.


`face-candidate.png` and `face-interviewer.png` are photographs supplied for
the interview panel. Check the licence before this page goes anywhere public.
