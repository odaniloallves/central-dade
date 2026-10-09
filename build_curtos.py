# Links curtos para mandar aos clientes. O GitHub Pages serve /p como p.html, então:
#   central.dadedesign.com.br/p?<slug>   -> proposta.html?slug=<slug>
#   central.dadedesign.com.br/v?<token>  -> previa.html?t=<token>
#   central.dadedesign.com.br/t?<token>  -> linha.html?t=<token> (linha do tempo)
#   central.dadedesign.com.br/lp, /site, /identidade -> briefing/<tipo>.html
# Os links antigos continuam funcionando.
PAG = '''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{titulo} | dade.design</title><meta name="robots" content="noindex">
<meta property="og:title" content="{titulo} | dade.design"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://central.dadedesign.com.br/assets/img/app-icon-180.png">
<meta name="theme-color" content="#171617"><link rel="icon" type="image/png" href="assets/img/favicon.png">
<style>body{{margin:0;background:#171617;color:#9b9b9b;font:15px/1.5 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}</style>
<script>(function(){{var q=location.search.slice(1),d={destino};location.replace(d)}})()</script>
</head><body><noscript><a href="{fallback}" style="color:#C1FD42">Abrir</a></noscript></body></html>
'''
def pagina(nome, titulo, desc, destino, fallback):
    open(f'site/{nome}.html', 'w', encoding='utf-8').write(PAG.format(titulo=titulo, desc=desc, destino=destino, fallback=fallback))

pagina('p', 'Proposta', 'A proposta da dade.design para o seu projeto.',
       "q&&q.indexOf('=')<0?'proposta.html?slug='+encodeURIComponent(decodeURIComponent(q)):'proposta.html'+location.search", 'proposta.html')
pagina('v', 'Prévia do projeto', 'Veja a prévia e aprove ou peça ajustes.',
       "q&&q.indexOf('=')<0?'previa.html?t='+encodeURIComponent(decodeURIComponent(q)):'previa.html'+location.search", 'previa.html')
pagina('t', 'Acompanhe seu projeto', 'Veja em que etapa está o seu projeto com a dade.design.',
       "q&&q.indexOf('=')<0?'linha.html?t='+encodeURIComponent(decodeURIComponent(q)):'linha.html'+location.search", 'linha.html')
for k, t in (('lp', 'Briefing de landing page'), ('site', 'Briefing de site institucional'), ('identidade', 'Briefing de identidade visual')):
    pagina(k, t, 'Conte sobre o seu projeto para a dade.design.', f"'briefing/{k}.html'+location.search", f'briefing/{k}.html')
print('curtos ok')
