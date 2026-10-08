import asyncio, datetime
from playwright.async_api import async_playwright
import test5 as T5
T=T5.T; DB=T.DB; BASE=T.BASE
h=datetime.date.today(); ontem=str(h-datetime.timedelta(days=1)); hj=str(h)
DB['central_tarefas']=[{'id':'t1','texto':'Mandar proposta da Lume','data':ontem,'feita_em':None,'ordem':0,'created_at':T.now()},{'id':'t2','texto':'Revisar copy','data':hj,'feita_em':None,'ordem':0,'created_at':T.now()}]
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={'width':1280,'height':900}); await T5.setup(ctx)
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(BASE+'index.html'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('.stats-row')
        print('menu:',[ (await x.inner_text()).replace('\n',' ') for x in await pg.locator('#nav a, #nav .nav-group').all()])
        print('início:',await pg.inner_text('.page-header h1'),'|',(await pg.inner_text('.page-header p'))[:40],'| agenda hoje:',[ (await x.inner_text()).replace('\n',' ') for x in await pg.locator('.panel .tarefa').all()])
        await pg.screenshot(path='n_home.png',full_page=True)
        await pg.fill('#tarNova','Ligar para a gráfica'); await pg.press('#tarNova','Enter'); await pg.wait_for_timeout(400); print('adicionada:',[x['texto'] for x in DB['central_tarefas']][-1],DB['central_tarefas'][-1]['data']==hj)
        await pg.click('[data-c=tar-ck][data-id=t1]'); await pg.wait_for_timeout(400); print('t1 feita:',bool(DB['central_tarefas'][0]['feita_em']))
        await pg.goto(BASE+'index.html#/agenda'); await pg.wait_for_selector('.ag-nav'); await pg.screenshot(path='n_agenda.png',full_page=True)
        print('agenda:',await pg.inner_text('.ag-nav strong'),'|',[ (await x.inner_text()).replace('\n',' ')[:40] for x in await pg.locator('.tarefa').all()])
        await pg.click('[data-a=tar-amanha][data-id=t2]'); await pg.wait_for_timeout(400); print('t2 amanhã:',DB['central_tarefas'][1]['data'])
        await pg.click('[data-a=ag-dia][data-v="1"]'); print('amanhã mostra:',[ (await x.inner_text())[:20] for x in await pg.locator('.tarefa .tx').all()])
        await pg.click('[data-a=ag-dia][data-v="0"]'); await pg.click('[data-a=ag-dia][data-v="-1"]'); print('ontem:',await pg.inner_text('.panel'))
        await pg.goto(BASE+'index.html#/copys'); await pg.wait_for_selector('.tabs'); print('abas briefings:',[await x.inner_text() for x in await pg.locator('.tab').all()],'| ativo menu:',await pg.inner_text('#nav a.active'))
        await pg.goto(BASE+'index.html#/condicoes'); await pg.wait_for_selector('.tabs'); print('abas propostas:',[await x.inner_text() for x in await pg.locator('.tab').all()],'| ativo:',await pg.inner_text('.tab.on')); await pg.screenshot(path='n_tabs.png')
        await pg.goto(BASE+'index.html#/previa/x'); await pg.wait_for_timeout(200); print('prévia sem abas:',await pg.locator('.tabs').count())
        m=await b.new_context(viewport={'width':375,'height':740}); await T5.setup(m); mp=await m.new_page(); await mp.goto(BASE+'index.html'); await mp.fill('#lEmail','a@a.com'); await mp.fill('#lPass','x'); await mp.click('#lBtn'); await mp.wait_for_selector('.stats-row')
        for k in ['','agenda','propostas']: await mp.goto(BASE+'index.html#/'+k); await mp.wait_for_timeout(200); print('mobile',k,'overflow',await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await mp.goto(BASE+'index.html#/agenda'); await mp.screenshot(path='n_m_agenda.png',full_page=True)
        print('ERRS',errs); await b.close()
asyncio.run(main())
