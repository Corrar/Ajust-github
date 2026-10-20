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
| "Passagens e pacotes com preços de outro mundo." | No estilo dos cards do Apple Maps: o botão-pílula "✈ Passagens" se expande num card com foto (Lisboa), com título digitado e espaçamento entre letras se fechando. No "pacotes", o card sai girando em 3D e uma linha azul leva até o card de Maceió. No "preços", entra o selo "Preço Black Friday". No "outro mundo", o card vira um planeta e a linha vira órbita, com o avião e as fotos dos destinos circulando. |
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

## Som

- **Voz** (`sound.py`):
  - EQ de locutor, compressão e saturação leve;
  - "Psiu…" passeando entre os ouvidos, com reverb íntimo;
  - reverb invertido puxando o "E aqui na Fly Upper";
  - ecos em pingue-pongue no "DECOLAR!", no "VOAM!" e no "direct";
  - "Funciona assim" com filtro de aviso de bordo, logo depois de um ding-dong de avião (a locução ganhou 0,55s de respiro nesse ponto).
- **Trilha:** gerada no ElevenLabs Music (`assets/trilha.mp3`, 124 BPM) e editada por compassos:
  - intro etérea sob o sussurro;
  - drop no "DECOLAR";
  - groove leve no "Funciona assim";
  - trecho abafado no "Mas corre";
  - drop de volta no "VOAM".
  
  A trilha abaixa sozinha quando a voz fala.
- **Efeitos:** gerados no ElevenLabs Sound Effects (`assets/sfx/`): notificação, braam, passagem de jato, ding-dong de bordo, "ka-ching" do Pix, aproximação do cartão e whoosh. Somam-se a pops, ticks e brilhos sintetizados, todos alinhados pelo ataque real de cada arquivo.
- `STEM=voz` ou `STEM=fundo` exportam só a voz ou só o fundo, para conferir a mixagem.

## Antes de publicar

- As rotas e os preços (GRU → LIS, R$ 2.390 etc.) e os destinos (Lisboa, Maceió, Nova York) são exemplos. Troque pelas ofertas reais da Black Friday.
- As fotos de Lisboa e Maceió foram geradas por IA (Seedream 5 Pro, via ElevenLabs). Se preferir, troque por fotos próprias em `assets/lisboa.jpg` e `assets/maceio.jpg`.
