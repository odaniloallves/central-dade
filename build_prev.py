prev = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Prévia | dade.design</title>
<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#171617">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>__PAG_CSS__
.imgs{display:flex;flex-direction:column;gap:14px;margin:8px 0 32px}
.imgs a{display:block;border-radius:var(--r-lg);overflow:hidden;background:var(--surface-elevated)}
.imgs img{display:block;width:100%;height:auto}
.resp{max-width:640px}
</style>
</head>
<body>
<main class="pg wide">
  <div class="pg-top"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade"><span style="font-size:13px;color:var(--ink-300)">Prévia para aprovação</span></div>
  <div id="root"><div class="wait">Carregando…</div></div>
  <p class="priv" style="margin-top:48px"><a href="privacidade.html" target="_blank" rel="noopener">Aviso de privacidade</a></p>
</main>
<script src="assets/dade.js"></script>
<script>
const SB='__SB_URL__',KEY='__SB_KEY__',D=window.DADE;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const root=document.getElementById('root'),token=new URLSearchParams(location.search).get('t')||'';
const rpc=async(fn,body)=>{const r=await fetch(SB+'/rest/v1/rpc/'+fn,{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw new Error((await r.json().catch(()=>({}))).message||'erro');return r.json()};
const img=p=>SB+'/storage/v1/object/public/central-previas/'+String(p).split('/').map(encodeURIComponent).join('/');
const linkOk=l=>/^https:\/\//i.test(l||'');
const wpp=t=>'https://wa.me/'+D.whatsapp+'?text='+encodeURIComponent(t);
let pv=null,modo='';
function aviso(t,p){root.innerHTML=`<div class="resp"><span class="eyebrow">dade.design</span><h1>${t}</h1><p class="lede">${p}</p></div>`}
function galeria(){return `${(pv.imagens||[]).length?`<div class="imgs">${pv.imagens.map((p,i)=>`<a href="${esc(img(p))}" target="_blank" rel="noopener"><img src="${esc(img(p))}" alt="Imagem ${i+1} da prévia" loading="${i?'lazy':'eager'}"></a>`).join('')}</div>`:''}${linkOk(pv.link_externo)?`<div class="acts resp" style="margin:0 0 32px"><a class="btn btn-outline-dark" href="${esc(pv.link_externo)}" target="_blank" rel="noopener">Abrir o arquivo completo</a></div>`:''}`}
function cab(){return `<div class="resp"><span class="eyebrow">${pv.cliente?esc(pv.cliente)+' · ':''}versão ${Number(pv.rodada)}</span><h1>${esc(pv.titulo)}</h1></div>`}
function tela(){
  document.title=pv.titulo+' | dade.design';
  if(pv.status!=='aguardando'){
    const ok=pv.status==='aprovada';
    root.innerHTML=cab()+`<div class="resp"><p class="lede">${ok?`Prévia aprovada por ${esc(pv.resposta_nome)}. A dade segue com o restante do projeto.`:`${esc(pv.resposta_nome)} pediu ajustes. A dade já foi avisada e envia a nova versão neste mesmo link.`}</p>${ok?'':`<div class="box"><h2>Ajustes pedidos</h2>${(pv.resposta_ajustes||[]).map((a,i)=>`<div class="ln"><span>${i+1}. ${esc(a)}</span><span></span></div>`).join('')}</div>`}<div class="acts" style="margin-bottom:36px"><a class="btn btn-outline-dark" href="${wpp('Olá! Estou vendo a prévia "'+pv.titulo+'" da dade.design.')}" target="_blank" rel="noopener">Falar com a dade no WhatsApp</a></div></div>`+galeria();
    return;
  }
  const inclusa=Number(pv.rodada)===1;
  root.innerHTML=cab()+`<div class="resp"><p class="lede">Esta é a primeira etapa do projeto. Veja com calma e diga se podemos seguir ou se quer ajustar algo.</p></div>`+galeria()+
  `<div class="resp"><div class="box"><h2>O que você achou?</h2><div role="radiogroup" aria-label="Sua resposta">
    <button type="button" class="opt" role="radio" aria-checked="false" data-m="aprovar"><b>Aprovar</b><span>Está no caminho certo. A dade pode seguir com o restante do projeto.</span></button>
    <button type="button" class="opt" role="radio" aria-checked="false" data-m="ajustes"><b>Pedir ajustes</b><span>${inclusa?'Você tem <strong>1 rodada de ajustes inclusa, com até 3 ajustes</strong>. Depois dela, novos ajustes são cobrados à parte.':'A rodada de ajustes inclusa já foi usada. <strong>Estes ajustes serão orçados e cobrados à parte.</strong>'}</span></button></div>
    <div id="aj" hidden>${[1,2,3].map(i=>`<label class="fl" for="a${i}">Ajuste ${i}${i>1?' (opcional)':''}</label><textarea class="inp" id="a${i}" rows="2" maxlength="1000" placeholder="Descreva o que você quer mudar"></textarea>`).join('')}</div></div>
  <label class="fl" for="nome">Seu nome completo</label><input class="inp" id="nome" autocomplete="name" placeholder="Quem está respondendo">
  <p class="err" id="err" role="alert"></p><div class="acts"><button type="button" class="btn btn-primary" id="ok">Enviar resposta</button></div></div>`;
  root.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{modo=b.dataset.m;root.querySelectorAll('.opt').forEach(x=>x.setAttribute('aria-checked',x===b));document.getElementById('aj').hidden=modo!=='ajustes';if(modo==='ajustes')document.getElementById('a1').focus()});
  document.getElementById('ok').onclick=enviar;
}
async function enviar(){
  const err=document.getElementById('err'),btn=document.getElementById('ok'),nome=document.getElementById('nome').value.trim();
  const aj=[1,2,3].map(i=>document.getElementById('a'+i).value.trim()).filter(Boolean);
  if(!modo){err.textContent='Escolha se quer aprovar ou pedir ajustes.';return}
  if(modo==='ajustes'&&!aj.length){err.textContent='Descreva ao menos um ajuste.';document.getElementById('a1').focus();return}
  if(nome.length<2){err.textContent='Informe o seu nome.';document.getElementById('nome').focus();return}
  err.textContent='';btn.disabled=true;btn.textContent='Enviando…';
  try{
    const r=await rpc('central_responder_previa',{p_token:token,p_nome:nome,p_acao:modo,p_ajustes:modo==='ajustes'?aj:[]});if(!r)throw new Error('x');pv=r;
    fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({access_key:D.avisoKey,subject:`Prévia ${pv.status==='aprovada'?'aprovada':'com ajustes'} — ${pv.cliente||pv.titulo}`,from_name:'Central dade',message:`${nome} ${pv.status==='aprovada'?'aprovou':'pediu ajustes n'}a prévia "${pv.titulo}"${pv.cliente?' de '+pv.cliente:''} (versão ${pv.rodada}).${aj.length&&pv.status!=='aprovada'?'\n\n'+aj.map((a,i)=>`${i+1}. ${a}`).join('\n'):''}`})}).catch(()=>{});
    tela();window.scrollTo(0,0);
  }catch(e){btn.disabled=false;btn.textContent='Enviar resposta';err.textContent='Não foi possível enviar agora. Recarregue a página e tente de novo, ou fale com a dade pelo WhatsApp.'}
}
(async()=>{
  try{pv=token?await rpc('central_previa_publica',{p_token:token}):null}catch(e){return aviso('Não foi possível abrir','Confira a sua conexão e recarregue a página.')}
  if(!pv)return aviso('Prévia não encontrada','Confira o link que você recebeu ou fale com a dade.design.');
  tela();
})();
</script>
</body></html>
'''.replace('__SB_URL__',SB_URL).replace('__SB_KEY__',SB_KEY).replace('__PAG_CSS__',PAG_CSS)
open('site/previa.html','w',encoding='utf-8').write(prev)
open('check_prev.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',prev,re.S)[0])
