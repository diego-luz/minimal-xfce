// Previa da area de trabalho e da tela de login, desenhada com as opcoes
// marcadas na pagina (antes de aplicar), e a galeria do fundo do login com o
// botao de escolher uma imagem. As cores repetem as do projeto.py.
"use strict";

const Previa = (() => {
  const DESTAQUE = "#1a73e8";
  // projeto.py: CORES_PAPEL (cima, baixo)
  const CORES_PAPEL = {
    grafite: ["#2b2f33", "#141618"], ardosia: ["#2a3340", "#141a21"], oliva: ["#2f352a", "#171a14"],
    areia: ["#3a352c", "#1c1a15"], vinho: ["#33262b", "#181214"],
  };
  // projeto.py: AMOSTRA (janela, titulo, texto, lateral, destaque, borda) e o fundo da barra
  const MODO = {
    escuro: {janela: "#2c2c2c", titulo: "#252525", texto: "#e6e6e6", lado: "#262626",
             linha: "rgba(255,255,255,.10)", barra: "rgba(20,23,26,.92)", ilha: "rgba(51,54,59,.90)"},
    claro:  {janela: "#fafafa", titulo: "#f2f2f2", texto: "#2b2b2b", lado: "#f5f5f5",
             linha: "rgba(0,0,0,.08)", barra: "rgba(250,250,250,.92)", ilha: "rgba(250,250,250,.88)"},
  };
  const CORES_DOCK = ["#4a90d9", "#3b3b3b", "#e66a2c", "#6aa84f"];
  const RELOGIO = {curto: "qui 08 out  10:40", completo: "qui, 08 de outubro de 2026  10:40", so_hora: "10:40"};

  let maximizada = false;
  let versaoPropria = 0;
  const faltam = new Set();
  const el = (tag, classe, texto) => {
    const e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texto !== undefined) e.textContent = texto;
    return e;
  };

  // o papel de parede: degrade ou cor lisa nas cores do projeto; "manter"
  // mostra o que esta na tela agora, em miniatura pela API
  function papelDe(e){
    if (e.papel === "manter") return {url: "/api/papel-atual.jpg"};
    const [cima, baixo] = CORES_PAPEL[e.cor_papel] || CORES_PAPEL.grafite;
    return {css: e.papel === "liso" ? cima : `linear-gradient(${cima}, ${baixo})`};
  }
  function fundoLoginDe(e){
    if (e.login_fundo === "propria") return {url: `/api/login-propria.jpg?v=${versaoPropria}`};
    return papelDe(e);
  }

  // imagem que pode nao existir (nenhuma escolhida, papel fora do xfdesktop):
  // o fundo listrado com o texto fica no lugar
  function pintarFundo(caixa, fundo, texto){
    const sem = () => {
      caixa.style.background = "";
      caixa.classList.add("sem-imagem");
      caixa.dataset.texto = texto;
    };
    if (fundo.css){ caixa.style.background = fundo.css; return; }
    if (!fundo.url || faltam.has(fundo.url)) return sem();
    caixa.style.backgroundImage = `url("${fundo.url}")`;
    const prova = new Image();
    prova.onerror = () => { faltam.add(fundo.url); sem(); };
    prova.src = fundo.url;
  }

  // ---- area de trabalho ---------------------------------------------------
  function desktop(e){
    const m = MODO[e.modo] || MODO.escuro;
    const tela = el("div", "pv-tela");
    tela.style.setProperty("--pv-acento", DESTAQUE);
    tela.style.setProperty("--pv-texto", m.texto);
    pintarFundo(tela, papelDe(e), "papel de parede atual");

    // icones da area de trabalho
    if (e.icones_area && e.icones_area !== "nenhum"){
      const icones = el("div", "pv-icones-area");
      const lista = e.icones_area === "tudo"
        ? [["🏠", "Pasta pessoal"], ["🗑", "Lixeira"], ["💾", "Pendrive"]] : [["💾", "Pendrive"]];
      lista.forEach(([i, n]) => { const d = el("div", "pv-icone"); d.append(el("span", "", i), el("small", "", n)); icones.appendChild(d); });
      tela.appendChild(icones);
    }

    const menu = () => {
      if (e.menu === "nenhum") return null;
      const b = el("span", "pv-menu");
      b.appendChild(el("i"));
      if (e.menu === "icone_texto") b.appendChild(el("span", "", "Aplicativos"));
      return b;
    };
    const tarefas = () => {
      if (e.barra_tarefas === "nenhuma") return el("span", "pv-esp");
      if (e.barra_tarefas === "botoes"){
        const t = el("div", "pv-botoes-jan");
        ["Arquivos", "Terminal"].forEach((n, i) => t.appendChild(el("span", i === 0 ? "ativo" : "", n)));
        return t;
      }
      const d = el("div", "pv-dock");
      CORES_DOCK.forEach((c, i) => { const x = el("i", i === 0 ? "ativo" : ""); x.style.background = c; d.appendChild(x); });
      return d;
    };
    const relogio = el("span", "pv-hora", RELOGIO[e.relogio] || RELOGIO.curto);
    const bandeja = el("span", "pv-bandeja", "◦ ◦ ◦");

    // a barra continua com a janela maximizada: ela reserva o espaco dela
    if (e.barra === "ilhas"){
      // barra fina solta no topo e as janelas numa ilha embaixo
      const topo = el("div", "pv-topo");
      topo.style.background = m.barra;
      [menu(), el("span", "pv-esp"), bandeja, relogio].forEach(x => x && topo.appendChild(x));
      const ilha = el("div", "pv-ilha");
      ilha.style.background = m.ilha;
      ilha.appendChild(tarefas());
      tela.append(topo, ilha);
    } else {
      const barra = el("div", "pv-barra " + (e.barra === "baixo" ? "baixo" : "topo"));
      barra.style.background = m.barra;
      const t = tarefas(); t.classList.add("pv-meio");
      [menu(), t, bandeja, relogio].forEach(x => x && barra.appendChild(x));
      tela.appendChild(barra);
    }

    // uma janela de arquivos do Orchis, com a selecao e o botao em azul
    const jan = el("div", "pv-janela" + (maximizada ? " cheia " + (e.barra || "topo") : "")
                          + (e.compacto === "nao" ? "" : " compacta"));
    jan.style.background = m.janela;
    jan.style.color = m.texto;
    const tit = el("div", "pv-tit");
    tit.style.background = m.titulo;
    tit.append(el("span", "", "Arquivos"), el("span", "pv-botoes", "–  ▢  ✕"));
    const corpo = el("div", "pv-corpo");
    const lado = el("div", "pv-lado");
    lado.style.background = m.lado;
    ["Pasta pessoal", "Documentos", "Imagens", "Downloads"].forEach((n, i) =>
      lado.appendChild(el("div", "pv-item" + (i === 2 ? " sel" : ""), n)));
    const area = el("div", "pv-area");
    for (let i = 0; i < 4; i++){
      const l = el("i"); l.style.background = m.linha; l.style.width = (90 - i * 14) + "%"; area.appendChild(l);
    }
    area.appendChild(el("span", "pv-bt", "Abrir"));
    corpo.append(lado, area);
    jan.append(tit, corpo);
    tela.appendChild(jan);
    return tela;
  }

  // ---- tela de login ------------------------------------------------------
  function login(e){
    const tela = el("div", "pv-tela pv-login");
    tela.style.setProperty("--pv-acento", DESTAQUE);
    const fundo = el("div", "pv-login-fundo" + (e.login_desfoque !== "nao" ? " desfocado" : ""));
    pintarFundo(fundo, fundoLoginDe(e), e.login_fundo === "propria"
      ? "escolha uma imagem nos ajustes" : "papel de parede atual");
    const topo = el("div", "pv-login-topo", "qui 08 out  10:40  ⏻");
    const meio = el("div", "pv-login-meio");
    meio.appendChild(el("div", "pv-foto"));
    if (e.login_usuarios === "lista") meio.appendChild(el("div", "pv-nome", "seu usuário ▾"));
    else meio.appendChild(el("div", "pv-campo", "Nome"));
    meio.appendChild(el("div", "pv-campo", "Senha"));
    const bts = el("div", "pv-login-bts");
    bts.append(el("span", "pv-bt-vidro", "Cancelar"), el("span", "pv-bt-entrar", "Entrar"));
    meio.appendChild(bts);
    tela.append(fundo, topo, meio);
    if (e.login === "nao") tela.appendChild(el("div", "pv-desligada", "Tela de login do sistema (sem a do projeto)"));
    return tela;
  }

  // ---- montagem -----------------------------------------------------------
  function desenhar(e){
    const caixa = document.querySelector("#previas");
    if (!caixa) return;
    caixa.textContent = "";
    caixa.hidden = false;

    const c1 = el("div", "cartao pv-cartao");
    c1.appendChild(el("h2", "", "Área de trabalho"));
    c1.appendChild(desktop(e));
    const pe = el("div", "pv-pe");
    pe.appendChild(el("span", "", "Muda na hora a cada opção; o desenho é aproximado."));
    const b = el("button", "bt sec pv-alterna", maximizada ? "Ver janela normal" : "Ver janela maximizada");
    b.addEventListener("click", () => { maximizada = !maximizada; desenhar(e); });
    pe.appendChild(b);
    c1.appendChild(pe);

    const c2 = el("div", "cartao pv-cartao");
    c2.appendChild(el("h2", "", "Tela de login e de bloqueio"));
    c2.appendChild(login(e));
    c2.appendChild(el("div", "pv-pe", "A de verdade aparece no próximo reinício; a de bloqueio muda na hora."));
    caixa.append(c1, c2);
  }

  // galeria do fundo do login: as duas escolhas em miniatura e o botao
  function galeria(o, e, escolher){
    if (o.chave !== "login_fundo") return null;
    const g = el("div", "pv-galeria");
    o.valores.forEach(v => {
      const b = el("button", "pv-mini");
      b.type = "button";
      b.setAttribute("aria-pressed", String(e[o.chave] === v));
      const img = el("span", "pv-mini-img");
      pintarFundo(img, v === "propria" ? {url: `/api/login-propria.jpg?v=${versaoPropria}`} : papelDe(e),
                  v === "propria" ? "nenhuma ainda" : "papel atual");
      const nome = (o.nomes || {})[v] || v;
      b.append(img, el("span", "pv-mini-nome", nome));
      b.title = nome;
      b.addEventListener("click", () => escolher(v));
      g.appendChild(b);
    });

    // escolher uma imagem do computador: reduzida aqui, guardada pelo painel
    const caixa = el("div", "pv-galeria-caixa");
    const acoes = el("div", "pv-escolher");
    const entrada = el("input");
    entrada.type = "file";
    entrada.accept = "image/jpeg,image/png,image/webp";
    entrada.hidden = true;
    const botao = el("button", "bt sec", "Escolher imagem…");
    botao.type = "button";
    const aviso = el("span", "pv-aviso", "JPEG, PNG ou WebP; vai para o fundo do login");
    botao.addEventListener("click", () => entrada.click());
    entrada.addEventListener("change", async () => {
      const arquivo = entrada.files && entrada.files[0];
      entrada.value = "";
      if (!arquivo) return;
      botao.disabled = true;
      aviso.classList.remove("erro");
      aviso.textContent = "Preparando a imagem…";
      try {
        const imagem = await reduzir(arquivo);
        aviso.textContent = "Enviando…";
        const r = await fetch("/api/login-imagem", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify({imagem}),
        }).then(x => x.json());
        if (!r.ok) throw new Error(r.erro || "o painel recusou a imagem");
        versaoPropria++;
        faltam.forEach(u => { if (u.startsWith("/api/login-propria")) faltam.delete(u); });
        escolher("propria");
      } catch (erro){
        aviso.textContent = "Não deu: " + erro.message;
        aviso.classList.add("erro");
        botao.disabled = false;
      }
    });
    acoes.append(botao, aviso, entrada);
    caixa.append(g, acoes);
    return caixa;
  }

  // a foto inteira de uma camera passaria do limite do painel: sai em JPEG de
  // no maximo 2560x1600, que e mais do que a tela de login precisa
  function reduzir(arquivo){
    return new Promise((ok, falha) => {
      const url = URL.createObjectURL(arquivo);
      const img = new Image();
      img.onload = () => {
        const escala = Math.min(1, 2560 / img.naturalWidth, 1600 / img.naturalHeight);
        const c = document.createElement("canvas");
        c.width = Math.round(img.naturalWidth * escala);
        c.height = Math.round(img.naturalHeight * escala);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        ok(c.toDataURL("image/jpeg", 0.9).split(",")[1]);
      };
      img.onerror = () => { URL.revokeObjectURL(url); falha(new Error("o navegador não abriu essa imagem")); };
      img.src = url;
    });
  }

  return {desenhar, galeria};
})();
