import asyncio
from playwright.async_api import async_playwright
import test25 as T25
T = T25.T; DB = T.DB; BASE = T.BASE; d = T25.d
DB['central_tarefas'] = [{'id':'t1','texto':'Revisar logo Lucrum','data':d(0),'feita_em':None,'ordem':10,'created_at':T.now(),'prazo':None,'descricao':None},
  {'id':'t2','texto':'Posts da semana Forster','data':d(0),'feita_em':None,'ordem':20,'created_at':T.now(),'prazo':d(2),'descricao':'Fazer 3 posts de feed e 2 stories com a campanha de Black Friday, seguindo o briefing que chegou por e-mail'}]
DB['central_tarefas'][1]['data']=d(0); DB['central_tarefas'][1]['prazo']=None
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    for vw, nm in (((1280, 900), 'd'), ((390, 844), 'm')):
      ctx = await b.new_context(viewport={'width':vw[0],'height':vw[1]}); await T25.setup(ctx)
      await ctx.grant_permissions(['clipboard-read','clipboard-write'], origin='http://localhost:8765')
      pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
      await pg.goto(BASE + 'index.html#/agenda'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('#tarNova')
      await pg.click('[data-a=g-ligar]'); await pg.wait_for_timeout(800)
      if nm == 'd':
        await pg.click('.reu-it [data-a=copy-text]'); await pg.wait_for_timeout(200); print('copiado:', await pg.evaluate('navigator.clipboard.readText()'), '|', await pg.locator('.reu-lk').first.inner_text())
        h1 = await pg.locator('.tarefa[data-tid=t1]').bounding_box()
        await pg.hover('.tarefa[data-tid=t1]'); await pg.click('[data-a=tar-ds][data-id=t1]'); await pg.fill('.ds-ed', 'Ajustar o dourado e mandar versão final'); await pg.click('.page-header h1'); await pg.wait_for_timeout(500)
        print('salvo:', DB['central_tarefas'][0]['descricao'])
        h2 = await pg.locator('.tarefa[data-tid=t1]').bounding_box(); print('altura antes/depois:', round(h1['height']), round(h2['height']))
        await pg.click('[data-a=tar-ds][data-id=t2]'); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300); print('esc mantém:', DB['central_tarefas'][1]['descricao'][:20], await pg.locator('#modal.open').count())
      await pg.screenshot(path=f'ds_{nm}.png', full_page=True)
      print(nm, 'overflow', await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
    print('ERRS', errs); await b.close()
asyncio.run(main())
