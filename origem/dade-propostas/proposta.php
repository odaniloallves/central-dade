<?php
require_once __DIR__.'/config/database.php';
require_once __DIR__.'/templates/servicos_data.php';

header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');

/* =====================================================================
   DADOS DA DADE (edite aqui)
   ===================================================================== */
$DADE = [
  'fundador'  => 'Danilo Alves',
  'cargo'     => 'Fundador e diretor criativo',
  'email'     => 'danilo@dadedesign.com.br',
  'site'      => 'dadedesign.com.br',
  'instagram' => '',            // ex: 'dadedesign' (vazio = não aparece)
];
/* Foto do fundador: coloque em assets/img/dade/fundador.jpg
   Logos de clientes: coloque os arquivos em assets/img/clientes-dade/
   (se a pasta estiver vazia, a página mostra os segmentos atendidos) */

$slug = $_GET['slug'] ?? '';
if (!$slug) { http_response_code(404); echo 'Proposta não encontrada.'; exit; }
$db = getDB(); atualizarExpiradas();
$st = $db->prepare('SELECT * FROM propostas WHERE slug=? AND deleted_at IS NULL'); $st->execute([$slug]);
$pr = $st->fetch();
if (!$pr) { http_response_code(404); echo 'Proposta não encontrada.'; exit; }

$expirada = in_array($pr['status'], ['expirada','perdida']);
$catalogo = catalogoServicos();
$svs = [];
foreach (servicosDaProposta($pr['id']) as $s) {
    $meta = $catalogo[$s['servico']] ?? ['nome'=>$s['servico'],'subtitulo'=>'Serviço sob medida','escopo'=>['Escopo conforme alinhado com o cliente'],'entrega'=>['Entrega conforme alinhado com o cliente']];
    $svs[] = array_merge($meta, $s);
}
$tm = 0; $tu = 0; foreach ($svs as $s) { if ($s['cobranca']==='mensal') $tm += (float)$s['valor']; else $tu += (float)$s['valor']; }
if ($tu > 0 && $tm > 0)  { $headline = formatarMoeda($tu); $headSub = '+ '.formatarMoeda($tm).'/mês'; }
elseif ($tu > 0)         { $headline = formatarMoeda($tu); $headSub = ''; }
elseif ($tm > 0)         { $headline = formatarMoeda($tm).' <small>/mês</small>'; $headSub = ''; }
else                     { $headline = 'Sob consulta'; $headSub = ''; }

$cliente = limpar($pr['cliente_nome']);
$wpp = WHATSAPP;
$wppFmt = preg_replace('/^55(\d{2})(\d{4,5})(\d{4})$/', '($1) $2-$3', $wpp);
$wppMsg = rawurlencode('Olá! Quero aprovar a proposta da dade.design para '.$pr['cliente_nome'].'.');
$wppLink = 'https://wa.me/'.$wpp.'?text='.$wppMsg;
$U = SITE_URL;
$svgWpp = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>';

$fotoFundador = is_file(__DIR__.'/assets/img/dade/fundador.jpg');
$logosClientes = [];
foreach (glob(__DIR__.'/assets/img/clientes-dade/*.{png,jpg,jpeg,svg,webp}', GLOB_BRACE) ?: [] as $f) {
    $logosClientes[] = ['file'=>basename($f), 'alt'=>ucwords(str_replace(['-','_'],' ',pathinfo($f, PATHINFO_FILENAME)))];
}
$validade = $pr['data_expiracao'] ? date('d/m/Y', strtotime($pr['data_expiracao'])) : null;
$numero = str_pad($pr['id'], 4, '0', STR_PAD_LEFT);

