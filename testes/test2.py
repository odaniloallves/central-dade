import asyncio, json, uuid, datetime
from urllib.parse import urlparse, parse_qsl
from playwright.async_api import async_playwright
BASE='http://localhost:8765/'
DB={'central_tarefas':[],'central_entradas':[],'central_planos':[],'central_fechamentos':[],'central_admins':[{'user_id':'u1'}],'central_clientes':[{'id':'cl1','nome':'Studio Forma Fitness','contato':'Marina','email':None,'whatsapp':None,'segmento':'Fitness','created_at':'2026-10-01T10:00:00Z','deleted_at':None}],
    'central_briefings':[{'id':'b1','cliente_id':None,'tipo':'identidade','empresa':'Rota Log','responsavel':'Bruno','email':'b@r.com','whatsapp':'11','respostas':{'etapas':[]},'status':'novo','created_at':'2026-10-06T10:00:00Z','deleted_at':None}],
    'central_copys':[],'central_propostas':[
      {'id':1,'cliente_id':'cl1','cliente_nome':'Studio Forma Fitness','slug':'studio-forma-fitness','status':'ativa','prazo_meses':6,'condicao_pagamento':'50_50_data','data_proposta':'2026-09-20','data_expiracao':'2026-10-10','created_at':'2026-09-20T10:00:00Z','deleted_at':None},
      {'id':2,'cliente_id':None,'cliente_nome':'Casa Nobre','slug':'casa-nobre','status':'ativa','prazo_meses':None,'condicao_pagamento':'avista','data_proposta':'2026-07-05','data_expiracao':'2026-08-05','created_at':'2026-07-05T10:00:00Z','deleted_at':None}],
    'central_proposta_servicos':[{'id':1,'proposta_id':1,'servico':'identidade_visual','cobranca':'unico','valor':6800,'ordem':0},{'id':2,'proposta_id':1,'servico':'criativos_social','cobranca':'mensal','valor':2400,'ordem':1},{'id':3,'proposta_id':2,'servico':'landing_page','cobranca':'unico','valor':7000,'ordem':0}]}
