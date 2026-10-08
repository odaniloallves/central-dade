priv = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Aviso de privacidade | dade.design</title>
<meta name="theme-color" content="#171617">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/proposta.css">
<style>__PAG_CSS__
.txt h2{font-size:18px;font-weight:700;margin:34px 0 10px;color:var(--white)}
.txt p,.txt li{font-size:15px;color:var(--ink-300);line-height:1.65}
.txt p+p{margin-top:10px}
.txt ul{list-style:none;display:flex;flex-direction:column;gap:8px;margin-top:6px}
.txt li{display:flex;gap:12px}
.txt li::before{content:"";flex:none;width:5px;height:5px;border-radius:50%;background:var(--lime);margin-top:10px}
.txt strong{color:var(--white);font-weight:600}
.txt a{color:var(--white);text-decoration:underline}
</style>
</head>
<body>
<main class="pg">
  <div class="pg-top"><img src="assets/img/dade/logo-dade-colorido.png" alt="dade"></div>
  <span class="eyebrow">dade.design</span>
  <h1>Aviso de privacidade</h1>
  <p class="lede">Como a dade.design cuida dos dados que você informa nos formulários, propostas e prévias. Atualizado em outubro de 2026.</p>
  <div class="txt">
    <h2>Quem cuida dos seus dados</h2>
    <p><strong>dade.design</strong>, CNPJ 52.409.459/0001-47, responsável pelo tratamento dos dados descritos aqui. Para qualquer assunto sobre os seus dados, fale com <strong>Danilo Alves</strong> pelo e-mail <a href="mailto:danilo@dadedesign.com.br">danilo@dadedesign.com.br</a> ou pelo WhatsApp <a href="https://wa.me/5511947504840" target="_blank" rel="noopener">(11) 94750-4840</a>.</p>

    <h2>Quais dados coletamos</h2>
    <ul>
      <li>Dados de identificação e contato: nome da empresa, nome do responsável, CPF ou CNPJ, e-mail e WhatsApp.</li>
      <li>As respostas que você dá nos formulários de briefing.</li>
      <li>O registro da aprovação de uma proposta: nome, CPF ou CNPJ, data e hora, itens escolhidos e as condições aceitas.</li>
      <li>As respostas e os comentários que você envia em uma prévia de projeto.</li>
    </ul>

    <h2>Para que usamos</h2>
    <ul>
      <li>Preparar a proposta e executar o projeto contratado.</li>
      <li>Emitir nota fiscal e, quando houver, o contrato.</li>
      <li>Falar com você sobre o andamento do projeto e os pagamentos.</li>
    </ul>
    <p>Não vendemos os seus dados e não os usamos para publicidade de terceiros.</p>

    <h2>Base legal</h2>
    <p>Tratamos os dados com base na Lei Geral de Proteção de Dados (Lei 13.709/2018), para a execução do contrato e dos passos que vêm antes dele, para o cumprimento de obrigações legais, como as fiscais, e para guardar o registro da aprovação da proposta.</p>

    <h2>Com quem os dados são compartilhados</h2>
    <p>Só com os fornecedores necessários para o serviço funcionar:</p>
    <ul>
      <li><strong>Supabase</strong>, que armazena os dados em servidores em São Paulo.</li>
      <li><strong>Web3Forms</strong>, que envia à dade o aviso por e-mail quando você preenche um formulário ou aprova uma proposta.</li>
      <li><strong>InfinitePay</strong>, só se você escolher pagar com cartão de crédito. Os dados do cartão são informados direto a eles e a dade não tem acesso.</li>
      <li><strong>Google Fonts</strong>, que fornece a fonte destas páginas e recebe o endereço de acesso do seu navegador.</li>
    </ul>

    <h2>Como protegemos</h2>
    <ul>
      <li>Toda a comunicação é feita por conexão criptografada (HTTPS).</li>
      <li>Só o responsável pela dade acessa os dados, com login e senha.</li>
      <li>O banco de dados tem regras que impedem a leitura por qualquer outra pessoa. Quem preenche um formulário consegue enviar, mas não consegue ler nada que já está guardado.</li>
      <li>Os links de proposta e de prévia têm um código único, difícil de adivinhar, e mostram só o que é daquele projeto.</li>
    </ul>

    <h2>Por quanto tempo guardamos</h2>
    <p>Pelo tempo do projeto e, depois dele, pelo prazo que a lei exige para documentos fiscais e contratuais. Fora isso, os dados podem ser apagados a qualquer momento a seu pedido.</p>

    <h2>Os seus direitos</h2>
    <p>Você pode pedir para confirmar se tratamos os seus dados, ter acesso a eles, corrigir o que estiver errado, pedir a exclusão do que não for obrigatório guardar e saber com quem eles foram compartilhados. É só falar com a dade pelo e-mail ou WhatsApp acima. Respondemos em até 15 dias.</p>
  </div>
</main>
</body></html>
'''.replace('__PAG_CSS__', PAG_CSS)
open('site/privacidade.html', 'w', encoding='utf-8').write(priv)
