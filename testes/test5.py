import asyncio, json, datetime, uuid, copy
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import test2 as T
BASE=T.BASE; DB=T.DB; CORS=T.CORS; J={**CORS,'content-type':'application/json'}
hoje=datetime.date.today()
COND=[{'titulo':'Validade da proposta','texto':'Válida até a data indicada.','so_impresso':False},{'titulo':'Ajustes','texto':'1 rodada com até 3 ajustes.','so_impresso':False},{'titulo':'Acompanhamento gráfico','texto':'15% sobre fornecedores.','so_impresso':True}]
DB.update({'central_clientes':[{'id':'cl1','nome':'Brasil Web Logística','contato':'Marcos','created_at':T.now(),'deleted_at':None,'arquivado_em':None}],'central_briefings':[],'central_copys':[],'central_propostas':[],'central_proposta_servicos':[],'central_previas':[],'central_config':[{'chave':'condicoes','valor':{'itens':copy.deepcopy(COND)}}]})
T.SEQ.update({'central_propostas':0,'central_proposta_servicos':0}); W3=[]; UP=[]
PNG=open('t_img1.png','rb').read()
def conds(p): return [c for c in DB['central_config'][0]['valor']['itens'] if p.get('impresso') or not c['so_impresso']]
def pub(p):
    if not p: return None
    st='expirada' if p['status']=='ativa' and p['data_expiracao']<str(hoje) else p['status']
    return {**{k:p.get(k) for k in('id','cliente_nome','slug','prazo_meses','data_proposta','data_expiracao','link_cartao','dia_cobranca','apresentacao','impresso','exige_contrato','aprovada_em','aprovada_por','forma_pagamento')},'status':st,'pago':bool(p.get('pago_entrada_em')),'condicoes':(p.get('aceite') or {}).get('condicoes') or conds(p),'servicos':[s for s in DB['central_proposta_servicos'] if s['proposta_id']==p['id']]}
def pvpub(v):
    c=next((c for c in DB['central_clientes'] if c['id']==v['cliente_id']),None)
    return {**{k:v[k] for k in('titulo','imagens','link_externo','rodada','status','resposta_nome','resposta_ajustes','respondida_em')},'cliente':c and c['nome']}
async def rpc(route):
    rq=route.request
    if rq.method=='OPTIONS': return await route.fulfill(status=204,headers=CORS)
    b=json.loads(rq.post_data); fn=rq.url.split('/')[-1]; err=lambda m:route.fulfill(status=400,headers=J,body=json.dumps({'message':m}))
    if 'previa' in fn:
        v=next((v for v in DB['central_previas'] if v['token']==b['p_token'] and not v['deleted_at']),None)
        if fn=='central_responder_previa' and v and v['status']=='aguardando':
            aj=[a for a in b['p_ajustes'] if a.strip()] if b['p_acao']=='ajustes' else None
            if aj is not None and len(aj)>3: return await err('limite')
            v.update(status='aprovada' if b['p_acao']=='aprovar' else 'ajustes',resposta_nome=b['p_nome'],resposta_ajustes=aj,respondida_em=T.now()); v['historico'].append({'rodada':v['rodada'],'acao':b['p_acao'],'nome':b['p_nome'],'ajustes':aj,'em':T.now()})
        return await route.fulfill(status=200,headers=J,body=json.dumps(v and pvpub(v)))
    p=next((p for p in DB['central_propostas'] if p['slug']==b['p_slug'] and not p['deleted_at']),None)
    if fn=='central_aprovar_proposta': return await err('use central_aceitar_proposta')
    if fn=='central_aceitar_proposta' and p and not p.get('aprovada_em'):
        d=''.join(ch for ch in b['p_documento'] if ch.isdigit())
        if len(d) not in(11,14): return await err('documento invalido')
        sv=[s for s in DB['central_proposta_servicos'] if s['proposta_id']==p['id']]
        for s in sv:
            if s.get('opcional'): s['aceito']=str(s['id']) in [str(x) for x in b['p_opcionais']]
        ok=[s for s in sv if not s.get('opcional') or s.get('aceito')]; u=sum(s['valor'] for s in ok if s['cobranca']=='unico'); m=sum(s['valor'] for s in ok if s['cobranca']=='mensal')
        if u and b['p_forma'] not in('pix','cartao'): return await err('forma')
        p.update(status='fechada',aprovada_em=T.now(),aprovada_por=b['p_nome'],aprovada_doc=d,forma_pagamento=b['p_forma'] if u else None,aceite={'nome':b['p_nome'],'documento':d,'em':T.now(),'forma':b['p_forma'] if u else None,'total_unico':u,'total_mensal':m,'apresentacao':p.get('apresentacao'),'condicoes':conds(p),'servicos':ok})
    if fn=='central_trocar_forma' and p: p['forma_pagamento']=b['p_forma']
    await route.fulfill(status=200,headers=J,body=json.dumps(pub(p)))
