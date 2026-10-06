# Desenvolvimento

[← voltar ao README](../README.md)

Painel em Python puro (só a biblioteca padrão) com HTML/JS sem dependências.
O motor, o servidor e as telas comuns vêm do [modelo](https://git.saberdl.dev.br/d3bian/modelo);
os detalhes deles e as armadilhas conhecidas estão em [nucleo.md](nucleo.md).

## Receitas

| id | nome | afetada por |
|---|---|---|
| 00 | backup (arquivos e a barra de antes) | |
| 10 | pacotes | `icones`, `fonte`, `barra_tarefas` |
| 20 | aparência (tema, ícones, fonte, janelas) | `modo`, `compacto`, `icones`, `fonte` |
| 30 | barra | `barra`, `barra_tarefas`, `relogio`, `menu`, `modo` |
| 35 | janelas (encaixe, bordas e atalhos) | `janelas`, `modo`, `compacto` |
| 36 | novo terminal no clique direito | |
| 40 | papel de parede e área de trabalho | `papel`, `cor_papel`, `icones_area` |

Nomes de tema, ícones, cores do papel e formato do relógio ficam no `projeto.py`.

## Imagens de exemplo

As imagens de `recursos/web/exemplos` são simulações da área de trabalho
desenhadas em HTML e fotografadas pelo chromium pelo `ferramentas/gerar_exemplos.py`:
papel de parede, barra, uma janela e um terminal, com as cores aproximadas do
Orchis (`AMOSTRA` no `projeto.py`). Não é foto do Xfce rodando, e nada da máquina
de quem gera entra nelas: o usuário é sempre "ana", a máquina "debian" e o relógio
uma hora fixa.

```sh
python3 ferramentas/gerar_exemplos.py            # desenha e mostra o que faria
python3 ferramentas/gerar_exemplos.py --gravar   # e aponta no opcoes.toml
```

Precisa de chromium e ImageMagick.
