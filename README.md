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

## How to change it

**Don't hand-edit `index.html`** — it is generated, and it's 150KB of one file.

`build/build_recruitment_page.py` is the source of truth. It holds the markup
(`CONTENT`) and the styles (`EXTRA_CSS`), and writes the page out. Edit the
builder, run it, copy the result over `index.html`.

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

`face-candidate.png` and `face-interviewer.png` are photographs supplied for
the interview panel. Check the licence before this page goes anywhere public.
