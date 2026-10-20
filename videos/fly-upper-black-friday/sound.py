"""Trilha + efeitos sintetizados e mixagem com a locução do ElevenLabs.

Os tempos saem de assets/words.js (as mesmas palavras que guiam a animação),
então som, legenda e imagem ficam no mesmo relógio.

uso: python3 sound.py saida.wav
"""
import json
import re
import subprocess
import sys
import wave

import numpy as np

SR = 48000
txt = open('assets/words.js').read()
VO = json.loads(re.search(r'window\.VO=(\{.*?\});\n', txt).group(1))
OFF, DUR = VO['offset'], VO['duration']
W = VO['words']
K = lambda i: W[i]['s'] + OFF
KE = lambda i: W[i]['e'] + OFF
N = int(SR * DUR)
rng = np.random.default_rng(3)
t_all = np.arange(N) / SR

# cues (mesmos índices do index.html)
kBlack, kFri, kE, kDec, kPass, kPac = K(2), K(3), K(6), K(13), K(14), K(16)
kFunc, kVoce, kGente, kTarifa, kE2, kMalas = K(22), K(24), K(30), K(35), K(36), K(41)
kPague, kPix, kParc, kCart, kMas, kOfer, kVoam = K(42), K(44), K(46), K(48), K(49), K(53), K(54)
kChama, kDirect, eDirect = K(55), K(59), KE(59)
e0 = eDirect + 0.45


# ------------------------------------------------------------------ síntese
def svf(x, fc, q=0.7):
    lp = bp = 0.0
    o_lp, o_bp, o_hp = np.empty_like(x), np.empty_like(x), np.empty_like(x)
    f = 2 * np.sin(np.pi * np.clip(fc, 20, SR / 6) / SR)
    damp = 1 / q
    for i in range(len(x)):
        hp = x[i] - lp - damp * bp
        bp += f[i] * hp
        lp += f[i] * bp
        o_lp[i], o_bp[i], o_hp[i] = lp, bp, hp
    return o_lp, o_bp, o_hp


def norm(s):
    return s / (np.abs(s).max() + 1e-9)


def env_ar(n, peak=0.6, shape=1.8):
    x = np.linspace(0, 1, n)
    return np.where(x < peak, (x / peak) ** shape, ((1 - x) / (1 - peak)) ** (shape * 1.3))


def whoosh(dur=0.5, f0=300, f1=3200, f2=700, peak=0.55, q=1.2, bright=0.0):
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    fc = np.where(x < peak, f0 * (f1 / f0) ** (x / peak), f1 * (f2 / f1) ** ((x - peak) / (1 - peak)))
    lp, bp, hp = svf(rng.standard_normal(n), fc, q)
    return norm((bp * 0.9 + lp * 0.25 + hp * bright) * env_ar(n, peak))


def sweep(f_from, f_to, dur, decay, k=18):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f_to + (f_from - f_to) * np.exp(-t * k)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)


def boom(dur=1.4, f0=110, f1=40):
    s = sweep(f0, f1, dur, 3.0)
    n = len(s)
    click = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 90) * 0.3
    lp, _, _ = svf(click, np.full(n, 1800.0))
    return norm(np.tanh((s + lp) * 1.7))


def pop(f=820, dur=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.6 * np.exp(-t * 60))) / SR) * np.exp(-t * 38)
    return norm(s + rng.standard_normal(n) * np.exp(-t * 400) * 0.15)


def tick(f=2600, dur=0.025):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 260) + rng.standard_normal(n) * np.exp(-t * 900) * 0.4)


def bell(freqs, gaps, dur=0.9, decay=5.5):
    n = int((dur + sum(gaps)) * SR)
    out = np.zeros(n)
    off = 0.0
    for k, f in enumerate(freqs):
        i, m = int(off * SR), int(dur * SR)
        t = np.arange(m) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * f * 2.01 * t) + 0.06 * np.sin(2 * np.pi * f * 3.98 * t))
        out[i:i + m] += (s * np.exp(-t * decay) * (1 - np.exp(-t * 900)))[: n - i]
        if k < len(gaps):
            off += gaps[k]
    return norm(out)


