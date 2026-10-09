import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T5 = T9.T5; T = T9.T; DB = T.DB; BASE = T.BASE

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/propostas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('table')
        await pg.click('.page-header [data-a=pro-form]'); await pg.wait_for_selector('#svcList')
        await pg.select_option('#p_cli', 'cl1'); row = pg.locator('.svc-row').first
        await row.locator('[name=servico]').select_option('__custom__'); await row.locator('[name=servico_custom]').fill('Gravação de aulas')
        await row.locator('[name=valor]').type('250000'); await row.locator('[name=prazo]').fill('1 diária')
        await row.locator('[name=observacao]').fill('Valor de diária. Contempla até 10 aulas gravadas de até 15 minutos cada.')
        await pg.screenshot(path='x_form.png')
        await pg.click('[data-s=pro-save] [type=submit]'); await pg.wait_for_timeout(600)
        sv = DB['central_proposta_servicos'][-1]; pr = DB['central_propostas'][-1]
        print('salvo:', sv['servico'], sv['valor'], sv.get('observacao'), '| slug:', pr['slug'])
        await pg.goto(BASE + 'proposta.html?slug=' + pr['slug']); await pg.wait_for_selector('.pay-card')
        print('na proposta:', [t.replace('\n', ' | ') for t in await pg.locator('.pay-card').all_inner_texts()])
        await pg.locator('.pay-card').first.scroll_into_view_if_needed(); await pg.screenshot(path='x_prop.png')
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