$secoes = [
  'quemsomos'   => 'Quem somos',
  'pilares'     => 'Como pensamos',
  'escopo'      => 'Escopo e entregas',
  'processo'    => 'Como trabalhamos',
  'observacoes' => 'Observações',
  'fundador'    => 'Quem conduz',
  'clientes'    => 'Clientes',
  'investimento'=> 'Investimento',
];
$num = array_flip(array_keys($secoes));
function nsec($id){ global $num; return str_pad($num[$id]+1, 2, '0', STR_PAD_LEFT); }
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Proposta para <?=$cliente?> | dade.design</title>
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#171617">
<meta property="og:type" content="website">
<meta property="og:title" content="Proposta para <?=$cliente?> | dade.design">
<meta property="og:description" content="Proposta preparada pela dade.design, creative technology studio.">
<meta property="og:image" content="<?=$U?>/asset.php?f=img/app-icon-512.png">
<meta property="og:url" content="<?=limpar(propostaUrl($pr['slug']))?>">
<meta property="og:site_name" content="dade.design">
<link rel="icon" type="image/png" href="/asset.php?f=img/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/asset.php?f=img/app-icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style><?php echo cssInline(__DIR__.'/assets/css/proposta.css', ''); ?></style>
</head>
<body>
<?php if ($expirada): ?>
<main class="expired">
  <div class="box">
    <img src="/asset.php?f=img/dade/logo-dade-colorido.png" alt="dade">
    <h1>Esta proposta não está mais disponível</h1>
    <p>A proposta preparada para <strong><?=$cliente?></strong><?php if($validade):?> era válida até <?=$validade?><?php endif;?>. Se ainda fizer sentido para vocês, é só chamar que eu preparo uma versão atualizada.</p>
    <a href="<?=$wppLink?>" target="_blank" rel="noopener" class="btn btn-primary"><?=$svgWpp?>Pedir nova proposta</a>
  </div>
</main>
<?php else: ?>

<div id="progressBar"></div>

<nav class="pnav" id="pnav">
  <img class="brand" src="/asset.php?f=img/dade/logo-dade-colorido.png" alt="dade">
  <div class="nl">
    <?php foreach ($secoes as $id=>$nome): ?><a href="#<?=$id?>"><?=$nome?></a><?php endforeach; ?>
  </div>
</nav>

<div class="bfix" id="bfix">
  <div class="vl"><?php if($validade):?><span class="pre">Válida até </span><span class="pre-m">Até </span><strong><?=$validade?></strong><span class="cli"> para <?=$cliente?></span><?php else:?><span class="cli">Proposta para </span><strong><?=$cliente?></strong><?php endif;?></div>
  <a href="<?=$wppLink?>" class="btn btn-primary" target="_blank" rel="noopener"><?=$svgWpp?>Aprovar proposta</a>
</div>

<!-- HERO -->
<header class="hero" id="hero">
  <img class="hero-mark" src="/asset.php?f=img/dade/icone-dade-branco.png" alt="">
  <div class="hero-grid">
    <div>
      <span class="pill"><span class="dot"></span>Proposta nº <?=$numero?></span>
      <div class="for">Proposta preparada para</div>
      <h1><?=$cliente?></h1>
    </div>
    <div class="hero-meta">
      <dl>
        <div><dt>Preparada por</dt><dd>dade.design</dd></div>
        <div><dt>Data</dt><dd><?=date('d/m/Y', strtotime($pr['data_proposta']))?></dd></div>
        <?php if($validade):?><div><dt>Válida até</dt><dd><?=$validade?></dd></div><?php endif;?>
        <div><dt>Serviços</dt><dd><?=count($svs)?> <?=count($svs)===1?'serviço':'serviços'?></dd></div>
      </dl>
    </div>
  </div>
</header>

<!-- SUMÁRIO -->
<section class="band band--light" id="sumario">
  <div class="container">
    <div class="section-header">
      <div class="section-number">00</div>
      <div><div class="eyebrow">Sumário</div><h2>O que você vai encontrar aqui</h2></div>
    </div>
    <ol class="summary">
      <?php foreach ($secoes as $id=>$nome): ?><li><a href="#<?=$id?>"><span class="n"><?=nsec($id)?></span><?=$nome?></a></li><?php endforeach; ?>
    </ol>
  </div>