def shimmer(dur=0.8, n_part=26, lo=3500, hi=9000):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for _ in range(n_part):
        st, f = rng.uniform(0, dur * 0.55), rng.uniform(lo, hi)
        e = np.where(t > st, np.exp(-(t - st) * rng.uniform(8, 18)), 0) * (1 - np.exp(-np.maximum(t - st, 0) * 400))
        out += np.sin(2 * np.pi * f * t) * e * rng.uniform(0.4, 1)
    return norm(out)


def riser(dur=1.0):
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    _, bp, hp = svf(rng.standard_normal(n), 250 * (5200 / 250) ** (x ** 1.6), 2.2)
    s = norm((bp + hp * 0.15) * x ** 2.2) + np.sin(2 * np.pi * np.cumsum(220 * 2 ** (x * 2)) / SR) * x ** 3 * 0.25
    s[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return norm(s)


def jet(dur=1.6, peak=0.5):
    """Passagem de avião: ruído marrom grave + banda que sobe e cai (efeito Doppler)."""
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    brown = np.cumsum(rng.standard_normal(n))
    brown -= np.convolve(brown, np.ones(2000) / 2000, 'same')
    fc = np.where(x < peak, 500 * (2600 / 500) ** (x / peak), 2600 * (350 / 2600) ** ((x - peak) / (1 - peak)))
    _, bp, _ = svf(rng.standard_normal(n), fc, 2.5)
    whine = np.sin(2 * np.pi * np.cumsum(np.where(x < peak, 1800, 1800 * (0.7 ** ((x - peak) / (1 - peak))))) / SR) * 0.08
    return norm((norm(brown) * 0.7 + norm(bp) * 0.6 + whine) * env_ar(n, peak, 2.2))


def notif():
    """Notificação estilo iOS: duas notas de vidro."""
    return bell([1567.98, 2349.32], [0.11], 0.7, 7)


# ------------------------------------------------------------------ mix
L = np.zeros(N)
R = np.zeros(N)
MUS_L = np.zeros(N)
MUS_R = np.zeros(N)


def put(sig, t0, gain=1.0, pan=0.0, bus='fx'):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i] * gain
    p = np.asarray(pan, dtype=float)
    p = p[: len(sig)] if p.ndim else np.full(len(sig), float(p))
    l, r = sig * np.cos((p + 1) * np.pi / 4), sig * np.sin((p + 1) * np.pi / 4)
    if bus == 'mus':
        MUS_L[i:i + len(sig)] += l
        MUS_R[i:i + len(sig)] += r
    else:
        L[i:i + len(sig)] += l
        R[i:i + len(sig)] += r


def lin_pan(a, b, dur):
    return np.linspace(a, b, int(dur * SR))


# ---- trilha (128 bpm, grade ancorada no "DECOLAR")
BPM = 128
BEAT = 60 / BPM
grid0 = kDec
beats = [grid0 + BEAT * n for n in range(-6, 60) if 0 <= grid0 + BEAT * n < DUR]
CHORDS = [  # (fundamental do baixo, notas do pluck) — Dm9 · Bbmaj7 · F · C
    (73.42, [293.66, 349.23, 440.0, 523.25]),
    (58.27, [233.08, 293.66, 349.23, 440.0]),
    (87.31, [349.23, 440.0, 523.25, 659.25]),
    (65.41, [261.63, 329.63, 392.0, 493.88]),
]


def section(tt):
    if tt < kE - 0.3:
        return 'intro'
    if tt < grid0 - 0.01:
        return 'build'
    if kMas - 0.05 <= tt < kVoam - 0.02:
        return 'tension'
    if tt >= e0 + 2.2:
        return 'outro'
    return 'groove'


def kick():
    return np.tanh(sweep(160, 46, 0.36, 9, 30) * 1.8)


