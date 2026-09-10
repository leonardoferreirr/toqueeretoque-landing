#!/usr/bin/env python3
"""
Gera v2/index.html a partir do index.html.

A v2 e a mesma pagina em fundo claro do inicio ao fim: mesma copy, mesma
estrutura, mesmo JS. So muda a pele. Por isso ela e gerada, e nao copiada:
quando a copy mudar no index, basta rodar este script de novo.

    python3 build-v2.py

O que o script faz:
  1. le index.html
  2. injeta um bloco de override no fim do <style>
  3. corrige os caminhos relativos, ja que a v2 mora em /v2
  4. troca o theme-color e a canonical
"""
import hashlib
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- override
# Regra geral: o que era escuro vira claro, o que era texto claro vira tinta.
# A excecao sao os textos que ficam POR CIMA de foto (legendas da galeria, das
# lojas e o hero): esses continuam claros, senao somem no fundo da imagem.
PELE = """
/* ================= V2: a mesma pagina, em fundo claro =================
   Gerado por build-v2.py. Nao editar aqui: editar o index.html e rodar
   o script de novo. */
:root{
  --noite:#fff;--noite-2:#fbfaf9;--noite-3:#f3f1ee;
  --areia:#fff;--areia-2:#fbfaf9;
  --branco:#0b1224;
  --claro:#0b1224;--claro-2:#525c70;--claro-3:#6a7180;
  /* o cinza de apoio do tema escuro da 3,97:1 sobre branco. Em fundo claro ele
     precisa descer para passar em AA nos rotulos, no rodape e na ficha do produto */
  --tinta-3:#6a7180;
  --risco:rgba(11,18,36,.13);--risco-2:rgba(11,18,36,.07);
}
body{background:#fff;color:var(--tinta)}
h1,h2,h3{color:var(--tinta)}
.texto{color:var(--tinta-2)}

/* topo */
.nav__logo img,.rodape__logo img{filter:none}
.nav[data-fixa]{background:rgba(255,255,255,.9);border-bottom-color:rgba(11,18,36,.08)}
.gaveta{background:#fff}
.gaveta a{color:var(--tinta)}
.burger{color:var(--tinta)}

/* hero: o veu inverte, o texto escurece */
.hero__veu{background:
  linear-gradient(96deg,rgba(255,255,255,.96) 0%,rgba(255,255,255,.9) 40%,rgba(255,255,255,.55) 74%,rgba(255,255,255,.3) 100%),
  linear-gradient(0deg,rgba(255,255,255,.94) 0%,transparent 44%)}
.hero h1{color:var(--tinta)}
.hero .texto{color:var(--tinta-2)}

/* faixas e secoes */
.numeros{background:#fff;border-top-color:rgba(11,18,36,.08)}
.numeros__i{border-left-color:rgba(11,18,36,.08);border-top-color:rgba(11,18,36,.08)}
.numeros__n{color:var(--tinta)}
.numeros__r{color:var(--tinta-3)}
.numeros__i--frase .numeros__r{color:var(--tinta-2)}
.sec--fundo2{background:#fbfaf9}
.sec--claro{background:#fff}
.sec--areia2{background:#fbfaf9}
.marcas__t img{filter:none;opacity:.42}
.marcas__t img:hover{opacity:1}
.marcas__l{color:var(--tinta-3)}

/* produtos */
.item{border-top-color:rgba(11,18,36,.12)}
.sec:not(.sec--claro) .item{border-top-color:rgba(11,18,36,.12)}
.sec:not(.sec--claro) .item p{color:var(--tinta-2)}
.sec:not(.sec--claro) .item li{color:var(--tinta-2)}
.prod{background:#fff;border-color:rgba(11,18,36,.1)}
.prod:hover{border-color:rgba(240,84,24,.45)}
.prod__f{background:#f3f1ee}
.prod__n{color:var(--tinta)}
.prod__m{color:var(--tinta-3)}
.prod__m b{color:var(--tinta-2)}
.prod__cta{color:#0b7a3b}
.filtro{border-color:rgba(11,18,36,.16);color:var(--tinta-2)}
.filtro:hover{color:var(--tinta);border-color:var(--tinta-3)}
.seta{border-color:rgba(11,18,36,.16);color:var(--tinta)}
.seta:hover:not(:disabled){color:#160801}
.nota{color:var(--tinta-2)}

/* atendimento */
.passo{border-top-color:rgba(11,18,36,.12)}
.passo p{color:var(--tinta-2)}

/* instagram */
.insta__t a{background:#f3f1ee}
.insta__perfil{color:var(--tinta)}

/* contato */
.dados b{color:var(--tinta-3)}
.dados span,.dados a{color:var(--tinta)}
.form{background:#fbfaf9;border-color:rgba(11,18,36,.1)}
.campo label{color:var(--tinta-3)}
.campo input,.campo select,.campo textarea{background:#fff;border-color:rgba(11,18,36,.16);color:var(--tinta)}
.form__nota{color:var(--tinta-3)}

/* fechamento e rodape */
.final__cartao::before{background:linear-gradient(180deg,rgba(255,255,255,.93),rgba(255,255,255,.87))}
.final__cartao h2{color:var(--tinta)}
.final__cartao .texto{color:var(--tinta-2)}
.rodape{background:#fbfaf9;border-top-color:rgba(11,18,36,.08)}
.rodape p,.rodape h3{color:var(--tinta-3)}
.rodape li a{color:var(--tinta-2)}
.rodape__fim{color:var(--tinta-3)}
.rodape__g{border-bottom-color:rgba(11,18,36,.08)}

/* botoes e links */
.btn--vazado>span,.btn--vazado>i{color:var(--tinta);box-shadow:inset 0 0 0 1px rgba(11,18,36,.18)}
.btn--vazado:hover>span{background:rgba(11,18,36,.05)}
.mais{color:var(--tinta)}
.fq summary{color:var(--tinta)}
.fq details,.fq details:last-child{border-color:rgba(11,18,36,.12)}
.fq p{color:var(--tinta-2)}

/* o que fica POR CIMA de foto continua claro, senao some */
.peca__n,.loja__n{color:#fff}
.peca .mais,.loja .mais{color:rgba(255,255,255,.88)}
.loja__e{color:rgba(255,255,255,.82)}
"""


