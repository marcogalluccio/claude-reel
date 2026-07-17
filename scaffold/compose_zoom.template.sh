#!/usr/bin/env bash
# 9:16 reel — composite with CAMERA MOVES (digital punch-ins).
# The frozen base stays UNTOUCHED on disk: the zoom is baked only into the composite.
# Pipeline: upscale 2x (lanczos, smooth sub-pixel moves) -> zoompan -> overlay graphics.
# The graphics stay pinned while the footage moves under them (standard motion look).
#
# The Z segments below are a WORKED EXAMPLE for a hook. Adapt them to your speech:
#   0.30-2.00  ease-in  1.00 -> 1.06   (opening)
#   5.05-5.45  push     1.06 -> 1.12   (sync with the graphic slam)
#   6.90-8.60  release  1.12 -> 1.00   (rhetorical reveal)
# Each segment is a nested if():
#   if(lt(in/30,END), <value or ramp>, <rest>)
# Smoothstep ramp from A to B over [T0,T1]:
#   A+(B-A)*pow((in/30-T0)/(T1-T0),2)*(3-2*(in/30-T0)/(T1-T0))
# NOTE: in/30 = seconds at 30fps. Count the if(: the trailing close-parens must be
# exactly one per if. Invisible reset: while a full-frame cream card covers everything,
# snap the segment to 1.00 (the snap is not visible).
#
# Usage:  ./compose_zoom.template.sh <overlay.mov> <out.mp4> [trim_duration]
# The overlay is the qtrle .mov packed from the png-sequence (see compose.sh
# steps 1-2: NEVER png straight into overlay, and prefer png-sequence over webm).
set -e
BASE="./base.mp4"   # <-- point this at your frozen 1080x1920 base
OVERLAY="${1:?overlay.mov}"
OUT="${2:?out.mp4}"
TRIM="${3:-}"

TRIMARGS=()
if [ -n "$TRIM" ]; then TRIMARGS=(-t "$TRIM"); fi

Z="if(lt(in/30,0.30),1,if(lt(in/30,2.00),1+0.06*pow((in/30-0.30)/1.70,2)*(3-2*(in/30-0.30)/1.70),if(lt(in/30,5.05),1.06,if(lt(in/30,5.45),1.06+0.06*pow((in/30-5.05)/0.40,2)*(3-2*(in/30-5.05)/0.40),if(lt(in/30,6.90),1.12,if(lt(in/30,8.60),1.12-0.12*pow((in/30-6.90)/1.70,2)*(3-2*(in/30-6.90)/1.70),1))))))"

ffmpeg -y -i "$BASE" -i "$OVERLAY" \
  -filter_complex "[0:v]scale=2160:3840:flags=lanczos,zoompan=z='${Z}':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.46':d=1:s=1080x1920:fps=30[zb];[zb][1:v]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a "${TRIMARGS[@]}" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "OK -> $OUT"
