# Fly Upper · vídeo CTA de 25s

Motion graphics 9:16 (1080×1920, 60 qps) no estilo Apple, com fundo branco, tipografia escura e acentos em azul-claro.

## Roteiro

| Tempo | Cena | Na tela | Gatilho |
|---|---|---|---|
| 0–2,4s | Hook | "Ainda pagando **caro** pra viajar?". "Caro" é riscado e preços com taxas flutuam ao fundo. | Dor |
| 2,4–5s | Curiosidade | "E se a sua próxima viagem custasse **bem menos?**". Card GRU → LIS em que o preço cai de R$ 4.890 para R$ 2.390. | Curiosidade / ganho |
| 5–7,7s | Virada | "Então você chegou ao lugar **certo.**". Um traço azul leva o avião até o logo. | Autoridade |
| 7,7–15,6s | Como funciona | 1) Você diz pra onde quer ir (iMessage). 2) A gente acha a melhor tarifa (busca + seleção). 3) Você só faz as malas (cartão de embarque no estilo Wallet). | Simplicidade |
| 15,6–20,5s | Pagamento | "Pague do seu jeito." Comprovante de Pix aprovado, que vira um cartão de crédito com "Parcele em até 12x". | Quebra de objeção |
| 20,5–25s | CTA | "Sua próxima viagem começa com uma **mensagem.**" Botão "Fale com a gente" com toque, depois o lockup do logo e @flyupperviagens. | CTA discreto |

## Como renderizar

```bash
./render.sh                        # 240 qps em 4 processos → tmix (motion blur) → 60 qps
python3 audio.py out/audio.wav     # desenho de som sintetizado
ffmpeg -i out/video60.mkv -i out/audio.wav -af loudnorm=I=-14:TP=-1 \
  -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart fly-upper-cta.mp4
```

Para revisar quadros soltos: `node stills.mjs pasta 3.0 6.5 12.4`. Para ver a animação em tempo real no navegador, abra `index.html#play`.

## Antes de publicar

- **Logo:** o símbolo (avião branco num quadrado azul-claro) e o wordmark são provisórios. Troque pelo logo oficial em `#mark`, `#emk` e no cabeçalho do cartão de embarque.
- **Preços, rota e "12x":** são valores de exemplo. Ajuste para ofertas e condições reais da Fly Upper.
- **Fonte:** o vídeo usa Inter Display, uma alternativa livre à SF Pro. Se tiver a SF Pro instalada, troque o `font-family` no topo do CSS.
- **Velocidade:** a curva principal é `cubic-bezier(0.5, 0, 0, 1)`, que equivale a 50% de influência na saída e 100% na chegada (o "100/50" do After Effects): arranque rápido e pouso longo e suave.
