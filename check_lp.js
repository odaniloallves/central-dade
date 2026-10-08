
/* ============ CONFIG ============ */
const ACCESS_KEY = 'da574319-0e26-4eaf-b8b8-43e4e55143ce';
const STORE = 'dade-briefing-lp-v1';
const TIPO = 'lp';
const TIPO_NOME = 'Landing page';
const SB_URL = 'https://hgkxybswazgcpqpksvkf.supabase.co';
const SB_KEY = 'sb_publishable_4-plrhdRN1mZA6uDxnDmKA_muzq8QUu';
const DOC_TITLE = 'Briefing de Landing Page';
const LOGO_BLACK = 'data:image/png;base64,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';

/* ============ ETAPAS E CAMPOS ============
   Para mudar o formulário, edite só esta lista.
   Tipos: text, email, tel, textarea, select, cards, checks, tri, repeat */
const STEPS = [
  { title:'Seus dados', intro:'Só o essencial para a proposta, o contrato e a nota fiscal.', fields:[
    { id:'empresa', label:'Nome da empresa ou marca', type:'text', req:true },
    { id:'documento', label:'CNPJ ou CPF', type:'text', req:true, ph:'00.000.000/0000-00' },
    { id:'responsavel', label:'Nome do responsável', type:'text', req:true },
    { id:'email', label:'E-mail', type:'email', req:true, ph:'voce@empresa.com.br' },
    { id:'whatsapp', label:'WhatsApp', type:'tel', req:true, ph:'(11) 90000-0000' },
  ]},
  { title:'A página', intro:'O que a página precisa fazer.', fields:[
    { id:'tipo', label:'Que tipo de página você precisa?', type:'cards', req:true, options:[
      ['Vendas de serviço ou produto','Apresenta a oferta e leva a pessoa a comprar ou a chamar você.'],
      ['Vendas por aplicação','A pessoa se candidata e você decide quem entra. Comum em mentorias e clubes.'],
      ['Captura','Troca um material gratuito pelo contato da pessoa.'],
      ['Outro','Evento, lista de espera, pré-lançamento e afins.'],
    ]},
    { id:'acao', label:'Qual é a única ação que o visitante deve fazer?', type:'text', req:true, help:'Uma só. Exemplo: chamar no WhatsApp para agendar uma conversa.' },
    { id:'destino', label:'Para onde o botão leva?', type:'select', req:true, options:['WhatsApp','Formulário na própria página','Página de pagamento','Outro link'] },
    { id:'destino_detalhe', label:'Número ou link de destino', type:'text', ph:'(11) 90000-0000 ou https://' },
    { id:'trafego', label:'De onde as pessoas vão chegar?', type:'checks', options:['Anúncios pagos','Redes sociais','Google','Indicação','Lista de e-mail ou WhatsApp','Ainda não sei'] },
  ]},
  { title:'Público', intro:'Quem vai ler a página.', fields:[
    { id:'publico', label:'Quem é o seu cliente ideal?', type:'textarea', req:true, help:'Idade, profissão, momento de vida ou do negócio, o que ele já tentou.' },
    { id:'dores', label:'Quais problemas ele sente hoje?', type:'repeat', req:true, start:1, itemLabel:'Problema', addLabel:'Adicionar problema', help:'Um por item. Marque o que mais incomoda no dia a dia.', fields:[
      { id:'dor', label:'Problema', type:'textarea' },
      { id:'principal', label:'Este é o principal', type:'flag', unique:true },
    ]},
    { id:'decisao', label:'O que pesa na hora de ele decidir?', type:'textarea', help:'O que ele precisa ver ou ouvir para confiar. E o que faz ele desistir.' },
    { id:'nao_e', label:'Para quem essa oferta não é?', type:'textarea', help:'O tipo de cliente que você prefere não atrair.' },
  ]},
  { title:'Produto e oferta', intro:'O que você vende e como funciona.', fields:[
    { id:'def1', label:'Explique o que você vende em uma frase', type:'text', req:true },
    { id:'descricao', label:'Agora explique com mais detalhes', type:'textarea', req:true },
    { id:'entregas', label:'O que o cliente recebe?', type:'repeat', req:true, start:1, itemLabel:'Entrega', addLabel:'Adicionar entrega', help:'Um item por entrega, do jeito que você falaria para um cliente.', fields:[
      { id:'item', label:'Entrega', type:'text' },
    ]},
    { id:'nao_faz', label:'O que a oferta não inclui ou não faz?', type:'textarea', help:'Limites que precisam ficar claros para ninguém comprar esperando outra coisa.' },
    { id:'passos', label:'Como funciona, passo a passo?', type:'repeat', itemLabel:'Passo', addLabel:'Adicionar passo', help:'Do primeiro contato até a entrega. Inclua prazos, se houver.', fields:[
      { id:'titulo', label:'Nome do passo', type:'text' },
      { id:'descricao', label:'O que acontece', type:'textarea' },
    ]},
    { id:'diferenciais', label:'Por que escolher você e não outro?', type:'textarea' },
    { id:'headline', label:'Já tem uma frase de chamada em mente?', type:'text', help:'Se não tiver, deixe em branco. A gente cria.' },
    { id:'bonus', label:'Bônus', type:'tri', ph:'Descreva o bônus.' },
    { id:'valor', label:'Preço', type:'tri', ph:'Valor, formas de pagamento e condições.' },
    { id:'garantia', label:'Garantia', type:'tri', ph:'Prazo e condições da garantia.' },
  ]},
  { title:'Provas', intro:'O que sustenta o que a página vai prometer. Só entra na página o que puder ser comprovado.', fields:[
    { id:'numeros', label:'Números e resultados', type:'repeat', itemLabel:'Número', addLabel:'Adicionar número', help:'Clientes atendidos, anos de mercado, resultados obtidos.', fields:[
      { id:'valor', label:'Número', type:'text', ph:'Ex.: mais de 800 atendimentos' },
      { id:'mede', label:'O que ele mede', type:'text', ph:'Ex.: atendimentos em 8 meses, em um cliente' },
      { id:'fonte', label:'De onde vem esse dado', type:'text', ph:'Ex.: relatório do sistema' },
      { id:'publicar', label:'Pode ser publicado', type:'flag' },
    ]},
    { id:'historia', label:'Sua história e experiência', type:'textarea', help:'Como começou, formação, registros profissionais, empresas e clientes relevantes.' },
    { id:'depoimentos', label:'Depoimentos', type:'repeat', itemLabel:'Depoimento', addLabel:'Adicionar depoimento', fields:[
      { id:'texto', label:'O que a pessoa disse', type:'textarea' },
      { id:'nome', label:'Nome', type:'text' },
      { id:'quem', label:'Quem é', type:'text', ph:'Profissão, empresa, cidade' },
      { id:'formato', label:'Formato', type:'select', options:['Texto','Print','Áudio','Vídeo'] },
      { id:'autorizado', label:'Tenho autorização para publicar', type:'flag' },
    ]},
  ]},
  { title:'Objeções e linguagem', intro:'As dúvidas do cliente e o jeito certo de falar com ele.', fields:[
    { id:'faq', label:'Perguntas que os clientes sempre fazem', type:'repeat', itemLabel:'Pergunta', addLabel:'Adicionar pergunta', help:'Marque as que mais travam a venda.', fields:[
      { id:'pergunta', label:'Pergunta', type:'text' },
      { id:'resposta', label:'Sua resposta', type:'textarea' },
      { id:'prioritaria', label:'É das mais importantes', type:'flag' },
    ]},
    { id:'proibido', label:'O que a página não pode dizer ou prometer?', type:'textarea', help:'Palavras, promessas ou comparações que você não quer.' },
    { id:'restricao', label:'Sua profissão tem regras de publicidade?', type:'textarea', help:'Exemplo: OAB, CFM, CRO, CRN. Se não tiver, deixe em branco.' },
    { id:'tratamento', label:'Como a página deve tratar o leitor?', type:'select', options:['Você','Senhor / Senhora','Tanto faz'] },
    { id:'concorrentes', label:'Principais concorrentes', type:'repeat', max:3, itemLabel:'Concorrente', addLabel:'Adicionar concorrente', fields:[
      { id:'link', label:'Site ou perfil', type:'text', ph:'https://' },
      { id:'falha', label:'O que ele não resolve', type:'text' },
    ]},
  ]},
  { title:'Visual', intro:'Referências para o layout.', fields:[
    { id:'logo', label:'Logo e identidade visual', type:'text', help:'Link do Drive ou do site. Se não tiver, escreva "não tenho".' },
    { id:'aparencia', label:'Como a página deve parecer?', type:'textarea', help:'Exemplo: moderna e escura, clara e leve, sofisticada.' },
    { id:'cores', label:'Cores e padrões que precisam aparecer', type:'text' },
    { id:'referencias', label:'Páginas que você gosta', type:'textarea', help:'Cole os links, um por linha.' },
    { id:'midia', label:'Fotos e vídeos disponíveis', type:'text', help:'Link do Drive com fotos, vídeos e prints de depoimentos.' },
    { id:'obs', label:'Mais alguma coisa?', type:'textarea' },
  ]},
];
const TRI = ['Não tem','Tem, mas não mostrar na página','Tem e mostrar na página'];

