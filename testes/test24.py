import asyncio, datetime
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
hj = datetime.date.today(); d = lambda n: str(hj + datetime.timedelta(days=n))
DB['central_portfolio'] = []
DB['central_tarefas'] = [
 {'id':'t1','texto':'Revisar logo Lucrum','data':d(0),'feita_em':None,'ordem':10,'created_at':T.now(),'prazo':None},
 {'id':'t2','texto':'Posts da semana Forster','data':d(-2),'feita_em':None,'ordem':20,'created_at':T.now(),'prazo':d(-1)},
 {'id':'t3','texto':'Reunião com cliente novo','data':d(3),'feita_em':None,'ordem':30,'created_at':T.now(),'prazo':None},
 {'id':'t4','texto':'Mandar orçamento','data':d(0),'feita_em':T.now(),'ordem':5,'created_at':T.now(),'prazo':None}]
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    for vw, nm in (((1280, 900), 'd'), ((390, 844), 'm')):
      ctx = await b.new_context(viewport={'width': vw[0], 'height': vw[1]}); await T9.setup(ctx)
      pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
      await pg.goto(BASE + 'index.html#/agenda'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#tarNova')
      if nm == 'd':
        await pg.fill('#tarNova', 'Entregar identidade 2go'); await pg.fill('#tarPrazo', d(2)); await pg.click('.ag-add [type=submit]'); await pg.wait_for_timeout(500)
        print('nova:', [(x['texto'], x['data'], x.get('prazo')) for x in DB['central_tarefas'] if x['texto'].startswith('Entregar')])
        print('hoje:', await pg.locator('#agPend .tarefa .tx').all_inner_texts())
        await pg.click('[data-a=tar-prazo][data-id=t1]'); await pg.fill('#tp_d', d(5)); await pg.click('#modalBox [type=submit]'); await pg.wait_for_timeout(500)
        print('t1 prazo:', next(x for x in DB['central_tarefas'] if x['id']=='t1').get('prazo'))
      await pg.screenshot(path=f'ag_dia_{nm}.png', full_page=True)
      await pg.click('[data-a=ag-vis][data-v=mes]'); await pg.wait_for_timeout(300)
      await pg.screenshot(path=f'ag_mes_{nm}.png', full_page=True)
      print(nm, 'overflow', await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
      sel = '.cal .d.hj' if nm == 'd' else '.cal-lista .dl.hj'
      await pg.click(f'[data-a=ag-ir][data-v="{d(2)}"] >> visible=true'); await pg.wait_for_timeout(300)
      print('dia+2:', await pg.locator('.ag-nav strong').inner_text(), await pg.locator('.tarefa .tx').all_inner_texts())
    print('ERRS', errs); await b.close()
asyncio.run(main())
