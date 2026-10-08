# Gera os três formulários de briefing a partir do formulário de LP já aprovado.
import re, os
SRC = open('origem/briefing-lp.html', encoding='utf-8').read()
SB_URL = 'https://hgkxybswazgcpqpksvkf.supabase.co'
SB_KEY = 'sb_publishable_4-plrhdRN1mZA6uDxnDmKA_muzq8QUu'

m = re.search(r"const STEPS = \[\n(.*?)\n\];\nconst TRI", SRC, re.S)
LP_STEPS = m.group(1)
LP_STEPS = LP_STEPS[LP_STEPS.index("  { title:'A página'"):]

DADOS = """  { title:'Seus dados', intro:'Só o essencial para a proposta, o contrato e a nota fiscal.', fields:[
    { id:'empresa', label:'Nome da empresa ou marca', type:'text', req:true },
    { id:'documento', label:'CNPJ ou CPF', type:'text', req:true, ph:'00.000.000/0000-00' },
    { id:'responsavel', label:'Nome do responsável', type:'text', req:true },
    { id:'email', label:'E-mail', type:'email', req:true, ph:'voce@empresa.com.br' },
    { id:'whatsapp', label:'WhatsApp', type:'tel', req:true, ph:'(11) 90000-0000' },
  ]},"""
PROVAS = """    { id:'numeros', label:'Números e resultados', type:'repeat', itemLabel:'Número', addLabel:'Adicionar número', help:'Clientes atendidos, anos de mercado, resultados obtidos.', fields:[
      { id:'valor', label:'Número', type:'text', ph:'Ex.: mais de 2.000 clientes atendidos' },
      { id:'mede', label:'O que ele mede', type:'text' },
      { id:'fonte', label:'De onde vem esse dado', type:'text', ph:'Ex.: sistema de agendamento' },
      { id:'publicar', label:'Pode ser publicado', type:'flag' },
    ]},
    { id:'depoimentos', label:'Depoimentos', type:'repeat', itemLabel:'Depoimento', addLabel:'Adicionar depoimento', fields:[
      { id:'texto', label:'O que a pessoa disse', type:'textarea' },
      { id:'nome', label:'Nome', type:'text' },
      { id:'quem', label:'Quem é', type:'text', ph:'Profissão, empresa, cidade' },
      { id:'formato', label:'Formato', type:'select', options:['Texto','Print','Áudio','Vídeo'] },
      { id:'autorizado', label:'Tenho autorização para publicar', type:'flag' },
    ]},
    { id:'faq', label:'Perguntas que os clientes sempre fazem', type:'repeat', itemLabel:'Pergunta', addLabel:'Adicionar pergunta', fields:[
      { id:'pergunta', label:'Pergunta', type:'text' },
      { id:'resposta', label:'Sua resposta', type:'textarea' },
      { id:'prioritaria', label:'É das mais importantes', type:'flag' },
    ]},
    { id:'proibido', label:'O que o site não pode dizer ou prometer?', type:'textarea', help:'Palavras, promessas ou comparações que você não quer.' },
    { id:'restricao', label:'Sua profissão tem regras de publicidade?', type:'textarea', help:'Exemplo: OAB, CFM, CRO, CRN. Se não tiver, deixe em branco.' },
    { id:'tratamento', label:'Como o site deve tratar o leitor?', type:'select', options:['Você','Senhor / Senhora','Tanto faz'] },"""