</section>

<!-- QUEM SOMOS -->
<section class="band band--dark" id="quemsomos">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('quemsomos')?></div>
      <div><div class="eyebrow">Quem somos</div></div>
    </div>
    <div class="about">
      <h3>Design, tecnologia e estratégia <span class="muted">trabalhando juntos, do primeiro rascunho ao que vai para o ar.</span></h3>
      <div class="copy">
        <p>Olá, <strong><?=$cliente?></strong>. Obrigado pela oportunidade de apresentar esta proposta.</p>
        <p>A <strong>dade.design</strong> é um creative technology studio de São Paulo, ativo desde 2020. Criamos marcas, sites, apresentações, campanhas, protótipos e automações para empresas que querem se comunicar com mais clareza e mais presença.</p>
        <p>O nosso jeito de trabalhar junta pensamento estratégico com execução cuidadosa: cada entrega nasce de um entendimento real do seu negócio, não de um modelo pronto.</p>
      </div>
    </div>
  </div>
</section>

<!-- PILARES -->
<section class="band band--light" id="pilares">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('pilares')?></div>
      <div><div class="eyebrow">Como pensamos</div><h2>Três coisas que guiam todo projeto</h2></div>
    </div>
    <div class="pillars">
      <div class="pillar"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg></div><h4>Estratégia</h4><p>Antes de desenhar, entendemos o objetivo, o público e o que precisa mudar. É isso que define o que vale a pena fazer.</p></div>
      <div class="pillar"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z"/></svg></div><h4>Design</h4><p>Hierarquia, contraste e consistência. Um visual que funciona em qualquer tela e em qualquer ponto de contato.</p></div>
      <div class="pillar"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg></div><h4>Tecnologia</h4><p>Sites, protótipos e automações que saem do papel e funcionam de verdade, sem depender de dez fornecedores diferentes.</p></div>
    </div>
  </div>
</section>

<!-- ESCOPO -->
<section class="band band--dark" id="escopo">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('escopo')?></div>
      <div><div class="eyebrow">Escopo e entregas</div><h2>O que está incluso</h2><p class="lede">Cada serviço abaixo mostra o que será feito e o que você recebe no final.</p></div>
    </div>
    <div class="scope">
      <?php foreach ($svs as $idx => $s): ?>
      <article class="scope-card">
        <div>
          <div class="n">Serviço <?=str_pad($idx+1,2,'0',STR_PAD_LEFT)?></div>
          <h3><?=limpar($s['nome'])?></h3>
          <?php if(!empty($s['subtitulo'])):?><p class="sub"><?=limpar($s['subtitulo'])?></p><?php endif;?>
        </div>
        <div><div class="k">Escopo</div>
          <ul class="blist"><?php foreach (($s['escopo'] ?? []) as $item): ?><li><?=limpar($item)?></li><?php endforeach; ?></ul>
        </div>
        <div><?php if(!empty($s['entrega'])):?><div class="k">Entrega</div>
          <ul class="blist"><?php foreach ($s['entrega'] as $item): ?><li><?=limpar($item)?></li><?php endforeach; ?></ul>
        <?php endif;?></div>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<!-- PROCESSO -->
<section class="band band--light" id="processo">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('processo')?></div>
      <div><div class="eyebrow">Como trabalhamos</div><h2>Do briefing à entrega</h2></div>
    </div>
    <div class="proc">
      <div class="proc-step"><div class="st">Etapa 1</div><h4>Imersão</h4><p>Conversamos sobre o objetivo, o público e as referências. Tudo o que orienta o projeto sai daqui.</p></div>
      <div class="proc-step"><div class="st">Etapa 2</div><h4>Direção</h4><p>Apresentamos o caminho criativo e alinhamos antes de partir para a execução completa.</p></div>
      <div class="proc-step"><div class="st">Etapa 3</div><h4>Criação</h4><p>Desenvolvimento de todas as peças, com rodadas de ajuste combinadas no escopo.</p></div>
      <div class="proc-step"><div class="st">Etapa 4</div><h4>Entrega</h4><p>Arquivos finais organizados, publicação quando for o caso e orientação de uso.</p></div>
    </div>
  </div>
