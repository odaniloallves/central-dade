import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_propostas'].append({'id': 20, 'cliente_id': 'cl1', 'cliente_nome': 'Veste Aurea', 'slug': 'veste-x', 'status': 'ativa', 'data_proposta': '2026-10-09', 'data_expiracao': '2026-12-31', 'created_at': T.now(), 'deleted_at': None})
DB['central_proposta_servicos'] += [{'id': 200, 'proposta_id': 20, 'servico': 'materiais_impressos', 'cobranca': 'unico', 'valor': 500, 'ordem': 0, 'opcional': False},
                                     {'id': 201, 'proposta_id': 20, 'servico': 'pecas_digitais', 'cobranca': 'unico', 'valor': 400, 'ordem': 1, 'opcional': False},
                                     {'id': 202, 'proposta_id': 20, 'servico': 'motion', 'cobranca': 'unico', 'valor': 300, 'ordem': 2, 'opcional': True}]
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        for w, nome in ((1280, 'bb_prop.png'), (375, 'bb_m_prop.png')):
            ctx = await b.new_context(viewport={'width': w, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(BASE + 'proposta.html?slug=veste-x'); await pg.wait_for_selector('.inv-head')
            print(w, 'detalhe:', [t.replace('\n', ' ') for t in await pg.locator('.brk .ln').all_inner_texts()], '| overflow:', await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
            await pg.locator('.inv').scroll_into_view_if_needed(); await pg.screenshot(path=nome)
        DB['central_proposta_servicos'] = [s for s in DB['central_proposta_servicos'] if s['id'] != 201]
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page()
        await pg.goto(BASE + 'proposta.html?slug=veste-x'); await pg.wait_for_selector('.inv-head'); print('um serviço só, sem detalhe:', await pg.locator('.brk').count(), await pg.locator('.inv-head .items span').all_inner_texts())
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