def carimbar_versao():
    """Carimba no index.html o hash do site.js.

    O vercel.json serve /assets/* como immutable por um ano, entao quem ja
    visitou o site guarda o JS por um ano. O unico jeito de entregar uma versao
    nova e mudar a URL, e a URL so muda se este carimbo mudar. Editar o site.js
    sem carimbar deixa todo visitante antigo com o script velho.
    """
    js = os.path.join(RAIZ, "assets", "js", "site.js")
    h = hashlib.sha1(open(js, "rb").read()).hexdigest()[:10]
    caminho = os.path.join(RAIZ, "index.html")
    s = open(caminho, encoding="utf-8").read()
    novo = re.sub(r"site\.js\?v=[0-9a-f]+", f"site.js?v={h}", s)
    if novo != s:
        open(caminho, "w", encoding="utf-8").write(novo)
        print(f"site.js carimbado como v={h}")
    return h


def gerar():
    carimbar_versao()
    origem = os.path.join(RAIZ, "index.html")
    destino_dir = os.path.join(RAIZ, "v2")
    os.makedirs(destino_dir, exist_ok=True)

    s = open(origem, encoding="utf-8").read()

    # 1. a pele entra no fim do <style>, para vencer tudo o que veio antes
    i = s.rindex("</style>")
    s = s[:i] + PELE + s[i:]

    # 2. a v2 mora em /v2, entao todo caminho relativo sobe um nivel.
    #    Uma regra so, porque srcset tem varios caminhos no mesmo atributo e
    #    trocar "atributo por atributo" deixa o segundo e o terceiro para tras.
    #    O lookbehind protege o que ja e absoluto (https://.../assets, /assets).
    s = re.sub(r'(?<![./\w])assets/', '../assets/', s)
    s = re.sub(r'(src|href)="(favicon|apple-touch)', r'\1="../\2', s)

    # 3. cabecalho
    s = s.replace('<meta name="theme-color" content="#183084">',
                  '<meta name="theme-color" content="#ffffff">')
    s = s.replace('<link rel="canonical" href="https://toqueeretoque.com/">',
                  '<link rel="canonical" href="https://toqueeretoque.com/">\n'
                  '<meta name="robots" content="noindex,follow">')
    s = s.replace("<title>", "<title>V2 · ", 1)

    destino = os.path.join(destino_dir, "index.html")
    open(destino, "w", encoding="utf-8").write(s)
    print(f"v2/index.html gerado, {len(s) // 1024} KB")


if __name__ == "__main__":
    gerar()
