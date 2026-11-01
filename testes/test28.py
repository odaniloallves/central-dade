import asyncio, json
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
DB['central_portfolio'] = []; DB['central_cofre'] = []; DB.setdefault('central_config', [])
XL = open('/tmp/claude-0/-home-claude/cf68f954-590c-57c9-b515-43e4bf505a82/scratchpad/xl/node_modules/xlsx/dist/xlsx.full.min.js').read()
async def setup(ctx):
    await T9.setup(ctx)
    await ctx.route('https://cdnjs.cloudflare.com/ajax/libs/xlsx/**', lambda r: r.fulfill(status=200, content_type='application/javascript', body=XL))
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    ctx = await b.new_context(viewport={'width':1280,'height':900}); await setup(ctx)
    await ctx.grant_permissions(['clipboard-read','clipboard-write'], origin='http://localhost:8765')
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + 'index.html#/senhas'); await pg.fill('#lEmail','d@d.com'); await pg.fill('#lPass','x'); await pg.click('#lBtn'); await pg.wait_for_selector('#cf_s')
    print('tela:', await pg.locator('.pin-box h1').inner_text())
    await pg.fill('#cf_s', 'curta'); await pg.fill('#cf_s2', 'curta'); await pg.click('#cf_ok'); print('curta:', await pg.locator('#cfErr').inner_text())
    await pg.fill('#cf_s', 'MinhaSenhaMestra#2026'); await pg.fill('#cf_s2', 'MinhaSenhaMestra#2026'); await pg.click('#cf_ok'); await pg.wait_for_selector('.cf-busca', timeout=15000)
    cfg = next(c for c in DB['central_config'] if c['chave']=='cofre')['valor']; print('config salva:', sorted(cfg.keys()), 'tem senha em claro?', 'MinhaSenha' in json.dumps(cfg))
    await pg.set_input_files('[data-c=cof-import]', 'cofre_fake.xlsx'); await pg.wait_for_timeout(1500)
    print('importadas:', len(DB['central_cofre']), '| texto em claro no banco?', any('SenhaFalsa' in json.dumps(r) or 'Site Teste' in json.dumps(r) for r in DB['central_cofre']))
    await pg.wait_for_timeout(800)
    print('lista:', await pg.locator('.cf-p b').all_inner_texts())
    await pg.set_input_files('[data-c=cof-import]', 'cofre_fake.xlsx'); await pg.wait_for_timeout(800); print('reimportar duplica?', len(DB['central_cofre']))
    first = pg.locator('.cf-it').first
    await first.locator('[data-a=cof-copiar][data-k=senha]').click(); await pg.wait_for_timeout(200); print('copiou senha:', await pg.evaluate('navigator.clipboard.readText()'))
    print('mascarada:', await first.locator('.cf-s').inner_text()); await first.locator('[data-a=cof-ver]').click(); print('mostrada:', await pg.locator('.cf-it').first.locator('.cf-s').inner_text())
    await pg.fill('#cfBusca', 'banco'); await pg.wait_for_timeout(300); print('busca:', await pg.locator('.cf-p b').all_inner_texts())
    await pg.fill('#cfBusca', ''); await pg.click('.page-header [data-a=cof-form]'); await pg.fill('#cs_p','Registro.br'); await pg.fill('#cs_u','dan'); await pg.click('[data-a=cof-gerar]'); g = await pg.input_value('#cs_s'); await pg.click('#cs_ok'); await pg.wait_for_timeout(800)
    print('nova:', len(DB['central_cofre']), 'gerada len', len(g), 'na lista:', 'Registro.br' in await pg.locator('.cf-p b').all_inner_texts())
    await pg.screenshot(path='cof_d.png', full_page=True)
    await pg.click('[data-a=cof-travar]'); await pg.wait_for_selector('#cf_s'); await pg.fill('#cf_s','errada'); await pg.click('#cf_ok'); await pg.wait_for_timeout(1500); print('errada:', await pg.locator('#cfErr').inner_text())
    await pg.fill('#cf_s','MinhaSenhaMestra#2026'); await pg.click('#cf_ok'); await pg.wait_for_selector('.cf-it', timeout=15000); print('reaberto:', await pg.locator('.cf-it').count())
    await pg.goto(BASE + 'index.html#/agenda'); await pg.wait_for_timeout(300); await pg.goto(BASE + 'index.html#/senhas'); await pg.wait_for_timeout(300); print('travou ao sair:', await pg.locator('#cf_s').count())
    m = await b.new_context(viewport={'width':390,'height':844}); await setup(m); mp = await m.new_page()
    await mp.goto(BASE + 'index.html#/senhas'); await mp.fill('#lEmail','d@d.com'); await mp.fill('#lPass','x'); await mp.click('#lBtn'); await mp.wait_for_selector('#cf_s'); await mp.fill('#cf_s','MinhaSenhaMestra#2026'); await mp.click('#cf_ok'); await mp.wait_for_selector('.cf-it', timeout=15000)
    print('mobile overflow:', await mp.evaluate('document.documentElement.scrollWidth>innerWidth')); await mp.screenshot(path='cof_m.png', full_page=True)
    print('ERRS', errs); await b.close()
asyncio.run(main())
