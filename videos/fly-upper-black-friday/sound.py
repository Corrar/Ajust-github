"""Desenho de som: locução tratada, trilha do ElevenLabs editada por compassos e efeitos.

Tudo no mesmo relógio da animação (assets/words.js).

uso: python3 sound.py saida.wav
"""
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

SR = 48000
txt = open('assets/words.js').read()
VO = json.loads(re.search(r'window\.VO=(\{.*?\});\n', txt).group(1))
OFF, DUR = VO['offset'], VO['duration']
GAP_CUT, GAP = VO['gap']['cut'], VO['gap']['len']
W = VO['words']
K = lambda i: W[i]['s'] + OFF
KE = lambda i: W[i]['e'] + OFF
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(3)

kBlack, kFri, kE, kDec, kPass, kPac = K(2), K(3), K(6), K(13), K(14), K(16)
kPrec, kOutro, kMundo = K(18), K(20), K(21)
kFunc, kVoce, kGente, kTarifa, kE2, kMalas = K(22), K(24), K(30), K(35), K(36), K(41)
kPague, kPix, kParc, kCart, kMas, kOfer, kVoam = K(42), K(44), K(46), K(48), K(49), K(53), K(54)
kChama, kDirect, eDirect = K(55), K(59), KE(59)
e0 = eDirect + 0.45


# ------------------------------------------------------------------ utilidades
def load(path, af=None, ch=2):
    cmd = ['ffmpeg', '-v', 'error', '-i', path]
    if af:
        cmd += ['-af', af]
    cmd += ['-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32).astype(float)
    return a.reshape(-1, ch) if ch > 1 else a


def norm(s):
    return s / (np.abs(s).max() + 1e-9)


def onset(sig, thr_db=-30):
    """Primeira amostra acima do limiar (relativo ao pico) — para alinhar o ataque do efeito ao corte."""
    m = np.abs(sig if sig.ndim == 1 else sig.mean(1))
    idx = np.where(m > m.max() * 10 ** (thr_db / 20))[0]
    return idx[0] / SR if len(idx) else 0.0


def peak_time(sig, win=0.05):
    m = sig if sig.ndim == 1 else sig.mean(1)
    w = int(win * SR)
    e = np.convolve(m ** 2, np.ones(w) / w, 'same')
    return np.argmax(e) / SR


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
    click = rng.standard_normal(len(s)) * np.exp(-np.arange(len(s)) / SR * 90) * 0.3
    lp, _, _ = svf(click, np.full(len(s), 1800.0))
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
        s = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * f * 2.01 * t) + 0.06 * np.sin(2 * np.pi * f * 3.98 * t)
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


def fft_conv(x, ir):
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:n]


def make_ir(dur=1.4, decay=4.0, seed=0, predelay=0.018, damp=8):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-t * decay)
    ir = np.convolve(ir, np.ones(damp) / damp, 'same')          # amortece os agudos
    ir = np.concatenate([np.zeros(int(predelay * SR)), ir])
    return ir / np.sqrt((ir ** 2).sum())


IR_L, IR_R = make_ir(seed=1), make_ir(seed=2)


def lowpass1(x, a):
    """Passa-baixa de 1 polo vetorizado o suficiente para trechos curtos."""
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc)
        y[i] = acc
    return y


# ------------------------------------------------------------------ barramentos
FX = np.zeros((N, 2))
MUS = np.zeros((N, 2))
VOX = np.zeros((N, 2))
REV_SEND = np.zeros(N)


def put(sig, t0, gain=1.0, pan=0.0, bus=None):
    bus = FX if bus is None else bus
    if sig.ndim == 2:
        sig = sig.mean(1) if pan is not None else sig
    i = int(round(t0 * SR))
    if i < 0:
        sig, i = sig[-i:], 0
    if i >= N:
        return
    sig = sig[: N - i] * gain
    p = np.asarray(pan, dtype=float)
    p = p[: len(sig)] if p.ndim else np.full(len(sig), float(p))
    if len(p) < len(sig):
        p = np.concatenate([p, np.full(len(sig) - len(p), p[-1] if len(p) else 0.0)])
    bus[i:i + len(sig), 0] += sig * np.cos((p + 1) * np.pi / 4)
    bus[i:i + len(sig), 1] += sig * np.sin((p + 1) * np.pi / 4)


