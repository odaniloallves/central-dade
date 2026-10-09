import asyncio, json
from playwright.async_api import async_playwright
import test9 as T9
T5 = T9.T5; T = T9.T; DB = T.DB; BASE = T.BASE

async def setup(ctx):
    await T9.setup(ctx)
    async def linha(route):
        if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        tok = json.loads(route.request.post_data)['p_token']
        p = next((x for x in DB['central_propostas'] if x.get('linha_token') == tok and x.get('linha_etapas')), None)
        body = p and {'cliente_nome': p['cliente_nome'], 'servicos': [s['servico'] for s in DB['central_proposta_servicos'] if s['proposta_id'] == p['id']], 'etapas': p['linha_etapas'], 'atual': p.get('linha_atual', 0), 'atualizada_em': p.get('linha_atualizada_em')}
        await route.fulfill(status=200, headers={**T.CORS, 'content-type': 'application/json'}, body=json.dumps(body))
    await ctx.route('**/rest/v1/rpc/central_linha_publica', linha)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/propostas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('table')
        await pg.click('[data-a=lin-open][data-id="11"]'); await pg.wait_for_selector('#etList')
        print('sugestão:', [await i.input_value() for i in await pg.locator('#etList input').all()])
        await pg.screenshot(path='y_editor.png')
        await pg.click('#etList .et-row >> nth=3 >> [data-a=lin-rm]')
        await pg.click('[data-a=lin-add]'); await pg.locator('#etList input').last.fill('Treinamento de uso')
        await pg.click('#etList .et-row >> nth=-1 >> [data-a=lin-up]')
        await pg.click('[data-s=lin-save] [type=submit]'); await pg.wait_for_selector('.lt')
        p = next(x for x in DB['central_propostas'] if x['id'] == 11)
        print('salvo:', p['linha_etapas'], '| token:', p['linha_token'], len(p['linha_token']), '| atual:', p['linha_atual'])
        await pg.click('[data-a=lin-step][data-v="1"]'); await pg.wait_for_timeout(400); await pg.click('[data-a=lin-step][data-v="1"]'); await pg.wait_for_timeout(400)
        print('após 2 etapas:', p['linha_atual'], '|', (await pg.inner_text('.modal-head p')))
        await pg.click('[data-a=lin-set][data-v="4"]'); await pg.wait_for_timeout(400); print('ir para 5ª:', p['linha_atual'])
        await pg.click('[data-a=lin-step][data-v="-1"]'); await pg.wait_for_timeout(400); print('voltar:', p['linha_atual'])
        link = await pg.locator('#modalBox [data-a=copy-text]').get_attribute('data-text'); print('link:', link)
        await pg.screenshot(path='y_modal.png')
        await pg.goto(BASE + 'index.html#/cliente/cl1'); await pg.wait_for_selector('.panel')
        print('ficha:', [t.replace('\n', ' ') for t in await pg.locator('.panel', has_text='Propostas').locator('.row').all_inner_texts()])
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage')
        print('card:', (await pg.locator('.cv-card[data-cv=proj]').inner_text()).replace('\n', ' | '))
        await pg.goto(BASE + 't.html?' + p['linha_token']); await pg.wait_for_selector('.tl')
        print('cliente vê:', pg.url.replace(BASE, ''), '|', [t.replace('\n', ' ') for t in await pg.locator('.tl li').all_inner_texts()], '|', await pg.inner_text('.prog-top'))
        await pg.screenshot(path='y_cliente.png', full_page=True)
        await pg.goto(BASE + 'linha.html?t=naoexiste1234'); await pg.wait_for_selector('h1'); print('inválido:', await pg.inner_text('h1'))
        m = await b.new_context(viewport={'width': 375, 'height': 760}); await setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'linha.html?t=' + p['linha_token']); await mp.wait_for_selector('.tl'); print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='y_m_cliente.png', full_page=True)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
