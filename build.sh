#!/bin/sh
# Gera a pasta site/ (o que vai para o branch main / GitHub Pages).
# Requer python3 com Pillow e php (para ler o catálogo de serviços).
set -e
cd "$(dirname "$0")"
rm -rf site
python3 build_prop.py      # proposta, pagamento, prévia, privacidade e assets
python3 build_app.py       # a central (index.html)
python3 forms.py           # formulários de briefing
echo "central.dadedesign.com.br" > site/CNAME
touch site/.nojekyll
printf "User-agent: *\nDisallow: /\n" > site/robots.txt
echo "ok: site/ gerado"
