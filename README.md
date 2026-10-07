<div align="center">

<img src="docs/logo.svg" alt="d3bian-init minimal-xfce" width="420">

**O Xfce do Debian minimalista, só com o que vem no repositório: Orchis, Papirus e uma barra só.**

[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](docs/desenvolvimento.md)
[![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-brightgreen)](docs/desenvolvimento.md)
[![Debian 13](https://img.shields.io/badge/Debian-13-A81D33?logo=debian&logoColor=white)](docs/uso.md#sistemas)
[![Xfce](https://img.shields.io/badge/desktop-Xfce-2284F2?logo=xfce&logoColor=white)](docs/uso.md#sistemas)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](LICENSE)

</div>

> Um painel local, aberto no navegador, que deixa o Xfce do Debian minimalista
> usando **só o que vem no repositório**: nada é clonado nem compilado, e por isso
> o desfazer é simples. Só Python da biblioteca padrão — nada de pip.

```sh
git clone https://git.saberdl.dev.br/d3bian-temas/minimal-xfce.git d3bian_init_minimal_xfce
python3 -m d3bian_init_minimal_xfce        # pede a senha uma vez e abre o painel
```

<div align="center">
  <img src="docs/imagens/resultado-instalado.jpg" alt="Logo depois de instalar, com as opções padrão" width="820">
</div>

---

## O que ele faz

- **Tema** Orchis (pacote `orchis-gtk-theme`), claro ou escuro, com a variante
  compacta para barras de título estreitas
- **Ícones** Papirus, Numix ou os Adwaita que já vêm no sistema
- **Fonte** Inter ou Cantarell, também do repositório
- **Barra única no topo**, sem dock: menu só com ícone, janelas abertas no
  `xfce4-docklike-plugin` (ícones agrupados, sem texto), relógio e bandeja
- **Área de trabalho** sem ícones, com papel de parede liso ou em degradê
  desenhado na hora pelo ImageMagick, em tons discretos
- **Encaixe de janelas** por atalho, bordas mais largas, e nova janela e nova aba no clique direito do terminal
- **Barra em ilhas**, se quiser: barra fina solta no topo e as janelas abertas numa
  ilha embaixo, com cantos redondos (vinda do [oasis-xfce](https://git.saberdl.dev.br/d3bian-temas/oasis-xfce))
- **Efeitos com o picom**, se quiser: sombras, cantos redondos e desfoque, em modo
  leve onde não há aceleração de vídeo
- **Programas úteis**: uma lista pronta do repositório oficial do Debian, conforme o hardware
- **Voltar ao que era antes** com o diário de alterações do [modelo](https://git.saberdl.dev.br/d3bian-temas/modelo)

<!-- imagens: gerado a partir do teste num Debian 13; refazer, nao editar a mao -->
## Telas

| Com outras opções da página | Mais uma combinação de opções |
|---|---|
| ![Com outras opções da página](docs/imagens/resultado-opcao.jpg) | ![Mais uma combinação de opções](docs/imagens/resultado-opcao2.jpg) |

| Barra em ilhas, com o picom (`barra = ilhas`, `efeitos = desfoque`) |
|---|
| ![Barra em ilhas, com o picom](docs/imagens/resultado-ilhas.jpg) |

| Início | Opções | Programas úteis |
|---|---|---|
| ![Início](docs/imagens/painel-inicio.jpg) | ![Opções](docs/imagens/painel-opcoes.jpg) | ![Programas úteis](docs/imagens/painel-programas.jpg) |

<details>
<summary><b>A instalação pela página, do começo ao resultado</b></summary>

![A instalação pela página, do começo ao resultado](docs/imagens/instalacao.gif)

</details>
<!-- fim imagens -->

## Documentação

| | |
|---|---|
| 🚀 [Usando](docs/uso.md) | rodar, opções, o que fica onde, sistemas, voltar ao que era antes |
| 🛠️ [Desenvolvimento](docs/desenvolvimento.md) | receitas, como as imagens de exemplo são geradas |
| ⚙️ [Núcleo](docs/nucleo.md) | o motor, o servidor e as telas comuns a toda a família |

## Família d3bian-init

Todos com o mesmo motor e o mesmo jeito de usar: um painel local, só Python da biblioteca padrão, e "voltar ao que era antes".
Os de terminal ficam em [d3bian-terminal](https://git.saberdl.dev.br/d3bian-terminal); os temas e o modelo, em [d3bian-temas](https://git.saberdl.dev.br/d3bian-temas).

| | Projeto | O que faz |
|---|---|---|
| 💻 | [terminal](https://git.saberdl.dev.br/d3bian-terminal/terminal) · [terminal-kde](https://git.saberdl.dev.br/d3bian-terminal/terminal-kde) | Fish, Oh My Posh, Nerd Font e cores (xfce4-terminal/GNOME Terminal ou Konsole) |
| 💻 | [zsh](https://git.saberdl.dev.br/d3bian-terminal/zsh) · [zsh-kde](https://git.saberdl.dev.br/d3bian-terminal/zsh-kde) | Zsh com sugestões e realce, Oh My Posh, Nerd Font e cores |
| 💻 | [bash](https://git.saberdl.dev.br/d3bian-terminal/bash) · [bash-kde](https://git.saberdl.dev.br/d3bian-terminal/bash-kde) | O bash de sempre, com sugestões e realce, Oh My Posh e Nerd Font |
| 🎨 | [bigsur-kde](https://git.saberdl.dev.br/d3bian-temas/bigsur-kde) · [mactahoe-kde](https://git.saberdl.dev.br/d3bian-temas/mactahoe-kde) | Cara de macOS (Big Sur ou Tahoe) no KDE Plasma 6 |
| 🎨 | [fluent-kde](https://git.saberdl.dev.br/d3bian-temas/fluent-kde) · [chromeos-kde](https://git.saberdl.dev.br/d3bian-temas/chromeos-kde) | Cara de Windows 11 ou de ChromeOS no KDE Plasma 6 |
| 🎨 | [catppuccin-kde](https://git.saberdl.dev.br/d3bian-temas/catppuccin-kde) · [graphite-kde](https://git.saberdl.dev.br/d3bian-temas/graphite-kde) · [layan-kde](https://git.saberdl.dev.br/d3bian-temas/layan-kde) · [orchis-kde](https://git.saberdl.dev.br/d3bian-temas/orchis-kde) | Temas Catppuccin, Graphite, Layan e Orchis no KDE Plasma 6 |
| 🪟 | [bigsur-xfce](https://git.saberdl.dev.br/d3bian-temas/bigsur-xfce) · [bigsur-minimalista-xfce](https://git.saberdl.dev.br/d3bian-temas/bigsur-minimalista-xfce) | Cara de macOS Big Sur no Xfce, completo ou minimalista |
| 🪟 | **minimal-xfce** · [paleta-xfce](https://git.saberdl.dev.br/d3bian-temas/paleta-xfce) | Xfce enxuto, ou numa paleta só (Nord, Gruvbox, Everforest) |
| 🍎 | [tahoe-gnome](https://git.saberdl.dev.br/d3bian-temas/tahoe-gnome) | Cara de macOS Tahoe no GNOME 48 |
| 🧩 | [modelo](https://git.saberdl.dev.br/d3bian-temas/modelo) | O modelo de onde todos saem: crie o seu próprio d3bian-init |

## Créditos

- O visual segue o que aparece nas montagens minimalistas de Xfce que circulam por aí —
  [esta do Diolinux Plus](https://plus.diolinux.com.br/t/void-xfce-minimalista/74056),
  por exemplo, usa Orchis Dark com Papirus Dark, a mesma dupla deste projeto, ambas no
  repositório do Debian.
- Tudo é instalado do repositório oficial do Debian, cada um com a sua licença:
  [Orchis](https://github.com/vinceliuice/Orchis-theme) (GPL-3.0),
  [Papirus](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) (GPL-3.0),
  [Numix](https://github.com/numixproject/numix-icon-theme) (GPL-3.0), as fontes
  [Inter](https://rsms.me/inter/) e [Cantarell](https://gitlab.gnome.org/GNOME/cantarell-fonts)
  (SIL OFL) e o [docklike](https://docs.xfce.org/panel-plugins/xfce4-docklike-plugin/start).
  O repositório não traz nenhum deles.

---

<div align="center">
<sub>Código sob a <a href="LICENSE">licença MIT</a> · feito para o Debian 13</sub>
</div>
