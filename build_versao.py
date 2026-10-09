# Cache: o GitHub Pages deixa o navegador guardar os arquivos por 10 min.
# Cada build marca os links de CSS e JS com uma versão (hash do conteúdo),
# então quando o arquivo muda o navegador busca o novo na hora.
import hashlib, glob, re
def h(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
ver = {a: h('site/' + a) for a in ('assets/dade.js', 'assets/css/proposta.css')}
for f in glob.glob('site/**/*.html', recursive=True):
    t = open(f, encoding='utf-8').read(); n = t
    for a, v in ver.items(): n = re.sub(r'((?:\.\./)?' + re.escape(a) + r')(\?v=[0-9a-f]+)?(?=["\'])', r'\g<1>?v=' + v, n)
    if n != t: open(f, 'w', encoding='utf-8').write(n)
print('versões', ver)
