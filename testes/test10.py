import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_config'].append({'chave': 'metas', 'valor': {'padrao': None, 'meses': {}}})

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1366, 'height': 900}); await T9.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#cvStage')
        print('saudação:', await pg.inner_text('.page-header h1'))
        print('ordem:', await pg.locator('.cv-card .cv-top span:not(.m)').all_inner_texts())
        meta = pg.locator('.cv-card[data-cv=meta]'); print('meta vazia:', (await meta.inner_text()).replace('\n', ' | '))
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.wait_for_selector('#meta_v')
        await pg.type('#meta_v', '1000000'); await pg.click('[data-s=meta-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('salvo:', DB['central_config'][-1]['valor'])
        print('painel:', (await pg.locator('.panel', has_text='Meta de').first.inner_text()).replace('\n', ' | ')[:220])
        await pg.screenshot(path='s_fin.png')
        # mês seguinte com meta própria
        await pg.click('.fin-nav a[aria-label="Próximo mês"]'); await pg.wait_for_selector('#meta_v')
        await pg.fill('#meta_v', ''); await pg.type('#meta_v', '1500000'); await pg.uncheck('#meta_p'); await pg.click('[data-s=meta-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('salvo 2:', DB['central_config'][-1]['valor'])
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage'); await pg.click('[data-a=cv-go][data-v="1"]'); await pg.wait_for_timeout(700)
        print('card meta:', (await pg.locator('.cv-card[data-cv=meta]').inner_text()).replace('\n', ' | '))
        await pg.screenshot(path='s_home.png')
        m = await b.new_context(viewport={'width': 375, 'height': 760}); await T9.setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'index.html'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('#cvStage')
        for k in ['', 'financeiro']:
            await mp.goto(BASE + 'index.html#/' + k); await mp.wait_for_timeout(300); print('mobile', k, 'overflow', await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
