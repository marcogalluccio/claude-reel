# Sectional compositions + subagent orchestration

## Sectional compositions — the shape

- ONE HyperFrames composition per section (hook, cream, content beats, CTA…), timeline LOCAL to the
  section. Root `data-duration` = section length (may exceed the section's base if a payoff bleeds
  into the next part — the overlay chain handles it).
- Every composition must be **transparent at local frame 0** (first element enters ≥0.2s in) and
  end transparent (or run to video end, CTA only). This is what makes the assembly chain seamless:
  ffmpeg's framesync extends the first frame BACKWARDS before the overlay's offset.
- **NO subtitles inside section compositions** — karaoke PIL is applied once at assembly. (Demos
  for review may include static cues; strip them before final render.)
- Each section renders to its own qtrle `overlay.mov` (png-sequence → qtrle, see SKILL step 3).
  Verify `nb_read_frames == data-duration × 30 (±1)` per mov.

## Subagent protocol (parallel builds)

- **Scaffolds:** one isolated dir per agent OUTSIDE the repo (a scratch/tmp dir), pre-seeded by the
  orchestrator: `assets/fonts/` (Poppins 400-900), `assets/gsap.min.js`, logos/covers needed,
  `qa_composition.py`, `renders/`. A `shared/` dir holds the section bases, QA face-frames,
  approved reference compositions, and ONE `SPEC-shared.md`.
- **SPEC-shared.md contains:** word timestamps of the section (from the OUTPUT transcript), house
  rules + hard gotchas (fromTo trap, degenerate matrix, never animate `.clip` wrappers, index.html,
  concrete font names), the canonical `class="beat clip"` form for every timed beat (clip = renderer
  tracking, beat = CSS hooks; QA targets `.clip[data-start]`), face geometry from real frames, the
  exact pipeline commands (QA → png-sequence → qtrle → composite), and the self-check requirement.
- **Dedicated QA port per agent** (e.g. 8631/8632/8633/8634): the stock `qa_composition.py` port
  collides between parallel agents, and an agent can otherwise QA ANOTHER agent's composition.
- **Prompt musts:** "run through all steps without stopping" (subagents stall between long steps
  otherwise), timeline with per-word anchor times, explicit layout numbers or a mockup to
  reproduce, mandatory reply format (deliverable paths + QA outcome + compromises).
- **If an agent goes silent:** don't re-ping forever — read its artifacts on disk (index.html,
  renders/, demo) and verify yourself; the work is usually done.
- **Orchestrator verification is NON-optional:** extract frames from every agent deliverable at the
  payoff times and Read them (contact sheets). Agents' self-QA misses collisions and can lie.

## Assembly (one encode)

Inputs: base with cuts → (optional speed ÷k) → zoompan → N section overlays → karaoke track.

```bash
ffmpeg -y -i zoomed.mp4 \
  -i sec1/overlay.mov -i sec2/overlay.mov ... -i subs_track.mov \
  -filter_complex "\
[1:v]setpts=PTS-STARTPTS[o1];\
[2:v]setpts=PTS-STARTPTS+<OFF2>/TB[o2];\
...\
[N:v]setpts=PTS-STARTPTS[su];\
[0:v][o1]overlay=0:0:eof_action=pass[v1];\
[v1][o2]overlay=0:0:eof_action=pass[v2];\
...\
[vN-1][su]overlay=0:1420:eof_action=pass[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy \
  -movflags +faststart FINAL_reel_vN.mp4
```

- Offsets = section start in the FINAL timeline (after cuts: old_start − total_cut_before).
- `setpts` shifting (not `-itsoffset`) + transparent frame-0 comps = clean chain, one generation.
- With a speed change k: overlays become `setpts=(PTS-STARTPTS)/k+<OFF/k>/TB,fps=30` — see
  `speed-change.md`.
- Zoom expression: generate the piecewise-smoothstep `z` with a small python (SEGS list → nested
  ifs), don't hand-write it. Place releases SPANNING every base jump cut to mask them.
- Karaoke: retranscribe the FINAL base (disable keyterms; set the transcript language), rebuild the
  track with the project's `build_subs_karaoke*.py` (params: transcript path, END, SPEED).

## Verification checklist (before delivering)

1. Duration + frame count vs expected.
2. Contact sheet ~25 frames across ALL sections (payoff times): graphics land on their words,
   karaoke present, no face collisions.
3. Anti-dropout scan on full-frame windows (extract all frames small, test a corner pixel across
   every cream window). A mid-fade frame can false-positive: verify flagged frames visually.
4. Joins: step frame-by-frame across each base cut (the zoom release must span it).
5. Deliverable: versioned name, saved to `edit/`, comps to `edit/v2-compositions/` WITH their
   render `assets/` + `fonts/` (or a shared project `_scaffold-kit/`) so every section re-renders
   from the repo after a reboot, plus EVERY generated script (assembly/zoom/SFX/BGM mix) in `edit/`.
   REFINEMENT-NOTES + project notes updated. Chat uploads cap at 30 MiB — send a `-crf 27` preview
   if the master exceeds it, and open the master in the player.
