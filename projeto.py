"""O que e proprio deste projeto e nao cabe numa receita.

Tudo aqui sai do repositorio do Debian: o tema Orchis, os icones Papirus ou
Numix e as fontes. O papel de parede e desenhado pelo ImageMagick na hora, com
duas cores proximas, para nao baixar imagem nenhuma.
"""

from __future__ import annotations

import os
import shutil
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

# fora da pasta pessoal as receitas nao criam nada; o desfazer nao apaga la
APAGAVEIS_FORA_DE_CASA: set[str] = set()


def contexto(cfg: dict[str, str]) -> dict[str, str]:
    escuro = cfg.get("modo", "escuro") == "escuro"
    compacto = cfg.get("compacto", "sim") == "sim"
    tema = f"{TEMA_BASE}-{'Dark' if escuro else 'Light'}" + ("-Compact" if compacto else "")
    claros, escuros = ICONES.get(cfg.get("icones", ""), ICONES["papirus"])
    fonte = FONTES.get(cfg.get("fonte", ""), "Inter")
    cima, baixo = CORES_PAPEL.get(cfg.get("cor_papel", ""), CORES_PAPEL["grafite"])
    papel = cfg.get("papel", "degrade")
    return {
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
        "painel_posicao": POSICAO_BARRA.get(cfg.get("barra", ""), POSICAO_BARRA["topo"]),
        # fundo da barra em rgba, quase opaco, e o texto que le bem sobre ele
        "painel_fundo": "0.08 0.09 0.10 0.92" if escuro else "0.98 0.98 0.98 0.92",
        "painel_texto": "#e6e6e6" if escuro else "#1c1c1c",
        "papeis_dir": str(PAPEIS_DIR),
    }


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
