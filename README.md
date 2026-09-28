# Monta i reel verticali con Claude

Skill per montare reel verticali 9:16 (talking-head) con Claude Code: un layer di grafiche
animate a tempo (HyperFrames), sottotitoli karaoke, camera move digitali, musica ed effetti
sonori — sopra un girato fatto col telefono.

Non e zero-setup come altre skill: serve un vero ambiente di render (Claude Code, Node +
HyperFrames CLI, ffmpeg, Playwright; opzionale ElevenLabs/HeyGen per l'audio). Il sito spiega
tutto in chiaro.

- **Sito:** https://marcogalluccio.com/claude-reel/
- **Guida PDF:** https://marcogalluccio.com/claude-reel/guida/claude-reel-guida.pdf
- **Motore:** https://github.com/heygen-com/hyperframes

## Come si parte

1. Installa Claude Code, Node.js, ffmpeg, Playwright (il prompt di setup sul sito controlla e
   installa quello che manca)
2. Incolla in Claude Code il prompt di setup (vedi sito o guida)
3. Opzionale: chiavi ElevenLabs (voce/trascrizione) e/o HeyGen (musica/SFX)

Poi metti un talking-head in una cartella, apri Claude e digli cosa vuoi sopra.

## Struttura

- `index.html` — la landing
- `guida/claude-reel-guida.pdf` — la guida di setup
- `examples/novita-app-claude-web.mp4` — un reel montato con questo metodo
- `SKILL.md` — la skill completa: pipeline, house style, archetipi, gotcha
- `BUILD-SPEC.template.md` — worksheet da compilare prima di ogni montaggio
- `references/` — approfondimenti (orchestrazione multi-agente, refinement, speed change)
- `scaffold/` — script di partenza (composition HTML, compositing, sottotitoli, QA)

Made with Claude. Licenza MIT.
