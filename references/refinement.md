# Refinement & multiple directions — worked flow

The flow that turns "iterate after the render" into "choose before building". Two uses:
(a) plan gate on a NEW reel (design the load-bearing beats), (b) refinement pass on an
existing FINAL.

## 1. Section review (existing FINAL)

- Split the reel into ~6 parts by beat groups; cut section clips with ffmpeg into `edit/review/`
  (`P1.mp4` … `P6.mp4`, re-encode `-crf 18 -preset fast` for exact cuts).
- Open the current part in the player (`open Pn.mp4`). One part at a time: comments → proposals →
  approval → next part. ONE full re-render at the end.
- Track every decision in `edit/review/REFINEMENT-NOTES.md`: cut points (old timeline), approved
  directions, per-section time remaps, assembly plan. This file is what makes the final rebuild
  mechanical instead of archaeological.

## 2. Static mockups (2-3 directions per load-bearing beat)

- Extract REAL base frames at the beat's times (`ffmpeg -ss t -i base.mp4 -frames:v 1`). Read them
  and note the face geometry (head y-range, free top band, chest band) — it varies per beat.
- ONE multi-state HTML (`mockups.html`): common CSS (palette, `.onface`, karaoke-sub mock at the
  real y), one `.shot` div per state with the frame as `<img class="bg">`, a tiny script showing
  the state matching `location.hash`.
- Screenshot all states with Playwright over `http://127.0.0.1:<port>` (NEVER `file://`);
  hash-only navigation does not re-run scripts → `pg.reload()` after `pg.goto(...#state)`.
- QA the shots yourself (Read as contact sheets), then present them labeled by direction
  (A/B/C + 2-3 key moments each). Offer mixes ("ping-pong of C + ring of A").

## 3. Animated demos (when you need to judge motion)

- Build a DEMO BASE of the section (with any agreed audio cuts already applied, so the flow is
  judged too). All demo directions share it.
- One subagent per direction, parallel, isolated scaffolds + shared SPEC file
  (word timestamps, house rules, pipeline commands, geometry) — protocol in `orchestration.md`.
- Demos MAY bake static subtitle cues inside the overlay (demo only — the FINAL uses karaoke PIL;
  strip the sub beats from the composition before final assembly).
- Verify each demo yourself on extracted frames before forwarding (agents' QA can collide/lie).
- Deliver all directions together + open in player; pick one; sync/polish fixes on the chosen one
  are done directly by the orchestrator (small edits + single re-render, ~1 min).

## 4. Final rebuild

Sectional assembly (one comp per approved section, offsets from REFINEMENT-NOTES) — see
`orchestration.md` §Assembly. Apply the speed pass decision (`speed-change.md`) in the same
assembly. Save comps + scripts into `edit/v2-compositions/`, update REFINEMENT-NOTES and the
project notes.

## 5. Audio auditions (SFX / BGM variants) — worked flow

The choose-by-ear twin of the visual mockups:

- ONE segment of the current master (pick one with voice + a payoff), repeated × N variants, each
  with a different sound/track mixed in, hard-labeled on screen, concatenated into a single test
  bed (`edit/review/sfx-demos/`). 7 payoff-sound variants ≈ 14s of test bed.
- **Labels:** if your ffmpeg build has NO `drawtext`, render label PNGs with PIL (Poppins, dark
  rounded box) and `overlay` them per variant.
- **Level-match before comparing:** measure each music track's integrated LUFS
  (`loudnorm=print_format=json`) and normalize all candidates to the same target — tracks can differ
  by several dB, and an unmatched audition is a loudness contest, not a style choice. SFX variants:
  same relative volume per candidate.
- **Delivery:** `open` the test bed in the player; compressed copy in chat if >30 MiB. For music
  ALSO deliver the clean mp3s (chat + `open -R` in Finder) — you may want the raw tracks alone, at
  full volume, before hearing them under the reel.
- **Iterate in rounds** like the visual directions: give a reference + direction ("like track X but
  less pushed") → next 5-6 candidates spread across the named poles → converge (a few rounds is
  typical). A research subagent with the Mixkit JSON-LD method fetches each round in minutes; keep
  it alive (SendMessage) so rounds stay cheap.
- First-audition presets that work: SFX volumes 0.3–0.55 under voice; BGM at −31 LUFS; payoff
  candidates worth auditioning: whoosh-impact, pop, glitch, chime, sparkle, whoosh+pop layered.