def hat(dec=40):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    _, _, hp = svf(rng.standard_normal(n), np.full(n, 7500.0), 0.9)
    return norm(hp) * np.exp(-t * dec)


def clap():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    _, bp, _ = svf(rng.standard_normal(n), np.full(n, 1500.0), 1.4)
    e = sum(np.exp(-np.maximum(t - d, 0) * 60) * (t >= d) for d in (0, 0.012, 0.024))
    return norm(bp * e)


KICK, HAT, CLAP = kick(), hat(), clap()
for bi, bt in enumerate(beats):
    sec = section(bt)
    bar_beat = round((bt - grid0) / BEAT) % 4
    if sec == 'build':
        put(KICK, bt, 0.55, bus='mus')
    elif sec == 'groove':
        put(KICK, bt, 0.95, bus='mus')
        put(HAT, bt + BEAT / 2, 0.22, 0.25, bus='mus')
        if bar_beat in (1, 3):
            put(CLAP, bt, 0.42, -0.1, bus='mus')
    elif sec == 'tension':
        put(HAT, bt, 0.25, -0.2, bus='mus')
        put(HAT, bt + BEAT / 2, 0.18, 0.2, bus='mus')

# baixo + pluck (por compasso de 4 tempos)
bar_len = BEAT * 4
b0 = grid0 - bar_len * 2
nb = int((DUR - b0) / bar_len) + 1
for b in range(nb):
    st = b0 + b * bar_len
    root, notes = CHORDS[b % 4]
    for s in range(8):
        tt = st + s * BEAT / 2
        if tt < 0 or tt >= DUR:
            continue
        sec = section(tt)
        if sec in ('groove', 'outro') or (sec == 'build' and s % 2 == 0):
            m = int(BEAT / 2 * SR * 0.95)
            t = np.arange(m) / SR
            bass = (np.sin(2 * np.pi * root * t) + 0.35 * np.sin(4 * np.pi * root * t)) * np.exp(-t * 3.5) * (1 - np.exp(-t * 300))
            put(np.tanh(bass * 1.5), tt, 0.32 if sec != 'outro' else 0.18, bus='mus')
        if sec in ('groove', 'outro', 'tension'):
            f = notes[[0, 2, 1, 3, 2, 1, 3, 2][s]] * 2
            m = int(0.3 * SR)
            t = np.arange(m) / SR
            pl = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 13) * (1 - np.exp(-t * 600))
            put(pl, tt, (0.16 if s % 2 == 0 else 0.11) * (0.6 if sec == 'tension' else 1), 0.35 if s % 2 else -0.35, bus='mus')

# pad (todas as seções) — escuro na intro, abre no groove
pad = np.zeros(N)
for b in range(nb):
    st = b0 + b * bar_len
    _, notes = CHORDS[b % 4]
    a, z = int(max(0, st) * SR), int(min(DUR, st + bar_len + 0.6) * SR)
    if z <= a:
        continue
    tt = t_all[a:z] - st
    e = (1 - np.exp(-tt * 2.2)) * np.exp(-np.maximum(tt - bar_len, 0) * 6)
    sig = sum(np.sin(2 * np.pi * f / 2 * 2 ** (d / 12) * tt + rng.uniform(0, 6)) for f in notes for d in (-0.1, 0.1))
    pad[a:z] += sig * e / 8
pad_fc = np.interp(t_all, [0, kE - 0.3, grid0, kMas, kVoam, e0, DUR], [500, 900, 3200, 1200, 3200, 3200, 1500])
pad, _, _ = svf(pad, pad_fc, 0.8)
intro_drone = np.sin(2 * np.pi * 36.71 * t_all) * np.clip(1 - t_all / (kE + 0.5), 0, 1) * 0.5
MUS_L += norm(pad) * 0.28 + intro_drone * 0.5
MUS_R += norm(pad) * 0.28 + intro_drone * 0.5

