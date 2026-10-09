import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.fin-nav')
        n0 = len(DB['central_planos'])
        await pg.click('.panel [data-a=pla-form]:not([data-id])'); await pg.wait_for_selector('#pl_cli')
        await pg.fill('#pl_desc', 'Gestão de redes'); await pg.type('#pl_val', '180000'); await pg.click('[data-s=pla-save] [type=submit]'); await pg.wait_for_timeout(300)
        print('sem cliente bloqueia:', len(DB['central_planos']) == n0, '|', await pg.inner_text('#toast'))
        await pg.select_option('#pl_cli', 'cl1'); await pg.click('[data-s=pla-save] [type=submit]'); await pg.wait_for_timeout(500)
        pl = DB['central_planos'][-1]; print('plano criado:', pl['descricao'], pl['valor_base'], pl['cliente_id'], pl['cliente_nome'])
        await pg.screenshot(path='aa_fin.png')
        await pg.goto(BASE + 'index.html#/propostas'); await pg.click('.page-header [data-a=pro-form]'); await pg.wait_for_selector('#svcList')
        opts = await pg.locator('.svc-row [name=servico] option').all_inner_texts(); print('serviços novos:', [o for o in opts if 'Impress' in o or 'Digitais' in o])
        print('impresso antes:', await pg.is_checked('#p_imp')); await pg.locator('.svc-row [name=servico]').first.select_option('materiais_impressos'); print('impresso depois:', await pg.is_checked('#p_imp'))
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
