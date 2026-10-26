import asyncio, datetime, json
from playwright.async_api import async_playwright
import test9 as T9
T = T9.T; DB = T.DB; BASE = T.BASE
hj = datetime.date.today(); d = lambda n: str(hj + datetime.timedelta(days=n))
DB['central_portfolio'] = []
for c in DB['central_clientes']: c['email'] = 'marina@forma.com'
DB['central_tarefas'] = [{'id':'t1','texto':'Revisar logo','data':d(0),'feita_em':None,'ordem':10,'created_at':T.now(),'prazo':None}]
EV = [{'id':'e1','status':'confirmed','summary':'Call com Albory','start':{'dateTime':d(0)+'T14:00:00-03:00'},'end':{'dateTime':d(0)+'T15:00:00-03:00'},'hangoutLink':'https://meet.google.com/abc','htmlLink':'https://calendar.google.com/x','attendees':[{'email':'a@b.com'},{'email':'me@x.com','self':True}]},
      {'id':'e2','status':'confirmed','summary':'Feriado','start':{'date':d(3)},'end':{'date':d(4)},'htmlLink':'https://calendar.google.com/y'}]
POSTS = []
STUB = "window.google={accounts:{oauth2:{initTokenClient:function(o){return{requestAccessToken:function(){setTimeout(function(){o.callback({access_token:'tok',expires_in:3600})},10)}}},revoke:function(t,c){c&&c()}}}};"
async def setup(ctx):
    await T9.setup(ctx)
    await ctx.route('https://accounts.google.com/gsi/client', lambda r: r.fulfill(status=200, content_type='application/javascript', body=STUB))
    async def gapi(route):
        rq = route.request; H = {'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*'}
        if rq.method == 'OPTIONS': return await route.fulfill(status=204, headers=H)
        if rq.method == 'POST':
            b = json.loads(rq.post_data); POSTS.append((rq.url, b)); ev = {'id':'n'+str(len(POSTS)),'status':'confirmed', **b, 'hangoutLink':'https://meet.google.com/new' if 'conferenceData' in b else None,'htmlLink':'https://calendar.google.com/z'}
            EV.append(ev); return await route.fulfill(status=200, headers={**H,'content-type':'application/json'}, body=json.dumps(ev))
        await route.fulfill(status=200, headers={**H,'content-type':'application/json'}, body=json.dumps({'items':EV}))
    await ctx.route('https://www.googleapis.com/**', gapi)
async def main():
  async with async_playwright() as pw:
    b = await pw.chromium.launch(); errs = []
    for vw, nm in (((1280, 900), 'd'), ((390, 844), 'm')):
      ctx = await b.new_context(viewport={'width': vw[0], 'height': vw[1]}); await setup(ctx)
      pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
      await pg.goto(BASE + 'index.html#/agenda'); await pg.fill('#lEmail', 'd@d.com'); await pg.fill('#lPass', 'x'); await pg.click('#lBtn'); await pg.wait_for_selector('#tarNova')
      print(nm, 'antes:', (await pg.locator('.reu-off').inner_text()).replace('\n',' | '))
      await pg.wait_for_timeout(300)
      await pg.click('[data-a=reu-form]'); await pg.wait_for_selector('#r_t', timeout=5000)
      await pg.wait_for_timeout(300)
      print('reuniões hoje:', await pg.locator('.reu-it .tt a').all_inner_texts())
      await pg.select_option('#r_c', 'cl1'); await pg.fill('#r_e', (await pg.input_value('#r_e')) + ', socio@dade.com')
      print('auto:', await pg.input_value('#r_t'), '|', await pg.input_value('#r_e'))
      await pg.fill('#r_d', d(2)); await pg.fill('#r_h', '10:30'); await pg.select_option('#r_du', '45')
      if nm == 'd':
          await pg.screenshot(path='reu_modal.png')
          await pg.click('#r_ok')
      else:
          await pg.check('input[name=r_tipo][value=local]'); await pg.fill('#r_l', 'Rua X, 10'); await pg.click('#r_ok')
      await pg.wait_for_timeout(800)
      u, bd = POSTS[-1]; print('POST', 'sendUpdates=all' in u, bd['summary'], bd['start'], [a['email'] for a in bd['attendees']], 'meet' if 'conferenceData' in bd else bd.get('location'))
      print('toast:', await pg.locator('#toast').inner_text(), '| dia:', await pg.locator('.ag-nav strong').inner_text(), await pg.locator('.reu-it .tt a').all_inner_texts())
      await pg.screenshot(path=f'reu_dia_{nm}.png', full_page=True)
      await pg.click('[data-a=ag-vis][data-v=mes]'); await pg.wait_for_timeout(400); await pg.screenshot(path=f'reu_mes_{nm}.png', full_page=True)
      print(nm, 'overflow', await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
    print('ERRS', errs); await b.close()
asyncio.run(main())
