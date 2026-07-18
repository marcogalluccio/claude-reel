# scaffold — HyperFrames overlay base, adapt per video

The graphics layer of the 9:16 reel is built with **HyperFrames** (transparent
overlay — png-sequence packed into a qtrle `.mov` — over a frozen base, then PIL
subtitles). Copy these into the project's ISOLATED scaffold dir (a scratch/tmp dir,
**outside your repo**) and adapt per video.

| File | Stage | Adapt |
|---|---|---|
| `composition.template.html` | graphics layer | the beat track (one `class="beat clip"` per beat: staging mode + archetype + window + payoff word) and the single paused GSAP timeline; set `data-duration` to the base length; fetch `assets/gsap.min.js` once + add Poppins under `assets/fonts/`; rename/copy to `index.html` before rendering |
| `compose.sh` | pack + composite | `BASE` / frames dir / `OUT` paths (packs `renders/frames` into qtrle `overlay.mov`, asserts the frame count, composites video-over-video) |
| `compose_zoom.template.sh` | composite with camera moves | `BASE`, the `Z` segments; takes the qtrle `overlay.mov` as arg 1 |
| `build_subs.py` | subtitles (LAST) | `FONTDIR`, `TOTAL`, the `CUES` list (subs are ALWAYS ON — never suppress on cream) |
| `qa_composition.py` | pre-render QA | the probe times (payoff moments) — run BEFORE every render: serves the dir over 127.0.0.1, seeks the paused timeline, screenshots each state into `qa/` (catches invisible elements, wrong positions, face overlaps in ~30s instead of a burned render) |

Poppins fetch (Regular/Medium/SemiBold/Bold/Black), needed by `composition.template.html` and `build_subs.py`:

```bash
mkdir -p assets/fonts && for w in Regular Medium SemiBold Bold Black; do curl -sL "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-$w.ttf" -o "assets/fonts/Poppins-$w.ttf"; done
```

Render the graphics (pinned, no `--expose`, from the scaffold dir; ALWAYS wipe the
frames dir first — leftovers from a longer previous render would be packed into the tail):

```bash
rm -rf renders/frames
npx --yes hyperframes@0.7.17 render . --format png-sequence -o renders/frames --fps 30 --quality high
```

Then `bash compose.sh <base.mp4>` and `python3 build_subs.py`. (Direct `--format webm`
can flatten the alpha on some machines; PNGs fed straight into `overlay` drop frames —
the qtrle route is the one verified frame-exact.)

**SAVE** the filled `composition.html` + `compose.sh` + `build_subs.py` into the
project's `edit/` dir for reproducibility — the scratchpad scaffold is ephemeral.

## Fallback (no scaffold shipped)

If HyperFrames is unavailable, the graphics layer can be rendered by hand as PIL-generated PNG
frames instead — see `../SKILL.md` (Fallback section) for the shape of that pipeline. There's no
ready-to-copy scaffold for it in this repo: the original was hand-tuned to one specific past video
(hardcoded durations, filenames, keyword lists) and wouldn't transfer as a template.
