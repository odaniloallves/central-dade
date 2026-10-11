ent = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Suas peças | dade.design</title>
<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#171617">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>__PAG_CSS__
.resp{max-width:720px}
.sem{margin-top:44px}
.sem-h{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.sem-h h2{font-size:24px;font-weight:700;color:var(--white);letter-spacing:-.01em}
.sem-h p{font-size:13px;color:var(--ink-400);margin-top:4px}
.sem-h .acts{margin:0;gap:8px}
.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.pc{border:1px solid var(--hairline-dark);border-radius:var(--r-lg);overflow:hidden;background:var(--surface-elevated);display:flex;flex-direction:column}
.pc.alt{border-color:#f5a524}
.pc.ok{border-color:rgba(193,253,66,.45)}
.pc .mid{display:block;background:#0f0f0f;aspect-ratio:4/5;position:relative}
.pc .mid img,.pc .mid video{width:100%;height:100%;object-fit:contain;display:block}
.pc .mid .pdf{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:14px;color:var(--ink-300)}
.pc .inf{padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;flex:1}
.pc .nm{font-size:13px;color:var(--ink-300);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chip{align-self:flex-start;font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;border:1px solid var(--hairline-dark);color:var(--ink-400)}
.pc.ok .chip{color:var(--lime);border-color:rgba(193,253,66,.35)}
.pc.alt .chip{color:#f5a524;border-color:rgba(245,165,36,.45)}
.pc .ped{font-size:13px;color:var(--ink-200);background:rgba(245,165,36,.08);border-radius:10px;padding:10px 12px;line-height:1.45}
.pc .bts{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto}
.pc .bts .btn{height:40px;padding:0 14px;font-size:13px}
.pc textarea{width:100%;min-height:76px;resize:vertical}
.vazio{margin-top:36px;padding:26px;border:1px dashed var(--hairline-dark);border-radius:var(--r-lg);color:var(--ink-300);font-size:15px}
.ajuda{margin-top:44px;font-size:14px;color:var(--ink-300)}
.ajuda a{color:var(--white);text-decoration:underline}
</style>
</head>
<body>
<main class="pg wide">
  <div class="pg-top"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade"><span style="font-size:13px;color:var(--ink-300)">Suas peças</span></div>
  <div id="root"><div class="wait">Carregando…</div></div>
  <p class="priv" style="margin-top:48px"><a href="privacidade.html" target="_blank" rel="noopener">Aviso de privacidade</a></p>
</main>
<script src="assets/dade.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js" defer></script>
<script>
const SB='__SB_URL__',KEY='__SB_KEY__',D=window.DADE;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const root=document.getElementById('root'),token=new URLSearchParams(location.search).get('t')||'';
const rpc=async(fn,body)=>{const r=await fetch(SB+'/rest/v1/rpc/'+fn,{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw new Error('erro');return r.json()};
const url=p=>SB+'/storage/v1/object/public/central-entregas/'+String(p).split('/').map(encodeURIComponent).join('/');
const baixar=(p,n)=>url(p)+'?download='+encodeURIComponent(n);
const dmy=d=>d?String(d).slice(0,10).split('-').reverse().join('/'):'';
let data=null,aberto=null;
const meuNome=()=>{try{return localStorage.getItem('dade-nome')||''}catch(e){return ''}};
function aviso(t,p){root.innerHTML=`<div class="resp"><span class="eyebrow">dade.design</span><h1>${t}</h1><p class="lede">${p}</p></div>`}
function peca(e,p){
  const c=p.status==='aprovada'?'ok':p.status==='alteracao'?'alt':'',edit=aberto===p.id;
  const mid=p.tipo==='video'?`<video src="${esc(url(p.path))}" controls playsinline preload="metadata"></video>`:p.tipo==='pdf'?`<span class="pdf">PDF · ${esc(p.nome)}</span>`:`<img src="${esc(url(p.path))}" alt="${esc(p.nome)}" loading="lazy">`;
  return `<div class="pc ${c}" id="p-${p.id}"><a class="mid" href="${esc(url(p.path))}" target="_blank" rel="noopener" aria-label="Abrir ${esc(p.nome)} em tamanho real">${mid}</a><div class="inf">
    <span class="nm" title="${esc(p.nome)}">${esc(p.nome)}</span><span class="chip">${c==='ok'?'Aprovada':c==='alt'?'Alteração pedida':'Nova'}</span>
    ${p.status==='alteracao'&&p.pedido&&!edit?`<div class="ped">${esc(p.pedido)}</div>`:''}
    ${edit?`<label class="fl" for="tx-${p.id}" style="margin:0">O que você quer mudar?</label><textarea class="inp" id="tx-${p.id}" maxlength="1000" placeholder="Ex.: trocar a foto, aumentar o título">${p.status==='alteracao'?esc(p.pedido):''}</textarea>
      <input class="inp" id="nm-${p.id}" maxlength="120" placeholder="Seu nome (opcional)" value="${esc(meuNome())}" autocomplete="name">
      <div class="bts"><button class="btn btn-primary" data-x="enviar" data-e="${e.id}" data-p="${p.id}" type="button">Enviar pedido</button><button class="btn btn-outline-dark" data-x="cancelar" type="button">Cancelar</button></div>`
    :`<div class="bts"><a class="btn btn-outline-dark" href="${esc(baixar(p.path,p.nome))}" download="${esc(p.nome)}">Baixar</a>${c==='ok'?'':`<button class="btn btn-outline-dark" data-x="aprovar" data-e="${e.id}" data-p="${p.id}" type="button">Aprovar</button>`}<button class="btn btn-outline-dark" data-x="alterar" data-p="${p.id}" type="button">${c==='alt'?'Editar pedido':'Pedir alteração'}</button></div>`}
  </div></div>`;
}
function tela(){
  const es=data.entregas||[];
  root.innerHTML=`<div class="resp"><span class="eyebrow">${esc(data.cliente_nome)}</span><h1>Suas peças</h1><p class="lede">As peças que a dade criou para você, por semana. Baixe, aprove ou peça alteração direto por aqui.</p></div>`+
    (es.length?es.map(e=>{const pend=e.pecas.filter(p=>p.status==='nova').length;return `<section class="sem"><div class="sem-h"><div><h2>${esc(e.titulo)}</h2><p>${e.pecas.length} ${e.pecas.length===1?'peça':'peças'} · disponível para baixar até ${dmy(e.expira_em)}</p></div><div class="acts">${e.pecas.length>1?`<button class="btn btn-outline-dark" data-x="zip" data-e="${e.id}" type="button">Baixar todas</button>`:''}${pend?`<button class="btn btn-primary" data-x="todas" data-e="${e.id}" type="button">Aprovar ${pend>1?'todas':'a peça'}</button>`:''}</div></div><div class="grade">${e.pecas.map(p=>peca(e,p)).join('')}</div></section>`}).join('')
      :'<div class="vazio">Nenhuma peça disponível agora. Quando a dade enviar as próximas, elas aparecem aqui neste mesmo link.</div>')+
    `<p class="ajuda">As peças ficam disponíveis por alguns dias. Baixe as que for usar. Alguma dúvida? <a href="https://wa.me/${D.whatsapp}?text=${encodeURIComponent('Olá! Vi as peças no link e queria falar sobre elas.')}" target="_blank" rel="noopener">Fale com a dade no WhatsApp</a>.</p>`;
}
function avisaDade(assunto,texto){fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({access_key:D.avisoKey,subject:assunto,from_name:'Central dade',message:texto})}).catch(()=>{})}
async function responder(e,p,acao,texto,nome){
  const r=await rpc('central_entrega_responder',{p_token:token,p_entrega:e,p_peca:p||null,p_acao:acao,p_texto:texto||null,p_nome:nome||null});if(!r)throw new Error('x');data=r;
}
async function zip(eid,btn){
  const e=data.entregas.find(x=>x.id===eid);if(!window.JSZip){e.pecas.forEach((p,i)=>setTimeout(()=>{const a=document.createElement('a');a.href=baixar(p.path,p.nome);a.download=p.nome;document.body.appendChild(a);a.click();a.remove()},i*600));return}
  btn.disabled=true;const t=btn.textContent;btn.textContent='Preparando…';
  try{const z=new JSZip(),usados={};for(const p of e.pecas){const b=await (await fetch(url(p.path))).blob();let n=p.nome;usados[n]=(usados[n]||0)+1;if(usados[n]>1)n=n.replace(/(\.[^.]+)?$/,'-'+usados[n]+'$1');z.file(n,b)}
    const blob=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(e.titulo||'pecas').replace(/\//g,'-').replace(/[^\w\- À-ú]/g,'').trim()+'.zip';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},2000)}
  catch(er){alert('Não foi possível juntar os arquivos. Baixe uma por uma.')}
  btn.disabled=false;btn.textContent=t;
}
root.addEventListener('click',async ev=>{
  const b=ev.target.closest('[data-x]');if(!b)return;const x=b.dataset.x;
  if(x==='alterar'){aberto=b.dataset.p;tela();const t=document.getElementById('tx-'+aberto);if(t)t.focus();return}
  if(x==='cancelar'){aberto=null;tela();return}
  if(x==='zip')return zip(b.dataset.e,b);
  b.disabled=true;
  try{
    if(x==='enviar'){const p=b.dataset.p,tx=document.getElementById('tx-'+p).value.trim(),nm=document.getElementById('nm-'+p).value.trim();
      if(tx.length<2){b.disabled=false;document.getElementById('tx-'+p).focus();return}
      try{if(nm)localStorage.setItem('dade-nome',nm)}catch(e){}
      const pc=data.entregas.flatMap(e=>e.pecas).find(q=>q.id===p);await responder(b.dataset.e,p,'alterar',tx,nm);aberto=null;tela();
      avisaDade(`Pedido de alteração — ${data.cliente_nome}`,`${nm||'O cliente'} pediu alteração na peça "${pc?pc.nome:''}":\n\n${tx}`);
      const el=document.getElementById('p-'+p);if(el)el.scrollIntoView({block:'center'});return}
    if(x==='aprovar'){await responder(b.dataset.e,b.dataset.p,'aprovar');tela();return}
    if(x==='todas'){await responder(b.dataset.e,null,'aprovar_todas');tela();const e=data.entregas.find(q=>q.id===b.dataset.e);avisaDade(`Peças aprovadas — ${data.cliente_nome}`,`${data.cliente_nome} aprovou as peças de "${e?e.titulo:''}".`);return}
  }catch(er){b.disabled=false;alert('Não foi possível enviar agora. Recarregue a página e tente de novo.')}
});
(async()=>{
  try{data=token?await rpc('central_entregas_publica',{p_token:token}):null}catch(e){return aviso('Não foi possível abrir','Confira a sua conexão e recarregue a página.')}
  if(!data)return aviso('Link não encontrado','Confira o link que você recebeu ou fale com a dade.design.');
  tela();
})();
</script>
</body></html>
'''.replace('__SB_URL__', SB_URL).replace('__SB_KEY__', SB_KEY).replace('__PAG_CSS__', PAG_CSS)
open('site/entregas.html', 'w', encoding='utf-8').write(ent)
