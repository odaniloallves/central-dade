import asyncio, json, datetime
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright
import test9 as T9
T5 = T9.T5; T = T9.T; DB = T.DB; BASE = T.BASE
hj = str(datetime.date.today())
UPS, DELS = [], []
def publica(tok):
    c = next((x for x in DB['central_clientes'] if x.get('entregas_token') == tok), None)
    if not c: return None
    es = sorted([e for e in DB['central_entregas'] if e['cliente_id'] == c['id'] and e['expira_em'] >= hj], key=lambda e: e['created_at'], reverse=True)
    return {'cliente_nome': c['nome'], 'entregas': [{**e, 'pecas': sorted([p for p in DB['central_entrega_pecas'] if p['entrega_id'] == e['id']], key=lambda p: p['ordem'])} for e in es]}
async def setup(ctx):
    await T9.setup(ctx)
    J = {**T.CORS, 'content-type': 'application/json'}
    async def stor(route):
        rq = route.request
        if rq.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        if 'central-entregas' not in rq.url: return await route.fallback()
        if rq.method == 'POST': UPS.append(unquote(urlparse(rq.url).path.split('central-entregas/')[1])); return await route.fulfill(status=200, headers=J, body='{}')
        if rq.method == 'DELETE': DELS.extend(json.loads(rq.post_data)['prefixes']); return await route.fulfill(status=200, headers=J, body='[]')
        await route.fulfill(status=200, headers={**T.CORS, 'content-type': 'image/png'}, body=T5.PNG)
    await ctx.route('**/storage/v1/**', stor)
    async def rpcp(route):
        if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        await route.fulfill(status=200, headers=J, body=json.dumps(publica(json.loads(route.request.post_data)['p_token'])))
    async def rpcr(route):
        if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
        b = json.loads(route.request.post_data); ps = [p for p in DB['central_entrega_pecas'] if p['entrega_id'] == b['p_entrega']]
        if b['p_acao'] == 'aprovar_todas': [p.update(status='aprovada') for p in ps if p['status'] != 'alteracao']
        elif b['p_acao'] == 'aprovar': [p.update(status='aprovada', pedido=None) for p in ps if p['id'] == b['p_peca']]
        elif b['p_acao'] == 'alterar': [p.update(status='alteracao', pedido=b['p_texto'], pedido_nome=b['p_nome'], pedido_em=T.now()) for p in ps if p['id'] == b['p_peca']]
        await route.fulfill(status=200, headers=J, body=json.dumps(publica(b['p_token'])))
    JZ = open('/tmp/claude-0/-home-claude/cf68f954-590c-57c9-b515-43e4bf505a82/scratchpad/jz/node_modules/jszip/dist/jszip.min.js').read()
    await ctx.route('https://cdnjs.cloudflare.com/**', lambda r: r.fulfill(status=200, content_type='application/javascript', body=JZ))
    await ctx.route('**/rpc/central_entregas_publica', rpcp); await ctx.route('**/rpc/central_entrega_responder', rpcr)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}, accept_downloads=True); await setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/entregas'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.tabs')
        print('menu:', await pg.locator('#nav a.active').inner_text(), '| abas:', await pg.locator('.tab').all_inner_texts())
        await pg.click('.page-header [data-a=ent-form]'); await pg.select_option('#e_cli', 'cl1'); await pg.select_option('#e_dias', '7')
        await pg.set_input_files('#e_arq', ['t_img1.png', 't_img2.png']); await pg.set_input_files('#e_arq', ['t_img1.png'])
        print('escolhidos:', len(await pg.locator('#e_arqs .arq').all())); await pg.click('[data-a=ent-rm][data-i="2"]')
        await pg.screenshot(path='ee_modal.png')
        await pg.click('#e_ok'); await pg.wait_for_selector('.pz .it', timeout=10000)
        c = next(x for x in DB['central_clientes'] if x['id'] == 'cl1'); e = DB['central_entregas'][-1]
        print('entrega:', e['titulo'], e['expira_em'], '| token:', c.get('entregas_token'), c.get('entregas_dias'), '| peças:', [p['nome'] for p in DB['central_entrega_pecas']], '| uploads:', len(UPS), UPS[0][:40])
        await pg.screenshot(path='ee_pasta.png', full_page=True)
        link = await pg.locator('.page-header [data-a=copy-text]').get_attribute('data-text'); print('link:', link)
        # cliente
        cp = await ctx.new_page(); cp.on('pageerror', lambda e: errs.append(str(e)))
        await cp.goto(BASE + 'e.html?' + c['entregas_token']); await cp.wait_for_selector('.pc')
        print('cliente vê:', cp.url.replace(BASE, ''), '|', await cp.locator('.sem-h h2').all_inner_texts(), await cp.locator('.pc .chip').all_inner_texts())
        p1, p2 = DB['central_entrega_pecas'][0]['id'], DB['central_entrega_pecas'][1]['id']
        await cp.click(f'[data-x=alterar][data-p="{p1}"]'); await cp.fill(f'#tx-{p1}', 'Trocar a foto de fundo'); await cp.fill(f'#nm-{p1}', 'Marcos'); await cp.click('[data-x=enviar]'); await cp.wait_for_timeout(400)
        await cp.click(f'[data-x=aprovar][data-p="{p2}"]'); await cp.wait_for_timeout(400)
        print('após respostas:', [(p['status'], p.get('pedido')) for p in DB['central_entrega_pecas']])
        async with cp.expect_download() as dl: await cp.click('[data-x=zip]')
        d = await dl.value; print('zip:', d.suggested_filename)
        await cp.screenshot(path='ee_cliente.png', full_page=True)
        # central mostra o pedido
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage')
        print('precisa de você:', [t.replace('\n', ' ') for t in await pg.locator('.panel', has_text='Precisa de você').locator('.row', has_text='alteração').all_inner_texts()])
        print('contagem menu:', await pg.locator('#nav a[href="#/previas"]').inner_text())
        await pg.goto(BASE + f'index.html#/entrega/cl1'); await pg.wait_for_selector('.pz')
        await pg.set_input_files(f'[data-c=pec-trocar][data-id="{p1}"]', 't_img2.png'); await pg.wait_for_timeout(600)
        x = next(p for p in DB['central_entrega_pecas'] if p['id'] == p1); print('trocado:', x['nome'], x['status'], x['pedido'], '| apagou antigo:', len(DELS))
        await pg.select_option('[data-c=ent-dias]', '21'); await pg.wait_for_timeout(500); print('dias:', c['entregas_dias'], DB['central_entregas'][-1]['expira_em'])
        # vencida some e é limpa
        DB['central_entregas'].append({'id': 'old', 'cliente_id': 'cl1', 'titulo': 'Semana velha', 'expira_em': '2026-01-01', 'created_at': '2025-12-20T10:00:00Z', 'deleted_at': None})
        DB['central_entrega_pecas'].append({'id': 'po', 'entrega_id': 'old', 'path': 'cl1/old/x.png', 'nome': 'x.png', 'tipo': 'imagem', 'status': 'nova', 'ordem': 0, 'created_at': T.now()})
        np = await ctx.new_page(); await np.goto(BASE + 'index.html#/entregas'); await np.wait_for_selector('.tabs'); await np.wait_for_timeout(800)
        print('limpeza:', 'old' not in [e['id'] for e in DB['central_entregas']], 'cl1/old/x.png' in DELS)
        m = await b.new_context(viewport={'width': 375, 'height': 760}); await setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'e.html?' + c['entregas_token']); await mp.wait_for_selector('.pc'); print('mobile cliente overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='ee_m_cliente.png', full_page=True)
        await mp.goto(BASE + 'index.html#/entrega/cl1'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('.pz'); print('mobile central overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
