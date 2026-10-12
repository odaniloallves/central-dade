import asyncio, datetime
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
h = datetime.date.today(); m = str(h)[:7]
def madd(mm, n):
    y, mo = int(mm[:4]), int(mm[5:]) + n
    while mo > 12: y += 1; mo -= 12
    while mo < 1: y -= 1; mo += 12
    return f'{y}-{mo:02d}'
prox = madd(m, 1)
DB['central_pessoal_contas'] = [{'id': 'c1', 'descricao': 'Aluguel', 'tipo': 'fixa', 'valor': 2800, 'dia_venc': 10, 'inicio': m, 'parcela_total': None, 'fim': None, 'codigo': None, 'created_at': T.now()},
                                {'id': 'c2', 'descricao': 'Havan - Panelas', 'tipo': 'parcelada', 'valor': 100, 'dia_venc': 10, 'inicio': madd(m, -3), 'parcela_total': 6, 'fim': None, 'codigo': None, 'created_at': T.now()},
                                {'id': 'c3', 'descricao': 'Cartão Nubank', 'tipo': 'variavel', 'valor': 2918.48, 'dia_venc': 28, 'inicio': m, 'parcela_total': None, 'fim': None, 'codigo': '8265000000112015', 'created_at': T.now()}]
DB['central_pessoal_lanc'] = [{'id': 'l1', 'conta_id': 'c1', 'mes': m, 'descricao': 'Aluguel', 'valor': 2800, 'dia_venc': 10, 'parcela': None, 'parcela_total': None, 'codigo': None, 'pago_em': str(h), 'oculto': False, 'created_at': T.now()},
                              {'id': 'l2', 'conta_id': 'c2', 'mes': m, 'descricao': 'Havan - Panelas', 'valor': 100, 'dia_venc': 1, 'parcela': 4, 'parcela_total': 6, 'codigo': None, 'pago_em': None, 'oculto': False, 'created_at': T.now()},
                              {'id': 'l3', 'conta_id': 'c3', 'mes': m, 'descricao': 'Cartão Nubank', 'valor': 2918.48, 'dia_venc': 28, 'parcela': None, 'parcela_total': None, 'codigo': '8265000000112015', 'pago_em': None, 'oculto': False, 'created_at': T.now()}]
DB['central_config'].append({'chave': 'pessoal_pin', 'valor': {}})
async def pin(pg, d, segundo=False):
    for i, ch in enumerate(d): await pg.fill(f'[data-pin="{i}"]', ''); await pg.type(f'[data-pin="{i}"]', ch)
    if segundo:
        for i, ch in enumerate(d): await pg.type(f'[data-pin2="{i}"]', ch)
    await pg.wait_for_timeout(500)
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/pessoal'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('.pin-box')
        print('menu:', [t for t in await pg.locator('#nav .nav-group, #nav a').all_inner_texts()][-4:], '| tela:', await pg.inner_text('.pin-box h1'))
        await pg.screenshot(path='ff_pin.png')
        await pin(pg, '1234', True); await pg.wait_for_selector('.ct')
        print('pin salvo:', bool(DB['central_config'][-1]['valor'].get('hash')), '| stats:', [t.replace('\n', ': ') for t in await pg.locator('.stat-card').all_inner_texts()])
        print('linhas:', [t.split('\n')[0] for t in await pg.locator('.ct .ds b').all_inner_texts()])
        await pg.click('[data-c=pc-pago][data-id=l3]'); await pg.wait_for_timeout(400); print('nubank pago:', next(x for x in DB['central_pessoal_lanc'] if x['id'] == 'l3')['pago_em'])
        await pg.screenshot(path='ff_mes.png', full_page=True)
        await pg.click('.fin-nav a[aria-label="Próximo mês"]'); await pg.wait_for_timeout(800)
        nov = [x for x in DB['central_pessoal_lanc'] if x['mes'] == prox]; print('gerados:', [(x['descricao'], x['valor'], x.get('parcela')) for x in nov])
        await pg.goto(BASE + f'index.html#/pessoal/{prox}'); await pg.wait_for_selector('.ct'); await pg.wait_for_timeout(300)
        lid = next(x['id'] for x in nov if x['descricao'] == 'Cartão Nubank')
        await pg.click(f'[data-a=pc-form][data-id="{lid}"]'); await pg.fill('#pc_v', ''); await pg.type('#pc_v', '300000'); await pg.click('[data-s=pc-save] [type=submit]'); await pg.wait_for_timeout(400)
        print('nubank próximo editado:', next(x for x in DB['central_pessoal_lanc'] if x['id'] == lid)['valor'], '| conta base:', DB['central_pessoal_contas'][2]['valor'])
        await pg.click('.page-header [data-a=pc-form]'); await pg.fill('#pc_d', 'Sofá'); await pg.type('#pc_v', '45000'); await pg.fill('#pc_dia', '5'); await pg.select_option('#pc_t', 'parcelada'); await pg.fill('#pc_pa', '1'); await pg.fill('#pc_pt', '10'); await pg.click('[data-s=pc-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('parcelada nova:', [(c['descricao'], c['tipo'], c['inicio'], c['parcela_total']) for c in DB['central_pessoal_contas'] if c['descricao'] == 'Sofá'], [(x['parcela'], x['parcela_total']) for x in DB['central_pessoal_lanc'] if x['descricao'] == 'Sofá'])
        alu = next(x['id'] for x in DB['central_pessoal_lanc'] if x['mes'] == prox and x['descricao'] == 'Aluguel')
        await pg.click(f'[data-a=pc-del-ask][data-id="{alu}"]'); await pg.click('[data-a=pc-del][data-v=mes]'); await pg.wait_for_timeout(400)
        print('aluguel só deste mês:', next(x for x in DB['central_pessoal_lanc'] if x['id'] == alu)['oculto'], '| na tela:', 'Aluguel' in await pg.inner_text('.panel'))
        await pg.screenshot(path='ff_prox.png', full_page=True)
        await pg.click('[data-a=pin-travar]'); await pg.wait_for_selector('.pin-box'); await pin(pg, '9999'); print('pin errado:', await pg.inner_text('#pinErr'))
        await pin(pg, '1234'); await pg.wait_for_selector('.ct'); print('reabriu:', await pg.inner_text('.page-header h1'))
        await pg.goto(BASE + 'index.html#/clientes'); await pg.wait_for_timeout(200); await pg.goto(BASE + 'index.html#/pessoal'); await pg.wait_for_timeout(300); print('saiu e voltou trava:', await pg.locator('.pin-box').count())
        mm = await b.new_context(viewport={'width': 375, 'height': 760}); await T9.setup(mm); mp = await mm.new_page()
        await mp.goto(BASE + 'index.html#/pessoal'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('.pin-box'); await pin(mp, '1234'); await mp.wait_for_selector('.ct')
        print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='ff_m.png', full_page=True)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
