# Usando o d3bian-init-minimal-xfce

[← voltar ao README](../README.md)

## Rodar

Clone com o nome da pasta igual ao do pacote Python (com `_`) e rode como módulo:

```sh
git clone https://git.saberdl.dev.br/d3bian/minimal-xfce.git d3bian_init_minimal_xfce
python3 -m d3bian_init_minimal_xfce            # pede a senha uma vez e abre o painel
python3 -m d3bian_init_minimal_xfce aplicar --simular
```

O painel abre em `http://127.0.0.1:8896`. A página é verde-água, para não
confundir com os outros painéis.

## Instalação pelo painel

1. `python3 -m d3bian_init_minimal_xfce` abre a página no navegador (pede a senha de administrador uma vez, no terminal).
2. Em **Ajustes**, escolha as opções e clique em **Instalar tudo**; o progresso de cada etapa aparece na hora.
3. Depois, mudar uma opção e **Aplicar** roda de novo só as etapas afetadas.
4. **Voltar ao que era antes** desfaz tudo; com **Remover também o que foi instalado**, tira também os pacotes.

A tela **Programas úteis** traz uma lista pronta de programas do repositório
oficial do Debian, mostrando só o que serve para o hardware encontrado.

## Opções

| Opção | Valores |
|---|---|
| `modo` | escuro, claro |
| `compacto` (barras de título estreitas) | sim, não |
| `icones` | Papirus, Numix, Adwaita |
| `fonte` | Inter, Cantarell, a do sistema |
| `barra` | topo, embaixo |
| `barra_tarefas` (janelas abertas na barra) | docklike, botões, nenhuma |
| `relogio` | curto, completo, só a hora |
| `menu` | só ícone, ícone e texto, nenhum |
| `papel` | degradê, liso, manter o atual |
| `cor_papel` | grafite, ardósia, oliva, areia, vinho |
| `icones_area` | nenhum, só removíveis, tudo |
| `janelas` (encaixe e bordas) | sim, não |

## O que fica onde

| Caminho | Escrito por |
|---|---|
| `~/.config/d3bian-init-minimal-xfce` | opções |
| `~/.local/state/d3bian-init-minimal-xfce` | estado, registro, diário e cópias de segurança |
| `~/.local/share/backgrounds/minimal` | papel de parede desenhado pelo ImageMagick |
| `~/.local/bin/d3bian-janelas`, `d3bian-layouts`, `d3bian-bordas` | encaixe, layouts e bordas de janela |
| `~/.themes` | cópia do tema das janelas com bordas mais largas |
| `~/.local/share/applications/xfce4-terminal.desktop` | nova janela e nova aba no clique direito do terminal |
| `~/.config/gtk-3.0/settings.ini`, `gtk.css`, `~/.gtkrc-2.0` | tema e fonte para os programas GTK |
| xfconf (`xsettings`, `xfwm4`, `xfce4-panel`, `xfce4-desktop`, `xfce4-keyboard-shortcuts`) | tema, ícones, fonte, barra, área de trabalho e atalhos |

## Sistemas

Família Debian (a verificação aceita `debian` no `ID` ou no `ID_LIKE` do
`/etc/os-release`), numa sessão gráfica do Xfce com o `xfconf-query`. Tudo vem do
repositório: nada é clonado nem compilado. Sem o ImageMagick o papel de parede
gerado não é criado (aviso, não impede).

## Voltar ao que era antes

Em Ajustes, **Voltar ao que era antes**, ou `restaurar --sim`. A barra volta pelo
`xfce4-panel-profiles`, guardada na receita 00; o resto vem do diário. Com
**Remover também o que foi instalado** saem os pacotes que o projeto instalou.