SITE_STEPS = DADOS + """
  { title:'A empresa', intro:'O básico sobre o seu negócio.', fields:[
    { id:'ramo', label:'Ramo de atuação e tempo de mercado', type:'text', req:true },
    { id:'slogan', label:'Slogan', type:'text', help:'Se não tiver, deixe em branco.' },
    { id:'historia', label:'História do negócio', type:'textarea', req:true, help:'Como começou, onde está hoje e para onde quer ir.' },
    { id:'mvv', label:'Missão, visão e valores', type:'textarea' },
  ]},
  { title:'Serviços e equipe', intro:'O que você entrega e quem entrega.', fields:[
    { id:'servicos', label:'Produtos ou serviços', type:'repeat', req:true, start:1, itemLabel:'Serviço', addLabel:'Adicionar serviço', fields:[
      { id:'nome', label:'Nome', type:'text' },
      { id:'descricao', label:'O que é', type:'textarea' },
      { id:'para_quem', label:'Para quem é', type:'text' },
    ]},
    { id:'diferenciais', label:'Por que o cliente deveria contratar você?', type:'textarea', req:true },
    { id:'equipe', label:'Profissionais que devem aparecer no site', type:'repeat', itemLabel:'Profissional', addLabel:'Adicionar profissional', fields:[
      { id:'nome', label:'Nome', type:'text' },
      { id:'formacao', label:'Formação e especialidade', type:'text' },
      { id:'registro', label:'Registro profissional', type:'text', ph:'Ex.: CRM 000000' },
    ]},
  ]},
  { title:'Público e estratégia', intro:'Para quem é o site e o que ele precisa fazer.', fields:[
    { id:'publico', label:'Quem é o seu cliente ideal?', type:'textarea', req:true },
    { id:'dores', label:'Principais dúvidas e dores do cliente', type:'repeat', itemLabel:'Dúvida ou dor', addLabel:'Adicionar', help:'Uma por item. Marque a que mais pesa.', fields:[
      { id:'dor', label:'Dúvida ou dor', type:'textarea' },
      { id:'principal', label:'Esta é a principal', type:'flag', unique:true },
    ]},
    { id:'acao', label:'O que o visitante deve fazer no site?', type:'text', req:true, help:'Exemplo: agendar pelo WhatsApp, pedir orçamento, ligar.' },
    { id:'atendimento', label:'Como você atende?', type:'checks', options:['Presencial','Online','Em domicílio'] },
    { id:'concorrentes', label:'Principais concorrentes', type:'repeat', max:3, itemLabel:'Concorrente', addLabel:'Adicionar concorrente', fields:[
      { id:'link', label:'Site ou perfil', type:'text', ph:'https://' },
      { id:'falha', label:'O que ele não resolve', type:'text' },
    ]},
  ]},
  { title:'Contato e operação', intro:'Os dados que vão aparecer no site.', fields:[
    { id:'telefone', label:'Telefone', type:'tel' },
    { id:'whatsapp_site', label:'WhatsApp que vai no site', type:'tel' },
    { id:'email_site', label:'E-mail que vai no site', type:'text' },
    { id:'endereco', label:'Endereço', type:'text' },
    { id:'redes', label:'Redes sociais', type:'textarea', help:'Cole os links, um por linha.' },
    { id:'email_form', label:'E-mail que vai receber os formulários do site', type:'text' },
    { id:'horario', label:'Horário de atendimento', type:'text' },
  ]},
  { title:'Provas e linguagem', intro:'O que sustenta o que o site vai dizer. Só entra o que puder ser comprovado.', fields:[
""" + PROVAS + """
  ]},
  { title:'Visual', intro:'Referências para o layout.', fields:[
    { id:'logo', label:'Logo e identidade visual', type:'text', help:'Link do Drive ou do site atual. Se não tiver, escreva "não tenho".' },
    { id:'aparencia', label:'Como o site deve parecer?', type:'textarea', help:'Exemplo: moderno e escuro, claro e leve, sofisticado.' },
    { id:'cores', label:'Cores e padrões que precisam aparecer', type:'text' },
    { id:'referencias', label:'Sites que você gosta', type:'textarea', help:'Cole os links, um por linha.' },
    { id:'midia', label:'Fotos e vídeos disponíveis', type:'text', help:'Link do Drive com fotos da equipe, do espaço e dos serviços.' },
    { id:'obs', label:'Mais alguma coisa?', type:'textarea' },
  ]},"""