# ---- efeitos
put(whoosh(0.4, 600, 3000, 900), 0.08, 0.18, -0.3)
put(notif(), 0.22, 0.30, 0.2)                                     # notificação
put(boom(1.8, 90, 34), kBlack - 0.05, 0.85)                        # BLACK
put(whoosh(0.5, 200, 2200, 300, 0.4), kBlack - 0.15, 0.30)
put(boom(1.2, 120, 50), kFri - 0.05, 0.45)                         # FRIDAY
put(shimmer(0.8, 24), kFri, 0.10)
put(riser(1.0), kE - 1.0, 0.30)
put(whoosh(0.7, 200, 5200, 600, 0.55, 0.9, 0.3), kE - 0.42, 0.75)  # estouro de nuvens
put(jet(2.0, 0.85), kE - 0.1, 0.32, lin_pan(-0.3, 0.2, 2.0))       # motores ganhando força
put(riser(0.9), kDec - 0.85, 0.35)
put(jet(1.5, 0.35), kDec - 0.1, 0.90, lin_pan(-0.2, 0.5, 1.5))     # DECOLAR: passagem
put(boom(1.8), kDec + 0.35, 0.95)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.06, 0.06, 0.08], 1.4, 3.2), kDec + 0.42, 0.20)
put(shimmer(1.0, 40), kDec + 0.42, 0.15)
put(whoosh(0.45, 300, 3600, 600, 0.6), kPass + 0.15, 0.45)
put(pop(900), kPass + 0.45, 0.25, -0.4)
put(pop(1100), kPac + 0.12, 0.25, 0.4)
put(shimmer(0.7, 22), K(20), 0.10, 0.4)                            # "outro mundo"
put(whoosh(0.4, 400, 3200, 700, 0.6), kFunc - 0.2, 0.45, lin_pan(0.5, -0.5, 0.4))
put(whoosh(0.22, 800, 4200, 2000, 0.5, 1.6, 0.2), kVoce - 0.05, 0.30, 0.4)
put(pop(1250, 0.1), kVoce, 0.28, 0.4)
put(bell([1567.98, 2093.0], [0.075], 0.55, 8), kVoce + 0.42, 0.28, -0.3)
put(whoosh(0.38, 400, 3200, 800, 0.6), kGente, 0.42, lin_pan(0.5, -0.6, 0.38))
for i in range(12):
    put(tick(3000 + (i % 3) * 300, 0.02), kGente + 0.2 + i * 0.03, 0.12, -0.1)
for i in range(3):
    put(pop(700 + i * 120, 0.09), kGente + 0.4 + i * 0.07, 0.16, 0.1 * i)
put(whoosh(0.6, 1500, 6500, 2500, 0.5, 3.0, 0.3), kGente + 0.65, 0.15)
put(pop(980), kTarifa - 0.15, 0.38, 0.2)
put(pop(1400, 0.08), kTarifa, 0.25, 0.3)
put(whoosh(0.38, 400, 3200, 800, 0.6), kE2 - 0.25, 0.40, lin_pan(0.5, -0.6, 0.38))
put(whoosh(0.7, 150, 2600, 400, 0.6, 0.9), kE2 - 0.1, 0.45)
put(shimmer(0.7, 26, 4000, 10000), kE2 + 0.55, 0.11, 0.2)
put(bell([1318.51, 1661.22, 1975.53], [0.07, 0.07], 1.0, 4.5), kMalas, 0.24, 0.5)
put(whoosh(0.45, 400, 3200, 700, 0.6), kPague - 0.2, 0.42, lin_pan(0.5, -0.5, 0.45))
put(pop(1050), kPix - 0.05, 0.30)
put(bell([1046.5, 1318.51, 1567.98, 2093.0], [0.06, 0.06, 0.06], 1.0, 4.0), kPix + 0.05, 0.24)
put(whoosh(0.35, 600, 3600, 900, 0.7, 1.3, 0.2), kParc - 0.3, 0.38, lin_pan(0.6, -0.2, 0.35))
put(whoosh(0.4, 600, 2800, 700, 0.3, 1.3, 0.1), kParc + 0.05, 0.32, lin_pan(-0.2, 0.4, 0.4))
put(tick(2200, 0.03), kCart - 0.08, 0.35)
put(pop(700, 0.08), kCart + 0.1, 0.2)
put(boom(1.6, 80, 32), kMas - 0.02, 0.80)                          # "Mas corre" — noite
put(whoosh(0.4, 300, 2200, 400, 0.4), kMas - 0.12, 0.35)
secs_prev = None                                                   # tique a cada segundo do timer
for tt in np.arange(kMas + 0.1, kVoam, 1 / 240):
    p = min(1, max(0, (tt - (kMas + 0.1)) / (kVoam - (kMas + 0.1))))
    s = max(0, round(59 * (1 - p * 0.97)))
    if s != secs_prev and secs_prev is not None:
        put(tick(2000 if s % 2 else 2400, 0.03), tt, 0.16, 0.3 if s % 2 else -0.3)
    secs_prev = s
