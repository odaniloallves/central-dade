import asyncio
from playwright.async_api import async_playwright
import test11 as T11
T9 = T11.T9; T5 = T9.T5; T = T9.T; DB = T.DB; BASE = T.BASE
DELS = []
async def setup(ctx):
    await T9.setup(ctx)
    async def stor(route):
        if route.request.method == 'DELETE': DELS.append(route.request.url.split('central-previas/')[1]); return await route.fulfill(status=200, headers={**T.CORS, 'content-type': 'application/json'}, body='{}')
        await route.fallback()
    await ctx.route('**/storage/v1/**', stor)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/previas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('[data-a=pre-form]')
        await pg.click('.page-header [data-a=pre-form]'); await pg.fill('#v_tit', 'Logo · primeira versão')
        await pg.set_input_files('#v_img', ['t_img1.png', 't_img2.png']); await pg.wait_for_timeout(200)
        print('escolhidos:', await pg.locator('.arq div').all_inner_texts())
        await pg.screenshot(path='w_modal.png')
        await pg.click('[data-a=pre-rm][data-i="0"]'); print('após remover:', await pg.locator('.arq div').all_inner_texts())
        await pg.set_input_files('#v_img', ['t_img1.png']); print('após somar:', await pg.locator('.arq div').all_inner_texts())
        n0 = len(T5.UP); await pg.click('#v_ok'); await pg.wait_for_selector('.thumbs .th', timeout=10000)
        v = DB['central_previas'][0]; print('enviadas:', len(T5.UP) - n0, '| imagens:', len(v['imagens']))
        await pg.click('.thumbs .th button >> nth=0'); await pg.click('[data-a=pre-img-del]'); await pg.wait_for_timeout(500)
        print('após remover enviada:', len(DB['central_previas'][0]['imagens']), '| storage apagado:', len(DELS))
        link = await pg.locator('.page-header [data-a=copy-text]').get_attribute('data-text'); print('link prévia:', link, len(link))
        await pg.goto(BASE + 'index.html#/briefings'); await pg.wait_for_selector('.linkcard')
        print('links briefing:', await pg.locator('.linkcard code').all_inner_texts())
        await pg.goto(BASE + 'index.html#/propostas'); await pg.wait_for_selector('table')
        pl = await pg.locator('[data-a=copy-text]').first.get_attribute('data-text'); print('link proposta:', pl, len(pl))
        await pg.goto(BASE + 'p.html?veste-aurea-jd0kem'); await pg.wait_for_timeout(500); print('p redireciona:', pg.url.replace(BASE, ''))
        await pg.goto(BASE + 'v.html?abc123def456'); await pg.wait_for_timeout(500); print('v redireciona:', pg.url.replace(BASE, ''))
        await pg.goto(BASE + 'lp.html'); await pg.wait_for_timeout(500); print('lp redireciona:', pg.url.replace(BASE, ''))
        print('ERRS', errs); await b.close()
asyncio.run(main())
