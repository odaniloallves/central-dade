# Central dade: arquivos de montagem

Este branch (`fonte`) guarda o que gera a central. O site publicado fica no branch `main`, que é o que o GitHub Pages serve em https://central.dadedesign.com.br. Nada daqui aparece no site.

## Como gerar o site

```
./build.sh
```

Gera a pasta `site/`. O conteúdo de `site/` é o que vai para a raiz do branch `main`.

Requisitos: `python3` com Pillow e `php` (só para ler o catálogo de serviços em `origem/dade-propostas/templates/servicos_data.php`).

## O que é cada arquivo

| Arquivo | Gera |
|---|---|
| `app.tpl.html` + `build_app.py` | `index.html`, a central (login, Início, Agenda, Clientes, Briefings e copys, Prévias, Propostas, Lixeira) |
| `build_prop.py` | `proposta.html`, copia os assets e roda os três abaixo |
| `build_pag.py` | `pagamento.html` (aceite e forma de pagamento) e o CSS das páginas públicas |
| `build_prev.py` | `previa.html` (aprovação de prévias) |
| `build_priv.py` | `privacidade.html` (aviso LGPD) |
| `forms.py` | `briefing/lp.html`, `briefing/site.html`, `briefing/identidade.html` |

`origem/` tem o material de partida:
- `dade-propostas/`: CSS, imagens e a página de proposta do sistema em PHP antigo do Dan.
- `logos/`: logos dos clientes.
- `briefing-lp.html`: base dos formulários.
- `central-tpl.html`: CSS extra da central.

`testes/` tem os testes com Playwright e o Supabase simulado. Antes de rodar, sirva `site/` em http://localhost:8765:

```
cd site && python3 -m http.server 8765
```

## Banco

Supabase, projeto Onboard Photos (`hgkxybswazgcpqpksvkf`), tabelas `central_*` e bucket `central-previas`. As regras e o estado completo estão no projeto "Sites" do Claude (`claude/central-dade-estado-e-pagamento.md`).
