"""O que e proprio deste projeto e nao cabe numa receita.

Tudo aqui sai do repositorio do Debian: o tema Orchis, os icones Papirus ou
Numix, as fontes e o picom. O papel de parede e desenhado pelo ImageMagick na
hora, com duas cores proximas, para nao baixar imagem nenhuma.

A barra em ilhas, o picom e o encaixe que respeita as margens vem do
d3bian-init-oasis-xfce.
"""

from __future__ import annotations

import functools
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Callable

# opcao -> (nome do tema no /usr/share/themes, claro e escuro)
# o pacote orchis-gtk-theme do Debian traz Orchis, Orchis-Light, Orchis-Dark e
# as variantes -Compact; nao traz cores de destaque
TEMA_BASE = "Orchis"

# opcao -> (icones no modo claro, icones no modo escuro)
ICONES = {
    "papirus": ("Papirus", "Papirus-Dark"),
    "numix": ("Numix-Light", "Numix"),
    "adwaita": ("Adwaita", "Adwaita"),
}

FONTES = {"inter": "Inter", "cantarell": "Cantarell", "sistema": ""}

# Cores so para as imagens de exemplo da pagina: uma aproximacao do que o
# Orchis pinta nas janelas, para a pessoa escolher vendo. Nao entram em receita
# nenhuma, quem manda na maquina e o tema instalado.
#   modo -> janela, barra de titulo, texto, lateral, destaque, borda
AMOSTRA = {
    "escuro": ("#2c2c2c", "#252525", "#e6e6e6", "#262626", "#1a73e8", "#3a3a3a"),
    "claro": ("#fafafa", "#f2f2f2", "#2b2b2b", "#f5f5f5", "#1a73e8", "#e0e0e0"),
}

# opcao -> (cor de cima, cor de baixo) do papel de parede gerado
CORES_PAPEL = {
    "grafite": ("#2b2f33", "#141618"),
    "ardosia": ("#2a3340", "#141a21"),
    "oliva": ("#2f352a", "#171a14"),
    "areia": ("#3a352c", "#1c1a15"),
    "vinho": ("#33262b", "#181214"),
}

# posicao da barra, no formato que o xfce4-panel grava: p e a borda em que ela
# encosta, pela ordem do enum SnapPosition do painel (6 = canto superior
# esquerdo, 8 = inferior esquerdo), e a barra se estica dali
POSICAO_BARRA = {"topo": "p=6;x=0;y=0", "baixo": "p=8;x=0;y=0"}

# o relogio do painel: formato do proprio strftime
RELOGIO = {
    "curto": "%a %d %b  %H:%M",
    "completo": "%a, %d de %B de %Y  %H:%M",
    "so_hora": "%H:%M",
}

PAPEIS_DIR = Path.home() / ".local/share/backgrounds/minimal"

# a cor de destaque do Orchis do Debian (so vem em azul): pinta o botao marcado
# das ilhas e o indicador do dock
DESTAQUE = "#1a73e8"

# raio dos cantos das ilhas; o picom usa o mesmo, para o desfoque nao vazar
RAIO = 14

# programas fixados no dock da ilha de baixo, na ordem; so entram os que existem
FAVORITOS = ["thunar", "xfce4-terminal", "firefox-esr", "firefox", "org.xfce.mousepad"]

# fora da pasta pessoal as receitas nao criam nada; o desfazer nao apaga la
APAGAVEIS_FORA_DE_CASA: set[str] = set()


def exec_desktop(*argumentos: str) -> str:
    """A linha Exec de um .desktop, com as aspas da especificacao: a pasta
    pessoal pode ter espaco ("/home/joao silva") ou %."""
    def um(arg: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_./:=+,@-]+", arg):
            arg = '"' + re.sub(r'([\\"`$])', r"\\\1", arg) + '"'
        return arg.replace("%", "%%")

    # o valor do .desktop tem os escapes do proprio arquivo: \ vira \\
    return " ".join(um(a) for a in argumentos).replace("\\", "\\\\")


# video sem aceleracao: o picom com glx e desfoque fica lento, ou as janelas
# param de redesenhar (o caso classico e a VM sem 3D)
_SOFTWARE = ("llvmpipe", "softpipe", "swrast", "software rasterizer")
# drivers de video que nao tem 3D (o virtio_gpu pode ter, com virgl, e fica de fora)
_VIDEO_SEM_3D = {"qxl", "bochs", "bochs-drm", "cirrus", "cirrus-qemu", "vboxvideo",
                 "simpledrm", "efifb", "vesafb", "hyperv_drm", "hyperv_fb"}