/* ============ ESTADO ============ */
let data = {};
try { data = JSON.parse(localStorage.getItem(STORE) || '{}') || {}; } catch(e) { data = {}; }
let step = Math.min(Math.max(parseInt(data.__step, 10) || 0, 0), STEPS.length - 1);
let finished = false;

STEPS.forEach(s => s.fields.forEach(f => {
  if (f.type === 'repeat' && !Array.isArray(data[f.id])) data[f.id] = Array.from({length: f.start || 0}, () => ({}));
  if (f.type === 'checks' && !Array.isArray(data[f.id])) data[f.id] = [];
  if (f.type === 'tri' && (typeof data[f.id] !== 'object' || !data[f.id])) data[f.id] = {estado:'', texto:''};
}));

const $ = id => document.getElementById(id);
const form = $('form');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const txt = v => String(v ?? '').trim();
const findField = id => { for (const s of STEPS) for (const f of s.fields) if (f.id === id) return f; };
const filled = (f, it) => f.fields.some(s => s.type !== 'flag' && txt(it[s.id]));

let saveTimer;
function save() {
  data.__step = step;
  try { localStorage.setItem(STORE, JSON.stringify(data)); $('saved').textContent = 'Rascunho salvo neste navegador.'; }
  catch(e) { $('saved').textContent = ''; }
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => { $('saved').textContent = ''; }, 2500);
}

