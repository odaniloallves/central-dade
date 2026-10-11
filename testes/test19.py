import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_propostas'] += [{'id': 30, 'cliente_id': None, 'cliente_nome': 'Perdida SA', 'slug': 'perdida', 'status': 'perdida', 'data_proposta': '2026-10-01', 'data_expiracao': '2026-12-01', 'created_at': T.now(), 'deleted_at': None},
                            {'id': 31, 'cliente_id': None, 'cliente_nome': 'Ativa Ltda', 'slug': 'ativa', 'status': 'ativa', 'data_proposta': '2026-10-01', 'data_expiracao': '2026-12-01', 'created_at': T.now(), 'deleted_at': None}]
DB['central_proposta_servicos'] += [{'id': 300, 'proposta_id': 30, 'servico': 'landing_page', 'cobranca': 'unico', 'valor': 1000, 'ordem': 0}, {'id': 310, 'proposta_id': 31, 'servico': 'landing_page', 'cobranca': 'unico', 'valor': 1000, 'ordem': 0}]
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/propostas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.pills')
        nomes = lambda: pg.locator('tbody tr td:first-child strong').all_inner_texts()
        print('abas:', await pg.locator('.pills .pillf').all_inner_texts())
        print('em aberto:', await nomes())
        await pg.click('[data-a=pro-vis][data-v=perdida]'); print('perdidas:', await nomes())
        await pg.click('[data-a=pro-vis][data-v=todas]'); print('todas:', await nomes())
        await pg.click('[data-a=pro-vis][data-v=abertas]'); await pg.screenshot(path='dd_lista.png')
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
