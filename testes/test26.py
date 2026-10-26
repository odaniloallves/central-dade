import asyncio, datetime, json, random
from playwright.async_api import async_playwright
import test25 as T25
T = T25.T; DB = T.DB; BASE = T.BASE; d = T25.d
DB['central_tarefas'] = [{'id':f't{i}','texto':f'Tarefa {i}','data':d(random.randint(-40,30)),'feita_em':(T.now() if i%2 else None),'ordem':i,'created_at':T.now(),'prazo':(d(random.randint(-5,30)) if i%3==0 else None)} for i in range(400)]
T25.EV += [{'id':f'x{i}','status':'confirmed','summary':f'Evento {i}','start':{'dateTime':d(random.randint(-7,40))+'T10:00:00-03:00'},'end':{'dateTime':d(0)+'T11:00:00-03:00'},'htmlLink':'#'} for i in range(200)]
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    ctx = await b.new_context(viewport={'width':1280,'height':900}); await T25.setup(ctx)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(BASE + 'index.html#/agenda'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('#tarNova')
    await pg.click('[data-a=g-ligar]'); await pg.wait_for_timeout(800)
    for i in range(3):
      t = await pg.evaluate("()=>{const t=performance.now();document.querySelector('[data-a=ag-vis][data-v=mes]').click();return performance.now()-t}")
      print('mês ms:', round(t), await pg.locator('.cal .d .it').count())
      await pg.click('[data-a=ag-vis][data-v=dia]')
    print('ERRS', errs); await b.close()
asyncio.run(main())