def lin_pan(a, b, dur):
    return np.linspace(a, b, int(dur * SR))


def efx(name):
    p = f'assets/sfx/{name}.mp3'
    return norm(load(p, ch=1)) if os.path.exists(p) else None


# ------------------------------------------------------------------ locução
MAIN_CHAIN = ('highpass=f=80,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3800:t=q:w=1.2:g=3,'
              'highshelf=f=9000:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3')
PA_CHAIN = ('highpass=f=380,lowpass=f=3300,equalizer=f=1800:t=q:w=1:g=5,'
            'acompressor=threshold=-26dB:ratio=6:attack=2:release=60:makeup=6,aecho=0.8:0.55:23|41:0.22|0.14')
vo_main = load('assets/locucao.mp3', MAIN_CHAIN, ch=1)
vo_pa = load('assets/locucao.mp3', PA_CHAIN, ch=1)
vo_main = np.tanh(norm(vo_main) * 1.5) / np.tanh(1.5)            # saturação leve: voz mais "na cara"
vo_pa = np.tanh(norm(vo_pa) * 2.2) / np.tanh(2.2) * 0.9


def vo_place(src):
    """Coloca a locução no relógio do vídeo, abrindo o respiro antes do 'Funciona assim'."""
    out = np.zeros(N)
    c = int(GAP_CUT * SR)
    a, b = int(OFF * SR), int((OFF + GAP_CUT + GAP) * SR)
    out[a:a + c] = src[:c][: N - a]
    rest = src[c:][: N - b]
    out[b:b + len(rest)] = rest
    return out


V = vo_place(vo_main)
VPA = vo_place(vo_pa)

# trecho "Funciona assim:" com cara de aviso de bordo (crossfade de 30 ms)
pa_w = np.zeros(N)
s0, s1 = K(22) - 0.06, KE(23) + 0.12
xf = 0.03
pa_w = np.clip(np.minimum((t_all - s0) / xf, (s1 - t_all) / xf), 0, 1)
voice = V * (1 - pa_w) + VPA * pa_w

# pan do sussurro: o "Psiu…" passeia de um ouvido ao outro
pan = np.zeros(N)
ps0, ps1 = K(0) - 0.05, KE(0) + 0.15
pan += np.where((t_all >= ps0) & (t_all < ps1), np.interp(t_all, [ps0, ps1], [-0.55, 0.55]), 0)
VOX[:, 0] += voice * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
VOX[:, 1] += voice * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)

# reverb: mais no sussurro (íntimo e espacial), quase nada no resto
send = np.interp(t_all, [0, KE(5), KE(5) + 0.3, DUR], [0.30, 0.30, 0.06, 0.06])
REV_SEND += voice * send


def echo_throw(i_word, start_frac=0.35, taps=5, delay=60 / 124 / 2, fb=0.5, gain=0.55):
    """Ecos em pingue-pongue no final da palavra, cada repetição mais escura e fina."""
    s, e = K(i_word), KE(i_word)
    a = int((s + (e - s) * start_frac) * SR)
    b = int((e + 0.05) * SR)
    seg = voice[a:b].copy()
    seg *= np.hanning(len(seg)) ** 0.3
    for k in range(1, taps + 1):
        rep = lowpass1(seg, max(0.08, 0.6 / k))
        rep = rep - lowpass1(rep, 0.02)                            # tira o grave das repetições
        put(rep, a / SR + k * delay, gain * fb ** (k - 1), -0.7 if k % 2 else 0.7, bus=VOX)


echo_throw(13)                     # DECOLAR!
echo_throw(54, gain=0.6)           # VOAM!
echo_throw(59, start_frac=0.5, taps=3, gain=0.3)   # direct

