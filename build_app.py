import base64, re
P='origem/dade-propostas/'
b=lambda f:'data:image/png;base64,'+base64.b64encode(open(P+f,'rb').read()).decode()
proto=open('origem/central-tpl.html',encoding='utf-8').read()
extra=re.search(r'(/\* ===== acréscimos.*?)</style>',proto,re.S).group(1)+'\n[hidden]{display:none!important}\n'
t=open('app.tpl.html',encoding='utf-8').read()
for k,v in {'__BRAND_CSS__':open(P+'assets/css/brand.css',encoding='utf-8').read(),'__EXTRA_CSS__':extra,'__LOGO_COLOR__':b('assets/img/dade/logo-dade-colorido.png'),'__LOGO_BLACK__':b('assets/img/dade/logo-dade-preto.png'),'__FAVICON__':b('assets/img/favicon.png'),'__SB_URL__':'https://hgkxybswazgcpqpksvkf.supabase.co','__SB_KEY__':'sb_publishable_4-plrhdRN1mZA6uDxnDmKA_muzq8QUu'}.items():
    assert k in t,k; t=t.replace(k,v)
open('site/index.html','w',encoding='utf-8').write(t)
open('check_app.js','w',encoding='utf-8').write(re.search(r'<script>\n/\* =+ CONFIG.*?</script>',t,re.S).group(0)[8:-9])
print(len(t))
