# Reel "<TITLE>" (9:16) — BUILD SPEC

> Fill this BEFORE montaging. It is the source of truth for the build.
> The audio script + cut are FROZEN once locked (`edit/base.mp4`, `edit/cues.json`): only the
> graphics layer is remounted on top.
> Copy this file into your project's `edit/` dir and fill the angle brackets.

## Global decisions (apply across the whole reel)

- **Brand kit (house style, example — swap for your own):** cream `#FBF7EC` · ink `#1F1B16` ·
  **gold keyword `#F5A623`** · red `#E5484D` · green `#2FA968` · line `#E4DDC9` · dim `#8A8170` ·
  Poppins 400-900.
- **Subtitle keyword = gold `#F5A623`** (white + 8-direction shadow; keyword in gold; fixed y ~1496).
- **Staging:** each beat is a HyperFrames card in one of the staging modes — (1) full-frame cream
  (`.full` + `.kicker`) for message beats · (2) floating card over the face (`.panel` / chip /
  button) · (3) on-face slam stage for content beats. Subtitles run continuously in ALL modes.
- **No handles, no channel badges.**
- **Graphics layer = HyperFrames** (transparent overlay: PNG-sequence packed into a qtrle `.mov`,
  composited over the frozen base). Base + audio = ffmpeg, never touched by HyperFrames.

## Sources / frozen timing

- Frozen base: `edit/base.mp4` (1080×1920, final audio, <DUR>s).
- Word stamps on the output base: transcribe the base with a word-timestamp ASR service (disable any
  keyterm list) → `edit/cues.json`.
- Composition `data-duration` = **<DUR>s**.

## Beat map (spoken beat · window · staging mode · archetype · payoff word)

| # | Act | Beat (spoken) | Window (output timeline) | Staging mode | Archetype (classes) | Payoff word |
|---|-----|---------------|--------------------------|--------------|---------------------|-------------|
| 1 | HOOK | <hook line> | 0.0–<t> | MODE 2 floating | `.panel` + `.chip`/`.strike` | <word> |
| 2 | HOOK | <nice> | <t>–<t> | MODE 1 full card | `.doc` (gold top-border) | <word> |
| 3 | EXPLAINER | <method> | <t>–<t> | MODE 2 floating | `.chip` + `.strike` | <word> |
| 4 | EXPLAINER | <trick> | <t>–<t> | MODE 1 full card | `.big` + `.g` + `.sub` | <word> |
| 5 | EXPLAINER | <html→browser> | <t>–<t> | MODE 2 floating | `.codewin` + browser mock | <word> |
| 6 | EXPLAINER | <download> | <t>–<t> | MODE 2 floating | `.btn` + cursor | <word> |
| 7 | EXPLAINER | <context> | <t>–<t> | MODE 1 full card | `.swatch` + `.chip` | <word> |
| 8 | ENDCARD | <CTA> | <t>–<t> | MODE 2 lower-third | `.pill` + `.plus` | <word> |

> Each beat's reveal is synced to its payoff word. Subtitles run continuously — never suppressed.

## Keywords to highlight in gold

<Claude · skill · HTML · PDF · ...> — refine against `cues.json`.

## Assets / pipeline

- HyperFrames composition from `scaffold/composition.template.html` (house style), in an isolated
  scaffold OUTSIDE your repo; GSAP vendored locally; pin `hyperframes@0.7.17`.
- Render: `npx --yes hyperframes@0.7.17 render . --format png-sequence -o renders/frames --fps 30 --quality high`.
- Composite: `scaffold/compose.sh` (packs the PNG-sequence into a qtrle `.mov`, then composites
  video-over-video).
- PIL subs: `scaffold/build_subs.py` (last step, fixed y, gold keyword, continuous — never
  suppressed).
- Preview-gate per block (base → graphics → composite → subs). Save the composition into `edit/`.
- Fallback: all-PIL pipeline (no scaffold shipped — see SKILL.md, Fallback section, for the shape of that pipeline).
