import asyncio, json
from playwright.async_api import async_playwright
import test5 as T5
T=T5.T; DB=T.DB; BASE=T.BASE; J=T5.J
_pub=T5.pub
def pub(p):
    o=_pub(p)
    if o:
        c=next((c for c in DB['central_clientes'] if c['id']==p.get('cliente_id')),None)
        o['cadastro_ok']=bool(p.get('cadastro_em')) or bool(c and c.get('documento') and c.get('endereco') and c.get('email')); o['aprovada_doc']=p.get('aprovada_doc')
    return o
T5.pub=pub
async def rpc(route):
    rq=route.request
    if rq.method!='OPTIONS' and rq.url.endswith('central_cadastro_cliente'):
        b=json.loads(rq.post_data); p=next(p for p in DB['central_propostas'] if p['slug']==b['p_slug'])
        if not p.get('cliente_id'): DB['central_clientes'].append({'id':'novo','nome':p['cliente_nome'],'created_at':T.now(),'deleted_at':None,'arquivado_em':None}); p['cliente_id']='novo'
        c=next(c for c in DB['central_clientes'] if c['id']==p['cliente_id'])
        for k,v in b['p'].items():
            if v and not c.get(k): c[k]=''.join(ch for ch in v if ch.isdigit()) if k=='documento' else v
        p['cadastro_em']=T.now(); return await route.fulfill(status=200,headers=J,body=json.dumps(pub(p)))
    await T5.rpc(route)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={'width':1280,'height':900}); await T5.setup(ctx); await ctx.route('**/rest/v1/rpc/**',rpc)
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        # formulário de briefing
        await pg.goto(BASE+'briefing/identidade.html'); await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.wait_for_selector('[data-id=documento]')
        print('etapa 1 campos:',[await x.inner_text() for x in await pg.locator('.lbl').all()])
        for k,v in dict(empresa='Rota Log',documento='11.111.111/1111-11',responsavel='Bruno',email='b@rota.com.br',whatsapp='11 98888-7777').items(): await pg.fill(f'[data-id={k}]',v)
        await pg.click('#next'); print('doc inválido:',await pg.inner_text('.field.invalid .err'))
        await pg.fill('[data-id=documento]','52.409.459/0001-47'); await pg.click('#next'); print('avançou para:',await pg.inner_text('#progress-name'))
        for s in range(5):
            await pg.evaluate("""()=>{STEPS[step].fields.forEach(f=>{if(!f.req)return;if(f.type==='repeat'){data[f.id]=[Object.fromEntries(f.fields.filter(x=>x.type!=='flag').map(x=>[x.id,'Teste']))]}else if(f.type==='cards'){data[f.id]=f.options[0][0]}else if(!data[f.id]){data[f.id]='Teste'}});save();render()}"""); await pg.click('#next')
        await pg.wait_for_selector('.done'); bri=DB['central_briefings'][0]; print('gravado:',bri['documento'],bri.get('razao_social'),bri.get('endereco'))
        # central: cliente a partir do briefing
        await pg.goto(BASE+'index.html'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('#cvStage')
        await pg.goto(BASE+'index.html#/briefing/'+bri['id']); await pg.wait_for_selector('[data-a=bri-newcli]'); await pg.click('[data-a=bri-newcli]'); await pg.wait_for_selector('[data-a=bri-unlink]')
        c=DB['central_clientes'][-1]; print('cliente criado:',c['nome'],c['documento'],c['contato'],c['email'],c['whatsapp'])
        # vincular a cliente existente completa os vazios
        DB['central_briefings'].append({**bri,'id':'b2','cliente_id':None,'empresa':'Brasil Web'}); await pg.goto(BASE+'index.html#/briefing/b2'); await pg.reload(); await pg.wait_for_selector('[data-c=bri-link]')
        await pg.select_option('[data-c=bri-link]','cl1'); await pg.wait_for_timeout(500); c1=DB['central_clientes'][0]; print('existente completado:',c1['nome'],c1.get('documento'),c1.get('email'),'| contato mantido:',c1['contato'],'|',await pg.inner_text('#toast'))
        # proposta sem briefing: cadastro depois da aprovação
        T.SEQ['central_propostas']+=1; DB['central_propostas'].append({'id':T.SEQ['central_propostas'],'cliente_id':None,'cliente_nome':'Casa Nobre','slug':'casa-nobre','status':'ativa','data_proposta':'2026-10-08','data_expiracao':'2026-12-01','created_at':T.now(),'deleted_at':None,'impresso':False,'exige_contrato':True})
        T.SEQ['central_proposta_servicos']+=1; DB['central_proposta_servicos'].append({'id':T.SEQ['central_proposta_servicos'],'proposta_id':T.SEQ['central_propostas'],'servico':'landing_page','cobranca':'unico','valor':7000,'ordem':0,'opcional':False})
        pp=await ctx.new_page(); pp.on('pageerror',lambda e:errs.append('PAG '+str(e)))
        await pp.goto(BASE+'pagamento.html?slug=casa-nobre'); await pp.wait_for_selector('#ok'); await pp.click('.opt[data-f=pix]'); await pp.fill('#nome','Helena Prado'); await pp.fill('#doc','52409459000147'); await pp.check('#li'); await pp.click('#ok')
        await pp.wait_for_selector('#cok'); print('pede cadastro:',await pp.inner_text('#cad h2'),'| doc preenchido:',await pp.input_value('#c_documento'),'| responsável:',await pp.input_value('#c_contato')); await pp.screenshot(path='m_cad.png',full_page=True)
        await pp.click('#cok'); print('validação:',await pp.inner_text('#cerr'))
        await pp.fill('#c_email','h@casanobre.com.br'); await pp.fill('#c_whatsapp','11 97777-0000'); await pp.click('#cok'); await pp.wait_for_selector('text=Dados recebidos')
        nc=next(c for c in DB['central_clientes'] if c['id']=='novo'); print('cliente novo pela aprovação:',nc['nome'],nc.get('contato'),nc.get('whatsapp'),nc['documento'],nc['email'],'| aviso:',T5.W3[-1]['subject'])
        await pp.reload(); await pp.wait_for_selector('h1'); print('recarregar não pede de novo:',await pp.locator('#cok').count())
        m=await b.new_context(viewport={'width':375,'height':740}); await T5.setup(m); mp=await m.new_page(); await mp.goto(BASE+'briefing/lp.html'); await mp.wait_for_selector('[data-id=documento]'); print('mobile overflow:',await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        print('ERRS',errs); await b.close()
asyncio.run(main())