# reverb invertido puxando o "E aqui na Fly Upper"
a, b = int(K(6) * SR), int((K(6) + 0.55) * SR)
rv = fft_conv(voice[a:b], IR_L[: int(1.2 * SR)])
rv = rv[::-1]
rv = rv / (np.abs(rv).max() + 1e-9)
put(rv, K(6) - len(rv) / SR + 0.02, 0.32, lin_pan(-0.4, 0.2, len(rv) / SR), bus=VOX)

# ------------------------------------------------------------------ trilha (ElevenLabs, editada por compassos)
mus = load('assets/trilha.mp3')
mus_lp = load('assets/trilha.mp3', 'lowpass=f=650,lowpass=f=650')
BAR = 4 * 60 / 124


def mseg(dst, v0, v1, src, m0, fade=0.025, gain=1.0):
    """Copia música[m0..] para o vídeo[v0..v1) com fades curtos nas emendas."""
    a, b = int(v0 * SR), int(v1 * SR)
    f = int(fade * SR)
    a2, b2 = max(0, a - f), min(N, b + f)
    m_a = int(m0 * SR) - (a - a2)
    seg = src[m_a:m_a + (b2 - a2)]
    if len(seg) < b2 - a2:
        seg = np.vstack([seg, np.zeros((b2 - a2 - len(seg), 2))])
    w = np.ones(b2 - a2)
    w[:2 * f] = np.linspace(0, 1, 2 * f) if a > 0 else 1
    w[-2 * f:] = np.minimum(w[-2 * f:], np.linspace(1, 0, 2 * f))
    dst[a2:b2] += seg * w[:, None] * gain


DROP, LIGHT = 15.0, 7.74
mseg(MUS, 0, kDec, mus, 5.8 - kDec)                                      # intro etérea: termina no 1º tempo da música
v = kDec
mseg(MUS, v, v + 2 * BAR, mus, DROP)                                        # DECOLAR → drop
v += 2 * BAR
mseg(MUS, v, v + 2 * BAR, mus, LIGHT, gain=0.9)                             # aviso de bordo / como funciona: groove leve
v += 2 * BAR
while v < kMas - 0.01:                                                      # energia até o "Mas corre"
    v1 = min(kMas, v + 2 * BAR)
    mseg(MUS, v, v1, mus, DROP)
    v = v1
mseg(MUS, kMas, kVoam, mus_lp, 1.6, gain=1.3)                               # tensão: tudo abafado
mseg(MUS, kVoam, DUR, mus, DROP)                                            # VOAM → drop de volta até o fim
MUS *= np.clip((DUR - t_all) / 1.6, 0, 1)[:, None] * np.clip(t_all / 0.4, 0, 1)[:, None]

# ------------------------------------------------------------------ efeitos
E_notif, E_braam, E_jet, E_chime = efx('notificacao'), efx('braam'), efx('jato'), efx('chime')
E_cash, E_whoosh, E_nfc = efx('caixa'), efx('whoosh'), efx('aproximacao')


def put_on(sig, cue, gain, pan=0.0, align='onset'):
    """Alinha o ataque (ou o pico) do efeito ao momento da animação."""
    if sig is None:
        return
    off = onset(sig) if align == 'onset' else peak_time(sig)
    put(sig, cue - off, gain, pan)


def wh(cue, gain=0.4, pan=0.0, dur=0.45, f1=3200):
    """Whoosh em camadas: corpo sintetizado + o 'swish' do ElevenLabs no ponto de corte."""
    put(whoosh(dur, 400, f1, 700, 0.6), cue - dur * 0.6, gain * 0.8, pan)
    if E_whoosh is not None:
        put_on(E_whoosh, cue, gain * 0.7, pan, align='peak')


