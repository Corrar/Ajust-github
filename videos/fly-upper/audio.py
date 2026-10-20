"""Desenho de som sintetizado (sem samples de terceiros), sincronizado com index.html.

uso: python3 audio.py saida.wav
"""
import sys
import wave

import numpy as np

SR = 48000
DUR = 25.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N)
R = np.zeros(N)


def put(sig, t0, gain=1.0, pan=0.0):
    """Soma um sinal mono no master em t0 (s), com pan -1..1 (fixo ou array)."""
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    p = np.broadcast_to(np.asarray(pan, dtype=float), sig.shape) if np.ndim(pan) else np.full(sig.shape, pan)
    p = p[: len(sig)]
    L[i:i + len(sig)] += sig * np.cos((p + 1) * np.pi / 4)
    R[i:i + len(sig)] += sig * np.sin((p + 1) * np.pi / 4)


def env_ar(n, a, peak=0.6, shape=2.0):
    x = np.linspace(0, 1, n)
    e = np.where(x < peak, (x / peak) ** shape, ((1 - x) / (1 - peak)) ** (shape * 1.3))
    return e * (1 - np.exp(-x * a)) if a else e


def svf_bp(x, fc, q=0.7):
    """Filtro state-variable com corte variável no tempo (fc: array). Retorna (lp, bp, hp)."""
    lp = bp = 0.0
    out_lp = np.empty_like(x)
    out_bp = np.empty_like(x)
    out_hp = np.empty_like(x)
    f = 2 * np.sin(np.pi * np.clip(fc, 20, SR / 6) / SR)
    damp = 1 / q
    for i in range(len(x)):
        hp = x[i] - lp - damp * bp
        bp += f[i] * hp
        lp += f[i] * bp
        out_lp[i] = lp
        out_bp[i] = bp
        out_hp[i] = hp
    return out_lp, out_bp, out_hp


def whoosh(dur=0.5, f0=300, f1=3200, f2=700, peak=0.55, q=1.2, bright=0.0):
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    fc = np.where(x < peak, f0 * (f1 / f0) ** (x / peak), f1 * (f2 / f1) ** ((x - peak) / (1 - peak)))
    noise = rng.standard_normal(n)
    lp, bp, hp = svf_bp(noise, fc, q)
    s = bp * 0.9 + lp * 0.25 + hp * bright
    s *= env_ar(n, 0, peak, 1.8)
    return s / (np.abs(s).max() + 1e-9)


def sine_sweep(f_from, f_to, dur, decay):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f_to + (f_from - f_to) * np.exp(-t * 18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * decay)


def boom(dur=1.4):
    s = sine_sweep(110, 42, dur, 3.2)
    n = len(s)
    click = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 90) * 0.25
    lp, _, _ = svf_bp(click, np.full(n, 1800.0), 0.7)
    s = np.tanh((s + lp) * 1.6)
    return s / np.abs(s).max()


def pop(f=820, dur=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f_t = f * (1 + 0.6 * np.exp(-t * 60))
    s = np.sin(2 * np.pi * np.cumsum(f_t) / SR) * np.exp(-t * 38)
    s += rng.standard_normal(n) * np.exp(-t * 400) * 0.15
    return s / np.abs(s).max()


def tick(f=2600, dur=0.025):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 260) + rng.standard_normal(n) * np.exp(-t * 900) * 0.4
    return s / np.abs(s).max()


def bell(freqs, gaps, dur=0.9, decay=5.5):
    n = int((dur + sum(gaps)) * SR)
    out = np.zeros(n)
    off = 0.0
    for k, f in enumerate(freqs):
        i = int(off * SR)
        m = int(dur * SR)
        t = np.arange(m) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * f * 2.01 * t) + 0.06 * np.sin(2 * np.pi * f * 3.98 * t))
        s *= np.exp(-t * decay) * (1 - np.exp(-t * 900))
        out[i:i + m] += s[: n - i]
        if k < len(gaps):
            off += gaps[k]
    return out / np.abs(out).max()


def shimmer(dur=0.8, n_part=26, lo=3500, hi=9000):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for _ in range(n_part):
        st = rng.uniform(0, dur * 0.55)
        f = rng.uniform(lo, hi)
        e = np.where(t > st, np.exp(-(t - st) * rng.uniform(8, 18)), 0) * (1 - np.exp(-np.maximum(t - st, 0) * 400))
        out += np.sin(2 * np.pi * f * t) * e * rng.uniform(0.4, 1)
    return out / np.abs(out).max()