@functools.lru_cache(maxsize=4)
def _render_software(glxinfo: str, display: str, virtual: bool) -> tuple[bool, str]:
    if os.environ.get("LIBGL_ALWAYS_SOFTWARE") in ("1", "true"):
        return True, "LIBGL_ALWAYS_SOFTWARE ligado"
    if glxinfo and display:
        try:
            saida = subprocess.run([glxinfo, "-B"], capture_output=True, text=True, timeout=6,
                                   stdin=subprocess.DEVNULL,
                                   env={**os.environ, "LC_ALL": "C"}).stdout.lower()
        except (OSError, subprocess.TimeoutExpired):
            saida = ""
        if "direct rendering: no" in saida:
            return True, "sem renderizacao direta (glxinfo)"
        for linha in saida.splitlines():
            if "opengl renderer string" in linha:
                if any(s in linha for s in _SOFTWARE):
                    return True, "video desenhado pelo processador (" + linha.split(":", 1)[1].strip() + ")"
                return False, ""
    drivers = set()
    for card in Path("/sys/class/drm").glob("card[0-9]"):
        try:
            drivers.add(os.path.basename(os.readlink(card / "device/driver")))
        except OSError:
            pass
    if drivers and drivers <= _VIDEO_SEM_3D:
        return True, "placa de video sem 3D (" + ", ".join(sorted(drivers)) + ")"
    if virtual:
        return True, "maquina virtual sem confirmacao de aceleracao 3D"
    return False, ""


def render_software() -> tuple[bool, str]:
    """(sim ou nao, motivo). O glxinfo (mesa-utils) chega com a receita 10."""
    from . import sistema
    return _render_software(shutil.which("glxinfo") or "", os.environ.get("DISPLAY", ""),
                            sistema.maquina_virtual())


def _picom(cfg: dict[str, str]) -> dict[str, str]:
    efeitos = cfg.get("efeitos", "desligado")
    # so pergunta ao video quando o picom vai rodar
    software, motivo = render_software() if efeitos != "desligado" else (False, "")
    desfoque = efeitos == "desfoque" and not software
    if efeitos == "desligado":
        aviso = "efeitos desligados: vale o compositor do proprio Xfce"
    elif software:
        aviso = f"picom em modo leve (xrender, sem desfoque nem vsync): {motivo}"
    elif desfoque:
        aviso = "picom com desfoque, sombras e cantos arredondados"
    else:
        aviso = "picom com sombras e cantos arredondados, sem desfoque"
    linhas_desfoque = "\n".join([
        'blur-method = "dual_kawase";',
        "blur-strength = 5;",
        "blur-background = true;",
        "blur-background-frame = false;",
        "blur-background-fixed = false;",
        "blur-background-exclude = [",
        '  "window_type = \'desktop\'",',
        '  "window_type = \'dnd\'",',
        '  "window_type = \'tooltip\'",',
        '  "_GTK_FRAME_EXTENTS@",',
        '  "class_g = \'firefox\' && argb",',
        '  "class_g = \'firefox-esr\' && argb",',
        '  "class_g = \'Firefox-esr\' && argb"',
        "];",
    ]) if desfoque else "# sem desfoque (pela opcao ou pelo video desta maquina)"
    # janelas translucidas so com desfoque; sem ele o texto de tras atrapalha
    linhas_opacidade = "\n".join([
        "opacity-rule = [",
        '  "94:class_g = \'Xfce4-terminal\' && focused",',
        '  "88:class_g = \'Xfce4-terminal\' && !focused"',
        "];",
    ]) if desfoque else "# janelas opacas: a transparencia so vale junto com o desfoque"
    # a barra colada na borda fica reta; as ilhas sao arredondadas
    excluir_barra = "" if cfg.get("barra") == "ilhas" else '  "window_type = \'dock\'",'
    return {
        "picom_backend": "xrender" if software else "glx",
        "picom_vsync": "false" if software else "true",
        "picom_desfoque": linhas_desfoque,
        "picom_opacidade": linhas_opacidade,
        "picom_excluir_barra": excluir_barra,
        "picom_aviso": aviso,
        # o autostart chama o d3bian-picom, que religa o xfwm4 se o picom cair
        "picom_exec": exec_desktop(str(Path.home() / ".local/bin/d3bian-picom")),
    }