# abertura
put_on(E_notif, 0.22, 0.55, 0.15)
put(whoosh(0.4, 600, 3000, 900), 0.08, 0.12, -0.3)
put_on(E_braam, kBlack - 0.04, 0.55)
put(boom(1.2, 120, 50), kFri - 0.05, 0.22)
put(shimmer(0.8, 24), kFri, 0.08)
put(riser(1.1), kE - 1.1, 0.30)
wh(kE - 0.18, 0.7)
put(whoosh(0.7, 200, 5200, 600, 0.55, 0.9, 0.3), kE - 0.45, 0.4)
# decolagem
put(riser(0.9), kDec - 0.85, 0.30)
put_on(E_jet, kDec + 0.35, 1.0, lin_pan(-0.4, 0.5, 3.2), align='peak')
put(boom(1.8), kDec + 0.35, 0.8)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.06, 0.06, 0.08], 1.4, 3.2), kDec + 0.42, 0.16)
put(shimmer(1.0, 40), kDec + 0.42, 0.12)
# ofertas: pílula → card → linha → card → planeta
put(pop(1150, 0.1), kPass, 0.35)
put(whoosh(0.45, 500, 4200, 1500, 0.7, 1.4, 0.2), kPass + 0.1, 0.30)
for i in range(6):
    put(tick(3600 + i * 120, 0.02), kPass + 0.34 + i * 0.035, 0.10, 0.1)
wh(kPac - 0.02, 0.55, lin_pan(0.5, -0.7, 0.8))
put(whoosh(0.55, 1500, 7000, 2500, 0.5, 2.2, 0.35), kPac - 0.08, 0.22, lin_pan(-0.6, 0.6, 0.55))
for i in range(6):
    put(tick(3600 + i * 120, 0.02), kPac + 0.28 + i * 0.035, 0.10, -0.1)
put(pop(900, 0.12), kPac + 0.45, 0.28, 0.2)
put(pop(1300, 0.1), kPrec, 0.38, -0.3)
put(shimmer(0.9, 34), kOutro - 0.12, 0.16)
put(boom(1.4, 90, 45), kOutro - 0.05, 0.4)
put(whoosh(0.9, 300, 2600, 600, 0.5, 1.0), kOutro + 0.05, 0.28, lin_pan(-0.8, 0.8, 0.9))
put(pop(1500, 0.08), kMundo, 0.22, -0.5)
put(pop(1700, 0.08), kMundo + 0.08, 0.2, 0.5)
# aviso de bordo + como funciona
put_on(E_chime, kFunc - 1.0, 0.75)
wh(kFunc - 0.15, 0.35, lin_pan(0.5, -0.5, 0.8))
put(whoosh(0.22, 800, 4200, 2000, 0.5, 1.6, 0.2), kVoce - 0.05, 0.25, 0.4)
put(pop(1250, 0.1), kVoce, 0.25, 0.4)
put(bell([1567.98, 2093.0], [0.075], 0.55, 8), kVoce + 0.42, 0.22, -0.3)
wh(kGente + 0.15, 0.35, lin_pan(0.5, -0.6, 0.8))
for i in range(12):
    put(tick(3000 + (i % 3) * 300, 0.02), kGente + 0.2 + i * 0.03, 0.10, -0.1)
for i in range(3):
    put(pop(700 + i * 120, 0.09), kGente + 0.4 + i * 0.07, 0.14, 0.1 * i)
put(whoosh(0.6, 1500, 6500, 2500, 0.5, 3.0, 0.3), kGente + 0.65, 0.12)
put(pop(980), kTarifa - 0.15, 0.32, 0.2)
put(pop(1400, 0.08), kTarifa, 0.22, 0.3)
wh(kE2 - 0.1, 0.35, lin_pan(0.5, -0.6, 0.8))
put(whoosh(0.7, 150, 2600, 400, 0.6, 0.9), kE2 - 0.1, 0.35)
put(shimmer(0.7, 26, 4000, 10000), kE2 + 0.55, 0.09, 0.2)
put(bell([1318.51, 1661.22, 1975.53], [0.07, 0.07], 1.0, 4.5), kMalas, 0.2, 0.5)
# pagamento
wh(kPague - 0.12, 0.35, lin_pan(0.5, -0.5, 0.8))
put(pop(1050), kPix - 0.05, 0.22)
if E_cash is not None:
    put_on(E_cash, kPix + 0.02, 0.6)
