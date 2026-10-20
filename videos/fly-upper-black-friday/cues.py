"""Gera assets/words.js a partir da transcrição do ElevenLabs (Scribe) e da logo extraída do PDF.

- remove as tags de emoção ([excited] etc.) e o travessão, que não são falados;
- corrige os pontos em que o alinhamento escorrega, conferidos pela energia do áudio;
- tira a pontuação final das legendas (mantém "…" e "!").
"""
import json
import re

OFFSET = 0.5          # a voz entra 0,5s depois do início do vídeo
DURATION = 24.0       # duração total (locução + respiro do lockup final)
FIX = {               # índice → (início, fim) medidos na forma de onda
    0: (0.11, 0.40),  # "Psiu…"
    5: (1.72, 2.14),  # "chegando"
    57: (19.62, 19.80),  # "gente"
    58: (19.80, 19.88),  # "no"
    59: (19.90, 20.25),  # "direct"
}
EMPH = ['Black', 'Friday', 'Fly', 'Upper', 'DECOLAR', 'outro', 'mundo', 'melhor', 'tarifa', 'malas', 'Pix', 'cartão', 'corre', 'VOAM', 'direct']

raw = json.load(open('assets/transcricao.json'))['words']
words = [w for w in raw if not re.fullmatch(r'\[.*\]', w['text']) and w['text'] != '—']
out = []
for i, w in enumerate(words):
    s, e = FIX.get(i, (w['start'], w['end']))
    txt = re.sub(r'[.,:]+$', '', w['text'])
    out.append({'w': txt, 's': round(s, 3), 'e': round(e, 3)})
emph = [i for i, w in enumerate(out) if re.sub(r'[!…]', '', w['w']) in EMPH]
logo = json.load(open('assets/logo_paths.json'))
with open('assets/words.js', 'w') as f:
    f.write('window.VO=' + json.dumps({'offset': OFFSET, 'duration': DURATION, 'words': out, 'emph': emph}, ensure_ascii=False) + ';\n')
    f.write('window.LOGO=' + json.dumps(logo) + ';\n')
for i, w in enumerate(out):
    print(i, w['w'], w['s'], w['e'], '*' if i in emph else '')
