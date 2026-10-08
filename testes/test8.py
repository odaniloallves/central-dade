import asyncio, datetime
from playwright.async_api import async_playwright
import test5 as T5
T = T5.T; DB = T.DB; BASE = T.BASE
h = datetime.date.today(); hj = str(h)
mes = hj[:7]; ant = str((h.replace(day=1) - datetime.timedelta(days=1)))[:7]
DB['central_config'].append({'chave': 'imposto', 'valor': {'tipo': 'percentual', 'valor': None}})
# proposta mensal já fechada (vira plano sozinha) e uma pontual com entrada paga hoje
DB['central_propostas'] = [
    {'id': 10, 'cliente_id': 'cl1', 'cliente_nome': 'Brasil Web Logística', 'slug': 'bw-1', 'status': 'fechada', 'dia_cobranca': 5, 'aprovada_em': hj + 'T12:00:00Z', 'data_proposta': hj, 'data_expiracao': hj, 'created_at': T.now(), 'deleted_at': None},
    {'id': 11, 'cliente_id': 'cl1', 'cliente_nome': 'Brasil Web Logística', 'slug': 'bw-2', 'status': 'fechada', 'forma_pagamento': 'pix', 'pago_entrada_em': hj + 'T15:00:00Z', 'data_proposta': hj, 'data_expiracao': hj, 'created_at': T.now(), 'deleted_at': None}]
DB['central_proposta_servicos'] = [
    {'id': 100, 'proposta_id': 10, 'servico': 'criativos_social', 'cobranca': 'mensal', 'valor': 1500, 'ordem': 0},
    {'id': 101, 'proposta_id': 11, 'servico': 'landing_page', 'cobranca': 'unico', 'valor': 7000, 'ordem': 0}]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T5.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#cvStage')
        print('plano automático:', [(p['descricao'], p['valor_base'], p['inicio'], p['proposta_id']) for p in DB['central_planos']])
        print('menu:', [(await x.inner_text()).replace('\n', ' ') for x in await pg.locator('#nav a').all()])
        # plano de pacote pela ficha
        await pg.goto(BASE + 'index.html#/cliente/cl1'); await pg.wait_for_selector('[data-a=pla-form]')
        await pg.click('[data-a=pla-form][data-cli=cl1]')
        await pg.fill('#pl_desc', 'Pacote de artes'); await pg.type('#pl_val', '40000'); await pg.fill('#pl_dia', '5')
        await pg.check('#pl_pac'); await pg.fill('#pl_qtd', '10'); await pg.type('#pl_ext', '4000'); await pg.fill('#pl_ini', ant)
        await pg.click('[data-s=pla-save] [type=submit]'); await pg.wait_for_timeout(500)
        pl = DB['central_planos'][-1]; print('plano pacote:', pl['descricao'], pl['valor_base'], pl['qtd_inclusa'], pl['valor_extra'], pl['inicio'], pl['dia_cobranca'])
        print('ficha:', (await pg.locator('.panel', has_text='Plano mensal').inner_text()).replace('\n', ' | ')[:300])
        await pg.screenshot(path='q_ficha.png', full_page=True)
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage')
        print('início pendências:', [t.replace('\n', ' ') for t in await pg.locator('.panel', has_text='Precisa de você').locator('.row').all_inner_texts()])
        print('badge financeiro:', await pg.locator('#nav a[href="#/financeiro"]').inner_text())
        # financeiro
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.wait_for_selector('.fin-nav')
        print('mês:', await pg.inner_text('.fin-nav strong'))
        q = pg.locator('[data-c=fec-qtd]'); print('qtd padrão:', await q.input_value())
        await q.fill('18'); await q.dispatch_event('change'); await pg.wait_for_timeout(500)
        print('fechamento:', [(f['mes'], f['qtd'], f['valor']) for f in DB['central_fechamentos']])
        await pg.click(f'[data-a=fec-set][data-pl="{pl["id"]}"][data-v=pago_em]'); await pg.wait_for_timeout(500)
        print('pago:', DB['central_fechamentos'][0]['pago_em'] == hj)
        await pg.fill('#imp_v', '6'); await pg.click('[data-s=imp-save] [type=submit]'); await pg.wait_for_timeout(500)
        print('imposto cfg:', DB['central_config'][-1]['valor'])
        print('stats:', [t.replace('\n', ': ') for t in await pg.locator('.stat-card').all_inner_texts()])
        print('entradas:', [t.replace('\n', ' ') for t in await pg.locator('.panel', has_text='Entradas de').locator('.row').all_inner_texts()])
        await pg.screenshot(path='q_fin.png', full_page=True)
        # encerrar plano -> churn
        await pg.goto(BASE + 'index.html#/cliente/cl1'); await pg.wait_for_selector('[data-a=pla-enc-ask]')
        await pg.click(f'[data-a=pla-enc-ask][data-id="{pl["id"]}"]'); await pg.click('[data-s=pla-enc] [type=submit]'); await pg.wait_for_timeout(500)
        print('encerrado:', DB['central_planos'][-1]['encerrado_em'])
        await pg.goto(BASE + 'index.html#/financeiro'); await pg.wait_for_selector('.fin-nav')
        print('churn:', (await pg.locator('.panel', has_text='Churn de').inner_text()).replace('\n', ' | '))
        await pg.click('.fin-nav a[aria-label="Próximo mês"]'); await pg.wait_for_timeout(200)
        print('mês seguinte:', await pg.inner_text('.fin-nav strong'), '| recorrente:', await pg.locator('.stat-card', has_text='Receita recorrente').inner_text())
        # pagamento da proposta mensal aponta para o financeiro
        await pg.goto(BASE + 'index.html#/propostas'); await pg.click('[data-a=pay-open][data-id="10"]'); print('modal mensal:', (await pg.inner_text('#modalBox')).replace('\n', ' ')[-120:])
        m = await b.new_context(viewport={'width': 375, 'height': 740}); await T5.setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'index.html'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('#cvStage')
        for k in ['financeiro', 'cliente/cl1', '']:
            await mp.goto(BASE + 'index.html#/' + k); await mp.wait_for_timeout(250); print('mobile', k, 'overflow', await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await mp.goto(BASE + 'index.html#/financeiro'); await mp.wait_for_timeout(250); await mp.screenshot(path='q_m_fin.png', full_page=True)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