else:
    put(bell([1046.5, 1318.51, 1567.98, 2093.0], [0.06, 0.06, 0.06], 1.0, 4.0), kPix + 0.05, 0.22)
wh(kParc - 0.18, 0.32, lin_pan(0.6, -0.2, 0.8))
put(tick(2200, 0.03), kCart - 0.08, 0.28)
if E_nfc is not None:
    put_on(E_nfc, kCart + 0.05, 0.5)
# urgência
put_on(E_braam, kMas - 0.02, 0.4)
put(boom(1.6, 80, 32), kMas - 0.02, 0.5)
secs_prev = None
for tt in np.arange(kMas + 0.1, kVoam, 1 / 240):
    p = min(1, max(0, (tt - (kMas + 0.1)) / (kVoam - (kMas + 0.1))))
    s = max(0, round(59 * (1 - p * 0.97)))
    if s != secs_prev and secs_prev is not None:
        put(tick(2000 if s % 2 else 2400, 0.03), tt, 0.16, 0.3 if s % 2 else -0.3)
    secs_prev = s
put(riser(kVoam - kMas), kMas, 0.3)
for d, pn in ((0, -0.5), (0.07, 0.5), (0.14, 0.3)):
    put(pop(900 + d * 2000, 0.1), kOfer - 0.1 + d, 0.2, pn)
put_on(E_jet, kVoam + 0.4, 0.8, lin_pan(-0.85, 0.85, 3.2), align='peak')
put(boom(1.4), kVoam, 0.6)
# CTA + final
wh(kChama - 0.2, 0.4)
put(pop(820, 0.14), kChama, 0.3)
put(whoosh(0.5, 900, 2200, 1100, 0.5, 2.0), kChama + 0.35, 0.08, lin_pan(0.6, 0, 0.5))
put(tick(3800, 0.03), kDirect, 0.4)
put(np.tanh(sweep(160, 90, 0.09, 45) * 2), kDirect, 0.45)
put(shimmer(0.5, 14, 3000, 8000), kDirect + 0.1, 0.08)
wh(eDirect + 0.3, 0.4)
put(boom(1.8), e0, 0.7)
put(bell([1174.66, 1479.98, 1760.0, 2349.32], [0.07, 0.07, 0.09], 1.8, 2.6), e0 + 0.02, 0.2)
put(shimmer(1.2, 40), e0 + 0.2, 0.11)

# ------------------------------------------------------------------ mix
rev = np.stack([fft_conv(REV_SEND, IR_L)[:N], fft_conv(REV_SEND, IR_R)[:N]], axis=1)

env = np.abs(VOX.mean(1))
win = int(0.03 * SR)
env = np.minimum(1, np.convolve(env, np.ones(win) / win, 'same') / 0.06)
sm = np.empty_like(env)
acc, kk = 0.0, np.exp(-64 / (0.25 * SR))
for j in range(0, N, 64):
    acc = max(env[j], acc * kk)
    sm[j:j + 64] = acc
duck = (1 - 0.72 * sm)[:, None]

stem = os.environ.get('STEM')                        # STEM=voz|fundo exporta só uma parte (conferência de mix)
gv, gb = (1, 0) if stem == 'voz' else (0, 1) if stem == 'fundo' else (1, 1)
fx_duck = (1 - 0.35 * sm)[:, None]                 # efeitos também cedem um pouco à voz
mix = (VOX * 0.95 + rev * 0.9) * gv + (FX * fx_duck * 0.5 + MUS * duck * 0.42) * gb
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix * 0.89 / 1.0 if stem else mix / np.abs(mix).max() * 0.89
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', sys.argv[1], f'{DUR:.2f}s')
