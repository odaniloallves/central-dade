import asyncio, json, datetime
from playwright.async_api import async_playwright
import test8 as T8
T5 = T8.T5; T = T5.T; DB = T.DB; BASE = T.BASE
hj = str(datetime.date.today())
DB['central_tarefas'] = [{'id': 't1', 'texto': 'Ligar para a gráfica', 'data': hj, 'feita_em': None, 'ordem': 0, 'created_at': T.now()},
                         {'id': 't2', 'texto': 'Revisar copy da Lume', 'data': hj, 'feita_em': T.now(), 'ordem': 1, 'created_at': T.now()}]
NEWS = {'itens': [{'titulo': 'Nova identidade visual da marca X aposta no minimalismo', 'link': 'https://exemplo.com/1', 'fonte': 'B9', 'data': T.now()},
                  {'titulo': 'Tendências de branding para 2027', 'link': 'https://exemplo.com/2', 'fonte': 'Meio & Mensagem', 'data': T.now()},
                  {'titulo': 'Link perigoso', 'link': 'javascript:alert(1)', 'fonte': 'X', 'data': T.now()}]}
CALLS = []
async def fn(route):
    if route.request.method == 'OPTIONS': return await route.fulfill(status=204, headers=T.CORS)
    CALLS.append(route.request.headers.get('authorization'))
    await route.fulfill(status=200, headers={**T.CORS, 'content-type': 'application/json'}, body=json.dumps(NEWS))

async def setup(ctx):
    await T5.setup(ctx); await ctx.route('**/functions/v1/**', fn)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1366, 'height': 900}); await setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#cvStage')
        await pg.wait_for_timeout(700)
        print('cards:', await pg.locator('.cv-card .cv-top span:not(.m)').all_inner_texts())
        print('ativo:', await pg.locator('.cv-card.on .cv-top').inner_text(), '| tarefas listadas no início:', await pg.locator('.tarefa').count())
        print('notícias:', await pg.locator('#cvNews li').all_inner_texts(), '| chamadas:', len(CALLS), CALLS[:1])
        await pg.screenshot(path='r_home.png')
        st = await pg.locator('#cvStage').bounding_box(); cx, cy = st['x'] + st['width'] / 2, st['y'] + 200
        await pg.mouse.move(cx, cy); await pg.mouse.down(); await pg.mouse.move(cx - 150, cy, steps=8); await pg.mouse.move(cx - 300, cy, steps=8); await pg.mouse.up(); await pg.wait_for_timeout(700)
        print('após arrastar:', await pg.locator('.cv-card.on .cv-top').inner_text())
        await pg.screenshot(path='r_drag.png')
        await pg.click('[data-a=cv-go][data-v="1"]'); await pg.wait_for_timeout(600); print('seta ›:', await pg.locator('.cv-card.on .cv-top').inner_text())
        await pg.focus('#cvStage'); await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(600); print('tecla ←:', await pg.locator('.cv-card.on .cv-top').inner_text())
        await pg.click('.cv-dots button >> nth=-1'); await pg.wait_for_timeout(600); print('último ponto:', await pg.locator('.cv-card.on .cv-top').inner_text())
        await pg.screenshot(path='r_news.png')
        # clicar num card lateral leva até ele, não abre o link
        side = pg.locator('.cv-card[data-cv=tar]'); await side.click(position={'x': 150, 'y': 60}); await pg.wait_for_timeout(600)
        print('clicou no lateral:', await pg.locator('.cv-card.on .cv-top').inner_text(), '| url:', pg.url.split('#')[1] if '#' in pg.url else '')
        await pg.click('.cv-card.on .cv-cta'); await pg.wait_for_timeout(300); print('CTA leva para:', pg.url.split('#')[1])
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage'); await pg.wait_for_timeout(300)
        print('chamadas após voltar (cache):', len(CALLS))
        await pg.evaluate("document.documentElement.setAttribute('data-theme','light')"); await pg.wait_for_timeout(300); await pg.screenshot(path='r_light.png')
        m = await b.new_context(viewport={'width': 375, 'height': 760}, has_touch=True); await setup(m); mp = await m.new_page(); mp.on('pageerror', lambda e: errs.append(str(e)))
        await mp.goto(BASE + 'index.html'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('#cvStage'); await mp.wait_for_timeout(600)
        print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await mp.screenshot(path='r_m_home.png', full_page=True)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