def contexto(cfg: dict[str, str]) -> dict[str, str]:
    escuro = cfg.get("modo", "escuro") == "escuro"
    compacto = cfg.get("compacto", "sim") == "sim"
    tema = f"{TEMA_BASE}-{'Dark' if escuro else 'Light'}" + ("-Compact" if compacto else "")
    claros, escuros = ICONES.get(cfg.get("icones", ""), ICONES["papirus"])
    fonte = FONTES.get(cfg.get("fonte", ""), "Inter")
    cima, baixo = CORES_PAPEL.get(cfg.get("cor_papel", ""), CORES_PAPEL["grafite"])
    papel = cfg.get("papel", "degrade")
    dr, dg, db = (int(DESTAQUE[i:i + 2], 16) for i in (1, 3, 5))
    ctx = {
        "gtk_tema": tema,
        "gtk_esquema": "prefer-dark" if escuro else "default",
        # o gtk-3.0/settings.ini pede o valor em texto, como o proprio GTK escreve
        "gtk_escuro": "1" if escuro else "0",
        "icones_tema": escuros if escuro else claros,
        # sem fonte escolhida, as receitas pulam o passo com se = "fonte != sistema"
        "fonte_ui": fonte or "Sans",
        "fonte_titulo": f"{fonte or 'Sans'} Bold 9",
        "papel_cor_cima": cima,
        "papel_cor_baixo": baixo,
        "papel_arquivo": str(PAPEIS_DIR / f"{cfg.get('cor_papel', 'grafite')}-{papel}.png"),
        "relogio_formato": RELOGIO.get(cfg.get("relogio", ""), RELOGIO["curto"]),
        # o xfdesktop usa 0 para nenhum icone, 1 para minimizadas e 2 para arquivos
        "icones_area_valor": {"nenhum": "0", "so_removiveis": "2", "tudo": "2"}.get(
            cfg.get("icones_area", "nenhum"), "0"),
        "mostrar_removiveis": "true" if cfg.get("icones_area") in ("so_removiveis", "tudo") else "false",
        "mostrar_arquivos": "true" if cfg.get("icones_area") == "tudo" else "false",
        "menu_titulo": "true" if cfg.get("menu") == "icone_texto" else "false",
        "papel_tipo": papel,
        # com ilhas, quem posiciona e o paineis.py; a barra unica fica no topo ou embaixo
        "painel_posicao": POSICAO_BARRA.get(cfg.get("barra", ""), POSICAO_BARRA["topo"]),
        # fundo da barra em rgba, quase opaco, e o texto que le bem sobre ele
        "painel_fundo": "0.08 0.09 0.10 0.92" if escuro else "0.98 0.98 0.98 0.92",
        "painel_texto": "#e6e6e6" if escuro else "#1c1c1c",
        "papeis_dir": str(PAPEIS_DIR),
        # barra em ilhas: um pouco translucida, com os cantos e o picom no mesmo raio
        "raio": str(RAIO),
        "ilha_fundo_barra": "0.08 0.09 0.10 0.80" if escuro else "0.98 0.98 0.98 0.82",
        # a ilha de baixo fica sobre a parte escura do papel: um tom mais clara
        "ilha_fundo": "0.20 0.21 0.23 0.90" if escuro else "0.98 0.98 0.98 0.88",
        "painel_hover": "rgba(255, 255, 255, 0.10)" if escuro else "rgba(0, 0, 0, 0.07)",
        "destaque_cor": DESTAQUE,
        "destaque_suave": f"rgba({dr}, {dg}, {db}, 0.22)",
        "favoritos": ";".join(FAVORITOS),
    }
    ctx.update(_picom(cfg))
    return ctx


def verificacoes(add: Callable[..., None]) -> None:
    """Checagens a mais. add(nome, ok, detalhe, critico=True, dica="")."""
    from . import sistema

    ambiente = sistema.desktop().upper()
    xfce = "XFCE" in ambiente
    add("Ambiente grafico", xfce, ambiente or "desconhecido",
        dica="este projeto e para o XFCE")

    tem_xfconf = bool(shutil.which("xfconf-query"))
    add("Configuracao do XFCE", tem_xfconf,
        "xfconf-query disponivel" if tem_xfconf else "falta o xfconf-query, que guarda os ajustes",
        dica="falta o xfconf-query")

    gravavel = os.access(Path.home(), os.W_OK)
    add("Pasta pessoal", gravavel,
        "gravavel" if gravavel else f"sem permissao de escrita em {Path.home()}",
        dica="não consigo escrever na pasta pessoal")

    # o papel de parede e desenhado aqui; sem o ImageMagick a opcao fica sem efeito
    tem_convert = bool(shutil.which("convert") or shutil.which("magick"))
    add("ImageMagick", tem_convert,
        "disponivel" if tem_convert else "sem o convert, o papel de parede gerado nao e criado",
        critico=False)

    # so informa: com video sem 3D o picom roda em modo leve, sem desfoque
    from . import config
    if config.ler().get("efeitos", "desligado") != "desligado":
        software, motivo = render_software()
        add("Aceleracao de video", not software,
            "o picom pode usar glx e desfoque" if not software
            else f"{motivo}; o picom fica em modo leve, sem desfoque",
            critico=False)