SEQ={'central_propostas':2,'central_proposta_servicos':3}
LOG=[]; CORS={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*'}
now=lambda:datetime.datetime.now(datetime.UTC).isoformat()
def match(r,q):
    for k,v in q:
        if k in('select','order') or '.' not in v: continue
        op,val=v.split('.',1); x=r.get(k)
        if op=='eq' and str(x)!=val: return False
        if op=='lt' and not (x is not None and str(x)<val): return False
        if op=='is' and val=='null' and x is not None: return False
        if op=='in' and str(x) not in val.strip('()').split(','): return False
    return True
def pub(slug):
    p=next((p for p in DB['central_propostas'] if p['slug']==slug and not p['deleted_at']),None)
    return p and {**p,'servicos':[s for s in DB['central_proposta_servicos'] if s['proposta_id']==p['id']]}
async def rest(route):
    rq=route.request; u=urlparse(rq.url); tab=u.path.split('/')[-1]; q=parse_qsl(u.query); h=rq.headers
    if rq.method=='OPTIONS': return await route.fulfill(status=204,headers=CORS)
    J={**CORS,'content-type':'application/json'}
    if '/rpc/' in u.path: return await route.fulfill(status=200,headers=J,body=json.dumps(pub(json.loads(rq.post_data)['p_slug'])))
    LOG.append((rq.method,tab,u.query[:60]))
    if 'authorization' not in h and rq.method!='POST': return await route.fulfill(status=401,headers=J,body='{}')
    rows=DB[tab]; sel=[r for r in rows if match(r,q)]
    if rq.method=='GET':
        out=[dict(r) for r in sel]
        if tab=='central_propostas':
            for r in out: r['servicos']=[s for s in DB['central_proposta_servicos'] if s['proposta_id']==r['id']]
    elif rq.method=='POST':
        body=json.loads(rq.post_data); body=body if isinstance(body,list) else [body]; out=[]
        for b in body:
            if tab in SEQ: SEQ[tab]+=1; i=SEQ[tab]
            else: i=str(uuid.uuid4())
            row={'id':i,'created_at':now(),'updated_at':now(),'deleted_at':None,**({'status':'ativa'} if tab=='central_propostas' else {}),**b}; rows.append(row); out.append(row)
    elif rq.method=='PATCH':
        for r in sel: r.update(json.loads(rq.post_data))
        out=sel
    else:
        DB[tab]=[r for r in rows if r not in sel]; out=sel
        if tab=='central_propostas': DB['central_proposta_servicos']=[s for s in DB['central_proposta_servicos'] if s['proposta_id'] not in [r['id'] for r in sel]]
    await route.fulfill(status=200,headers=J,body=json.dumps(out,default=str))
async def auth(route):
    if route.request.method=='OPTIONS': return await route.fulfill(status=204,headers=CORS)
    await route.fulfill(status=200,headers={**CORS,'content-type':'application/json'},body=json.dumps({'access_token':'tok','refresh_token':'ref','expires_in':3600,'user':{'email':'dan@dade.design'}}))
async def setup(ctx):
    await ctx.route('**/rest/v1/**',rest); await ctx.route('**/auth/v1/**',auth); await ctx.route('https://fonts.g*/**',lambda r:r.abort())
    await ctx.grant_permissions(['clipboard-read','clipboard-write'])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={'width':1440,'height':900}); await setup(ctx)
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
        await pg.goto(BASE+'index.html'); await pg.fill('#lEmail','dan@dade.design'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('.stats-row')
        print('expirou vencida:',[ (p['id'],p['status']) for p in DB['central_propostas']]); await pg.screenshot(path='p_home.png',full_page=True)
        await pg.goto(BASE+'index.html#/propostas'); await pg.wait_for_selector('table'); await pg.screenshot(path='p_lista.png',full_page=True)
        print('valores:',[await x.inner_text() for x in await pg.locator('.stats-row.values .stat-value').all()])
        # filtro
        await pg.select_option('.filters-bar [name=status]','expirada'); await pg.click('.filters-bar [type=submit]'); print('filtro expirada:',await pg.locator('tbody tr').count()); await pg.click('[data-a=pro-clear]')
        # nova proposta
        await pg.click('.page-header [data-a=pro-form]'); await pg.wait_for_selector('#svcList'); await pg.screenshot(path='p_modal.png')
        await pg.click('.modal-foot [type=submit]'); await pg.wait_for_timeout(200); print('validação:',await pg.inner_text('#toast'))
        await pg.select_option('#p_cli',''); await pg.fill('#p_nome','Clínica Ágil & Cia')
        await pg.select_option('#svcList [name=servico]','sustentacao'); print('cobrança auto:',await pg.input_value('#svcList [name=cobranca]'))
        await pg.locator('#svcList [name=valor]').press_sequentially('600000'); print('máscara:',await pg.input_value('#svcList [name=valor]'))
        await pg.click('[data-a=svc-add]'); r2=pg.locator('#svcList .svc-row').nth(1); await r2.locator('[name=servico]').select_option('__custom__'); await r2.locator('[name=servico_custom]').fill('Consultoria de marca'); await r2.locator('[name=valor]').press_sequentially('350000')
        await pg.select_option('#p_cond','custom'); await pg.fill('#p_condc','30/60/90'); await pg.fill('#p_prazo','12')
        await pg.click('.modal-foot [type=submit]'); await pg.wait_for_timeout(500)
        np=DB['central_propostas'][-1]; print('criada:',np['id'],np['slug'],np['condicao_pagamento'],np['prazo_meses'],[(s['servico'],s['cobranca'],s['valor'],s['ordem']) for s in DB['central_proposta_servicos'] if s['proposta_id']==np['id']])
        # editar
        await pg.click(f'[data-a=pro-form][data-id="{np["id"]}"]'); await pg.wait_for_selector('#p_st'); print('edição carrega:',await pg.input_value('#p_nome'),'|',await pg.input_value('#p_condc'),'|',[await x.input_value() for x in await pg.locator('#svcList [name=valor]').all()],'|',await pg.locator('#svcList [name=servico_custom]').nth(1).input_value())
        await pg.locator('#svcList .svc-row').nth(1).locator('[data-a=svc-rm]').click(); await pg.click('.modal-foot [type=submit]'); await pg.wait_for_timeout(500)
        print('após editar:',[(s['servico'],s['valor']) for s in DB['central_proposta_servicos'] if s['proposta_id']==np['id']])
        # fechar / reabrir / perder
        await pg.click(f'[data-a=pro-ask][data-id="{np["id"]}"][data-v=fechada]'); await pg.click('.modal [data-a=pro-st]'); await pg.wait_for_timeout(400); print('status:',np['status'])
        await pg.click(f'[data-a=pro-st][data-id="{np["id"]}"]'); await pg.wait_for_timeout(400); print('reaberta:',np['status'])
        await pg.click('[data-a=copy-text] >> nth=0'); print('link:',await pg.evaluate('navigator.clipboard.readText()'))
        # do briefing
        await pg.goto(BASE+'index.html#/briefing/b1'); await pg.wait_for_selector('[data-a=pro-form]'); await pg.screenshot(path='p_briefing.png'); await pg.click('[data-a=pro-form]'); await pg.wait_for_selector('#svcList')
        print('do briefing:',await pg.input_value('#p_nome'),'|',await pg.input_value('#svcList [name=servico]')); await pg.click('.modal [data-a=close]')
        await pg.goto(BASE+'index.html#/numeros'); await pg.wait_for_selector('.grid2'); await pg.screenshot(path='p_numeros.png',full_page=True)
        await pg.goto(BASE+'index.html#/cliente/cl1'); await pg.wait_for_selector('.panel'); print('ficha tem proposta:',await pg.locator('text=Proposta nº 0001').count())
        # lixeira
        await pg.goto(BASE+'index.html#/propostas'); await pg.wait_for_selector('table'); await pg.click('[data-a=trash][data-id="2"]'); await pg.wait_for_timeout(400)
        await pg.goto(BASE+'index.html#/lixeira'); await pg.wait_for_selector('table'); print('lixeira:',await pg.inner_text('tbody tr td:nth-child(2)'))
        # página pública
        pp=await ctx.new_page(); pp.on('pageerror',lambda e:errs.append('PUB '+str(e)))
        await pp.goto(BASE+'proposta.html?slug=studio-forma-fitness'); await pp.wait_for_selector('#hero'); await pp.wait_for_timeout(500); await pp.screenshot(path='pub_top.png')
        print('pública:',await pp.inner_text('#hero h1'),'|',await pp.inner_text('.inv .val'),'|',await pp.locator('.scope-card').count(),'cards |',await pp.title())
        await pp.locator('#investimento').scroll_into_view_if_needed(); await pp.wait_for_timeout(400); await pp.screenshot(path='pub_inv.png')
        await pp.locator('#fundador').scroll_into_view_if_needed(); await pp.wait_for_timeout(400); await pp.screenshot(path='pub_fund.png')
        await pp.goto(BASE+'proposta.html?slug=casa-nobre'); await pp.wait_for_selector('.expired'); print('lixeira/expirada ->',await pp.inner_text('.expired h1'))
        await pp.goto(BASE+'proposta.html?slug=nao-existe'); await pp.wait_for_selector('.expired'); print('inexistente ->',await pp.inner_text('.expired h1'))
        m=await b.new_context(viewport={'width':375,'height':740}); await setup(m); mp=await m.new_page()
        await mp.goto(BASE+'proposta.html?slug=studio-forma-fitness'); await mp.wait_for_selector('#hero'); print('pub mobile overflow',await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await mp.goto(BASE+'index.html'); await mp.fill('#lEmail','a@a.com'); await mp.fill('#lPass','x'); await mp.click('#lBtn'); await mp.wait_for_selector('.stats-row'); await mp.goto(BASE+'index.html#/propostas'); await mp.wait_for_timeout(300)
        print('app mobile overflow',await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.click('.page-header [data-a=pro-form]'); await mp.wait_for_selector('#svcList'); await mp.screenshot(path='p_m_modal.png')
        print('ERRS',errs); await b.close()
if __name__=="__main__": asyncio.run(main())
