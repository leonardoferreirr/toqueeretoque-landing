# Toque & Retoque — landing

Landing de conversão para a **Toque & Retoque Acabamentos**, loja de acabamentos
com mais de 25 anos e três lojas no Rio Grande do Sul (Taquara, Gramado e Novo
Hamburgo). Construída a partir do Raio-X de campanha preenchido pela Juliane
Nunes, para receber o tráfego pago.

Estático puro: HTML + CSS + um arquivo de JS sem dependência.

## Rodar local

```
npx serve -l 8859 .
```

## Depois de editar o CSS

O CSS é servido **inline** dentro do `index.html`, porque como arquivo ele
bloqueava a primeira pintura no celular. A fonte da verdade é
`assets/css/site.css`. Depois de editar:

```
python3 build.py
```

## O que o briefing determinou

O Raio-X responde perguntas que a landing precisa refletir, e nem todas são
óbvias no código:

- **Porcelanato é a prioridade número 1** das campanhas (ticket médio R$5 mil,
  boa disponibilidade nas três cidades). Por isso ele tem seção própria e
  aparece primeiro no menu.
- **A vantagem mais afiada é pronta-entrega.** No mercado de acabamento o medo
  real é a obra parar esperando material, e o cliente tem estoque próprio. Daí
  a headline "Escolheu hoje, sai hoje".
- **O FAQ não foi inventado.** As seis perguntas são exatamente as que o
  briefing lista como mais comuns no atendimento: preço, estoque, entrega na
  cidade, amostra, instalação e atendimento a arquiteto.
- **Público duplo:** consumidor final construindo ou reformando *e* arquitetos.
  Boa parte das vendas vem de indicação de projeto, por isso a última pergunta
  do FAQ é dedicada a profissionais.

## Identidade

Paleta amostrada do logotipo, não escolhida no olho:

| | |
|---|---|
| `#183084` | azul-royal, 74,6% dos pixels do logo |
| `#F05418` | laranja, 25,4% |
| `#0B7A3B` | verde, **exclusivo de CTA** |

O site antigo usava o laranja em ondas gigantes e chapadas, e a cor cansava.
Aqui ela é acento: número, fio acima do título, palavra em destaque. O verde
não aparece em mais nada além de botão, porque é a única coisa que pede clique.

Tipografia: Archivo (display, casa com o logotipo geométrico) + Manrope
(corpo). Self-hosted, com `font-display: optional` para não gerar CLS.

## Decisões que não são óbvias no código

- **Todo CTA passa por `obrigado.html`.** A página dispara o evento de conversão
  e só então abre o WhatsApp. Link direto para `wa.me` sai do site sem deixar
  rastro de que o lead converteu.
- **A mensagem vai por query e por `sessionStorage`.** Servidor com URL limpa
  redireciona `/obrigado.html` para `/obrigado`, e há quem descarte a query
  nesse pulo. O lead chegaria no WhatsApp com a conversa em branco.
- **A gravação acontece no clique, não ao montar os `href`.** O laço passa por
  todos os CTAs; gravar ali faria o último sobrescrever a mensagem de todos, e
  o lead da loja de Gramado sairia com a frase do rodapé.
- **Cada CTA tem a sua própria mensagem.** O texto do botão é o mesmo em todos
  ("Conversar com um especialista"), mas quem clica no card de Taquara abre a
  conversa dizendo que quer falar com Taquara. É invisível para o visitante e
  útil para quem atende.
- **A fita e a vitrine esmaecem com camada de cor, não com máscara.** Máscara
  não esmaece, ela fura, e o que apareceria nas bordas seria o fundo da página.

## Gate

Lighthouse com `--throttling-method=devtools` (o modo `simulate` é pessimista e
infla o LCP em cerca de 9 pontos):

| | perf | a11y | BP | SEO | LCP |
|---|---|---|---|---|---|
| mobile | 100 | 100 | 100 | 100 | 1,0 s |
| desktop | 100 | 100 | 100 | 100 | 0,2 s |

CLS zero. Duas rodadas por formato, para descartar cold start.

Verificado em Chromium e WebKit, em desktop, tablet e mobile: 8 seções, 11 CTAs
todos com o mesmo texto, galeria em largura única, nenhuma foto quebrada, sem
overflow horizontal, zero erro de JS. Os cinco caminhos de CTA testados ponta a
ponta, cada um chegando ao WhatsApp com a sua frase.

## A confirmar com o cliente

- **O WhatsApp tem conflito.** O site atual usa `51 8914-0112` em todos os
  botões; o Raio-X informa `51 99666-8832` (da Juliane). A landing usa o do
  Raio-X, por ser o documento da campanha. Confirmar qual recebe os leads.
- **Existe uma quarta loja, em Palhoça (SC)**, que o Raio-X não menciona e o
  site antigo mostra. As melhores fotos de showroom são de lá e estão em uso
  como "nossos showrooms", sem atribuição de cidade. O briefing manda focar em
  Taquara, Gramado e Novo Hamburgo, então Palhoça ficou fora da seção de lojas.
- **Os números do hero** (25 anos, 3 lojas) vieram do título da página do site
  atual e do briefing. Confirmar se seguem corretos.
- **As marcas da fita** vieram do briefing e do site. Confirmar se todas seguem
  ativas como parceiras antes de publicar.
