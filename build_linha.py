linha = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Acompanhe seu projeto | dade.design</title>
<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#171617">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>__PAG_CSS__
.resp{max-width:640px}
.prog-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin:8px 0 10px;font-size:14px;color:var(--ink-300)}
.prog-top b{font-size:28px;color:var(--white);font-weight:700;letter-spacing:-.02em}
.barra{height:8px;border-radius:20px;background:var(--surface-elevated);overflow:hidden;margin-bottom:36px}
.barra div{height:100%;background:var(--lime);border-radius:20px;transition:width .6s}
.tl{list-style:none;position:relative;margin:0;padding:0}
.tl li{position:relative;padding:0 0 30px 46px}
.tl li:last-child{padding-bottom:0}
.tl li::before{content:"";position:absolute;left:13px;top:30px;bottom:-2px;width:2px;background:var(--hairline-dark)}
.tl li:last-child::before{display:none}
.tl li.ok::before{background:var(--lime)}
.tl .dot{position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;border:2px solid var(--hairline-dark);background:var(--ink-900,#171617);display:flex;align-items:center;justify-content:center}
.tl li.ok .dot{background:var(--lime);border-color:var(--lime)}
.tl li.ok .dot svg{width:14px;height:14px;color:#171617}
.tl li.now .dot{border-color:var(--lime)}
.tl li.now .dot::after{content:"";width:10px;height:10px;border-radius:50%;background:var(--lime);animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.7)}}
.tl .t{font-size:17px;font-weight:600;color:var(--ink-300);line-height:1.35;padding-top:2px}
.tl li.ok .t{color:var(--ink-200)}
.tl li.now .t{color:var(--white);font-size:19px}
.tl .s{display:inline-block;margin-top:6px;font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;border:1px solid var(--hairline-dark);color:var(--ink-400)}
.tl li.ok .s{color:var(--lime);border-color:rgba(193,253,66,.35)}
.tl li.now .s{background:var(--lime);border-color:var(--lime);color:#171617}
.fim{margin-top:36px;padding:22px 24px;border:1px solid var(--lime);border-radius:var(--r-lg);font-size:15px;color:var(--ink-200)}
.fim b{color:var(--white)}
.ajuda{margin-top:40px;font-size:14px;color:var(--ink-300)}
.ajuda a{color:var(--white);text-decoration:underline}
@media (prefers-reduced-motion:reduce){.tl li.now .dot::after{animation:none}}
</style>
</head>
<body>
<main class="pg">
  <div class="pg-top"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade"><span style="font-size:13px;color:var(--ink-300)">Linha do tempo do projeto</span></div>
  <div id="root"><div class="wait">Carregando…</div></div>
  <p class="priv" style="margin-top:48px"><a href="privacidade.html" target="_blank" rel="noopener">Aviso de privacidade</a></p>
</main>
<script src="assets/dade.js"></script>
<script>
const SB='__SB_URL__',KEY='__SB_KEY__',D=window.DADE;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const root=document.getElementById('root'),token=new URLSearchParams(location.search).get('t')||'';
const rpc=async(fn,body)=>{const r=await fetch(SB+'/rest/v1/rpc/'+fn,{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw new Error('erro');return r.json()};
const OK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><polyline points="20 6 9 17 4 12"/></svg>';
function aviso(t,p){root.innerHTML=`<div class="resp"><span class="eyebrow">dade.design</span><h1>${t}</h1><p class="lede">${p}</p></div>`}
function tela(l){
  const et=(l.etapas||[]).map(e=>typeof e==='string'?e:(e&&e.titulo)||'').filter(Boolean),n=et.length,at=Math.max(0,Math.min(n,Number(l.atual)||0)),fim=at>=n,pct=n?Math.round(at/n*100):0;
  const servs=(l.servicos||[]).map(s=>window.dadeServNome?window.dadeServNome(s):s);
  document.title='Seu projeto | dade.design';
  root.innerHTML=`<div class="resp"><span class="eyebrow">${esc(l.cliente_nome)}</span><h1>${fim?'Projeto concluído':'Acompanhe o seu projeto'}</h1>
    <p class="lede">${servs.length?esc(servs.join(' · '))+'. ':''}${fim?'Todas as etapas foram concluídas. Obrigado pela confiança!':'Aqui você vê em que etapa o projeto está. A página se atualiza sempre que a dade avança.'}</p>
    <div class="prog-top"><span>${fim?'Todas as etapas concluídas':`Etapa ${at+1} de ${n}`}</span><b>${pct}%</b></div><div class="barra"><div style="width:${pct}%"></div></div>
    <ol class="tl">${et.map((t,i)=>{const c=i<at?'ok':i===at?'now':'';return `<li class="${c}"${c==='now'?' aria-current="step"':''}><span class="dot" aria-hidden="true">${c==='ok'?OK:''}</span><div class="t">${esc(t)}</div><span class="s">${c==='ok'?'Concluída':c==='now'?'Em andamento':'Próxima'}</span></li>`}).join('')}</ol>
    ${l.atualizada_em?`<p class="ajuda" style="margin-top:28px">Atualizado em ${new Date(l.atualizada_em).toLocaleDateString('pt-BR')}.</p>`:''}
    <p class="ajuda">Alguma dúvida? <a href="https://wa.me/${D.whatsapp}?text=${encodeURIComponent('Olá! Estou acompanhando o meu projeto e queria falar sobre ele.')}" target="_blank" rel="noopener">Fale com a dade no WhatsApp</a>.</p></div>`;
}
(async()=>{
  let l=null;
  try{l=token?await rpc('central_linha_publica',{p_token:token}):null}catch(e){return aviso('Não foi possível abrir','Confira a sua conexão e recarregue a página.')}
  if(!l)return aviso('Linha do tempo não encontrada','Confira o link que você recebeu ou fale com a dade.design.');
  tela(l);
})();
</script>
</body></html>
'''.replace('__SB_URL__', SB_URL).replace('__SB_KEY__', SB_KEY).replace('__PAG_CSS__', PAG_CSS)
open('site/linha.html', 'w', encoding='utf-8').write(linha)
