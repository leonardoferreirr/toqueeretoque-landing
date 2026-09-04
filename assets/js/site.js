/* TOQUE & RETOQUE — comportamento da pagina */
(function () {
  'use strict';

  var NUM = '5551996668832';
  var MSG = 'Ola! Vim pelo site da Toque & Retoque e quero um orcamento.';

  /* Todo CTA passa por obrigado.html antes de abrir a conversa: a pagina
     dispara o evento de conversao e so entao redireciona. Link direto pro
     wa.me sai do site sem deixar rastro de que o lead converteu.

     A mensagem vai por dois caminhos de proposito. A query e o caminho
     normal, mas quem serve o site com URL limpa redireciona /obrigado.html
     para /obrigado, e ha servidor que descarta a query nesse pulo -- o lead
     chega no WhatsApp sem nada escrito, justamente o que o formulario existe
     pra evitar. O sessionStorage sobrevive ao redirecionamento. */
  function ponte(msg) {
    return 'obrigado.html?n=' + NUM + '&t=' + encodeURIComponent(msg || MSG);
  }
  /* Guardar no CLIQUE, nunca ao montar os href: o laco abaixo passa por todos
     os CTAs, e gravar ali faria o ultimo link sobrescrever a mensagem de todos
     os outros -- o lead da loja de Gramado sairia com a frase do rodape. */
  function guarda(msg) {
    try { sessionStorage.setItem('tr_wa', JSON.stringify({ n: NUM, t: msg || MSG })); } catch (e) {}
  }
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    var msg = a.dataset.wa || '';
    a.href = ponte(msg);
    a.addEventListener('click', function () { guarda(msg); });
  });

  /* nav: fundo solido depois que sai do topo -------------------------------- */
  var nav = document.querySelector('.nav');
  var ultimo = -1;
  function pintaNav() {
    var fixa = window.scrollY > 40;
    if (fixa === ultimo) return;
    ultimo = fixa;
    nav.toggleAttribute('data-fixa', fixa);
  }
  pintaNav();
  addEventListener('scroll', pintaNav, { passive: true });

  /* gaveta mobile ----------------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var gaveta = document.getElementById('gaveta');
  function fecha() {
    gaveta.removeAttribute('data-aberta');
    document.body.classList.remove('travado');
    burger.setAttribute('aria-expanded', 'false');
  }
  burger.addEventListener('click', function () {
    var aberta = gaveta.toggleAttribute('data-aberta');
    document.body.classList.toggle('travado', aberta);
    burger.setAttribute('aria-expanded', aberta ? 'true' : 'false');
  });
  gaveta.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', fecha); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape') fecha(); });

  /* entrada das secoes ------------------------------------------------------ */
  var alvos = document.querySelectorAll('[data-sobe],[data-fade]');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('dentro'); obs.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    alvos.forEach(function (el) { obs.observe(el); });
  } else {
    alvos.forEach(function (el) { el.classList.add('dentro'); });
  }

  /* formulario: leva os dados para o WhatsApp -------------------------------- */
  var form = document.getElementById('lead');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var nome = (d.get('nome') || '').toString().trim();
      var loja = (d.get('loja') || '').toString().trim();
      var item = (d.get('item') || '').toString().trim();
      var obs = (d.get('obs') || '').toString().trim();

      var texto = 'Ola! Meu nome e ' + nome + ' e vim pelo site da Toque & Retoque.';
      if (item && item !== 'Ainda não sei') texto += ' Estou procurando ' + item + '.';
      if (item === 'Ainda não sei') texto += ' Ainda nao sei o que preciso e queria uma orientacao.';
      if (loja && loja !== 'Tanto faz') texto += ' A loja mais perto de mim e a de ' + loja + '.';
      if (obs) texto += ' ' + obs;

      guarda(texto);
      location.href = ponte(texto);
    });
  }

  /* vitrine: filtro por tipo + carrossel -------------------------------------- */
  var vitrine = document.getElementById('vitrine');

  if (vitrine) {
    var filtros = document.querySelectorAll('.filtro');
    var setas = document.querySelectorAll('.seta');
    var produtos = vitrine.querySelectorAll('.prod');

    /* O passo e medido no DOM, nao chutado: pega a distancia entre o comeco de
       dois cartoes visiveis seguidos e anda quantos cartoes couberem inteiros.
       Assim a seta acompanha o --vis do CSS sem repetir o numero aqui. */
    function passoEmPx() {
      var vis = Array.prototype.filter.call(produtos, function (p) { return !p.hidden; });
      if (vis.length < 2) return vitrine.clientWidth;
      var largura = vis[1].offsetLeft - vis[0].offsetLeft;
      var cabem = Math.max(1, Math.floor(vitrine.clientWidth / largura));
      return largura * cabem;
    }

    /* Margem de 2px: com scroll-snap e largura fracionada, o fim da trilha cai
       em valor quebrado e a seta ficaria acesa sem ter para onde ir. */
    function pintaSetas() {
      var fim = vitrine.scrollWidth - vitrine.clientWidth;
      setas.forEach(function (s) {
        s.disabled = Number(s.dataset.passo) < 0
          ? vitrine.scrollLeft <= 2
          : vitrine.scrollLeft >= fim - 2;
      });
    }

    setas.forEach(function (s) {
      s.addEventListener('click', function () {
        vitrine.scrollBy({ left: passoEmPx() * Number(s.dataset.passo), behavior: 'smooth' });
      });
    });
    vitrine.addEventListener('scroll', pintaSetas, { passive: true });
    addEventListener('resize', pintaSetas);
    pintaSetas();

    filtros.forEach(function (b) {
      b.addEventListener('click', function () {
        var alvo = b.dataset.filtro;
        filtros.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        produtos.forEach(function (p) {
          p.hidden = alvo !== 'todos' && p.dataset.tipo !== alvo;
        });
        /* Volta ao inicio: filtrar com a trilha no meio deixaria o visitante
           olhando para um vazio, ou para o fim de uma lista que encolheu. */
        vitrine.scrollTo({ left: 0, behavior: 'auto' });
        pintaSetas();
      });
    });
  }

  /* fita de marcas: laço sem emenda ------------------------------------------ */
  var fita = document.getElementById('trilho-marcas');
  var parado = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* O CSS anda a fita ate `-50% - gap/2`, que so cai em cima da copia se a
     lista estiver duplicada. Sem a copia, a fita chega ao fim, volta ao inicio
     e o corte aparece como um vazio depois do ultimo logo. A copia e o que
     fecha o laço: quando a trilha andou uma lista inteira mais um vao, a copia
     esta exatamente onde o original comecou. */
  if (fita && !parado) {
    Array.prototype.slice.call(fita.children).forEach(function (logo) {
      var copia = logo.cloneNode(true);
      copia.setAttribute('aria-hidden', 'true');
      copia.alt = '';
      fita.appendChild(copia);
    });

    /* Velocidade constante em vez de duracao fixa: com duracao fixa, mudar o
       numero de marcas muda a velocidade da fita. */
    var voltaEm = function () {
      var meia = fita.scrollWidth / 2;
      if (meia > 0) fita.style.setProperty('--dur', Math.round(meia / 48) + 's');
    };
    voltaEm();
    /* scrollWidth so fecha depois que os logos carregam. */
    if (document.readyState === 'complete') voltaEm();
    else addEventListener('load', voltaEm);
  }

  /* ano do rodape ------------------------------------------------------------ */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();
