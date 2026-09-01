#!/usr/bin/env python3
"""Injeta assets/css/site.css minificado dentro do <head> do index.html.

Por que inline: servido como arquivo, o CSS bloqueia a primeira pintura no
celular e derruba o Lighthouse. Inline, ele chega junto com o HTML.

A fonte da verdade continua sendo assets/css/site.css. Depois de editar o CSS,
rode este script.

    python3 build.py
"""
import hashlib, re, sys
from pathlib import Path

RAIZ = Path(__file__).parent
CSS  = RAIZ / "assets/css/site.css"
JS   = RAIZ / "assets/js/site.js"
HTML = RAIZ / "index.html"


def minificar(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    css = re.sub(r"\n{2,}", "\n", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def reancorar(css: str) -> str:
    """No arquivo, `../fonts/` sai de assets/css/ e chega em assets/fonts/.
    Inline no index.html, que esta na raiz, o mesmo caminho vira /fonts/ e da
    404: as fontes somem e a pagina cai no fallback sem avisar."""
    return re.sub(r"""url\((['"]?)\.\./""", r"url(\1assets/", css)


def versionar_script(html: str) -> tuple:
    """Carimba site.js com o hash do proprio conteudo.

    O Vercel serve /assets/ com max-age de um ano e immutable, o que so e
    seguro quando o nome do arquivo muda a cada versao. Com nome fixo, quem ja
    visitou fica um ANO com o JS velho."""
    if not JS.exists():
        return html, "-"
    v = hashlib.sha256(JS.read_bytes()).hexdigest()[:10]
    return re.sub(r'(src="assets/js/site\.js)(\?v=[a-f0-9]+)?"', rf'\1?v={v}"', html), v


def main() -> int:
    if not CSS.exists() or not HTML.exists():
        print("assets/css/site.css ou index.html nao encontrado", file=sys.stderr)
        return 1

    enxuto = reancorar(minificar(CSS.read_text(encoding="utf-8")))
    html = HTML.read_text(encoding="utf-8")

    if re.search(r"""url\((['"]?)\.\./""", enxuto):
        print("ainda ha caminho relativo ../ no CSS inline", file=sys.stderr)
        return 1

    ini, fim = html.find("<style>"), html.find("</style>")
    if ini == -1 or fim == -1:
        print("bloco <style> nao encontrado no index.html", file=sys.stderr)
        return 1

    novo, versao = versionar_script(html[:ini] + "<style>" + enxuto + html[fim:])
    if novo == html:
        print("nada mudou")
        return 0

    HTML.write_text(novo, encoding="utf-8")
    print(f"css -> {len(enxuto)} B | index.html {len(novo)} B | site.js?v={versao}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
