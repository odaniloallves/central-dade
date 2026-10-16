import asyncio, json
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_portfolio'] = []
UPS = []
async def setup(ctx):
    await T9.setup(ctx)
    J = {**T.CORS, 'content-type': 'application/json'}
    async def stor(route):
        rq = route.request
        if rq.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        if 'central-portfolio' not in rq.url: return await route.fallback()
        if rq.method == 'POST': UPS.append(rq.url.split('central-portfolio/')[1]); return await route.fulfill(status=200, headers=J, body='{}')
        if rq.method == 'DELETE': return await route.fulfill(status=200, headers=J, body='[]')
        await route.fulfill(status=200, headers={**T.CORS, 'content-type': 'image/jpeg'}, body=open('pf1.jpg','rb').read())
    await ctx.route('**/storage/v1/**', stor)
    async def pub(route):
        if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        out = [p for p in DB['central_portfolio'] if p.get('publicado') and not p.get('deleted_at') and p.get('imagens')]
        out.sort(key=lambda p: (not p.get('destaque'), p.get('ordem', 0)))
        await route.fulfill(status=200, headers=J, body=json.dumps(out))
    await ctx.route('**/rpc/central_portfolio_publico', pub)
async def novo(pg, t, cli, cat, files, dest=False):
    await pg.click('.page-header [data-a=pf-form]'); await pg.fill('#pf_t', t); await pg.fill('#pf_c', cli); await pg.select_option('#pf_k', cat)
    await pg.fill('#pf_x', 'Um projeto de teste com descrição.')
    if dest: await pg.check('#pf_d')
    await pg.set_input_files('#pf_f', files); await pg.click('#pf_ok'); await pg.wait_for_selector('#modal:not(.open)', state='attached'); await pg.wait_for_timeout(300)
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/portfolio'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.page-header h1')
        print('menu:', await pg.locator('#nav a.active').inner_text())
        await novo(pg, 'Rebranding Lucrum', 'Lucrum', 'identidade', ['pf2.jpg', 'pf0.jpg'], True)
        await novo(pg, 'Campanha de verão', 'DessaFit', 'posts', ['pf1.jpg'])
        await novo(pg, 'Manual de marca', 'Indugás', 'impressos', ['pf0.jpg', 'pf1.jpg', 'pf2.jpg'])
        print('projetos:', [(p['titulo'], p['categoria'], len(p['imagens']), p['slug']) for p in DB['central_portfolio']], 'ups', len(UPS))
        # editar: reordenar imagens
        await pg.click(f'.pz [data-a=pf-form][data-id="{DB["central_portfolio"][2]["id"]}"] >> nth=0')
        await pg.click('[data-a=pf-im][data-i="2"][data-v="-1"]'); await pg.click('[data-a=pf-im][data-i="0"][data-v="x"]'); await pg.click('#pf_ok'); await pg.wait_for_timeout(500)
        print('editado:', DB['central_portfolio'][2]['imagens'])
        await pg.click('[data-a=pf-sel][data-k=identidade]'); await pg.click('[data-a=pf-sel][data-k=posts]')
        link = await pg.locator('.linkcard [data-a=copy-text]').first.get_attribute('data-text'); print('link:', link)
        await pg.screenshot(path='pf_admin.png', full_page=True)
        pp = await ctx.new_page(); pp.on('pageerror', lambda e: errs.append(str(e)))
        await pp.goto(BASE + 'portfolio.html?identidade,posts'); await pp.wait_for_selector('.card')
        print('público filtrado:', await pp.locator('.card h3').all_inner_texts(), await pp.locator('#fil button').all_inner_texts())
        await pp.goto(BASE + 'portfolio.html'); await pp.wait_for_selector('.card'); print('público todos:', await pp.locator('.card h3').all_inner_texts())
        await pp.screenshot(path='pf_pub.png', full_page=True)
        await pp.click('.card >> nth=0'); await pp.wait_for_selector('.pj.on'); print('abriu:', pp.url.split('#')[1], await pp.locator('.imgs img').count())
        await pp.wait_for_timeout(500); await pp.screenshot(path='pf_proj.png')
        await pp.click('.nx .r'); await pp.wait_for_timeout(200); print('próximo:', await pp.locator('#pjT').inner_text())
        await pp.keyboard.press('Escape'); print('fechou:', not await pp.locator('.pj.on').count())
        m = await b.new_context(viewport={'width': 375, 'height': 760}); await setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'portfolio.html'); await mp.wait_for_selector('.card'); print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='pf_m.png', full_page=True)
        print('ERRS', errs); await b.close()
asyncio.run(main())
