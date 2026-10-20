# Fly Upper · Black Friday · vídeo CTA

Motion graphics 9:16 (1080×1920, 60 qps, 24s) no estilo Apple, com a logo oficial da Fly Upper, locução do ElevenLabs e legendas sincronizadas palavra a palavra.

## Locução (ElevenLabs)

- **Voz:** Nassif · Persuasive Sales & Ads (pt-BR, masculina, confiante, com a urgência de um locutor de ofertas).
- **Modelo:** `eleven_v4`, com tags de emoção: sussurro no gancho, empolgação na decolagem, tom acolhedor no "como funciona" e drama na urgência.
- **Texto:**
  > [mischievously] [whispers] Psiu… a Black Friday tá chegando. [excited] E aqui na Fly Upper, ela vai DECOLAR! Passagens e pacotes com preços de outro mundo. [warmly] Funciona assim: você diz pra onde quer ir, a gente acha a melhor tarifa… e você só faz as malas. Pague no Pix ou parcele no cartão. [dramatically] Mas corre — que essas ofertas VOAM! [warmly] Chama a gente no direct.
- **Tomada usada:** a 1 de 4 (`assets/locucao.mp3`), escolhida por ter o maior contraste entre o sussurro e a empolgação.
- **Legendas:** transcrição do ElevenLabs Scribe com o tempo de cada palavra (`assets/transcricao.json`). O `cues.py` gera `assets/words.js`, que guia a animação, as legendas e os efeitos sonoros.

## Roteiro visual

| Fala | Cena |
|---|---|
| "Psiu… a Black Friday tá chegando." | Céu noturno com um avião piscando ao longe, notificação de iPhone da Fly Upper, depois BLACK / FRIDAY (o FRIDAY vazado) e uma barra de carregamento. |
| "E aqui na Fly Upper, ela vai DECOLAR!" | As nuvens estouram e a noite vira dia. O avião da Fly Upper voa sobre as nuvens com sombra projetada e, no "DECOLAR", sobe em direção à câmera com linhas de velocidade. Aparece a logo oficial com o selo BLACK FRIDAY. |
| "Passagens e pacotes com preços de outro mundo." | Cards no estilo Apple Store: Passagens (avião numa rota tracejada) e Pacotes (planeta com o avião em órbita). |
| "Funciona assim… melhor tarifa… faz as malas." | iMessage, busca com a "Preço Black Friday" selecionada e cartão de embarque no estilo Wallet com check. |
| "Pague no Pix ou parcele no cartão." | Pix aprovado, que gira e vira um cartão de crédito preto, com o seletor À vista / Parcelado. |
| "Mas corre — que essas ofertas VOAM!" | Volta a noite: um timer circular corre, as ofertas voam para fora da tela e o avião cruza deixando rastro. |
| "Chama a gente no direct." | Botão "Chamar no direct" com toque, depois a logo oficial, o selo BLACK FRIDAY e @flyupperviagens. |

## Como renderizar

```bash
python3 cues.py          # palavras + logo → assets/words.js
./render.sh              # vídeo (240 qps → motion blur → 60 qps) + som + mix → out/fly-upper-black-friday.mp4
```

Para revisar quadros soltos: `node stills.mjs pasta 1.6 5.6 19.2`. Para ver em tempo real, abra `index.html#play`, sem som.

## Antes de publicar

- As rotas e os preços dos cards (GRU → LIS, R$ 2.390 etc.) e os destinos do timer (Lisboa, Maceió, Nova York) são exemplos. Troque pelas ofertas reais da Black Friday.
- A trilha e os efeitos são sintetizados em `sound.py`, sem samples de terceiros. Para usar uma música licenciada, substitua o bloco "trilha" e mantenha o sidechain com a voz.
