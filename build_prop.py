import re, os, shutil, json, subprocess
from PIL import Image
P='origem/dade-propostas/'
SB_URL='https://hgkxybswazgcpqpksvkf.supabase.co'; SB_KEY='sb_publishable_4-plrhdRN1mZA6uDxnDmKA_muzq8QUu'
os.makedirs('site/assets/img/dade',exist_ok=True); os.makedirs('site/assets/css',exist_ok=True)
for f in ('logo-dade-colorido.png','logo-dade-branco.png','icone-dade-branco.png'):
    shutil.copy(P+'assets/img/dade/'+f,'site/assets/img/dade/'+f)
Image.open(P+'assets/img/dade/fundador.jpg').convert('RGB').save('site/assets/img/dade/fundador.jpg',quality=84,optimize=True,progressive=True)
for f in ('favicon.png','app-icon-180.png'): shutil.copy(P+'assets/img/'+f,'site/assets/img/'+f)
shutil.copy(P+'assets/css/proposta.css','site/assets/css/proposta.css')
LOGOS=[('hisense','Hisense'),('electrolux','Electrolux'),('1a99','1A99'),('up365','UP365'),('logshare','LogShare'),('agencias-lucrativas','Agências Lucrativas'),('dessafit','DessaFit')]
os.makedirs('site/assets/img/clientes',exist_ok=True)
for f,_ in LOGOS: shutil.copy('origem/logos/'+f+'.png','site/assets/img/clientes/'+f+'.png')

# catálogo de serviços: PHP -> JSON, usando o próprio PHP para não redigitar nada
cat=json.loads(subprocess.check_output(['php','-r','require "'+P+'templates/servicos_data.php"; echo json_encode(catalogoServicos(), JSON_UNESCAPED_UNICODE);']))
open('site/assets/dade.js','w',encoding='utf-8').write('''/* dade.design | dados compartilhados pela central e pela página pública da proposta */
window.DADE = {
  whatsapp: '5511947504840', // com DDI e DDD, só dígitos
  pix: { chave: '52.409.459/0001-47', tipo: 'CNPJ' },
  avisoKey: 'da574319-0e26-4eaf-b8b8-43e4e55143ce', // Web3Forms: e-mail de aviso quando uma proposta é aprovada
  fundador: 'Danilo Alves',
  cargo: 'Fundador e diretor criativo',
  email: 'danilo@dadedesign.com.br',
  site: 'dadedesign.com.br',
  instagram: '', // ex.: 'dadedesign' (vazio = não aparece)
};
/* Catálogo de serviços. A chave (ex.: identidade_visual) é o que fica salvo no banco. */
window.DADE_SERVICOS = '''+json.dumps(cat,ensure_ascii=False,indent=2)+''';
window.DADE_COND = {
  '50_50_entrega': '50% na aprovação + 50% na entrega',
  '50_50_data': '50% na aprovação + 50% na metade do projeto',
  'avista': 'À vista no fechamento (com desconto)',
  '2x': 'Parcelado em 2x',
  '3x': 'Parcelado em 3x',
  'pix': 'Pix ou transferência bancária',
};
window.dadeCond = c => window.DADE_COND[c] || c || '';
window.dadeServNome = k => (window.DADE_SERVICOS[k] || {}).nome || k;
window.dadeMoney = v => 'R$ ' + Number(v || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
''')

# página pública: converte o corpo do proposta.php em um template JS
php=open(P+'proposta.php',encoding='utf-8').read()
body=php[php.index('<div id="progressBar"></div>'):php.index('<script>\n(function(){')]
scroll=re.search(r'<script>\n(\(function\(\)\{.*?\}\)\(\);)\n</script>',php,re.S).group(1)
assert '`' not in body and '${' not in body
def lit(a,b,n=1):
    global body
    assert body.count(a)==n,(body.count(a),a[:70]); body=body.replace(a,b)
def rx(a,b,n=None,flags=re.S):
    global body
    body,c=re.subn(a,b,body,flags=flags); assert c and (n is None or c==n),(c,a[:70])