ID_STEPS = DADOS + """
  { title:'A marca', intro:'O que ela é e o que faz.', fields:[
    { id:'marca', label:'Nome da marca', type:'text', req:true },
    { id:'faz', label:'O que a empresa faz?', type:'textarea', req:true, help:'O setor em que atua e o que entrega para o cliente.' },
    { id:'diferenciais', label:'O que diferencia a marca das outras?', type:'textarea' },
    { id:'missao', label:'Qual é a missão da marca?', type:'textarea', help:'O que ela busca alcançar ou qual problema resolve.' },
    { id:'personalidade', label:'Se a marca fosse uma pessoa, como ela seria?', type:'checks', options:['Moderna','Sofisticada','Divertida','Acessível','Séria','Acolhedora','Ousada','Tradicional','Minimalista','Tecnológica'] },
    { id:'personalidade_obs', label:'Quer descrever com as suas palavras?', type:'textarea' },
  ]},
  { title:'Público', intro:'Quem a marca precisa conquistar.', fields:[
    { id:'publico', label:'Quem é o público da marca?', type:'textarea', req:true, help:'Idade, interesses, hábitos de consumo, classe social.' },
    { id:'motivacao', label:'O que move esse público?', type:'textarea', help:'O que ele quer, o que teme e o que valoriza.' },
  ]},
  { title:'Mensagem', intro:'O que a marca precisa dizer sem usar palavras.', fields:[
    { id:'mensagem', label:'O que a marca precisa transmitir?', type:'textarea', req:true, help:'Os valores e a sensação que a pessoa deve ter ao ver a marca.' },
    { id:'concorrentes', label:'Principais concorrentes', type:'repeat', max:3, itemLabel:'Concorrente', addLabel:'Adicionar concorrente', fields:[
      { id:'link', label:'Site ou perfil', type:'text', ph:'https://' },
      { id:'falha', label:'O que você acha da marca dele', type:'text' },
    ]},
  ]},
  { title:'Preferências visuais', intro:'Seus gostos ajudam a apontar o caminho. As decisões de cor, letra e forma ficam com a dade.', fields:[
    { id:'cores_gosta', label:'Cores que você imagina na marca', type:'text' },
    { id:'cores_evita', label:'Cores que você não quer', type:'text' },
    { id:'letra', label:'Estilo de letra que combina', type:'checks', options:['Limpa e sem serifa','Clássica com serifa','Manuscrita','Geométrica','Não sei'] },
    { id:'elementos', label:'Elementos que você imagina', type:'textarea', help:'Ilustrações, ícones, padrões, símbolos. Se não souber, deixe em branco.' },
    { id:'fotografia', label:'A marca vai usar fotos? De que tipo?', type:'textarea' },
    { id:'admira', label:'Marcas que você admira', type:'textarea', help:'De qualquer segmento. Cole os links ou os nomes.' },
  ]},
  { title:'Uso e envio', intro:'Onde a marca vai aparecer.', fields:[
    { id:'usos', label:'Onde a marca vai ser usada?', type:'checks', options:['Redes sociais','Site','Fachada','Embalagem','Uniforme','Papelaria','Veículos','Outros'] },
    { id:'logo_atual', label:'Logo atual', type:'text', help:'Link do Drive, se já existir um logo.' },
    { id:'referencias', label:'Referências visuais', type:'textarea', help:'Cole os links de imagens e logos que você gosta, um por linha.' },
    { id:'obs', label:'Mais alguma coisa?', type:'textarea' },
  ]},"""