</section>

<!-- OBSERVAÇÕES -->
<section class="band band--fog" id="observacoes">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('observacoes')?></div>
      <div><div class="eyebrow">Observações</div><h2>Bom saber antes de começar</h2></div>
    </div>
    <div class="notes">
      <div class="note"><h4>Condições</h4><ul class="blist">
        <li>O projeto começa após a aprovação da proposta e o primeiro pagamento</li>
        <li>Os arquivos finais são entregues por link para download</li>
        <li>O cronograma é definido junto com você na etapa de imersão</li>
      </ul></div>
      <div class="note"><h4>Ajustes e alterações</h4><ul class="blist">
        <li>Rodadas de ajuste inclusas dentro do escopo acordado</li>
        <li>Pedidos fora do escopo são orçados à parte, sempre com aviso prévio</li>
        <li>Conteúdos como textos e fotos são enviados pelo cliente, salvo quando inclusos no escopo</li>
      </ul></div>
    </div>
  </div>
</section>

<!-- QUEM CONDUZ -->
<section class="band band--dark" id="fundador">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('fundador')?></div>
      <div><div class="eyebrow">Quem conduz o projeto</div></div>
    </div>
    <div class="founder">
      <div class="founder-photo">
        <?php if ($fotoFundador): ?><img class="photo" src="/asset.php?f=img/dade/fundador.jpg" alt="<?=limpar($DADE['fundador'])?>">
        <?php else: ?><img class="mark" src="/asset.php?f=img/dade/icone-dade-principal.png" alt=""><?php endif; ?>
      </div>
      <div class="founder-bio">
        <h3 style="margin-top:0"><?=limpar($DADE['fundador'])?></h3>
        <div class="role"><?=limpar($DADE['cargo'])?></div>
        <div class="copy">
          <p>Designer com atuação em marca, motion, ilustração e produtos digitais. Fundou a dade.design para unir criação e tecnologia no mesmo lugar e entregar projetos completos, sem ruído entre quem pensa e quem executa.</p>
          <p>Você fala direto com quem está fazendo o seu projeto, <strong>do primeiro contato até a entrega final</strong>.</p>
        </div>
        <dl class="facts">
          <div><dt>Desde</dt><dd>2020</dd></div>
          <div><dt>Base</dt><dd>São Paulo, atendendo todo o Brasil</dd></div>
          <div><dt>Atuação</dt><dd>Marca, digital e automação</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<!-- CLIENTES -->
<section class="band band--light" id="clientes">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('clientes')?></div>
      <div><div class="eyebrow">Clientes</div><h2>Quem já trabalhou com a gente</h2></div>
    </div>
    <?php if ($logosClientes): ?>
    <div class="logos">
      <?php foreach ($logosClientes as $l): ?><div class="logo-cell"><img src="/asset.php?f=img/clientes-dade/<?=rawurlencode($l['file'])?>" alt="<?=limpar($l['alt'])?>"></div><?php endforeach; ?>
    </div>
    <?php else: ?>
    <div class="segments">
      <div class="segment"><h4>Fitness e bem-estar</h4><p>Marcas, materiais e conteúdo para academias, estúdios e profissionais da área.</p></div>
      <div class="segment"><h4>Logística</h4><p>Presença digital e comunicação para plataformas e operações logísticas.</p></div>
      <div class="segment"><h4>Construção e imóveis</h4><p>Apresentações, sites e identidade para construtoras, incorporadoras e imobiliárias.</p></div>
    </div>
    <?php endif; ?>
  </div>