/* ============ RENDER ============ */
function control(f) {
  const v = data[f.id];
  const ph = f.ph ? ` placeholder="${esc(f.ph)}"` : '';
  const lab = ` aria-label="${esc(f.label)}"`;
  switch (f.type) {
    case 'textarea': return `<textarea class="input" data-id="${f.id}"${ph}${lab}>${esc(v)}</textarea>`;
    case 'select': return `<select class="input" data-id="${f.id}"${lab}><option value="">Selecione</option>${f.options.map(o => `<option${v === o ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select>`;
    case 'cards': return `<div class="cards" role="radiogroup"${lab}>${f.options.map(([t, d]) => `<button type="button" class="opt${v === t ? ' on' : ''}" role="radio" aria-checked="${v === t}" data-act="card" data-id="${f.id}" data-val="${esc(t)}"><strong>${esc(t)}</strong><span>${esc(d)}</span></button>`).join('')}</div>`;
    case 'checks': return `<div class="pills">${f.options.map(o => `<button type="button" class="pill${v.includes(o) ? ' on' : ''}" aria-pressed="${v.includes(o)}" data-act="check" data-id="${f.id}" data-val="${esc(o)}">${esc(o)}</button>`).join('')}</div>`;
    case 'tri': return `<div class="pills">${TRI.map(o => `<button type="button" class="pill${v.estado === o ? ' on' : ''}" aria-pressed="${v.estado === o}" data-act="tri" data-id="${f.id}" data-val="${esc(o)}">${esc(o)}</button>`).join('')}</div>` +
      (v.estado && v.estado !== TRI[0] ? `<textarea class="input tri-text" data-tri="${f.id}"${ph} aria-label="${esc(f.label)}: detalhes">${esc(v.texto)}</textarea>` : '');
    case 'repeat': {
      const items = v.map((it, i) => `<div class="item"><div class="item-head"><span>${esc(f.itemLabel)} ${i + 1}</span>${v.length > (f.req ? 1 : 0) ? `<button type="button" class="rm" data-act="rm" data-id="${f.id}" data-i="${i}">Remover</button>` : ''}</div>${f.fields.map(s => sub(f, s, it, i)).join('')}</div>`).join('');
      const canAdd = !f.max || v.length < f.max;
      return `<div class="items">${items}</div>${canAdd ? `<button type="button" class="btn btn-soft btn-sm" data-act="add" data-id="${f.id}">+ ${esc(f.addLabel)}</button>` : ''}`;
    }
    default: return `<input class="input" type="${f.type}" data-id="${f.id}" value="${esc(v)}"${ph}${lab} />`;
  }
}
function sub(f, s, it, i) {
  const a = `data-id="${f.id}" data-i="${i}" data-sub="${s.id}"`;
  const ph = s.ph ? ` placeholder="${esc(s.ph)}"` : '';
  const v = it[s.id];
  if (s.type === 'flag') return `<div class="sub"><label class="flag"><input type="checkbox" ${a}${v ? ' checked' : ''} />${esc(s.label)}</label></div>`;
  const single = f.fields.filter(x => x.type !== 'flag').length === 1;
  const lab = single ? '' : `<label class="sl">${esc(s.label)}</label>`;
  const al = ` aria-label="${esc(s.label)} ${i + 1}"`;
  if (s.type === 'textarea') return `<div class="sub">${lab}<textarea class="input" ${a}${ph}${al}>${esc(v)}</textarea></div>`;
  if (s.type === 'select') return `<div class="sub">${lab}<select class="input" ${a}${al}><option value="">Selecione</option>${s.options.map(o => `<option${v === o ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select></div>`;
  return `<div class="sub">${lab}<input class="input" type="text" ${a} value="${esc(v)}"${ph}${al} /></div>`;
}
function render() {
  if (finished) return;
  const s = STEPS[step];
  form.className = 'card';
  form.innerHTML = `<span class="eyebrow">Etapa ${String(step + 1).padStart(2, '0')}</span><h2>${esc(s.title)}</h2><p class="lede">${esc(s.intro)}</p>` +
    s.fields.map(f => `<div class="field" data-f="${f.id}"><span class="lbl">${esc(f.label)}${f.req ? ' <i>*</i>' : '<em>opcional</em>'}</span>${f.help ? `<p class="help">${esc(f.help)}</p>` : ''}${control(f)}<p class="err" role="alert"></p></div>`).join('');
  $('progress-step').textContent = `Etapa ${step + 1} de ${STEPS.length}`;
  $('progress-name').textContent = s.title;
  $('progress-bar').style.width = ((step + 1) / STEPS.length * 100) + '%';
  $('back').style.visibility = step === 0 ? 'hidden' : 'visible';
  $('next').textContent = step === STEPS.length - 1 ? 'Enviar briefing' : 'Próximo';
  $('progress').style.display = $('nav').style.display = '';
}

/* ============ EVENTOS ============ */
form.addEventListener('input', e => {
  const t = e.target;
  if (t.dataset.tri) { data[t.dataset.tri].texto = t.value; save(); return; }
  const id = t.dataset.id;
  if (!id) return;
  if (t.dataset.sub) {
    const f = findField(id), it = data[id][+t.dataset.i], s = f.fields.find(x => x.id === t.dataset.sub);
    if (t.type === 'checkbox') {
      it[s.id] = t.checked;
      if (t.checked && s.unique) { data[id].forEach(o => { if (o !== it) o[s.id] = false; }); save(); render(); return; }
    } else it[s.id] = t.value;
  } else data[id] = t.value;
  t.closest('.field')?.classList.remove('invalid');
  save();
});
form.addEventListener('click', e => {
  const b = e.target.closest('[data-act]');
  if (!b) return;
  const { act, id, val } = b.dataset;
  if (act === 'add') data[id].push({});
  if (act === 'rm') data[id].splice(+b.dataset.i, 1);
  if (act === 'card') data[id] = val;
  if (act === 'check') data[id] = data[id].includes(val) ? data[id].filter(x => x !== val) : [...data[id], val];
  if (act === 'tri') data[id].estado = val;
  save(); render();
  if (act === 'add') { const items = form.querySelectorAll(`[data-f="${id}"] .item`); items[items.length - 1]?.querySelector('.input')?.focus(); }
});
form.addEventListener('submit', e => e.preventDefault());

function docOk(v){const d=String(v).replace(/\D/g,'');if(/^(\d)\1+$/.test(d))return false;
  const dv=(n,w)=>{const r=n.split('').reduce((a,c,i)=>a+c*w[i],0)%11;return r<2?0:11-r};
  if(d.length===11){const a=(n,l)=>{let s=0;for(let i=0;i<l;i++)s+=n[i]*(l+1-i);const r=(s*10)%11;return r===10?0:r};return a(d,9)==d[9]&&a(d,10)==d[10]}
  if(d.length===14){const w1=[5,4,3,2,9,8,7,6,5,4,3,2],w2=[6,...w1];return dv(d.slice(0,12),w1)==d[12]&&dv(d.slice(0,13),w2)==d[13]}
  return false}
function validate() {
  const errors = [];
  STEPS[step].fields.forEach(f => {
    const v = data[f.id]; let msg = '';
    if (f.req) {
      if (f.type === 'repeat') { if (!v.some(it => filled(f, it))) msg = 'Adicione pelo menos um item.'; }
      else if (f.type === 'cards') { if (!v) msg = 'Escolha uma opção.'; }
      else if (!txt(v)) msg = 'Preencha este campo para continuar.';
    }
    if (!msg && f.type === 'email' && txt(v) && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(txt(v))) msg = 'Confira o e-mail. Exemplo: voce@empresa.com.br';
    if (!msg && f.id === 'documento' && txt(v) && !docOk(txt(v))) msg = 'Confira o CPF ou CNPJ. O número informado não é válido.';
    if (!msg && f.id === 'numeros' && v.some(it => txt(it.valor) && !txt(it.fonte))) msg = 'Informe de onde vem cada número. Sem fonte, ele não entra na página.';
    if (!msg && f.id === 'depoimentos' && v.some(it => txt(it.texto) && !txt(it.nome))) msg = 'Informe o nome de quem deu cada depoimento.';
    if (msg) errors.push([f.id, msg]);
  });
  form.querySelectorAll('.field').forEach(el => el.classList.remove('invalid'));
  errors.forEach(([id, msg]) => { const el = form.querySelector(`[data-f="${id}"]`); el.classList.add('invalid'); el.querySelector('.err').textContent = msg; });
  if (errors.length) { const first = form.querySelector('.field.invalid'); first.scrollIntoView({behavior:'smooth', block:'center'}); first.querySelector('.input, .opt, .btn')?.focus({preventScroll:true}); }
  return !errors.length;
}
function goTop() { $('progress').scrollIntoView({behavior:'smooth', block:'start'}); }
$('back').addEventListener('click', () => { if (step > 0) { step--; save(); render(); goTop(); } });
$('next').addEventListener('click', () => {
  if (!validate()) return;
  if (step < STEPS.length - 1) { step++; save(); render(); goTop(); }
  else send();
});

/* ============ SAÍDA (e-mail, arquivo e PDF usam a mesma estrutura) ============ */
function collect() {
  return STEPS.map((s, n) => ({ title: `${n + 1}. ${s.title}`, rows: s.fields.map(f => {
    const v = data[f.id], row = { label: f.label };
    if (f.type === 'repeat') {
      row.items = v.filter(it => filled(f, it)).map(it => {
        const subs = f.fields.filter(x => x.type !== 'flag');
        return { head: txt(it[subs[0].id]) || '(sem texto)',
          subs: [...subs.slice(1).filter(x => txt(it[x.id])).map(x => [x.label, txt(it[x.id])]),
                 ...f.fields.filter(x => x.type === 'flag').map(x => [x.label, it[x.id] ? 'sim' : 'não'])] };
      });
    } else if (f.type === 'checks') row.text = v.join(', ');
    else if (f.type === 'tri') row.text = v.estado ? (v.estado + (v.estado !== TRI[0] && txt(v.texto) ? '\n' + txt(v.texto) : '')) : '';
    else row.text = txt(v);
    return row;
  })}));
}
const today = () => new Date().toLocaleDateString('pt-BR');
function toMarkdown() {
  let md = `# ${DOC_TITLE} — ${txt(data.empresa)}\n\nData: ${today()}\n`;
  collect().forEach(sec => {
    md += `\n## ${sec.title}\n\n`;
    sec.rows.forEach(r => {
      if (r.items) {
        md += `**${r.label}**\n\n`;
        if (!r.items.length) md += `(não informado)\n\n`;
        r.items.forEach((it, i) => { md += `${i + 1}. ${it.head.replace(/\n+/g, ' ')}\n`; it.subs.forEach(([l, val]) => { md += `   - ${l}: ${val.replace(/\n+/g, ' ')}\n`; }); });
        if (r.items.length) md += '\n';
      } else md += `**${r.label}**\n\n${r.text || '(não informado)'}\n\n`;
    });
  });
  return md;
}
function toPrint() {
  $('print').innerHTML = `<div class="p-head"><img src="${LOGO_BLACK}" alt="dade" /><div>${esc(txt(data.empresa))}<br>${today()}</div></div><h1>${DOC_TITLE}</h1>` +
    collect().map(sec => `<h2>${esc(sec.title)}</h2>` + sec.rows.map(r => `<div class="row"><b>${esc(r.label)}</b>` +
      (r.items ? (r.items.length ? `<ol>${r.items.map(it => `<li>${esc(it.head)}${it.subs.map(([l, val]) => `<small>${esc(l)}: ${esc(val)}</small>`).join('')}</li>`).join('')}</ol>` : '<p>Não informado</p>')
               : `<p>${esc(r.text) || 'Não informado'}</p>`) + '</div>').join('')).join('');
}
const slug = () => (txt(data.empresa) || 'cliente').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
function download() {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([toMarkdown()], {type:'text/markdown;charset=utf-8'}));
  a.download = `briefing-${TIPO}-${slug()}.md`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

/* ============ ENVIO ============ */
async function send() {
  const btn = $('next');
  btn.disabled = true; btn.textContent = 'Enviando…';
  if ($('botcheck').checked) { btn.disabled = false; return done(true); }
  let saved = false, mailed = false;
  try {
    const res = await fetch(SB_URL + '/rest/v1/central_briefings', {
      method:'POST', headers:{'Content-Type':'application/json', 'apikey':SB_KEY, 'Prefer':'return=minimal'},
      body: JSON.stringify({ tipo: TIPO, empresa: txt(data.empresa).slice(0,200), responsavel: txt(data.responsavel), email: txt(data.email), whatsapp: txt(data.whatsapp), documento: txt(data.documento).replace(/\D/g, ''), respostas: { etapas: collect() } }),
    });
    saved = res.ok;
  } catch(e) { saved = false; }
  try {
    const res = await fetch('https://api.web3forms.com/submit', {
      method:'POST', headers:{'Content-Type':'application/json', 'Accept':'application/json'},
      body: JSON.stringify({
        access_key: ACCESS_KEY,
        subject: `Briefing ${TIPO_NOME} — ${txt(data.empresa)}` + (saved ? '' : ' (não gravou na central)'),
        from_name: 'Briefing dade',
        name: txt(data.responsavel), email: txt(data.email), whatsapp: txt(data.whatsapp),
        message: toMarkdown(),
      }),
    });
    mailed = (await res.json()).success === true;
  } catch(e) { mailed = false; }
  btn.disabled = false;
  done(saved || mailed);
}
function done(ok) {
  finished = true;
  $('progress').style.display = $('nav').style.display = 'none';
  form.className = 'card done';
  form.innerHTML = ok
    ? `<span class="eyebrow">Recebido</span><h2>Briefing enviado.</h2><p>Suas respostas chegaram para a dade. Entramos em contato pelo WhatsApp que você informou. Se quiser guardar uma cópia, salve o PDF.</p>`
    : `<span class="eyebrow">Envio não concluído</span><h2>Não conseguimos enviar agora.</h2><p>Suas respostas continuam salvas neste navegador. Tente enviar de novo. Se o erro continuar, baixe o arquivo e mande para a dade pelo WhatsApp.</p>`;
  form.innerHTML += `<div class="done-actions">${ok ? '' : '<button type="button" class="btn btn-dark" id="retry">Tentar de novo</button>'}<button type="button" class="btn ${ok ? 'btn-dark' : 'btn-soft'}" id="pdf">Salvar em PDF</button><button type="button" class="btn btn-soft" id="file">Baixar arquivo</button><button type="button" class="btn btn-soft" id="review">Revisar respostas</button></div>`;
  $('pdf').onclick = () => { toPrint(); window.print(); };
  $('file').onclick = download;
  $('review').onclick = () => { finished = false; step = 0; render(); goTop(); };
  if (!ok) $('retry').onclick = () => { finished = false; step = STEPS.length - 1; render(); send(); };
  goTop();
}

render();