lit('<?php foreach ($secoes as $id=>$nome): ?><a href="#<?=$id?>"><?=$nome?></a><?php endforeach; ?>','${SEC.map(([id,nome])=>`<a href="#${id}">${nome}</a>`).join("")}')
lit('<?php if($validade):?><span class="pre">Válida até </span><span class="pre-m">Até </span><strong><?=$validade?></strong><span class="cli"> para <?=$cliente?></span><?php else:?><span class="cli">Proposta para </span><strong><?=$cliente?></strong><?php endif;?>','${validade?`<span class="pre">Válida até </span><span class="pre-m">Até </span><strong>${validade}</strong><span class="cli"> para ${cliente}</span>`:`<span class="cli">Proposta para </span><strong>${cliente}</strong>`}')
lit('<?php if($validade):?><div><dt>Válida até</dt><dd><?=$validade?></dd></div><?php endif;?>','${validade?`<div><dt>Válida até</dt><dd>${validade}</dd></div>`:""}')
lit("<?=count($svs)?> <?=count($svs)===1?'serviço':'serviços'?>",'${svs.length} ${svs.length===1?"serviço":"serviços"}')
lit("<?=date('d/m/Y', strtotime($pr['data_proposta']))?>",'${dmy(pr.data_proposta)}')
lit('<?php foreach ($secoes as $id=>$nome): ?><li><a href="#<?=$id?>"><span class="n"><?=nsec($id)?></span><?=$nome?></a></li><?php endforeach; ?>','${SEC.map(([id,nome])=>`<li><a href="#${id}"><span class="n">${nsec(id)}</span>${nome}</a></li>`).join("")}')
rx(r"<\?=nsec\('(\w+)'\)\?>",r"${nsec('\1')}",8)
rx(r'<\?php foreach \(\$svs as \$idx => \$s\): \?>.*?</article>\s*<\?php endforeach; \?>',lambda m:'''${svs.map((s,idx)=>`
      <article class="scope-card">
        <div>
          <div class="n">Serviço ${String(idx+1).padStart(2,"0")}</div>
          <h3>${esc(s.nome)}</h3>
          ${s.subtitulo?`<p class="sub">${esc(s.subtitulo)}</p>`:""}
          ${s.opcional?`<p class="tag-opc">Opcional · ${money(s.valor)}${s.cobranca==="mensal"?" por mês":""}</p>`:""}
          ${s.prazo?`<p class="sub"><strong>Prazo:</strong> ${esc(s.prazo)}</p>`:""}
        </div>
        <div><div class="k">Escopo</div>
          <ul class="blist">${(s.escopo||[]).map(i=>`<li>${esc(i)}</li>`).join("")}</ul>
        </div>
        <div>${(s.entrega||[]).length?`<div class="k">Entrega</div>
          <ul class="blist">${s.entrega.map(i=>`<li>${esc(i)}</li>`).join("")}</ul>`:""}${s.nao_incluso?`<div class="k" style="margin-top:22px">Não incluso</div>
          <ul class="blist"><li>${esc(s.nao_incluso)}</li></ul>`:""}</div>
      </article>`).join("")}''',1)
rx(r'<\?php if \(\$fotoFundador\): \?>(.*?)\n\s*<\?php else: \?>.*?<\?php endif; \?>',lambda m:m.group(1),1)
rx(r"<\?=limpar\(\$DADE\['(\w+)'\]\)\?>",r"${esc(D.\1)}")
rx(r"<\?php if\(\$DADE\['instagram'\]\):\?>(.*?)<\?php endif;\?>",r'${D.instagram?`\1`:""}',1)
rx(r'<\?php if \(\$logosClientes\): \?>.*?<\?php endif; \?>',lambda m:'<div class="clients-row">'+''.join(f'<img src="assets/img/clientes/{f}.png" alt="{a}" loading="lazy">' for f,a in LOGOS)+'</div>',1)
lit('<footer class="pf"><span>dade.design · creative technology studio</span>','<footer class="pf"><span>dade.design · creative technology studio · <a href="privacidade.html" style="text-decoration:underline">Aviso de privacidade</a></span>')
lit('<h2>Quem já trabalhou com a gente</h2>','<h2 class="h2-clientes">Algumas das empresas que confiaram na dade para construir algo importante.</h2>')
lit('<?=$headline?>','${headline}')
lit('<?php if($headSub):?><div class="lbl" style="margin-top:12px;font-size:18px;color:var(--ink-200)"><?=$headSub?></div><?php endif;?>','${headSub?`<div class="lbl" style="margin-top:12px;font-size:18px;color:var(--ink-200)">${headSub}</div>`:""}')
lit("<?php foreach($svs as $s): ?><span><?=limpar($s['nome'])?></span><?php endforeach; ?>",'${svs.map(s=>`<span>${esc(s.nome)}</span>`).join("")}')
lit("<?=((int)$pr['prazo_meses']>0)?'Contrato inicial de '.(int)$pr['prazo_meses'].' meses':'Valor recorrente mensal'?>",'${pr.prazo_meses>0?"Contrato inicial de "+Number(pr.prazo_meses)+" meses":"Valor recorrente mensal"}')
rx(r'<\?=formatarMoeda\(\$(tu|tm)\)\?>',r'${money(\1)}',2)
rx(r'<\?php if \(\$(tu|tm) > 0\): \?>(.*?)<\?php endif; \?>',r'${\1>0?`\2`:""}',2)
lit("<?=limpar(condLabel($pr['condicao_pagamento']))?>",'${esc(dadeCond(pr.condicao_pagamento))}')
for a,b in (('<?=$cliente?>','${cliente}'),('<?=$wppLink?>','${wppLink}'),('<?=$svgWpp?>','${svgWpp}'),('<?=$numero?>','${numero}'),('<?=$wppFmt?>','${wppFmt}'),('<?=$wpp?>','${wpp}')):
    body=body.replace(a,b)
