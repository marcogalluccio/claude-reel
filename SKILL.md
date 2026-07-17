---
name: video-reel-9x16
description: Use to montage a vertical 9:16 talking-head reel for Instagram/social — a selfie explainer carried by animated graphics cards and a personal brand frame — or to start from a proven reel base and adapt it. Triggers: reel verticale, reel 9:16, video lead-magnet, montaggio reel, "start from the reel base", reel with subtitles and mockups.
---

# video-reel-9x16

A recipe for a vertical lead-magnet reel: a talking-head selfie carried by an animated graphics
layer and a branded frame, ending on a CTA. This skill is the **format + pipeline**; the graphics
layer is built with **HyperFrames**.

## Overview + prerequisites

- **Cut + clean audio** → produce the **frozen base mp4** (1080×1920) BEFORE this pipeline starts.
  Any editor, ffmpeg script, or transcript-based cutting approach works: trim the talk, remove
  filler words, denoise/declip/normalize the voice (an ffmpeg `arnndn`/`highpass`/`loudnorm` chain
  is enough). This skill's job begins AFTER that base exists. HyperFrames never touches the base or
  the audio.
- **Graphics layer** → **HyperFrames CLI** (pinned `hyperframes@0.7.17`), rendered as a
  **PNG-sequence packed into a qtrle `.mov`** (alpha) — see step 3 for why not webm.
