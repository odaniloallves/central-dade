import asyncio, datetime
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
hj = str(datetime.date.today()); ontem = str(datetime.date.today() - datetime.timedelta(days=1))
DB['central_tarefas'] = [{'id': f't{i}', 'texto': t, 'data': ontem if i == 1 else hj, 'feita_em': None, 'ordem': 0, 'created_at': f'2026-10-0{i}T10:00:00Z'} for i, t in enumerate(['Ligar para a gráfica', 'Revisar copy', 'Mandar proposta', 'Pagar boleto'], 1)]

def ordem(): return [x['texto'] for x in sorted([x for x in DB['central_tarefas'] if not x['feita_em']], key=lambda x: (x['ordem'] or 0, x['data'], x['created_at']))]
async def tela(pg): return [t.split('\n')[0] for t in await pg.locator('#agPend .tarefa .tx').all_inner_texts()]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); errs = []
        ctx = await b.new_context(viewport={'width': 1280, 'height': 900}); await T9.setup(ctx)
        pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(BASE + 'index.html#/agenda'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#agPend')
        print('inicial:', await tela(pg))
        await pg.click('[data-a=tar-mv][data-id=t1][data-v="1"]'); await pg.wait_for_timeout(500)
        print('t1 desce:', await tela(pg), '| banco:', ordem())
        await pg.click('[data-a=tar-mv][data-id=t4][data-v="-1"]'); await pg.wait_for_timeout(500)
        print('t4 sobe:', await tela(pg))
        await pg.screenshot(path='z_agenda.png')
        # arrastar a última para o topo
        alca = pg.locator('#agPend .tarefa').last.locator('[data-alca]'); bx = await alca.bounding_box(); topo = await pg.locator('#agPend .tarefa').first.bounding_box()
        await pg.mouse.move(bx['x'] + bx['width'] / 2, bx['y'] + bx['height'] / 2); await pg.mouse.down()
        for k in range(1, 13): await pg.mouse.move(bx['x'] + bx['width'] / 2, bx['y'] + bx['height'] / 2 - (bx['y'] - topo['y'] + 20) * k / 12)
        await pg.mouse.up(); await pg.wait_for_timeout(600)
        print('arrastou última p/ topo:', await tela(pg), '| banco:', ordem())
        await pg.fill('#tarNova', 'Nova tarefa'); await pg.press('#tarNova', 'Enter'); await pg.wait_for_timeout(500)
        print('nova vai pro fim:', (await tela(pg))[-1])
        await pg.goto(BASE + 'index.html'); await pg.wait_for_selector('#cvStage'); print('card próxima:', (await pg.locator('.cv-card[data-cv=tar] .cv-list').inner_text()).replace('\n', ' '))
        m = await b.new_context(viewport={'width': 375, 'height': 760}, has_touch=True); await T9.setup(m); mp = await m.new_page()
        await mp.goto(BASE + 'index.html#/agenda'); await mp.fill('#lEmail', 'a@a.com'); await mp.fill('#lPass', 'x'); await mp.click('#lBtn'); await mp.wait_for_selector('#agPend')
        print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='z_m_agenda.png', full_page=True)
        print('ERRS', errs); await b.close()
if __name__ == "__main__": asyncio.run(main())
