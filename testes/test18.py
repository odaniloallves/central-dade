import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
p = next(x for x in DB['central_propostas'] if x['id'] == 11); p['pago_entrada_em'] = None
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/propostas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('table')
        await pg.click('[data-a=pay-open][data-id="11"]'); await pg.wait_for_selector('#modalBox .row')
        print('final travado antes da entrada:', await pg.is_disabled('[data-v=pago_final_em]'))
        await pg.click('[data-v=pago_entrada_em]'); await pg.wait_for_timeout(500)
        print('após entrada:', bool(p['pago_entrada_em']), p.get('pago_final_em'), '|', await pg.inner_text('#modalBox .hint'))
        await pg.screenshot(path='cc_modal.png')
        await pg.click('[data-a=close]'); print('lista:', (await pg.locator('tr', has_text='nº 0011').locator('td').nth(4).inner_text()).replace('\n', ' | '))
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.wait_for_selector('.fin-nav'); print('financeiro:', (await pg.locator('.panel', has_text='50% finais').inner_text()).replace('\n', ' | '))
        await pg.click('.panel:has-text("50% finais") [data-a=pay-open]'); await pg.click('[data-v=pago_final_em]'); await pg.wait_for_timeout(500)
        print('após final:', bool(p['pago_final_em']), '|', await pg.inner_text('#modalBox .hint'), '| entrada travada:', await pg.is_disabled('[data-v=pago_entrada_em]'))
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
