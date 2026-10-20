#!/bin/bash
# Renderiza o vídeo final: 240 qps em 4 partes paralelas → motion blur (tmix) → 60 qps + áudio
set -e
cd "$(dirname "$0")"
OUT=${OUT:-out}; mkdir -p "$OUT"
FPS=240; N=$((25*FPS)); P=4; STEP=$(( (N+P-1)/P ))
for i in $(seq 0 $((P-1))); do
  a=$((i*STEP)); b=$(( (i+1)*STEP )); [ $b -gt $N ] && b=$N
  node render.mjs $FPS $a $b "$OUT/part$i.mkv" 1 &
done
wait
printf "file 'part%d.mkv'\n" $(seq 0 $((P-1))) > "$OUT/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/list.txt" -c copy "$OUT/raw240.mkv"
ffmpeg -v error -y -i "$OUT/raw240.mkv" -vf "tmix=frames=3,fps=60" -c:v libx264 -preset slow -crf 10 -pix_fmt yuv444p "$OUT/video60.mkv"
