import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_briefings'].append({'id': 'bx', 'cliente_id': None, 'tipo': 'identidade', 'empresa': 'BRASIL WEB LOGISTICA', 'responsavel': 'Marcos', 'email': 'm@bw.com', 'whatsapp': '11 9', 'documento': '52409459000147', 'respostas': {'etapas': []}, 'status': 'novo', 'created_at': T.now(), 'deleted_at': None})
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/briefing/bx'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('[data-a=bri-newcli]')
        n0 = len(DB['central_clientes']); await pg.click('[data-a=bri-newcli]'); await pg.wait_for_timeout(500)
        bx = next(x for x in DB['central_briefings'] if x['id'] == 'bx'); c = next(x for x in DB['central_clientes'] if x['id'] == 'cl1')
        print('briefing duplicado:', len(DB['central_clientes']) == n0, bx['cliente_id'], '| completou:', c.get('documento'), c.get('email'), '|', await pg.inner_text('#toast'))
        await pg.goto(BASE + 'index.html#/propostas'); await pg.click('.page-header [data-a=pro-form]'); await pg.wait_for_selector('#svcList')
        await pg.select_option('#p_cli', ''); await pg.fill('#p_nome', 'Brasil Web Logistica'); await pg.locator('.svc-row [name=valor]').first.type('10000'); await pg.click('[data-s=pro-save] [type=submit]'); await pg.wait_for_timeout(500)
        p = DB['central_propostas'][-1]; print('proposta outro nome:', p['cliente_nome'], p['cliente_id'])
        await pg.goto(BASE + 'index.html#/clientes'); await pg.click('.page-header [data-a=cli-form]'); await pg.fill('#c_nome', 'Novo Cliente'); await pg.fill('#c_documento', '52.409.459/0001-47')
        msgs = []; pg.once('dialog', lambda d: (msgs.append(d.message), asyncio.ensure_future(d.dismiss())))
        await pg.click('[data-s=cli-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('aviso:', msgs, '| não salvou:', len(DB['central_clientes']) == n0)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