- **Subtitles** → PIL (this skill's `scaffold/build_subs.py`).

Support files (load on demand): `references/refinement.md` (multi-direction proposals + per-part
refinement), `references/orchestration.md` (sectional compositions + subagent build),
`references/speed-change.md` (1.05–1.15x recipe).

**Render approach:** this is an **overlay-hybrid render** — a transparent overlay rendered *graphics
only*, composited over a separately-frozen base — plus **PIL subtitles**. The base and audio stay
outside HyperFrames entirely (as opposed to the video-in-composition flow, where the talking-head
clip lives inside the HyperFrames composition).

This is a **base to adapt, not a fixed template.** Work in a per-project `edit/` directory. Heavy
media stays gitignored.

Deliverables are **VERSIONED** (`FINAL_reel.mp4`, then `FINAL_reel_v2.mp4`, …) — never overwrite a
previous FINAL.

## Division of labor

```
cut + clean audio  (any editor / ffmpeg, BEFORE this pipeline)
        │
        ▼
   FROZEN base.mp4  (1080×1920, audio final)   ← HyperFrames never touches this
        │
        ▼
HyperFrames graphics layer  →  PNG-sequence  →  qtrle overlay.mov (alpha)
        │
        ▼
   composite  (ffmpeg overlay, video-over-video)
        │
        ▼
   PIL subtitles applied LAST  →  FINAL.mp4
```

## House-style spec (encode this in every composition)

- **Palette (example — swap for your own brand kit):** cream `#FBF7EC`, cream2 `#F4EFE0`,
  ink `#1F1B16`, dim `#8A8170`, **gold keyword `#F5A623`**, red `#E5484D`, green `#2FA968`,
  line `#E4DDC9`. Font: **Poppins 400–900**.
- **Real content first (the #1 rule):** carry **real, non-sensitive material**, not generic
  CSS mocks — screenshot actual HTML/PDF (proposals, CV, guides) to PNG and embed as
  `<img>`. CSS mocks (`.doc`/`.codewin`) only for the "ugly/before" example. Real brand logos too.
  Sources in **Real content sources** below.
- **Engagement grammar:**
  - Elements enter **BIG and ONE AT A TIME**, each on its spoken word — never a panel that
    assembles all at once.
  - The scene **alternates and overlaps** (a new element slams OVER the previous, pushes it away,
    knocks it down) — it does not "compose" into a static layout.
  - **Static cream panels are demoted:** `.panel`+chips is a residual fallback, not a default.
    Content beats live ON-FACE (mode 3) or in real-content windows (Finder, browser, editor);
    full-frame cream is reserved for message payoffs (mode 1).
  - Payoff = **slam** (`fromTo scale 2→1, back.out(1.4)`) landing exactly on the keyword.
  - When in doubt, show 2-3 directions as mockups first (see **Multiple directions**).
- **Three staging modes:**
  1. **FULL-FRAME cream card** (`.full` + `.kicker` = uppercase gold letter-spaced label) for
     message beats. The cream **enters late**: stay on the face through the rhetorical pivot, then
     fade the cream in (`gsap.fromTo("#cream",{opacity:0},{opacity:1})`). **No corner brackets**
     (`.ticks` are optional and usually dropped). Big, centered title. On exit, HOLD the settled
     content ~1s before fading (a payoff that pops and immediately fades reads as flicker).
  2. **FLOATING card over the live face** (`.panel` = rounded cream card with big shadow, or bare
     chips/buttons) — residual, see Engagement grammar.
  3. **ON-FACE slam stage (default for content beats):** big filled elements (tiles, doc cards,
     windows) in the FREE BANDS (top band y≈80–600, chest y≈1250–1420 — same floor as the filled-box
     rule below), `.onface` text allowed over the face, beams/connectors between elements,
     alternation and collision as the motion language.
- **Filled boxes NEVER in front of the face:** cards, chips and badges with a solid background never
  cover the face; over the face only NON-filled text with heavy shadow (`.onface`) is allowed.
  Reinforcement badges drop to the chest (y ≥ 1250, below the chin, above the subtitle strip).
  Exception only on explicit intent (e.g. the closing CTA on the face) — and even then the CTA never
  covers the EYES or the MOUTH while he speaks: at the CTA's wide field the free top band
  (y ≈ 130–500) holds the whole cluster (pill + comment mock + DM badge) cleanly. The head is NOT at
  a fixed height: it varies ~720–1200 across beats and moves WITHIN a beat (±180px in 3s while
  speaking) → audit per-beat on multiple REAL base frames (worst-case hairline), never with a fixed
  band.
- **Component archetypes** (carry the classes from the template):
  - `.chip` (+ `.ic` colored icon square) + `.strike` (red bar, GSAP `scaleX` 0→1 wipe)
  - `.big` (900, ~120px, `.g` = gold word) + `.sub`
  - `.doc` (white card + `.ln` lines; **gold top-border = "nice" pdf**)
  - `.codewin` (dark window + traffic dots + syntax colors) → browser mock
  - `.btn` (gold "Download as PDF") + cursor
  - `.swatch` palette squares; `.pill` (ink CTA pill) + `.plus` (gold circle)
- **Motion:** a single **paused** GSAP timeline. `power3.out` for enters (fade + y),
  `back.out(1.6–2)` for pops / payoff words, `power2.inOut` for the `.strike` wipe. **Every reveal
  lands on the spoken keyword.**
- **Motion techniques (worked examples, compose freely):**
  - *Typewriter without spans:* monospace text inside a mask span
    (`display:inline-block; overflow:hidden; white-space:pre`), tween `width`
    0→N px with `ease:"steps(<n_chars>)"` (Menlo advance ≈ 0.602em). One tween
    instead of dozens of per-char spans; keep per-char spans for pop-in effects.
  - *SVG stroke-draw:* give the path `pathLength="1"` +
    `stroke-dasharray:1; stroke-dashoffset:1`, tween dashoffset to 0. No path
    measuring. Works for maps, routes, beams, diagrams.
  - *Seek-safe numeric counter:* plain JS object + `onUpdate` writing
    `textContent` — deterministic under the renderer's seeks. This is the ONE
    sanctioned exception to "no other script logic".
  - *Growing container:* tween the window/card `height` as content types in —
    a file that visibly grows sells "the doc is filling up".
- **Subtitles (ALWAYS ON):** Poppins-Bold ~60px, white with **gold keyword**, heavy 8-direction
  black shadow (reads on both face and cream), **fixed y ≈ 1496**, **continuous for the whole video —
  never suppressed, even over cream cards**. Graphic text states the **concept**; subtitles track the
  **spoken words**, so they complement instead of doubling the message.
  **Auto-fit long cues:** if a cue exceeds ~1000px at the base size, scale its font down
  (floor ~40px, baseline unchanged) — `scaffold/build_subs.py` does this automatically.
  **Recommended standard: KARAOKE word-level** — 3-4 words per cue, all white, the SPOKEN word lights
  up gold (using ASR word timestamps). Single-track pipeline: 1 PNG-strip per word-state → concat
  demuxer → qtrle alpha track → **ONE overlay** on the composite (~2 min; an N-chained
  `overlay=enable='between(t,…)'` approach costs ~30 min per render). `scaffold/build_subs.py` ships
  the simple static variant; the karaoke variant follows the same single-track qtrle pattern.

## Plan gates — BEFORE building (what makes the first cut good)

1. **Multiple directions on the load-bearing beats.** For the hook and every beat that carries the
   video, design **2-3 distinct graphic directions** and show them as STATIC mockups (1080×1920 PNG,
   Playwright over REAL base frames, served on `http://127.0.0.1`, one multi-state HTML with a
   `#hash` switch). Pick (or mix); only then build. To judge motion, build short animated demos of
   each direction — in parallel via subagents (`references/orchestration.md`).
   Full flow + mockup scaffold pattern: `references/refinement.md`.
2. **Speed pass.** Ask explicitly at plan time: **1.0x natural or 1.05–1.15x?** Reels often want
   pace; don't leave it buried as an afterthought. The speed change happens at assembly (never on
   the frozen base): full recipe in `references/speed-change.md`.
3. **Per-beat table** (`BUILD-SPEC.template.md`): every reveal anchored to a word timestamp from the
   transcript, staging mode + archetype per beat.

## The hybrid render pattern (5+1 steps) — preview-gate each block

Build in blocks and **show a preview after each; wait for review before the next.**
For the densest beat (real textual content, e.g. a doc shown on screen), produce a STATIC
Playwright mockup over a real base frame and get sign-off on the exact copy BEFORE animating.
**Best review channel: open each preview/mockup in a local player** (Preview/QuickTime;
`open -R` to reveal audio files in Finder) rather than a chat file-send — a chat upload is a
complement for the phone, not the review surface. Chat uploads cap at 30 MiB: for bigger masters
open the file in the player and send a compressed copy in chat if useful.

1. **Cut + clean audio** (any editor / ffmpeg) → a **FROZEN base mp4** (1080×1920). Lock it;
   HyperFrames never touches the base or audio.
   **If the voice "crackles" on peaks, measure the SOURCE before blaming the denoise:**
   `ffmpeg -i src -af "asetnsamples=48000,astats=metadata=1:reset=1,ametadata=mode=print:key=lavfi.astats.Overall.Peak_level:file=peaks.txt" -f null -`
   — per-second peaks at full scale (≥ -0.2 dB) mean the mic clipped at recording and denoise
   will NOT remove the distortion: put `adeclip` as the FIRST filter of the audio chain
   (before highpass/arnndn).
2. **Transcribe the OUTPUT base itself** for output-timeline word stamps. Use a word-timestamp ASR
   service (this pipeline was built against ElevenLabs Scribe). Note: pass **no keyterm list** —
   sending the default keyterm list makes Scribe return HTTP 400, so disable it (`--no-keyterms` or
   the equivalent for your client).
3. **Author the HyperFrames composition** from `scaffold/composition.template.html` (house style).
   Scaffold in an **ISOLATED dir OUTSIDE your repo** (a scratch/tmp dir). **Pin** `hyperframes@0.7.17`.
   **Vendor GSAP LOCALLY** (not CDN). Render **graphics ONLY** as a PNG-sequence, then pack it
   into a lossless alpha `.mov`:
   ```bash
   rm -rf renders/frames   # leftovers from a longer previous render get packed into the tail
   npx --yes hyperframes@0.7.17 render . --format png-sequence -o renders/frames --fps 30 --quality high
   ffmpeg -y -framerate 30 -start_number 1 -i "renders/frames/frame_%06d.png" -c:v qtrle renders/overlay.mov
   ```
   (`scaffold/compose.sh` does the packing + a hard frame-count assert for you.)
   Why not the direct webm: on some machines `--format webm` FLATTENS the alpha (low-memory
   streaming); and feeding the PNGs straight into `overlay` DROPS frames (see Hard gotchas). The
   qtrle mov is the route verified frame-exact. Sanity check after packing:
   `nb_read_frames` of the mov == `data-duration` × fps (±1).
   The CLI looks for **`index.html`** in the dir — any other filename gives "No index.html file
   found" and exits 0 (a SILENT no-op: no overlay produced, no error code)
   (keep `index.html` in the scaffold, or `cp composition.html index.html` before rendering).
   **QA the composition BEFORE the first render** with `scaffold/qa_composition.py` (copy it into
   the scaffold): serves the dir over `http://127.0.0.1`, seeks the timeline at key times
   (`void tl.seek(t)`), emulates beat visibility from `data-start`/`data-duration`, screenshots each
   state. 30 seconds of QA instead of a burned 3-minute render — it catches invisible elements
   (opacity/matrix traps), wrong positions, one-line wraps, face overlaps. Pass the times of every
   payoff moment; read the shots as contact sheets.
4. **Composite** the qtrle overlay.mov over the frozen base, video-over-video (`scaffold/compose.sh`;
   with camera moves, `scaffold/compose_zoom.template.sh` — see **Camera moves** below):
   ```bash
   ffmpeg -y -i base.mp4 -i renders/overlay.mov \
     -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[v]" \
     -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -c:a copy composite.mp4
   ```
   (Legacy webm inputs only: decode with `-c:v libvpx-vp9` or ffmpeg drops the alpha plane.)
5. **PIL subtitles** applied LAST over the composite (`scaffold/build_subs.py`).
6. **SAVE** the filled `composition.html` + `compose.sh` + `build_subs.py` INTO the project's
   `edit/` dir (the scratchpad scaffold is ephemeral) for reproducibility. The bar is: **the FINAL
   must be regenerable from the repo after a reboot.** So save WITH each composition its render
   `assets/` + `fonts/` (gsap.min.js, Poppins, logos — or one shared `_scaffold-kit/` at project
   level), and save EVERY generated script too (assembly, zoom, SFX mix, BGM mix). A section folder
   with only index.html+overlay.mov is NOT re-renderable; an assembly that lives only in chat prose
   has to be reconstructed by hand.

## Camera moves (digital punch-ins) — optional layer, strongest on hooks

The base stays FROZEN on disk; camera moves are baked ONLY into the composite
(re-runnable at will). The numbers below are a worked example, not a mandate —
design the moves around the speech.

- **Where in the pipeline:** inside the composite step, BEFORE the overlay:
  upscale the base 2x (lanczos) → `zoompan` with a piecewise-smoothstep `z`
  expression → overlay the graphics qtrle mov. Graphics stay pinned while the
  footage moves under them (the standard motion-graphics look). Template:
  `scaffold/compose_zoom.template.sh`.
- **A grammar of moves that works:** slow ease-in on the opening hook
  (1.00→1.06 over ~1.7s) · fast push landing WITH a graphic slam or payoff
  word (→1.10-1.12 in ~0.4s) · slow release on a rhetorical reveal · micro
  push on emphasis/shake beats (~1.05) · wide field for the closing CTA.
  Keep subtle beats subtle: staying ≤ 1.12 keeps the moves felt-not-seen.
- **Invisible reset trick:** while a full-frame cream card covers the frame,
  snap the zoom back to 1.00 — the cut is invisible and the face returns to
  a normal field when the card exits.
- **Anchoring:** for a selfie, anchor the crop slightly above center
  (e.g. `y=(ih-ih/zoom)*0.46`, center-x) so the face stays composed.
- **Sync rule:** a camera push lands on the SAME spoken word as the graphic
  it accompanies — two different sync targets read as sloppiness.
- **Release across a cut join masks the jump cut:** place a zoom release (e.g. 1.10→1.00 over
  ~0.7s) so it SPANS the join of a base cut — the continuous motion makes the face jump read as an
  intentional jump cut.
- **Generate, don't hand-write:** build the `z` expression with a `build_zoom.py`-style generator —
  a commented SEGS list (one row per move, anchored to its word) → smoothstep nested ifs → the FULL
  assembly script, with asserts on parenthesis balance and z-continuity between segments.
  Quantitative check that the zoom landed: PSNR before↔after is LOW at push times, HIGH where z=1.00.
- **Speed change (1.05–1.15x): ask at PLAN time, execute at assembly.** Done INSIDE the composite,
  never on the frozen file. Full verified recipe (setpts+fps before zoompan, atempo, SEGS ÷k,
  overlays ÷k in-chain, karaoke `SPEED=k`): `references/speed-change.md`. Key trap: the `fps=30`
  after `setpts` is mandatory — **zoompan discards input PTS and re-stamps frames by index**, so a
  bare `setpts` is a no-op on the video (audio and graphics ahead, lips behind, `-shortest` masks
  it as truncation).

## Audio layers — SFX + BGM

Both are AUDIO-ONLY passes over the finished video master (`-map 0:v -c:v copy`): iterating costs
seconds — never re-encode the video for an audio change. Layer order: video master (assembly, incl.
zoom) → `FINAL_vN+1` = master + SFX → `FINAL_vN+2` = + BGM.

**SFX (sound effects on the graphic beats):**
- **Project library:** collect a set of short, royalty-free effects into `edit/assets/sfx/`.
  Good free sources with commercial-ok, no-attribution licenses: the HyperFrames media library
  (bundled SFX pack), Remotion's sound library
  (`curl -O https://remotion.media/<name>.wav` — whoosh, whip, page-turn, switch, mouse-click,
  shutter-modern/old, ding, error, etc.), plus Mixkit/Pixabay by hand. ~30 sounds cover most beats.
- **Cue map = a table-driven script** (a `build_sfx_mix.py`): one row per cue, each anchored to its
  graphic beat — time = `(section OFF + comp local time) / k`. Per cue:
  `afade=t=in:d=0.005, adelay=<ms>:all=1, volume=<v>`; then ONE
  `amix=inputs=N+1:duration=first:dropout_transition=0:normalize=0, alimiter=limit=0.95`.
  **`normalize=0` is mandatory** — default amix divides by the input count and buries the voice.
  Volumes 0.26–0.55 under the -14 LUFS voice: payoffs 0.5–0.55, whoosh/switch/click 0.35–0.5,
  pops 0.26–0.4. Verify with RMS windows master↔mix: higher at cue times, ≈equal elsewhere.
- **SFX grammar:** payoff slam = a `whoosh` impact (impact-bass tends to read as too heavy — prefer
  a whoosh); ding on notifications + closing CTA; switch on toggles/state flips; whip on strikes and
  fly-offs; mouse-click on cursor taps; pop on element pop-ins; error on warnings; a longer
  cinematic whoosh (atrim ~3.2s + fade-out) under long rises; skip meme sounds unless asked. Full
  map = every graphic beat gets its category, conservative volumes.

**BGM (music bed):**
- Instrumental only, normalized to **-31 LUFS integrated (~17 dB under the voice)**: measure with
  `loudnorm=print_format=json`, gain = −31 − input_i. Fade-in 1s, fade-out 2s at the end. Same
  audio-only pass (a `build_bgm_mix.sh`). Prefer tracks ≥ reel length.
- **Sourcing:** Mixkit — category pages carry parseable JSON-LD (title/artist/genre/duration/direct
  CDN URL) via curl with a browser user-agent; **Pixabay Music is Cloudflare-403 to scripts**.
  Keep a `CREDITS.md` next to the tracks (title, artist, source URL, license). Mixkit Free License
  = commercial ok, no attribution.
- **Taste that works for this format:** light funk / bright synth-pop, groove with drive but never
  aggressive. Plain lo-fi/ambient/piano beds tend to feel too soft under a punchy reel.
- **Choosing = audition, not description:** deliver candidates as clean mp3s (chat + `open -R` in
  Finder) and/or a labeled test bed under the actual reel (see `references/refinement.md` §5);
  remember that a track at full volume feels much stronger than it will at -31 LUFS.

## Security mitigations

HyperFrames pulls and runs npm at render time, so treat it as untrusted code:

- **Isolated scaffold outside your repo** (a scratch/tmp dir), so a compromised package can't read
  the repo.
- **Pin the version** (`hyperframes@0.7.17`) — no floating `@latest`.
- **Never `--expose` / no public bind.**
- **No access to credentials.** A git/CLI auth token on disk (e.g. `~/.config/gh/hosts.yml`) is the
  known supply-chain vector; keep it out of the render's reach.
- **Optional: log out of any CLI credentials before the first render** for max safety, then log back
  in after.
- Requirements: Node v24+, ffmpeg.

## Hard gotchas

- **PNG-sequence straight into `overlay` DROPS frames:** the image2↔mp4 PTS pairing is unreliable —
  a composite frame can lose its ENTIRE overlay (graphics + subs, perceived as a flicker); a
  `fps=30+setpts` "fix" lost 120 frames out of 366. ALWAYS pack the PNGs into a qtrle `.mov`
  first and composite video-over-video (step 3-4). Same rule for the karaoke subs track (already qtrle).
- **Alpha decode (legacy webm only):** if a webm overlay is ever used, decode it with
  `-c:v libvpx-vp9` — ffmpeg's default VP9 decoder drops the alpha → opaque/black overlay. Note:
  on some machines the direct webm render also FLATTENS alpha, hence the png-sequence route.
- **Never animate the beat wrapper `.clip` (inset:0):** scale/rotation on the full-frame wrapper
  pivot around the FRAME CENTER, not the element — cards land ~90px off, texts render at document
  top. Give inner elements their own ids and tween those; wrappers only gate visibility. Corollary:
  `.onface`-style classes need `position:absolute` or their `top/left` are inert.
- **Seek-renderer scale trap:** `.from({scale:>1})` or `keyframes` tweens on the same element leave a
  WRONG settled scale when the renderer seeks (a hook "?" can stick at ~80px instead of 360px). Set
  the initial state with `set()`, enter with `.to`, pulse with a `.to` yoyo pair — no `.from` with
  scale>1, no `keyframes` on animated elements.
- **`class="beat clip"` on EVERY timed beat (canonical form):** `clip` is what HyperFrames tracks
  (a beat without it won't render); the scaffold QA targets `.clip[data-start]`, but carry
  `beat` too — compositions and CSS in the wild key on it, and a SPEC that names only `clip` can
  leave a subagent's QA with every beat visible at once (multiple subtitle sets stacked).
- **Concrete font-family names** ("Poppins"), never CSS vars, in `font-family` — the renderer
  resolves `@font-face` by name, not by `var()`.
- **Single paused GSAP timeline** registered on `window.__timelines[<composition-id>]`; no other
  `<script>` logic.
- **`gsap.from({opacity:0})` on an element whose CSS already sets `opacity:0` stays invisible**
  (animates from-0 to current-0 → nothing). For late-entering layers (e.g. the cream fill) use
  `gsap.fromTo("#el",{opacity:0},{opacity:1})`.
  The combo `.to("#el",{opacity:1}) + .from("#el",{…,opacity:0})` on the same element/time is the
  SAME trap, and flaky on top (some beats render, others don't): either `fromTo`, or drop `opacity`
  from the `.from` and let the `.to` do the fade.
- **Degenerate transform matrix = invisible forever:** CSS initial state `transform:scaleX(0)
  rotate(-8deg)` (any scale-0 combined with a rotation) collapses the matrix — GSAP can't decompose
  the rotation and scaleY reads 0, so the element never appears even after the scaleX tween. Hide
  the element with `opacity:0` instead, and pass the rotation explicitly inside the `fromTo`
  (`fromTo(el,{scaleX:0,rotation:-8,opacity:1},{scaleX:1,rotation:-8,…})`).
- **SAVE the composition into the project dir** — the scratchpad scaffold is wiped.
- **Vendor GSAP locally** (`assets/gsap.min.js`); a CDN `<script src>` is both a network dependency
  and a supply-chain surface during render.
- **Blink tween beats a later `set`:** a caret/cursor blink built with `yoyo + even repeat` ends at
  opacity 1 and keeps running PAST a `set(...,{opacity:0})` scheduled before its real end — the set
  gets overridden. Schedule the off-set AFTER the last blink cycle.
- **Carry every CSS class when migrating markup** from the template into a new composition: a class
  used in the body but missing from `<style>` fails silently (invisible elements). Quick pre-render
  check: grep each `class="..."` token against the style block.
- **Playwright QA: never return the GSAP timeline to `pg.evaluate`** — `seek()`/`progress()` are
  chainable and return the timeline: Playwright tries to serialize the giant circular object and
  hangs forever (trivial evaluates OK, every seek hangs). Always `void tl.seek(t)` (or `&& 1`).
- **Shifting/scaling the timeline via script:** a regex on the end-of-line `, N);` positions does
  NOT see times inside const/dicts (`const b6t = {c1:51.4,…}`) — include them; and when scaling a
  dict do NOT scale digits inside KEY names (`c1:` → `c0.96:` = silent syntax error, symptom:
  `window.__timelines` undefined in QA). After any shift/scale, QA a beat that takes its times
  from a dict.
- **GSAP rotation/scale on a nested SVG `<g>` orbits out of place** (transform-origin resolves
  wrong; QA and render can even disagree). Rotate the WHOLE `<svg>` inside a positioned HTML div: pop
  the div `fromTo`, spin the svg with `transformOrigin:"50% 50%"`.
- **Never trust a previous session's "by ear" times:** re-anchor every reveal to word timestamps
  from the CURRENT base's transcript (payoffs can drift up to ~1s). If a documented transcript file
  is missing, rebuild it from the source transcription shifted by the trim offset and VERIFY with
  audio cross-correlation (lag 0ms) — saves an ASR call.

## Real content sources

- **Docs:** screenshot your own real (or pseudonymized) HTML/PDF to PNG with Playwright at 2× scale
  (A4 crops ≈ 760×1010). Vertical-scroll a tall doc by animating its `y` inside a clipped viewport
  (shows it's a real, long document).
- **Brand logos:** SimpleIcons has removed many brands (Canva/Adobe/OpenAI gone). Pull from
  `gilbarbara/logos` and `pheralb/svgl` via jsdelivr
  (`cdn.jsdelivr.net/gh/gilbarbara/logos/logos/<name>.svg`); use the *icon-only* variant in chips.
  Clearbit is often blocked in sandboxes (DNS fails). When neither repo has the brand (e.g. CapCut),
  the Wikimedia Commons API has official SVGs: search
  `commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<brand>%20logo%20svg&srnamespace=6`,
  then fetch the file URL via `prop=imageinfo&iiprop=url`. The official Claude sunburst is
  gilbarbara's `claude-icon.svg`.
- **Newsletter/email beats:** build a faithful email mock (header logo, gradient hero, REAL copy,
  CTA button), screenshot it with Playwright at 2x, and SCROLL it inside a clipped thumb (tween `y`
  inside an `overflow:hidden` viewport).
- **Never sensitive material** (client proposals, partner docs). Your own public docs (CV,
  one-pagers, public guides) and demo-data templates are fine.

## Sectional assembly & subagent orchestration

For anything beyond a single-block reel, build the graphics as **one composition PER SECTION**
(transparent at local frame 0, NO subtitles inside) and assemble them in ONE encode: base with cuts
→ zoompan → chain of qtrle overlays via `setpts=PTS-STARTPTS+<offset>/TB` (with a speed change k:
`setpts=(PTS-STARTPTS)/k+<offset/k>/TB` — offset divided by k too, see `references/speed-change.md`)
→ karaoke track last.
Any later retouch re-renders ONE section (~30s), not the whole reel. Building sections in parallel
with subagents (isolated scaffolds, shared SPEC file, DEDICATED QA port per agent, mandatory
report format, orchestrator verifies frames independently) is the proven fast path — full protocol,
assembly commands and verification checklist: `references/orchestration.md`.

## Refinement passes (after the first FINAL)

Split the reel into ~6 sections by beat groups and review them ONE at a time (cut the section clips
into `edit/review/`, open them in the player). Per part: comments → 2-3 direction mockups/demos →
choice → fix; ONE full re-render at the end via sectional assembly. Track decisions in
`edit/review/REFINEMENT-NOTES.md` (cut points, approved directions, time remaps). Full worked flow:
`references/refinement.md`.

## Beat-archetype reference (the component library)

| Archetype | Class(es) | Use for | Motion |
|---|---|---|---|
| Floating card | `.panel` + `.head` | a labeled group over the face | enter fade+y |
| Chip (+ strike) | `.chip` `.ic` `.strike` | tools / options, negate with red bar | `x` enter; `scaleX` wipe |
| Big payoff | `.big` `.g` + `.sub` | the keyword line | `back.out` pop on `.g` |
| Document (real) | real PDF `<img>` (fan/scroll) | the nice PDFs you make | fade+y / stagger / vertical scroll |
| Code → browser | `.codewin` + **real render `<img>`** in browser mock | HTML→render beat | line stagger, browser pop |
| Download (real) | real page `<img>` + faithful button + hand SVG + PDF `<img>` | the HTML→PDF download action | page shrinks → button pop → hand tap → PDF slides out |
| Brand kit | `.swatch` (real brand colors) + param chips (logo/colors/font/tone) + real doc `<img>` | brand-context beat | stagger |
| CTA | `.pill` `.plus` | the closing call | `back.out` pop |
| Editor tab-chip | `.ftab` `.fico` `.caret` | file names as characters (hooks about files) | 3D flip-in + typewriter, caret jumps tab to tab |
| Growing editor | `.vwin` + height tween | a real doc built section by section | lines cascade/type per section; side badges pop on the spoken word |
| Gauge + counter | fill bar + number | a quantity filling up (context, cost, load) | `scaleX` fill + object+`onUpdate` counter; shake at the ceiling |
| Stroke-draw | SVG path `pathLength="1"` | maps, routes, beams | dashoffset 1→0 draw landing on the keyword |
| Collapse handoff | scale-to-corner | a big element that becomes a chip in the next beat | `scale` toward the target corner, next beat pops the chip there |
| Phone cutaway (full-frame) | phone shell + REC UI + real base frame `<img>` | "I record myself with the phone" beats — covering the face fully is legit (it's a cutaway, like a cream card) | pop-in + slow handheld drift (rotate/scale), REC dot blink |
| NLE timeline | dark editor + ruler + clip blocks (blue + red labeled) + waveform track + playhead | beats about the editing itself | playhead `left` linear; red blocks fall out (`y`+rotate), survivors close the gap (`flexGrow`→0) on "cut" |
| Fight-card tiles | `.tile` (330px app-icon: cream/ink, logo + label) | two tools compared / "X vs Y" hooks | fly-in ±x `back.out`, VS spin-in, strike, collision + gold sparks, payoff slam |
| Finder window (growing) | `.fwin` `.tbar` `.frow` `.ftag` | REAL files appearing one by one ("inside the folder") | window pop, per-row slide-in + `height` tween, tag pill pop on the word |
| Cover fan | `.covwrap` (real cover `<img>` 260×462, white border, chip label) | "I cover this in earlier videos" — REAL covers of past episodes | staggered pop ±8° fan, exit fly-up |
| Gravity fall | tiles + crossed `.strike` X | tools that may disappear | X wipe + tilt, fall `y:+1900 power2.in`, mystery "✨/?" tiles pop in their place |
| Robot cream | folder CSS + 🤖 emoji ×3 | cream "for AI agents" (visual, not just text) | robots pop `back.out(2)` ONE per word |
| Beam connect + terminal chip | `.conn` gold bar + `>_` ink chip | tools wired to a folder/hub, "same prompt" | `scaleX/scaleY` draw from the source side, chip slide-up |

### Per-beat planning table (fill in `BUILD-SPEC.template.md`)

| # | Beat (spoken) | Window | Staging mode | Archetype | Payoff word |
|---|---|---|---|---|---|
| 1 | … | t–t | MODE 2 floating | `.panel` + chips | … |
| 2 | … | t–t | MODE 1 full card | `.big` + `.g` | … |

## Fallback — all-PIL pipeline

If HyperFrames is unavailable, or a beat needs deterministic frame-by-frame PIL rendering, you can
render the motion graphics by hand instead: build each beat as a sequence of RGBA PNG frames with
Pillow (position/opacity/scale computed per-frame in Python instead of a GSAP timeline), pack the
sequence into a qtrle `.mov` the same way as the HyperFrames output, and composite it with the same
`compose.sh` step. It's more code per beat and has no timeline scrubber, but it has zero render-time
dependencies beyond ffmpeg + Pillow + Playwright (for any mockup screenshots). This is a fallback
path, not a maintained scaffold in this repo — treat it as "the shape that works," not a
copy-paste template.

## Common mistakes

- Feeding the PNG-sequence straight into `overlay` (drops frames → flicker). Pack qtrle first.
- Rendering `--format webm` where alpha flattens, or compositing a legacy webm without
  `-c:v libvpx-vp9` (overlay goes opaque/black).
- Running the ASR with a keyterm list (HTTP 400) — disable it.
- Animating the `.clip` wrapper instead of the inner element (pivot on frame center).
- Building ONE graphic direction and iterating after the render, instead of 2-3 mockup directions
  BEFORE building (plan gate 1).
- Forgetting the speed question at plan time (1.0x vs 1.05–1.15x).
- Overwriting a previous FINAL instead of versioning.
- Using CSS vars in `font-family` (renderer can't resolve fonts).
- Forgetting `class="clip"` on a beat (it won't render).
- Letting HyperFrames touch the base or audio — only the graphics layer is HyperFrames.
- Using generic CSS mocks where a real screenshot belongs (real content wins).
- Suppressing subtitles on cream cards — DON'T; subtitles run continuously, the graphic just states
  the concept while the subtitle tracks the speech.
- Not saving the composition into the project dir after rendering from the scratchpad.
- Showing the whole reel before the current block was approved. Preview-gate each block.
- Long subtitle cues without auto-fit overflow the 1080px frame edges.
- Applying camera moves to the base file on disk instead of baking them into the composite
  (the frozen base must stay untouched and the moves re-runnable).
