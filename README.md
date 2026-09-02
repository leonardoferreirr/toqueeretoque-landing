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

## O que veio do site antigo deles

A primeira versão desta landing ficou parecida demais com as outras que fiz para
clientes de revestimento, e virou template. A correção foi partir do site antigo
do cliente e ficar com o que ali tinha personalidade:

- **A curva entre seções.** Lá ela ocupava meia tela e era chapada de laranja;
  aqui é uma faixa fina de 40 a 80px que só costura uma seção na outra. É a
  assinatura visual deles e a única coisa daquele site que valia manter.
- **A faixa de marcas em azul com logotipo branco.** É como o cliente já
  apresenta os parceiros, e os arquivos que eles têm são justamente a versão
  monocromática branca.
- **A seção de equipes em círculo.** Era a parte mais humana do site antigo
  ("Conheça nossa família"). Numa compra de ticket alto e presencial, saber quem
  vai atender pesa. Mantida, com a moldura mais discreta.

## Os logotipos das marcas

Os dez vieram da biblioteca de mídia do próprio cliente. Nove já eram versão
branca sobre transparente. **A Tramontina deu trabalho e vale o registro:** o
arquivo dela é uma caixa azul sólida com o texto em *recorte*, não em tinta
branca. Filtrar por "pixel branco" não acha nada, e filtrar por "pixel azul"
descarta as letras, porque em pixel totalmente transparente o RGB é lixo
(`43,43,41`) e não azul. O jeito que funciona é achar o retângulo da caixa pelo
alfa, encolher a margem para descartar o canto arredondado, e **inverter o alfa**
dentro dele.

A **Decortiles** também precisou de tratamento: o logotipo empilha símbolo e
palavra, então ao normalizar pela caixa a palavra encolhia e a marca aparecia
menor que as vizinhas. Ficou só a palavra.

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
- **A vitrine esmaece com camada de cor, não com máscara.** Máscara não esmaece,
  ela fura, e o que apareceria nas bordas seria o fundo da página.
- **As curvas são SVG com `preserveAspectRatio="none"`**, então esticam na
  largura sem deformar a altura. O `.onda` carrega a cor da seção de cima e o
  `path` é preenchido com a cor da de baixo.

## Gate

Lighthouse com `--throttling-method=devtools` (o modo `simulate` é pessimista e
infla o LCP em cerca de 9 pontos):

| | perf | a11y | BP | SEO | LCP |
|---|---|---|---|---|---|
| mobile | 99 | 100 | 100 | 100 | 2,0 s |
| desktop | 99 | 100 | 100 | 100 | 1,0 s |

Caiu de 100 para 99 quando o hero virou claro: a foto passou a ser o elemento de
LCP real, o que antes não acontecia com o hero escuro de fundo. É o custo do
layout que o cliente pediu, e segue acima do gate de 95.

CLS zero. Duas rodadas por formato, para descartar cold start.

Verificado em Chromium e WebKit, em desktop, tablet e mobile: 10 seções, 5
curvas com altura consistente, 10 logotipos, 4 equipes, 12 CTAs todos com o
mesmo texto, galeria em largura única, nenhuma foto quebrada, sem overflow
horizontal, zero erro de JS. Os caminhos de CTA testados ponta a ponta, cada um
chegando ao WhatsApp com a sua frase.

## Revisão do cliente (2026-09-02)

O cliente devolveu 10 páginas de revisão. O eixo: **o público é alto padrão**, e a
copy precisa comunicar isso. Palavras dele: os textos estavam "grosseiros" e não
refletiam o posicionamento de loja especializada com atendimento consultivo.

Correções factuais que ele apontou, e que eu tinha errado:

- **São 29 anos, não 25.** Em abril de 2027 completam 30.
- **Não há estoque em todas as lojas.** A distribuição sai da central em Taquara.
  Quem compra em Novo Hamburgo não retira na hora. O correto é comunicar um mix
  com boa parte a pronta entrega, nunca "estoque na loja".
- **A foto que eu rotulei como equipe de Novo Hamburgo era da equipe de Palhoça.**
- **O WhatsApp é o da loja**, não o do Raio-X.

Mudanças de direção:

- **Layout claro.** O hero escuro saiu: o material do próprio cliente é branco com
  azul e laranja entrando como forma geométrica no canto, e é isso que o hero
  reproduz agora.
- **Headline de realização**, no lugar de "Escolheu hoje, sai hoje".
- **Porcelanato e piso vinílico ganharam espaço próprio e lado a lado**, como no
  Fino Acabamento, porque a dúvida real do cliente costuma ser entre um e outro.
- **A seção de equipes virou o método de atendimento em quatro etapas.** Os times
  mudaram em todas as lojas e o cliente pediu sugestão, com copy voltada ao
  atendimento consultivo. Mostrar o percurso comunica isso melhor que foto posada
  e não depende de material que ainda não existe. Quando as fotos de atendimento
  chegarem, cada etapa comporta uma imagem.
- **Docol saiu da faixa de marcas**, a pedido.

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
- **Os dez logotipos** vieram da biblioteca de mídia do próprio cliente.
  Confirmar se todas as marcas seguem ativas como parceiras antes de publicar.
- **A Deca aparece no briefing mas não tem logotipo** na biblioteca deles, então
  ficou fora da faixa. Se for parceira ativa, vale pedir o arquivo.