def riser(dur=1.0):
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    fc = 250 * (5200 / 250) ** (x ** 1.6)
    _, bp, hp = svf_bp(rng.standard_normal(n), fc, 2.2)
    s = (bp + hp * 0.15) * (x ** 2.2)
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (x * 2)) / SR) * (x ** 3) * 0.25
    s = s / np.abs(s).max() + tone
    s[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return s / np.abs(s).max()


# ---------------------------------------------------------------- trilha
def pad_and_pulse():
    """Pad suave (acordes maj9) + pluck em colcheias, 100 bpm."""
    bpm = 100
    beat = 60 / bpm
    out = np.zeros(N)
    chords = [  # (início, notas Hz)
        (0.0, [146.83, 220.0, 277.18, 329.63, 440.0]),        # Dmaj9-ish
        (5.0, [123.47, 185.0, 246.94, 293.66, 369.99]),       # Bm9
        (10.0, [98.0, 196.0, 246.94, 293.66, 369.99]),        # Gmaj7
        (15.0, [110.0, 220.0, 277.18, 329.63, 493.88]),       # A add9
        (20.0, [146.83, 220.0, 293.66, 369.99, 440.0]),       # D
    ]
    t = np.arange(N) / SR
    for k, (st, notes) in enumerate(chords):
        en = chords[k + 1][0] if k + 1 < len(chords) else DUR
        a, b = int(st * SR), int(min(DUR, en + 1.2) * SR)
        tt = t[a:b] - st
        e = (1 - np.exp(-tt * 1.6)) * np.where(tt > en - st, np.exp(-(tt - (en - st)) * 4), 1)
        sig = np.zeros(b - a)
        for f in notes:
            for d in (-0.12, 0.0, 0.11):
                ff = f * 2 ** (d / 12)
                sig += np.sin(2 * np.pi * ff * tt + rng.uniform(0, 6)) + 0.22 * np.sin(4 * np.pi * ff * tt)
        out[a:b] += sig * e / (len(notes) * 3)
    # pluck em colcheias com as notas do acorde corrente
    step = beat / 2
    n_steps = int(DUR / step)
    for s in range(n_steps):
        st = s * step
        notes = [c for c in chords if c[0] <= st][-1][1]
        f = notes[[2, 3, 4, 3][s % 4]] * 2
        m = int(0.35 * SR)
        tt = np.arange(m) / SR
        pl = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 14) * (1 - np.exp(-tt * 600))
        i = int(st * SR)
        out[i:i + m] += pl[: N - i] * (0.55 if s % 2 == 0 else 0.35)
    # kick suave nas semínimas entre o hook e o fim, com sidechain no resto da trilha
    kick = np.zeros(N)
    duck = np.ones(N)
    b = 0
    while b * beat < DUR:
        st = b * beat
        if 2.4 <= st < 23.3 and not (6.0 <= st < 6.45):
            k = sine_sweep(150, 48, 0.32, 11)
            i = int(st * SR)
            kick[i:i + len(k)] += k[: N - i]
            m = int(0.3 * SR)
            duck[i:i + m] = np.minimum(duck[i:i + m], 1 - 0.45 * np.exp(-np.arange(min(m, N - i)) / SR * 9))
        b += 1
    mus = out * duck
    mus /= np.abs(mus).max()
    kick /= np.abs(kick).max() + 1e-9
    fade = np.clip(t / 0.6, 0, 1) * np.clip((DUR - t) / 1.2, 0, 1)
    return mus * fade, kick * fade


mus, kick = pad_and_pulse()
L += mus * 0.16 + kick * 0.22
R += mus * 0.16 + kick * 0.22

# ---------------------------------------------------------------- SFX
W = lambda *a, **k: whoosh(*a, **k)

# S1 hook
put(W(0.45, 400, 2600, 600), 0.0, 0.25, -0.2)
put(boom(1.2), 0.32, 0.55)
put(W(0.5, 200, 1800, 300, 0.4), 0.28, 0.45)
put(W(0.4, 500, 2400, 700), 0.70, 0.22, 0.3)
for a, p in [(0.18, -0.6), (0.34, 0.6), (0.5, -0.5), (0.62, 0.5)]:
    put(pop(1100, 0.08), a, 0.08, p)
put(W(0.3, 1500, 7000, 3000, 0.7, 2.0, 0.4), 1.10, 0.35, np.linspace(-0.6, 0.6, int(0.3 * SR)))
put(riser(0.5), 1.55, 0.18)
put(W(0.55, 200, 4200, 500, 0.75, 1.0, 0.2), 1.95, 0.75)          # zoom-through

# S2 cartão + preço
put(W(0.6, 300, 2600, 500, 0.45), 2.58, 0.45, 0.1)
put(W(0.9, 900, 2600, 1400, 0.5, 2.5), 2.95, 0.22, np.linspace(-0.7, 0.7, int(0.9 * SR)))
put(W(0.25, 2000, 7000, 3000, 0.6, 2.0, 0.4), 3.30, 0.22, 0.2)
ticks = np.linspace(0, 1, 15)
for i, x in enumerate(ticks):
    tt = 3.38 + (1 - (1 - x) ** 0.4) * 0.77
    put(tick(2400 + i * 40), tt, 0.18, 0.15)
put(pop(900), 4.05, 0.40, 0.3)
put(shimmer(0.6), 4.08, 0.12, 0.4)
put(W(0.45, 400, 3000, 600, 0.6), 4.70, 0.45, -0.2)