</section>

<!-- INVESTIMENTO -->
<section class="band band--dark" id="investimento">
  <div class="container">
    <div class="section-header">
      <div class="section-number"><?=nsec('investimento')?></div>
      <div><div class="eyebrow">Investimento</div><h2>Valores e condições</h2></div>
    </div>
    <div class="inv">
      <div class="inv-head">
        <div>
          <div class="lbl">Investimento do projeto</div>
          <div class="val" style="margin-top:14px"><?=$headline?></div>
          <?php if($headSub):?><div class="lbl" style="margin-top:12px;font-size:18px;color:var(--ink-200)"><?=$headSub?></div><?php endif;?>
        </div>
        <div class="items"><?php foreach($svs as $s): ?><span><?=limpar($s['nome'])?></span><?php endforeach; ?></div>
      </div>
      <div class="pay">
        <?php if ($tu > 0): ?>
        <div class="pay-card"><div class="pk">Valor único</div><div class="pv"><?=formatarMoeda($tu)?></div><div class="pd">Referente à criação e entrega do projeto</div></div>
        <?php endif; ?>
        <?php if ($tm > 0): ?>
        <div class="pay-card"><div class="pk">Valor mensal</div><div class="pv"><?=formatarMoeda($tm)?></div><div class="pd"><?=((int)$pr['prazo_meses']>0)?'Contrato inicial de '.(int)$pr['prazo_meses'].' meses':'Valor recorrente mensal'?></div></div>
        <?php endif; ?>
        <div class="pay-card hl"><div class="pk">Condição de pagamento</div><div class="pv txt"><?=limpar(condLabel($pr['condicao_pagamento']))?></div></div>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="band band--dark cta" style="border-top:1px solid var(--hairline-dark)">
  <div class="container">
    <h2>Vamos tirar esse projeto do papel?</h2>
    <p>Se estiver tudo certo, é só aprovar pelo WhatsApp. Se quiser ajustar algo, me chama por lá também.</p>
    <div class="actions">
      <a href="<?=$wppLink?>" class="btn btn-primary" target="_blank" rel="noopener"><?=$svgWpp?>Aprovar proposta</a>
      <a href="mailto:<?=limpar($DADE['email'])?>" class="btn btn-outline-dark">Enviar um e-mail</a>
    </div>
    <div class="contact">
      <a href="mailto:<?=limpar($DADE['email'])?>"><?=limpar($DADE['email'])?></a>
      <a href="https://wa.me/<?=$wpp?>" target="_blank" rel="noopener"><?=$wppFmt?></a>
      <a href="https://<?=limpar($DADE['site'])?>" target="_blank" rel="noopener"><?=limpar($DADE['site'])?></a>
      <?php if($DADE['instagram']):?><a href="https://instagram.com/<?=limpar($DADE['instagram'])?>" target="_blank" rel="noopener">@<?=limpar($DADE['instagram'])?></a><?php endif;?>
    </div>
  </div>
</section>

<footer class="pf"><span>dade.design · creative technology studio</span><img src="/asset.php?f=img/dade/logo-dade-branco.png" alt="dade"></footer>

<script>
(function(){
  var bar=document.getElementById('progressBar'),nav=document.getElementById('pnav'),bf=document.getElementById('bfix');
  var links=document.querySelectorAll('.nl a'),secs=document.querySelectorAll('section[id]');
  function onScroll(){
    var h=document.documentElement.scrollHeight-window.innerHeight,s=window.scrollY;
    bar.style.width=(h>0?s/h*100:0)+'%';
    nav.classList.toggle('sc',s>60); bf.classList.toggle('vis',s>window.innerHeight*.6);
    var cur=''; secs.forEach(function(sc){if(s>=sc.offsetTop-200)cur=sc.id});
    links.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+cur)});
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
})();
</script>
<?php endif; ?>
</body></html>