FORMS = {
 'lp': dict(nome='Landing page', titulo='Briefing de Landing Page', h1='Vamos entender a sua <span class="accent">oferta</span>.', intro='Suas respostas viram a base da copy e do layout da página.', steps=DADOS+'\n'+LP_STEPS, og='Preencha o briefing para criarmos a sua landing page.'),
 'site': dict(nome='Site institucional', titulo='Briefing de Site Institucional', h1='Vamos entender o seu <span class="accent">negócio</span>.', intro='Suas respostas viram a base dos textos e do layout do site.', steps=SITE_STEPS, og='Preencha o briefing para criarmos o seu site.'),
 'identidade': dict(nome='Identidade visual', titulo='Briefing de Identidade Visual', h1='Vamos entender a sua <span class="accent">marca</span>.', intro='Suas respostas são o ponto de partida da identidade visual. Seja generoso nas palavras.', steps=ID_STEPS, og='Preencha o briefing para criarmos a sua identidade visual.'),
}
DOCOK = r"""function docOk(v){const d=String(v).replace(/\D/g,'');if(/^(\d)\1+$/.test(d))return false;
  const dv=(n,w)=>{const r=n.split('').reduce((a,c,i)=>a+c*w[i],0)%11;return r<2?0:11-r};
  if(d.length===11){const a=(n,l)=>{let s=0;for(let i=0;i<l;i++)s+=n[i]*(l+1-i);const r=(s*10)%11;return r===10?0:r};return a(d,9)==d[9]&&a(d,10)==d[10]}
  if(d.length===14){const w1=[5,4,3,2,9,8,7,6,5,4,3,2],w2=[6,...w1];return dv(d.slice(0,12),w1)==d[12]&&dv(d.slice(0,13),w2)==d[13]}
  return false}
"""
SEND = r"""async function send() {
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
"""
os.makedirs('site/briefing', exist_ok=True)
for k, f in FORMS.items():
    t = SRC
    def sub1(pat, rep, flags=0):
        global t
        t, n = re.subn(pat, lambda _: rep, t, count=1, flags=flags)
        assert n == 1, pat
    sub1(r"<title>.*?</title>", f"<title>Briefing · {f['nome']} · dade.design</title>")
    sub1(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{f["titulo"]} · dade.design" />')
    sub1(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{f["og"]}" />')
    sub1(r'<span class="eyebrow">Briefing · Landing page</span>', f'<span class="eyebrow">Briefing · {f["nome"]}</span>')
    sub1(r"<h1>.*?</h1>", f"<h1>{f['h1']}</h1>")
    sub1(r'<p class="intro-lede">.*?</p>', f'<p class="intro-lede">{f["intro"]} Responda com as suas palavras. O preenchimento fica salvo neste navegador, então você pode parar e voltar depois.</p><p class="priv">Seus dados ficam protegidos e são usados só para o seu projeto. <a href="../privacidade.html" target="_blank" rel="noopener">Aviso de privacidade</a></p>')
    sub1(r"\.intro-lede\{", ".priv{font-size:12px;color:var(--ink-400);margin-top:12px}.priv a{color:var(--ink-200);text-decoration:underline}\n.intro-lede{")
    sub1(r"const STORE = '[^']*';", f"const STORE = 'dade-briefing-{k}-v1';\nconst TIPO = '{k}';\nconst TIPO_NOME = '{f['nome']}';\nconst SB_URL = '{SB_URL}';\nconst SB_KEY = '{SB_KEY}';")
    sub1(r"const DOC_TITLE = '[^']*';", f"const DOC_TITLE = '{f['titulo']}';")
    sub1(r"const STEPS = \[\n.*?\n\];\nconst TRI", "const STEPS = [\n" + f['steps'] + "\n];\nconst TRI", re.S)
    sub1(r"async function send\(\) \{.*?\n\}\n(?=function done)", SEND, re.S)
    sub1(r"a\.download = `briefing-lp-\$\{slug\(\)\}\.md`;", "a.download = `briefing-${TIPO}-${slug()}.md`;")
    sub1(r"    if \(!msg && f\.id === 'numeros'", "    if (!msg && f.id === 'documento' && txt(v) && !docOk(txt(v))) msg = 'Confira o CPF ou CNPJ. O número informado não é válido.';\n    if (!msg && f.id === 'numeros'")
    sub1(r"function validate\(\) \{", DOCOK + "function validate() {")
    open(f'site/briefing/{k}.html', 'w', encoding='utf-8').write(t)
    js = re.search(r'<script>\n/\* =+ CONFIG(.*)</script>', t, re.S).group(0)[8:-9]
    open(f'check_{k}.js', 'w', encoding='utf-8').write(js)
    print(k, len(t))