put(riser(kVoam - kMas), kMas, 0.32)
for d, pn in ((0, -0.5), (0.07, 0.5), (0.14, 0.3)):
    put(pop(900 + d * 2000, 0.1), kOfer - 0.1 + d, 0.22, pn)
put(jet(1.3, 0.4), kVoam - 0.12, 1.0, lin_pan(-0.8, 0.8, 1.3))     # VOAM: avião cruza
put(boom(1.4), kVoam, 0.75)
put(whoosh(0.4, 400, 3600, 600, 0.7), kChama - 0.3, 0.45)
put(pop(820, 0.14), kChama, 0.36)
put(whoosh(0.5, 900, 2200, 1100, 0.5, 2.0), kChama + 0.35, 0.10, lin_pan(0.6, 0, 0.5))
put(tick(3800, 0.03), kDirect, 0.45)
put(np.tanh(sweep(160, 90, 0.09, 45) * 2), kDirect, 0.5)
put(shimmer(0.5, 14, 3000, 8000), kDirect + 0.1, 0.10)
put(whoosh(0.45, 300, 3200, 600, 0.75, 1.0, 0.15), eDirect + 0.25, 0.45)
put(boom(1.8), e0, 0.80)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.07, 0.07, 0.09], 1.8, 2.6), e0 + 0.02, 0.24)
put(shimmer(1.2, 40), e0 + 0.2, 0.13)

# ---- locução
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'assets/locucao.mp3', '-af', 'highpass=f=70',
                      '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
vo = np.frombuffer(raw, dtype=np.float32).astype(float)
VOX = np.zeros(N)
i = int(OFF * SR)
VOX[i:i + len(vo)] = vo[: N - i]
VOX = norm(VOX)

# sidechain: a trilha abaixa ~9 dB enquanto a voz fala
env = np.abs(VOX)
win = int(0.03 * SR)
env = np.convolve(env, np.ones(win) / win, 'same')
env = np.minimum(1, env / 0.06)
k = np.exp(-1 / (0.25 * SR))
sm = np.empty_like(env)
acc = 0.0
for j in range(0, N, 64):                                          # release suave (por blocos)
    acc = max(env[j], acc * k ** 64)
    sm[j:j + 64] = acc
duck = 1 - 0.7 * sm
fade = np.clip(t_all / 0.3, 0, 1) * np.clip((DUR - t_all) / 1.2, 0, 1)
FX_GAIN, mus_gain = 0.5, 0.22
L *= FX_GAIN
R *= FX_GAIN
L += MUS_L * duck * fade * mus_gain
R += MUS_R * duck * fade * mus_gain
L += VOX * 0.95
R += VOX * 0.95

st = np.stack([L, R], axis=1)
st = np.tanh(st * 1.1) / np.tanh(1.1)
st = st / np.abs(st).max() * 0.89
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', sys.argv[1], f'{DUR:.2f}s')
