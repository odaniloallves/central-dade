import asyncio
from playwright.async_api import async_playwright
import test10 as T10
T9 = T10.T9; T = T9.T; DB = T.DB; BASE = T.BASE

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1366, 'height': 900}); await T9.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.fin-nav')
        antes = await pg.locator('.stat-card', has_text='Entrou no mês').inner_text()
        await pg.click('[data-a=avu-form]'); await pg.fill('#a_nome', 'Juliana Souza'); await pg.type('#a_val', '35000'); await pg.fill('#a_desc', 'Convite de aniversário')
        await pg.click('[data-s=avu-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('salvo:', [(a['nome'], a['valor'], a['recebido_em'], a['forma'], a['nf_em']) for a in DB['central_entradas']])
        print('entrou antes/depois:', antes.replace('\n', ' '), '->', (await pg.locator('.stat-card', has_text='Entrou no mês').inner_text()).replace('\n', ' '))
        print('linha:', (await pg.locator('.panel', has_text='Entradas de').locator('.row', has_text='Juliana').inner_text()).replace('\n', ' | '))
        await pg.screenshot(path='u_fin.png')
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage')
        print('pendência NF:', [t.replace('\n', ' ') for t in await pg.locator('.panel', has_text='Precisa de você').locator('.row', has_text='Juliana').all_inner_texts()])
        await pg.click('[data-a=avu-nf]'); await pg.wait_for_timeout(400); print('nf marcada:', DB['central_entradas'][0]['nf_em'])
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.wait_for_selector('.fin-nav')
        aid = DB['central_entradas'][0]['id']
        await pg.click(f'[data-a=avu-form][data-id="{aid}"]'); await pg.fill('#a_val', ''); await pg.type('#a_val', '40000'); await pg.click('[data-s=avu-save] [type=submit]'); await pg.wait_for_timeout(400)
        print('editado:', DB['central_entradas'][0]['valor'], DB['central_entradas'][0]['nf_em'] is not None)
        await pg.click(f'[data-a=avu-del-ask][data-id="{aid}"]'); await pg.click('[data-a=avu-del]'); await pg.wait_for_timeout(400); print('excluído:', len(DB['central_entradas']))
        m = await b.new_context(viewport={'width': 375, 'height': 760}); await T9.setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'index.html#/financeiro'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('.fin-nav')
        await mp.click('[data-a=avu-form]'); await mp.wait_for_timeout(300); print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='u_m_modal.png')
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
