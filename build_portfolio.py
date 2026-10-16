# Portfólio público: portfolio.html (link curto /portfolio).
#   /portfolio                      -> todos os projetos publicados
#   /portfolio?identidade,posts     -> só essas categorias (link montado na central)
#   /portfolio#<slug>               -> abre direto um projeto
# As imagens vêm do Supabase (bucket público central-portfolio) ou de assets/portfolio/ (subidas pelo build).
import os, shutil
if os.path.isdir('portfolio'):
    shutil.copytree('portfolio', 'site/assets/portfolio', dirs_exist_ok=True)
pf = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Portfólio | dade.design</title>
<meta name="description" content="Identidade visual, posts, materiais impressos e sites criados pela dade.design.">
<meta property="og:title" content="Portfólio | dade.design"><meta property="og:description" content="Trabalhos selecionados da dade.design."><meta property="og:image" content="https://central.dadedesign.com.br/assets/img/app-icon-180.png">
<meta name="theme-color" content="#171617">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>
body{background:var(--ink-900);color:var(--white);min-height:100vh}
.w{max-width:1240px;margin:0 auto;padding:0 24px}
.top{display:flex;justify-content:space-between;align-items:center;padding:28px 0}
.top img{height:26px;width:auto}
.pill{display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 20px;border-radius:var(--r-full);border:1px solid rgba(255,255,255,.3);color:var(--white);font-size:14px;font-weight:500;text-decoration:none;transition:.2s}
.pill:hover{background:var(--white);color:var(--ink-900)}
.pill.lime{background:var(--lime);border-color:var(--lime);color:var(--ink-900);font-weight:600}
.pill.lime:hover{background:var(--white);border-color:var(--white)}
.phero{padding:72px 0 40px}
.phero h1{font-size:clamp(40px,8vw,96px);font-weight:700;letter-spacing:-.04em;line-height:.98;margin:18px 0 22px;max-width:12ch}
.phero h1 em{font-style:normal;color:var(--lime)}
.phero p{color:var(--ink-300);font-size:18px;max-width:52ch;line-height:1.55}
.fil{display:flex;gap:8px;flex-wrap:wrap;margin:36px 0 34px}
.fil button{height:40px;padding:0 18px;border-radius:var(--r-full);border:1px solid var(--hairline-dark);background:transparent;color:var(--ink-300);font:500 14px var(--font);cursor:pointer;transition:.2s}
.fil button:hover{color:var(--white);border-color:rgba(255,255,255,.4)}
.fil button[aria-pressed=true]{background:var(--white);color:var(--ink-900);border-color:var(--white)}
.fil button span{opacity:.55;margin-left:6px;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:28px 24px}
.card{display:block;text-decoration:none;color:inherit;cursor:pointer;background:none;border:0;padding:0;text-align:left;font:inherit;width:100%}
.card .im{aspect-ratio:4/3;border-radius:var(--r-lg);overflow:hidden;background:var(--ink-800)}
.card.big{grid-column:span 2}.card.big .im{aspect-ratio:16/8}
.card img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.card:hover img{transform:scale(1.035)}
.card .meta{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:16px 4px 0}
.card h3{font-size:20px;font-weight:600;letter-spacing:-.01em;margin:0}
.card small{font-size:13px;color:var(--ink-400);white-space:nowrap}
.card p{font-size:14px;color:var(--ink-400);margin:4px 4px 0}
.vazio{padding:60px 0;color:var(--ink-300)}
.cta{margin:96px 0 40px;border-radius:var(--r-xl);background:var(--lime);color:var(--ink-900);padding:clamp(32px,6vw,72px);display:flex;justify-content:space-between;align-items:flex-end;gap:28px;flex-wrap:wrap}
.cta h2{font-size:clamp(30px,5vw,56px);font-weight:700;letter-spacing:-.03em;line-height:1.02;margin:0;max-width:14ch}
.cta .bt{display:flex;gap:10px;flex-wrap:wrap}
.cta .pill{border-color:var(--ink-900);color:var(--ink-900)}
.cta .pill:hover{background:var(--ink-900);color:var(--white)}
.cta .pill.dk{background:var(--ink-900);color:var(--white)}
.cta .pill.dk:hover{background:var(--white);color:var(--ink-900);border-color:var(--white)}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:24px 0 40px;font-size:13px;color:var(--ink-400)}
.foot a{color:var(--ink-300)}
/* projeto aberto */
.pj{position:fixed;inset:0;background:var(--ink-900);z-index:50;overflow-y:auto;opacity:0;pointer-events:none;transition:opacity .25s}
.pj.on{opacity:1;pointer-events:auto}
.pj-bar{position:sticky;top:0;z-index:2;background:rgba(23,22,23,.86);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--hairline-dark)}
.pj-bar .w{display:flex;justify-content:space-between;align-items:center;height:68px;gap:12px}
.pj-bar b{font-size:15px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.x{width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.3);background:transparent;color:var(--white);cursor:pointer;font-size:20px;line-height:1;flex:none}
.x:hover{background:var(--white);color:var(--ink-900)}
.pj-h{padding:56px 0 36px;display:grid;grid-template-columns:1.2fr 1fr;gap:32px;align-items:end}
.pj-h h2{font-size:clamp(34px,6vw,72px);font-weight:700;letter-spacing:-.035em;line-height:1;margin:14px 0 0}
.pj-h p{color:var(--ink-300);font-size:17px;line-height:1.6;margin:0;white-space:pre-line}
.pj-h dl{display:flex;gap:28px;margin:18px 0 0;font-size:13px}
.pj-h dt{color:var(--ink-400)}.pj-h dd{margin:2px 0 0;color:var(--white);font-weight:500}
.imgs{display:flex;flex-direction:column;gap:16px}
.imgs img,.imgs video{width:100%;height:auto;display:block;border-radius:var(--r-lg);background:var(--ink-800)}
.nx{display:flex;justify-content:space-between;gap:12px;margin:48px 0 64px;flex-wrap:wrap}
.nx button{flex:1 1 260px;text-align:left;padding:22px 24px;border-radius:var(--r-lg);border:1px solid var(--hairline-dark);background:transparent;color:var(--white);font:inherit;cursor:pointer;transition:.2s}
.nx button:hover{border-color:var(--lime)}
.nx button small{display:block;color:var(--ink-400);font-size:12px;margin-bottom:4px}
.nx button b{font-size:18px;font-weight:600}
.nx button.r{text-align:right}
@media (max-width:760px){.grid{grid-template-columns:1fr;gap:28px}.card.big{grid-column:auto}.card.big .im{aspect-ratio:4/3}.phero{padding:40px 0 20px}.pj-h{grid-template-columns:1fr;padding:36px 0 26px}.top .pill:not(.lime){display:none}.w{padding:0 16px}.imgs{gap:10px}.imgs img{border-radius:var(--r-md)}}
@media (prefers-reduced-motion:reduce){.card img,.pj{transition:none}}
</style>
</head>
<body>
<div class="w">
  <header class="top"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade.design"><a class="pill lime" id="zap" target="_blank" rel="noopener">Fale com a dade</a></header>
  <section class="phero"><span class="eyebrow">Portfólio</span><h1>Marcas com <em>presença</em>.</h1><p id="lede">Identidade visual, posts, materiais impressos e sites criados pela dade.design.</p></section>
  <nav class="fil" id="fil" aria-label="Filtrar por categoria"></nav>
  <main class="grid" id="grid"><p class="vazio">Carregando…</p></main>
  <section class="cta"><h2>Vamos criar a próxima?</h2><div class="bt"><a class="pill dk" id="zap2" target="_blank" rel="noopener">Conversar no WhatsApp</a><a class="pill" id="mail">Mandar e-mail</a></div></section>
  <footer class="foot"><span>© <span id="ano"></span> dade.design</span><a href="privacidade.html" target="_blank" rel="noopener">Aviso de privacidade</a></footer>
