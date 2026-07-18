#!/usr/bin/env bash
# 9:16 reel — HyperFrames overlay compositing (qtrle pipeline).
#
# Hybrid render pattern (overlay-hybrid, not the video-in-composition flow):
#   1) HyperFrames renders ONLY the motion-graphics layer as a PNG-SEQUENCE
#      (1080x1920, RGBA) from the house-style index.html, in the ISOLATED
#      scaffold dir (a scratch/tmp dir, outside your repo), pinned. ALWAYS wipe
#      the frames dir first (leftover higher-numbered frames from a previous
#      longer render would get packed into the tail):
#        rm -rf renders/frames
#        npx --yes hyperframes@0.7.17 render . --format png-sequence -o renders/frames --fps 30 --quality high
#   2) Pack the PNGs into a LOSSLESS ALPHA intermediate (qtrle .mov). NEVER feed
#      the PNGs straight into overlay: the image2<->mp4 PTS pairing drops frames
#      (1-frame overlay dropouts = flicker).
#   3) This script does both the packing and the video-over-video composite onto
#      the FROZEN base mp4. HyperFrames never touches the base or the audio.
#   4) PIL subtitles are applied LAST (build_subs.py / karaoke builder).
#
# Legacy note: a direct `--format webm` render can FLATTEN the alpha on some
# machines; if a webm overlay is ever used anyway, decode it with
# `-c:v libvpx-vp9` or the default decoder drops the alpha plane (opaque/black overlay).
set -e

BASE="${1:-../base.mp4}"            # frozen 1080x1920 base (cut + clean audio, done upstream)
FRAMES="${2:-renders/frames}"       # HyperFrames png-sequence dir
OUT="${3:-composite.mp4}"           # composite (no subs yet)
MOV="$(dirname "$FRAMES")/overlay.mov"

# 2) pack png-sequence -> qtrle alpha mov. ALWAYS repack: a dir-mtime freshness
# check is unreliable on APFS (overwriting existing frames in place does not
# touch the dir mtime -> stale overlay.mov silently reused).
PNGS=$(find "$FRAMES" -name 'frame_*.png' | wc -l | tr -d ' ')
[ "$PNGS" -gt 0 ] || { echo "ERROR: no frame_*.png in $FRAMES" >&2; exit 1; }
ffmpeg -y -framerate 30 -start_number 1 \
  -i "$FRAMES/frame_%06d.png" -frames:v "$PNGS" -c:v qtrle "$MOV"

# sanity: mov frame count MUST match png count (this is the dropped-frames guard)
MOVF=$(ffprobe -v error -select_streams v -count_frames -show_entries stream=nb_read_frames -of csv=p=0 "$MOV")
echo "frames: png=$PNGS mov=$MOVF"
[ "$PNGS" -eq "$MOVF" ] || { echo "ERROR: png/mov frame mismatch ($PNGS vs $MOVF)" >&2; exit 1; }

# 3) composite video-over-video
ffmpeg -y -i "$BASE" -i "$MOV" \
  -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

echo "composite -> $OUT"
echo "Next: python3 build_subs.py   (PIL subtitles, applied LAST)"