body=body.replace('/asset.php?f=img/','assets/img/')
lit('<a href="${wppLink}" class="btn btn-primary" target="_blank" rel="noopener">${svgWpp}Aprovar proposta</a>','<a href="${payLink}" class="btn btn-primary">${aprovada?"Ver pagamento":"Aprovar proposta"}</a>',2)
lit('<p>Se estiver tudo certo, é só aprovar pelo WhatsApp. Se quiser ajustar algo, me chama por lá também.</p>','<p>Se estiver tudo certo, é só aprovar e escolher a forma de pagamento. Se quiser ajustar algo, me chama no WhatsApp.</p>')
lit('<a href="mailto:${esc(D.email)}" class="btn btn-outline-dark">Enviar um e-mail</a>','<a href="${wppLink}" class="btn btn-outline-dark" target="_blank" rel="noopener">${svgWpp}Falar no WhatsApp</a>')
lit('${esc(dadeCond(pr.condicao_pagamento))}','${condTxt}')
lit('<p class="lede">Cada serviço abaixo mostra o que será feito e o que você recebe no final.</p>','<p class="lede">${pr.apresentacao?esc(pr.apresentacao):"Cada serviço abaixo mostra o que será feito e o que você recebe no final."}</p>')
rx(r'<div class="notes">.*?</ul></div>\s*</div>',lambda m:'<div class="notes">${(pr.condicoes||[]).map(c=>`<div class="note"><h4>${esc(c.titulo)}</h4><p>${esc(c.texto)}</p></div>`).join("")}</div>',1)
rx(r'(<div class="proc-step"><div class="st">Etapa 4</div>.*?</div>\s*</div>)',lambda m:m.group(1)+'${prazosHtml}',1)
lit('${svs.map(s=>`<span>${esc(s.nome)}</span>`).join("")}','${svs.filter(conta).map(s=>`<span>${esc(s.nome)}</span>`).join("")}')
lit('<div class="pay-card hl"><div class="pk">Condição de pagamento</div>','${opcs.length?`<div class="pay-card"><div class="pk">Opcionais, você escolhe na aprovação</div><div class="pv txt">${opcs.map(s=>esc(s.nome)+": + "+money(s.valor)+(s.cobranca==="mensal"?"/mês":"")).join("<br>")}</div></div>`:""}<div class="pay-card hl"><div class="pk">Condição de pagamento</div>')
assert '<?' not in body and '$pr' not in body and '$s[' not in body, re.findall(r'<\?[^>]{0,60}',body)[:5]
secoes=re.search(r"\$secoes = \[(.*?)\];",php,re.S).group(1)
SEC=re.findall(r"'(\w+)'\s*=>\s*'([^']+)'",secoes)
page='''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Proposta | dade.design</title>
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#171617">
<meta property="og:type" content="website">
<meta property="og:title" content="Proposta | dade.design">
<meta property="og:description" content="Proposta preparada pela dade.design, creative technology studio.">
<meta property="og:site_name" content="dade.design">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/img/app-icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>body.wait{background:#171617}
.h2-clientes{font-size:clamp(24px,3vw,38px)!important;line-height:1.2!important;max-width:22ch}
.tag-opc{display:inline-block;margin-top:12px;font-size:12px;font-weight:600;letter-spacing:.04em;color:var(--ink-900);background:var(--lime);border-radius:var(--r-full);padding:5px 12px}
.note p{font-size:15px;color:var(--ink-600);line-height:1.6}
.prazos{margin-top:48px;border:1px solid var(--hairline-light);border-radius:var(--r-lg);padding:28px 32px}
.prazos .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--ink-500);margin-bottom:10px}
.prazos .pz{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-bottom:1px solid var(--hairline-light);font-size:16px}
.prazos p{font-size:14px;color:var(--ink-500);margin-top:14px}
.clients-row{display:flex;align-items:center;flex-wrap:wrap;gap:36px 56px}
.clients-row img{height:34px;width:auto;filter:invert(1);opacity:.82}
@media (max-width:860px){.clients-row{gap:28px 36px}.clients-row img{height:26px}}</style>
</head>
<body class="wait">
<div id="root"></div>
<script src="assets/dade.js"></script>
<script>
const SB='__SB_URL__',KEY='__SB_KEY__';
const D=window.DADE,SEC=__SEC__;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=window.dadeMoney;
const dmy=d=>d?d.slice(0,10).split('-').reverse().join('/'):'';
const nsec=id=>String(SEC.findIndex(s=>s[0]===id)+1).padStart(2,'0');
const svgWpp='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>';
function aviso(titulo,texto,botao){return `<main class="expired"><div class="box"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade"><h1>${titulo}</h1><p>${texto}</p>${botao||''}</div></main>`}
function pagina(pr){
  const svs=(pr.servicos||[]).map(s=>({...(window.DADE_SERVICOS[s.servico]||{nome:s.servico,subtitulo:'Serviço sob medida',escopo:['Escopo conforme alinhado com o cliente'],entrega:['Entrega conforme alinhado com o cliente']}),...s}));
  const conta=s=>!s.opcional||s.aceito===true,opcs=pr.aprovada_em?[]:svs.filter(s=>s.opcional);
  let tm=0,tu=0;svs.filter(conta).forEach(s=>s.cobranca==='mensal'?tm+=Number(s.valor):tu+=Number(s.valor));
  const prazosHtml=svs.some(s=>s.prazo)?`<div class="prazos"><div class="k">Prazos deste projeto</div>${svs.filter(s=>s.prazo).map(s=>`<div class="pz"><span>${esc(s.nome)}</span><strong>${esc(s.prazo)}</strong></div>`).join('')}<p>Os prazos contam a partir do primeiro pagamento.</p></div>`:'';
  let headline='Sob consulta',headSub='';
  if(tu>0&&tm>0){headline=money(tu);headSub='+ '+money(tm)+'/mês'}else if(tu>0){headline=money(tu)}else if(tm>0){headline=money(tm)+' <small>/mês</small>'}
  const cliente=esc(pr.cliente_nome),wpp=D.whatsapp,wppFmt=wpp.replace(/^55(\\d{2})(\\d{4,5})(\\d{4})$/,'($1) $2-$3');
  const wppLink='https://wa.me/'+wpp+'?text='+encodeURIComponent('Olá! Estou vendo a proposta da dade.design para '+pr.cliente_nome+'.');
  const validade=dmy(pr.data_expiracao),numero=String(pr.id).padStart(4,'0');
  const aprovada=!!pr.aprovada_em,payLink='pagamento.html?slug='+encodeURIComponent(pr.slug);
  const condTxt=[tu>0?'Pix: 50% na aprovação e 50% na entrega':'',tu>0?'Cartão de crédito: valor total em até 4x':'',tm>0?'Mensalidade por Pix'+(pr.dia_cobranca?', todo dia '+Number(pr.dia_cobranca):'')+', após cada mês de trabalho':''].filter(Boolean).join('<br>');
  document.title='Proposta para '+pr.cliente_nome+' | dade.design';
  if(pr.status==='expirada'||pr.status==='perdida') return aviso('Esta proposta não está mais disponível',`A proposta preparada para <strong>${cliente}</strong>${validade?` era válida até ${validade}`:''}. Se ainda fizer sentido para vocês, é só chamar que eu preparo uma versão atualizada.`,`<a href="${wppLink}" target="_blank" rel="noopener" class="btn btn-primary">${svgWpp}Pedir nova proposta</a>`);
  return `__BODY__`;
}
function efeitos(){__SCROLL__}
(async()=>{
  const slug=new URLSearchParams(location.search).get('slug')||'',root=document.getElementById('root');
  let pr=null,falha=false;
  if(slug){try{const r=await fetch(SB+'/rest/v1/rpc/central_proposta_publica',{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify({p_slug:slug})});if(r.ok)pr=await r.json();else falha=true}catch(e){falha=true}}
  document.body.classList.remove('wait');
  if(falha){root.innerHTML=aviso('Não foi possível abrir a proposta','Confira a sua conexão e recarregue a página.');return}
  if(!pr){root.innerHTML=aviso('Proposta não encontrada','Confira o link que você recebeu ou fale com a dade.design.');return}
  root.innerHTML=pagina(pr);
  if(document.getElementById('progressBar'))efeitos();
})();
</script>
</body></html>
'''
page=page.replace('__SB_URL__',SB_URL).replace('__SB_KEY__',SB_KEY).replace('__SEC__',json.dumps(SEC,ensure_ascii=False)).replace('__SCROLL__',scroll).replace('__BODY__',body)
open('site/proposta.html','w',encoding='utf-8').write(page)
exec(open('build_pag.py',encoding='utf-8').read())
exec(open('build_prev.py',encoding='utf-8').read())
open('check_prop.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>',page,re.S)[0])
print(len(page), os.path.getsize('site/assets/img/dade/fundador.jpg'), list(cat.keys()))