</div>
<div class="pj" id="pj" role="dialog" aria-modal="true" aria-labelledby="pjT"></div>
<script src="assets/dade.js"></script>
<script>
const SB='__SB_URL__',KEY='__SB_KEY__',D=window.DADE;
const CAT={identidade:'Identidade visual',posts:'Posts e redes sociais',impressos:'Materiais impressos',sites:'Sites e landing pages',apresentacoes:'Apresentações',motion:'Motion e vídeo',outros:'Outros projetos'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=p=>/^assets\//.test(p)?p:SB+'/storage/v1/object/public/central-portfolio/'+p.split('/').map(encodeURIComponent).join('/');
const $=id=>document.getElementById(id);
const zap='https://wa.me/'+D.whatsapp+'?text='+encodeURIComponent('Olá! Vi o portfólio da dade e queria conversar sobre um projeto.');
$('zap').href=$('zap2').href=zap;$('mail').href='mailto:'+D.email;$('ano').textContent=new Date().getFullYear();
const q=location.search.slice(1).split(/[,&]/).map(decodeURIComponent).filter(k=>CAT[k]);
let P=[],vis=[],cat='';
const isVid=p=>/\.mp4$/i.test(p);
function cards(){
  vis=P.filter(p=>!cat||p.categoria===cat);
  $('grid').innerHTML=vis.length?vis.map((p,i)=>`<button class="card${p.destaque&&!cat&&vis.length>2?' big':''}" data-s="${esc(p.slug)}" type="button"><div class="im">${isVid(p.imagens[0])?`<video src="${esc(url(p.imagens[0]))}" muted loop playsinline autoplay></video>`:`<img src="${esc(url(p.imagens[0]))}" alt="${esc(p.titulo)}" ${i>1?'loading="lazy"':''}>`}</div><div class="meta"><h3>${esc(p.titulo)}</h3><small>${esc(CAT[p.categoria]||'')}</small></div>${p.cliente?`<p>${esc(p.cliente)}</p>`:''}</button>`).join(''):'<p class="vazio">Nenhum projeto por aqui ainda.</p>';
}
function filtros(){
  const cs=Object.keys(CAT).filter(k=>P.some(p=>p.categoria===k));
  $('fil').innerHTML=cs.length>1?[['','Todos',P.length],...cs.map(k=>[k,CAT[k],P.filter(p=>p.categoria===k).length])].map(([k,l,n])=>`<button type="button" data-c="${k}" aria-pressed="${cat===k}">${l}<span>${n}</span></button>`).join(''):'';
}
function abrir(slug,push=true){
  const i=vis.findIndex(p=>p.slug===slug),p=vis[i]||P.find(x=>x.slug===slug);if(!p)return fechar(false);
  const L=vis.length>1?vis:P,j=L.indexOf(p),ant=L[(j-1+L.length)%L.length],prox=L[(j+1)%L.length];
  $('pj').innerHTML=`<div class="pj-bar"><div class="w"><b>${esc(p.titulo)}</b><button class="x" data-x="1" type="button" aria-label="Fechar">×</button></div></div><div class="w">
    <div class="pj-h"><div><span class="eyebrow">${esc(CAT[p.categoria]||'')}</span><h2 id="pjT">${esc(p.titulo)}</h2><dl>${p.cliente?`<div><dt>Cliente</dt><dd>${esc(p.cliente)}</dd></div>`:''}${p.ano?`<div><dt>Ano</dt><dd>${p.ano}</dd></div>`:''}</dl></div>${p.descricao?`<p>${esc(p.descricao)}</p>`:'<span></span>'}</div>
    <div class="imgs">${p.imagens.map((m,k)=>isVid(m)?`<video src="${esc(url(m))}" controls playsinline muted loop autoplay></video>`:`<img src="${esc(url(m))}" alt="${esc(p.titulo)}, imagem ${k+1}" ${k?'loading="lazy"':''}>`).join('')}</div>
    ${L.length>1?`<div class="nx"><button data-s="${esc(ant.slug)}" type="button"><small>← Anterior</small><b>${esc(ant.titulo)}</b></button><button class="r" data-s="${esc(prox.slug)}" type="button"><small>Próximo →</small><b>${esc(prox.titulo)}</b></button></div>`:'<div style="height:64px"></div>'}</div>`;
  $('pj').classList.add('on');$('pj').scrollTop=0;document.body.style.overflow='hidden';document.title=p.titulo+' | dade.design';
  if(push&&location.hash!=='#'+p.slug)history.pushState(null,'','#'+p.slug);
  $('pj').querySelector('.x').focus({preventScroll:true});
}
function fechar(push=true){$('pj').classList.remove('on');document.body.style.overflow='';document.title='Portfólio | dade.design';if(push&&location.hash)history.pushState(null,'',location.pathname+location.search)}
document.addEventListener('click',e=>{const s=e.target.closest('[data-s]');if(s)return abrir(s.dataset.s);if(e.target.closest('[data-x]'))return fechar();const c=e.target.closest('[data-c]');if(c){cat=c.dataset.c;filtros();cards()}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('pj').classList.contains('on'))fechar()});
addEventListener('popstate',()=>{const h=decodeURIComponent(location.hash.slice(1));h?abrir(h,false):fechar(false)});
(async()=>{
  try{const r=await fetch(SB+'/rest/v1/rpc/central_portfolio_publico',{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:'{}'});if(!r.ok)throw 0;P=await r.json()}
  catch(e){$('grid').innerHTML='<p class="vazio">Não foi possível carregar o portfólio. Recarregue a página.</p>';return}
  if(q.length){P=P.filter(p=>q.includes(p.categoria));$('lede').textContent='Seleção de projetos: '+q.map(k=>CAT[k]).join(' · ')+'.'}
  filtros();cards();const h=decodeURIComponent(location.hash.slice(1));if(h)abrir(h,false);
})();
</script>
</body></html>
'''.replace('__SB_URL__', SB_URL).replace('__SB_KEY__', SB_KEY)
open('site/portfolio.html', 'w', encoding='utf-8').write(pf)
