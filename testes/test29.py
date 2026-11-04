import asyncio
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
import datetime
pass
async def _x(): pass
for p in []: pass
for p in DB.get('central_propostas', []): p['parcelas_cartao'] = 4; p['data_expiracao'] = str(datetime.date.today() + datetime.timedelta(days=20)); p['status']='ativa'; p['aprovada_em']=None
PR = lambda: next(p for p in DB['central_propostas'] if str(p['id']) == PID[0])
PID = ['']
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    ctx = await b.new_context(viewport={'width':1280,'height':900}); await T9.setup(ctx)
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(BASE + 'index.html#/propostas'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_timeout(800)
    await pg.click('[data-a=pro-vis][data-v=todas]'); await pg.click('[data-a=pro-form][data-id="11"]'); await pg.wait_for_selector('#p_parc')
    PID[0] = await pg.get_attribute('[data-a=pro-form][data-id="11"]','data-id'); print('padrão:', await pg.input_value('#p_parc')); await pg.select_option('#p_parc', '3'); await pg.click('#modalBox [type=submit]'); await pg.wait_for_timeout(800)
    print('salvo:', PR().get('parcelas_cartao'))
    import json
    async def rp(route):
        if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        pr = {**PR(), 'servicos':[x for x in DB['central_proposta_servicos'] if x['proposta_id'] == PR()['id']]}
        await route.fulfill(status=200, headers={**T.CORS, 'content-type':'application/json'}, body=json.dumps(pr, default=str))
    await ctx.route('**/rpc/central_proposta_publica', rp)
    pp = await ctx.new_page(); pp.on('pageerror', lambda e: errs.append(str(e)))
    await pp.goto(BASE + 'proposta.html?slug='+PR()['slug']+''); await pp.wait_for_selector('#hero'); await pp.wait_for_timeout(500)
    t = await pp.content(); print('proposta 3x:', 'em até 3x' in t, '4x' in t)
    await pp.goto(BASE + 'pagamento.html?slug='+PR()['slug']+''); await pp.wait_for_timeout(1200)
    t = await pp.content(); print('pagamento 3x:', 'em até 3x' in t, 'em até 4x' in t)
    for p in DB['central_propostas']: p.pop('parcelas_cartao', None)
    await pg.reload(); await pg.wait_for_timeout(800); await pg.click('[data-a=pro-vis][data-v=todas]'); await pg.click('[data-a=pro-form][data-id="11"]'); await pg.wait_for_selector('#p_parc'); await pg.click('#modalBox [type=submit]'); await pg.wait_for_timeout(800)
    print('sem coluna, não envia:', 'parcelas_cartao' not in PR())
    await pp.goto(BASE + 'proposta.html?slug='+PR()['slug']+''); await pp.wait_for_selector('#hero'); await pp.wait_for_timeout(500); print('sem coluna mostra 4x:', 'em até 4x' in await pp.content())
    print('ERRS', errs); await b.close()
asyncio.run(main())