async def previas_post(route):
    rq=route.request
    if rq.method!='POST': return await route.fallback()
    b=json.loads(rq.post_data); v={'id':str(uuid.uuid4()),'token':uuid.uuid4().hex,'cliente_id':None,'link_externo':None,'imagens':[],'rodada':1,'status':'aguardando','resposta_nome':None,'resposta_ajustes':None,'respondida_em':None,'historico':[],'created_at':T.now(),'deleted_at':None,**b}
    DB['central_previas'].insert(0,v); await route.fulfill(status=200,headers=J,body=json.dumps([v]))
async def storage(route):
    rq=route.request
    if rq.method=='OPTIONS': return await route.fulfill(status=204,headers=CORS)
    if rq.method=='POST': UP.append((urlparse(rq.url).path.split('central-previas/')[1],rq.headers.get('content-type'),len(rq.post_data_buffer or b''),'authorization' in rq.headers)); return await route.fulfill(status=200,headers=J,body='{}')
    await route.fulfill(status=200,headers={**CORS,'content-type':'image/png'},body=PNG)
async def w3(route): W3.append(json.loads(route.request.post_data)); await route.fulfill(status=200,content_type='application/json',body='{"success":true}')
async def setup(ctx):
    await T.setup(ctx); await ctx.route('**/rest/v1/rpc/**',rpc); await ctx.route('**/rest/v1/central_previas*',previas_post); await ctx.route('**/storage/v1/**',storage); await ctx.route('https://api.web3forms.com/**',w3)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={'width':1280,'height':900}); await setup(ctx)
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text and '400' not in m.text else None)
        await pg.add_init_script("window.print=()=>{window.__printed=(window.__printed||0)+1}")
        await pg.goto(BASE+'index.html'); await pg.fill('#lEmail','dan@dade.design'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('.stats-row')
        # condições
        await pg.goto(BASE+'index.html#/condicoes'); await pg.wait_for_selector('#condList'); print('condições carregadas:',await pg.locator('.cond-item').count()); await pg.screenshot(path='k_cond.png',full_page=True)
        await pg.click('[data-a=cond-add]'); it=pg.locator('.cond-item').last; await it.locator('[name=titulo]').fill('Textos'); await it.locator('[name=texto]').fill('Criação de textos não inclusa.'); await pg.click('[data-a=cond-save]'); await pg.wait_for_timeout(400); print('condições salvas:',[c['titulo'] for c in DB['central_config'][0]['valor']['itens']])
        # proposta com tudo
        await pg.goto(BASE+'index.html#/propostas'); await pg.wait_for_selector('.page-header'); await pg.click('.page-header [data-a=pro-form]'); await pg.wait_for_selector('#svcList')
        await pg.select_option('#p_cli','cl1'); await pg.fill('#p_apr','Desenvolvimento de folder institucional com dobra central.')
        r1=pg.locator('#svcList .svc-row').nth(0); await r1.locator('[name=servico]').select_option('__custom__'); await r1.locator('[name=servico_custom]').fill('Design de Folder Impresso'); await r1.locator('[name=valor]').press_sequentially('20000'); await r1.locator('[name=prazo]').fill('3 dias úteis'); await r1.locator('[name=nao_incluso]').fill('Criação ou redação dos textos internos')
        await pg.click('[data-a=svc-add]'); r2=pg.locator('#svcList .svc-row').nth(1); await r2.locator('[name=servico]').select_option('__custom__'); await r2.locator('[name=servico_custom]').fill('Criação dos textos'); await r2.locator('[name=valor]').press_sequentially('15000'); await r2.locator('[name=opcional]').check()
        await pg.check('#p_imp'); await pg.check('#p_ctr'); await pg.screenshot(path='k_form.png',full_page=True)
        await pg.click('.modal-foot [type=submit]'); await pg.wait_for_timeout(500); print('toast:',await pg.inner_text('#toast'),'| errs:',errs, '| log:',T.LOG[-3:])
        p=DB['central_propostas'][-1]; sv=[s for s in DB['central_proposta_servicos'] if s['proposta_id']==p['id']]
        print('proposta:',p['slug'],p['impresso'],p['exige_contrato'],p['apresentacao'][:30],'|',[(s['servico'],s['valor'],s['prazo'],s['opcional']) for s in sv])
        print('valor na lista (sem opcional):',(await pg.inner_text('tbody td:nth-child(3)')).strip())
        # proposta pública
        pp=await ctx.new_page(); pp.on('pageerror',lambda e:errs.append('PUB '+str(e)))
        await pp.goto(BASE+'proposta.html?slug='+p['slug']); await pp.wait_for_selector('#hero')
        print('pública: lede =',(await pp.inner_text('#escopo .lede'))[:40],'| prazo:',await pp.locator('.scope-card .sub:has-text("Prazo")').count(),'| não incluso:',await pp.locator('.scope-card .k:text("Não incluso")').count(),'| tag opcional:',await pp.inner_text('.tag-opc'))
        print('  condições:',[await x.inner_text() for x in await pp.locator('#observacoes .note h4').all()],'| prazos:',await pp.inner_text('.prazos .pz'),'| investimento:',await pp.inner_text('.inv .val'),'| card opcionais:',(await pp.inner_text('.pay-card:has-text("Opcionais") .pv')))
        await pp.locator('#observacoes').scroll_into_view_if_needed(); await pp.wait_for_timeout(300); await pp.screenshot(path='k_pub_obs.png'); await pp.locator('.prazos').scroll_into_view_if_needed(); await pp.screenshot(path='k_pub_prazos.png')
        # aprovação
        await pp.goto(BASE+'pagamento.html?slug='+p['slug']); await pp.wait_for_selector('#ok'); print('pix antes:',await pp.inner_text('.opt[data-f=pix] span'))
        await pp.click('.opt[data-o]'); print('pix com opcional:',await pp.inner_text('.opt[data-f=pix] span'),'| total:',await pp.inner_text('#totais .ln:last-child'))
        await pp.click('.opt[data-f=pix]'); await pp.fill('#nome','Marcos Silva'); await pp.fill('#doc','111.111.111-11'); await pp.click('#ok'); print('doc inválido:',await pp.inner_text('#err'))
        await pp.fill('#doc','52.409.459/0001-47'); await pp.click('#ok'); print('sem aceite:',await pp.inner_text('#err')); await pp.screenshot(path='k_aprovar.png',full_page=True)
        await pp.check('#li'); await pp.click('#ok'); await pp.wait_for_selector('.key'); print('aprovada: entrada',await pp.inner_text('.key strong >> nth=0'),'| contrato:',await pp.locator('.box:has(h2:text("Contrato"))').count())
        print('aceite gravado:',p['aprovada_doc'],p['aceite']['total_unico'],[c['titulo'] for c in p['aceite']['condicoes']],'| aviso:',W3[-1]['message'].replace('\n',' / ')[:230])
        # central: comprovante e pendência de contrato
        await pg.goto(BASE+'index.html#/'); await pg.reload(); await pg.wait_for_selector('.grid2'); print('pendências:',[ (await x.inner_text()).split('\n')[0] for x in await pg.locator('.grid2 .panel:first-child .row').all()])
        await pg.goto(BASE+'index.html#/propostas'); await pg.wait_for_selector('table'); await pg.click('[data-a=pay-open]'); await pg.wait_for_selector('[data-a=pro-comp]'); await pg.screenshot(path='k_paymodal.png'); await pg.click('[data-a=pro-comp]')
        txt=await pg.evaluate("document.getElementById('print').innerText"); print('comprovante:',await pg.evaluate('window.__printed'),'|',' / '.join(l for l in txt.split('\n') if l.strip())[:420])
        await pg.click('.modal [data-a=close]')
        # prévias
        await pg.goto(BASE+'index.html#/previas'); await pg.wait_for_selector('.page-header'); await pg.click('.page-header [data-a=pre-form]'); await pg.wait_for_selector('#v_img')
        await pg.select_option('#v_cli','cl1'); await pg.fill('#v_tit','Identidade visual · primeira versão'); await pg.set_input_files('#v_img',['t_img1.png','t_img2.png']); await pg.click('#v_ok'); await pg.wait_for_selector('.thumbs',timeout=15000)
        v=DB['central_previas'][0]; print('prévia criada:',v['titulo'],len(v['imagens']),'imgs | uploads:',[(u[0].split('/')[1][:8],u[1],u[2],u[3]) for u in UP]); await pg.screenshot(path='k_previa_adm.png',full_page=True)
        pv=await ctx.new_page(); pv.on('pageerror',lambda e:errs.append('PREV '+str(e)))
        await pv.goto(BASE+'previa.html?t='+v['token']); await pv.wait_for_selector('#ok'); await pv.wait_for_timeout(400); await pv.screenshot(path='k_previa_pub.png',full_page=True)
        await pv.click('#ok'); print('prévia sem escolha:',await pv.inner_text('#err')); await pv.click('.opt[data-m=ajustes]'); print('texto rodada 1:',(await pv.inner_text('.opt[data-m=ajustes] span'))[:60]); await pv.fill('#nome','Marcos'); await pv.click('#ok'); print('sem ajuste:',await pv.inner_text('#err'))
        await pv.fill('#a1','Deixar o azul mais escuro'); await pv.fill('#a2','Testar outra fonte no nome'); await pv.click('#ok'); await pv.wait_for_selector('text=Ajustes pedidos'); print('resposta:',v['status'],v['resposta_ajustes'],'| aviso:',W3[-1]['subject'])
        await pg.goto(BASE+'index.html#/'); await pg.reload(); await pg.wait_for_selector('.grid2'); print('pendência prévia:',await pg.locator('.row:has-text("pediu ajustes na prévia")').count(),'| badge menu:',await pg.inner_text('#nav a[href="#/previas"] .nav-count'))
        await pg.goto(BASE+'index.html#/previa/'+v['id']); await pg.wait_for_selector('.panel'); await pg.click('.page-header [data-a=pre-form]'); await pg.wait_for_selector('#v_img'); await pg.set_input_files('#v_img',['t_img1.png']); await pg.click('#v_ok'); await pg.wait_for_timeout(1500)
        print('nova versão: rodada',v['rodada'],v['status'],len(v['imagens']),'img | histórico:',len(v['historico']))
        await pv.reload(); await pv.wait_for_selector('#ok'); await pv.click('.opt[data-m=ajustes]'); print('texto rodada 2:',(await pv.inner_text('.opt[data-m=ajustes] span'))[:70]); await pv.click('.opt[data-m=aprovar]'); await pv.fill('#nome','Marcos'); await pv.click('#ok'); await pv.wait_for_selector('text=Prévia aprovada'); print('final:',v['status'],'| aviso:',W3[-1]['subject'])
        await pg.goto(BASE+'index.html#/cliente/cl1'); await pg.wait_for_selector('.dados'); print('ficha tem prévia:',await pg.locator('.panel:has(h2:text("Prévias")) .row').count())
        m=await b.new_context(viewport={'width':375,'height':740}); await setup(m); mp=await m.new_page()
        for u in ['previa.html?t='+v['token'],'pagamento.html?slug='+p['slug'],'proposta.html?slug='+p['slug']]:
            await mp.goto(BASE+u); await mp.wait_for_timeout(500); print('mobile',u.split('?')[0],'overflow',await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        print('ERRS',errs); await b.close()
if __name__=="__main__": asyncio.run(main())