# S3 virada + logo
put(W(0.4, 500, 2400, 700), 5.03, 0.22)
put(W(0.4, 500, 2400, 700), 5.28, 0.22, 0.2)
put(riser(0.97), 5.45, 0.42)
put(W(0.65, 600, 5000, 900, 0.6, 1.4, 0.15), 5.86, 0.55, np.linspace(-0.8, 0.0, int(0.65 * SR)))
put(boom(1.6), 6.42, 0.95)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.06, 0.06, 0.08], 1.4, 3.2), 6.44, 0.22)
put(shimmer(1.0, 40), 6.44, 0.18)
put(shimmer(0.7, 24, 4000, 10000), 6.95, 0.13, 0.3)
put(W(0.45, 300, 3200, 600, 0.6), 7.40, 0.50)

# S4 como funciona
put(W(0.4, 500, 2400, 700), 7.70, 0.25)
put(W(0.22, 800, 4200, 2000, 0.5, 1.6, 0.2), 8.28, 0.30, 0.4)      # envio iMessage
put(pop(1250, 0.1), 8.33, 0.28, 0.4)
put(bell([1567.98, 2093.0], [0.075], 0.55, 8), 9.45, 0.30, -0.3)   # recebida
put(pop(1500, 0.08), 10.0, 0.22, 0.3)
put(W(0.38, 400, 3200, 800, 0.6), 10.47, 0.45, np.linspace(0.5, -0.6, int(0.38 * SR)))
for i in range(14):
    put(tick(3000 + (i % 3) * 300, 0.02), 10.80 + i * (0.5 / 14), 0.15, -0.1)
for i in range(3):
    put(pop(700 + i * 120, 0.09), 11.05 + i * 0.09, 0.18, 0.1 * i)
put(W(0.6, 1500, 6500, 2500, 0.5, 3.0, 0.3), 11.40, 0.18)
put(pop(980), 12.00, 0.40, 0.2)
put(pop(1400, 0.08), 12.15, 0.25, 0.3)
put(W(0.38, 400, 3200, 800, 0.6), 12.92, 0.45, np.linspace(0.5, -0.6, int(0.38 * SR)))
put(W(0.8, 150, 2600, 400, 0.6, 0.9), 13.12, 0.55)
put(shimmer(0.7, 26, 4000, 10000), 14.00, 0.13, 0.2)
put(bell([1318.51, 1661.22, 1975.53], [0.07, 0.07], 1.0, 4.5), 14.30, 0.26, 0.5)
put(W(0.45, 300, 4000, 600, 0.7, 1.0, 0.2), 15.30, 0.65)

# S5 pagamento
put(W(0.4, 500, 2400, 700), 15.60, 0.25)
put(W(0.5, 300, 2200, 500, 0.5), 16.18, 0.35)
put(W(0.6, 300, 2600, 500, 0.45), 16.44, 0.35, 0.1)
put(pop(1050), 16.68, 0.32)
put(bell([1046.5, 1318.51, 1567.98, 2093.0], [0.06, 0.06, 0.06], 1.1, 4.0), 16.80, 0.28)
put(W(0.35, 600, 3600, 900, 0.7, 1.3, 0.2), 17.80, 0.40, np.linspace(0.6, -0.2, int(0.35 * SR)))
put(W(0.45, 600, 2800, 700, 0.3, 1.3, 0.1), 18.15, 0.35, np.linspace(-0.2, 0.4, int(0.45 * SR)))
put(shimmer(0.8, 26), 18.60, 0.12, -0.2)
for i in range(11):
    x = i / 10
    put(tick(2200 + i * 60), 18.85 + x * 0.75, 0.17)
put(pop(760, 0.14), 19.60, 0.30)
put(W(0.5, 300, 3600, 500, 0.75, 1.0, 0.2), 20.10, 0.65)

# S6 CTA
put(W(0.4, 500, 2400, 700), 20.48, 0.25)
put(W(0.4, 500, 2400, 700), 20.92, 0.20, 0.2)
put(pop(820, 0.14), 21.45, 0.40)
put(W(0.5, 900, 2200, 1100, 0.5, 2.0), 21.90, 0.12, np.linspace(0.6, 0.0, int(0.5 * SR)))
put(tick(3800, 0.03), 22.45, 0.45)
put(np.tanh(sine_sweep(160, 90, 0.09, 45) * 2), 22.45, 0.55)
put(shimmer(0.5, 14, 3000, 8000), 22.55, 0.10)
put(W(0.45, 300, 3200, 600, 0.75, 1.0, 0.15), 23.18, 0.55)
put(boom(1.6), 23.42, 0.75)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.07, 0.07, 0.09], 1.6, 2.8), 23.45, 0.22)
put(shimmer(1.2, 40), 23.6, 0.14)

# ---------------------------------------------------------------- master
st = np.stack([L, R], axis=1)
st = np.tanh(st * 1.15) / np.tanh(1.15)       # glue/soft clip
st /= np.abs(st).max()
st *= 0.89
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', sys.argv[1])
