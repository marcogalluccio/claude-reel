# Speed change (1.05–1.15x) — verified recipe

Ask at PLAN time ("1.0x natural or 1.05–1.15x?"). Execute at ASSEMBLY. The frozen base on disk is
NEVER touched; a 1.0x master and a k-x master can coexist (`FINAL_reel_v2.mp4` / `FINAL_reel_v3_11x.mp4`).

Let k = speed factor (e.g. 1.1). New duration = old / k.

## 1. Base: speed + zoom in one pass

```bash
ffmpeg -y -i base_final.mp4 -filter_complex \
  "[0:v]setpts=PTS/k,fps=30,scale=2160:3840:flags=lanczos,zoompan=z='<Z>':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.46':d=1:s=1080x1920:fps=30[v];\
   [0:a]atempo=k[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 14 -preset medium -c:a aac -b:a 256k zoomed_kx.mp4
```

- `fps=30` right after `setpts` is MANDATORY: zoompan discards input PTS and re-stamps frames by
  index — a bare `setpts` leaves the video at the old speed (audio/graphics ahead, lips behind,
  `-shortest` masks it as truncation).
- `atempo` preserves pitch (range 0.5–2.0 per instance).
- Zoom SEGS: divide every segment start/end by k, keep the z values. Regenerate `<Z>` with the
  SEGS→smoothstep generator; the cut-masking releases keep spanning the joins automatically
  (joins scale by ÷k too).

## 2. Section overlays: rescale IN-CHAIN (no composition edits)

Speeding the rendered qtrle movs is safer than rescaling the GSAP timelines (regex-on-times is a
documented trap). In the assembly filtergraph, per overlay input:

```
[k:v]setpts=(PTS-STARTPTS)/k+<OFFSET/k>/TB,fps=30:start_time=<OFFSET/k>[ok];
```

Animations get ~10% snappier — fine at k ≤ 1.15; every reveal still lands on its word because
speech scales identically.

## 3. Karaoke subtitles

The karaoke builder you wrote yourself (see SKILL.md, Subtitles section — the repo ships only the
static `scaffold/build_subs.py`) needs a `SPEED` knob: divide word times by `SPEED = k`, set
`END = old_end / k`, rebuild the track (`--track-only`), overlay at y=1420 as usual.

## 4. Verify

- Duration == old/k; frame count == duration × 30 (±2).
- Contact sheet at OLD payoff times ÷ k: same graphic+subtitle pairings as the 1.0x master.
- Anti-dropout scan on cream windows (bounds ÷ k). Mid-fade frames can false-positive — check
  flagged frames visually before calling it a dropout.

Two approaches, depending on the build: for a monolithic composition, rescale the comp times + dicts
+ SEGS + word times together (heavier — use only without sectional movs); for a sectional build,
rescale the sectional movs in-chain with this recipe (~10 min machine time end-to-end).
