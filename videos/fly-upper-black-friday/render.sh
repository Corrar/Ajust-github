#!/bin/bash
# Renderiza o vídeo final: 240 qps em 4 partes paralelas → motion blur (tmix) → 60 qps → mix com o som
set -e
cd "$(dirname "$0")"
OUT=${OUT:-out}; mkdir -p "$OUT"
python3 cues.py > /dev/null
DUR=$(python3 -c "import json,re;print(json.loads(re.search(r'window\.VO=(\{.*?\});\n',open('assets/words.js').read()).group(1))['duration'])")
FPS=240; N=$(python3 -c "print(int(round($DUR*$FPS)))"); P=4; STEP=$(( (N+P-1)/P ))
for i in $(seq 0 $((P-1))); do
  a=$((i*STEP)); b=$(( (i+1)*STEP )); [ $b -gt $N ] && b=$N
  node render.mjs $FPS $a $b "$OUT/part$i.mkv" 1 &
done
python3 sound.py "$OUT/audio.wav"
wait
printf "file 'part%d.mkv'\n" $(seq 0 $((P-1))) > "$OUT/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/list.txt" -c copy "$OUT/raw240.mkv"
ffmpeg -v error -y -i "$OUT/raw240.mkv" -i "$OUT/audio.wav" -filter_complex "[0:v]tmix=frames=3,fps=60,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1:LRA=9[a]" \
  -map "[v]" -map "[a]" -ar 48000 -c:v libx264 -preset slow -crf 15 -profile:v high -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT/fly-upper-black-friday.mp4"
echo pronto "$OUT/fly-upper-black-friday.mp4"
