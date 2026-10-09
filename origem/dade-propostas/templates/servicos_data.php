<?php
/* =====================================================================
   dade.design | Catálogo de serviços
   Cada serviço define: nome, subtitulo, cobrança padrão, escopo e entrega.
   A chave (ex: 'identidade_visual') é o que fica salvo no banco.
   Textos provisórios: revisar e ajustar com a realidade de cada entrega.
   ===================================================================== */

function catalogoServicos() {
    return [
        'identidade_visual' => [
            'nome'      => 'Identidade Visual',
            'subtitulo' => 'Uma marca com sistema, não só um desenho',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Imersão no negócio, no público e na concorrência',
                'Conceito criativo e direção visual',
                'Criação do logo e das suas variações',
                'Paleta de cores, tipografia e elementos de apoio',
            ],
            'entrega'   => [
                'Arquivos do logo em todos os formatos de uso',
                'Manual da marca em PDF',
            ],
        ],
        'site_institucional' => [
            'nome'      => 'Site Institucional',
            'subtitulo' => 'Presença digital com cara de marca grande',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Arquitetura de conteúdo e estrutura das páginas',
                'Design de interface para desktop e celular',
                'Desenvolvimento, animações e ajustes de performance',
                'Configuração de domínio e publicação',
            ],
            'entrega'   => [
                'Site publicado e funcionando no seu domínio',
                'Orientação de uso e atualização',
            ],
        ],
        'landing_page' => [
            'nome'      => 'Landing Page',
            'subtitulo' => 'Uma página com um único objetivo: converter',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Estrutura de copy focada na oferta',
                'Design e desenvolvimento responsivo',
                'Integração com WhatsApp, formulário ou checkout',
            ],
            'entrega'   => [
                'Página publicada e pronta para receber tráfego',
            ],
        ],
        'apresentacao' => [
            'nome'      => 'Apresentação Comercial',
            'subtitulo' => 'O seu pitch com o peso visual que ele merece',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Organização do conteúdo e da narrativa',
                'Design de todos os slides no padrão da marca',
                'Gráficos, ícones e elementos visuais sob medida',
            ],
            'entrega'   => [
                'Apresentação em PDF e em arquivo editável',
            ],
        ],
        'motion' => [
            'nome'      => 'Motion Design',
            'subtitulo' => 'Movimento para explicar, vender e marcar presença',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Roteiro e storyboard',
                'Animação, trilha e acabamento',
                'Versões nos formatos de cada canal',
            ],
            'entrega'   => [
                'Vídeos finalizados em alta resolução',
            ],
        ],
        'captacao_video' => [
            'nome'      => 'Captação de Vídeo',
            'subtitulo' => 'Imagem bem feita desde a gravação',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Planejamento da gravação e roteiro de cenas',
                'Captação com equipamento profissional de vídeo e áudio',
                'Direção no set e cuidado com luz e enquadramento',
            ],
            'entrega'   => [
                'Arquivos brutos organizados e prontos para edição',
            ],
        ],
        'edicao_video' => [
            'nome'      => 'Edição de Vídeo',
            'subtitulo' => 'Ritmo, corte e acabamento que prendem a atenção',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Seleção dos melhores trechos e montagem',
                'Cortes, trilha, legendas e tratamento de cor',
                'Ajustes de áudio e elementos gráficos da marca',
            ],
            'entrega'   => [
                'Vídeos finalizados nos formatos de cada canal',
            ],
        ],
        'captacao_edicao_video' => [
            'nome'      => 'Captação e Edição de Vídeos',
            'subtitulo' => 'Da gravação ao vídeo pronto para publicar',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Planejamento da gravação e roteiro de cenas',
                'Captação com equipamento profissional de vídeo e áudio',
                'Montagem, cortes, trilha, legendas e tratamento de cor',
                'Elementos gráficos e acabamento no padrão da marca',
            ],
            'entrega'   => [
                'Vídeos finalizados nos formatos de cada canal',
            ],
        ],
        'criativos_social' => [
            'nome'      => 'Criativos para Redes Sociais',
            'subtitulo' => 'Conteúdo visual consistente, todo mês',
            'cobranca'  => 'mensal',
            'escopo'    => [
                'Planejamento visual do mês',
                'Criação de posts, carrosséis e stories',
                'Criativos para anúncios',
            ],
            'entrega'   => [
                'Peças prontas para publicar, entregues por link',
            ],
        ],
        'prototipo_app' => [
            'nome'      => 'Protótipo e Produto Digital',
            'subtitulo' => 'Da ideia a algo que dá para clicar',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Mapeamento de fluxos e funcionalidades',
                'Design de interface das telas principais',
                'Protótipo navegável para validação',
            ],
            'entrega'   => [
                'Protótipo online e arquivos de design',
            ],
        ],
        'automacao' => [
            'nome'      => 'Automação e IA',
            'subtitulo' => 'Menos trabalho repetitivo, mais tempo para o que importa',
            'cobranca'  => 'unico',
            'escopo'    => [
                'Diagnóstico dos processos que podem ser automatizados',
                'Configuração das ferramentas e integrações',
                'Testes e ajustes com o time',
            ],
            'entrega'   => [
                'Automação funcionando e documentada',
            ],
        ],
        'sustentacao' => [
            'nome'      => 'Sustentação e Evolução',
            'subtitulo' => 'O seu projeto digital sempre em dia',
            'cobranca'  => 'mensal',
            'escopo'    => [
                'Ajustes e atualizações de conteúdo',
                'Pequenas melhorias de design e performance',
                'Acompanhamento técnico',
            ],
            'entrega'   => [
                'Horas mensais dedicadas ao projeto',
            ],
        ],
    ];
}
function getServico($key) {
    $c = catalogoServicos();
    return $c[$key] ?? null;
}
function servicoNome($key) {
    $s = getServico($key);
    return $s ? $s['nome'] : $key;
}
