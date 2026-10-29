# Dobra — contexto do projeto para o Grok

**Atualizado em 28/10/2026.** Este documento reúne a direção aprovada e a proposta técnica inicial. O projeto está na fase de especificação: o transpiler ainda não foi implementado e nenhum ganho de tokens ou desempenho foi demonstrado.

**Repositório:** [Dobra](https://github.com/pedroribeirodev/dobra).

Documentação: [especificação](https://github.com/pedroribeirodev/dobra/blob/main/SPEC.md), [núcleo semântico](https://github.com/pedroribeirodev/dobra/blob/main/CORE.md), [benchmarks](https://github.com/pedroribeirodev/dobra/blob/main/BENCHMARK.md) e [contribuições](https://github.com/pedroribeirodev/dobra/blob/main/CONTRIBUTING.md).

## Visão e decisões já tomadas

Dobra será uma linguagem geral de UI, destinada à autoria e manutenção por pessoas e agentes. A abrangência desejada é comparável à do React na plataforma web: componentes isolados, sites simples, aplicações complexas e interfaces dentro de webviews. Essa abrangência é uma direção de arquitetura, não uma afirmação sobre recursos disponíveis hoje.

O primeiro cenário de validação de webapps será CRM/ERP. A evolução para editores visuais deve permanecer possível: componentes livres, estado de domínio separado dos nós DOM e regiões externas com proprietário e descarte explícitos. M0 mantém JavaScript + DOM; M1 segue a direção de reatividade granular; M2 inclui um teste de canvas conectado a um painel HTML. WebGL/WebGPU, Workers e Wasm são opções futuras por integração, sem obrigação de adotá-las agora. Contrato em [CORE.md §0.2](CORE.md#02-direção-de-produto-e-caminho-para-editores).

Dois objetivos têm **o mesmo peso**:

1. Reduzir o custo total para LLMs criarem e modificarem interfaces, incluindo instruções, contexto, correções e falhas.
2. Produzir código eficiente no navegador, preservando comportamento, qualidade visual e acessibilidade.

O usuário decidiu desenvolver o projeto como open source e envolver a comunidade. Também definiu a sequência: **começar pelo transpiler e aumentar o nível gradualmente**. Uma primeira versão não precisa implementar um framework completo nem superar React em benchmarks.

O nome escolhido é **Dobra**, com `.dobra` como extensão definida e `dobra` como nome da CLI planejada. O usuário informou que `dobra.build` estava disponível para compra; a compra e a configuração do domínio **não foram confirmadas**. A licença escolhida é MIT.

## Problema e hipótese de diferenciação

Agentes precisam coordenar marcação, estilos, estado, efeitos e integrações. Nossa hipótese é que uma linguagem com semântica previsível, composição livre e diagnósticos precisos reduza erros e trabalho de manutenção. O compilador usaria essa estrutura para evitar trabalho desnecessário no cliente.

Não queremos um catálogo fechado de telas ou componentes. O autor precisa poder criar suas próprias abstrações. HTML, CSS e integração com JavaScript/TypeScript fazem parte da direção de longo prazo. A linguagem deve permitir adoção gradual em páginas existentes.

A sintaxe curta, sozinha, não diferencia o projeto. Uma linguagem desconhecida também custa contexto para ensinar ao modelo. O diferencial pretendido combina autoria e edição por agentes, custo do código compilado e, futuramente, contratos de comportamento com garantias específicas.

## M0: o primeiro transpiler

O contrato canônico e as decisões fixadas do M0 estão em [CORE.md §0.1](https://github.com/pedroribeirodev/dobra/blob/main/CORE.md#01-decisões-fixadas-para-o-m0). O resumo abaixo não substitui aquela seção.

Fluxo proposto:

```text
.dobra → Parser → AST → Semantic validation → JavaScript ES modules + CSS
```

A saída inicial gera operações DOM, sem dependência obrigatória de React. O stylesheet associado é preservado como **CSS global explícito**. Isolamento automático de estilos e saída HTML estática são evoluções posteriores; M0 não promete zero JavaScript.

O subconjunto inicial inclui:

- Componentes nomeados, definidos pelo autor e compostos estaticamente, inicialmente no mesmo módulo.
- Props escalares obrigatórias: `string`, `number` e `boolean`.
- Expressões restritas a literais e referências a props; não executar JavaScript arbitrário para avaliá-las.
- Composição sem ciclos: recursão direta ou indireta entre componentes produz diagnóstico com o caminho do ciclo.
- Operações conceituais `mount` e `dispose`. A montagem recebe raiz e props; o formato exato das exportações ainda será definido.
- Props capturadas e validadas na montagem, antes de anexar novos nós. M0 não possui atualização reativa de props.
- Propriedade explícita dos nós: cada montagem remove somente o que criou; `dispose` é idempotente e preserva nós anteriores e outras montagens.
- Tratamento correto de texto, atributos booleanos e propriedades dos elementos suportados; texto de props não vira HTML executável.
- Diagnósticos com código estável, mensagem, arquivo e posição. Mesma entrada, versão e configuração devem gerar os mesmos bytes.

**Ficam fora de M0:** estado reativo, handlers de eventos da linguagem, loops dinâmicos, efeitos, async gerenciado, imports gerais, SSR, hidratação e provas formais. A interação inicial usa links e controles nativos do HTML.

A aceitação exige componentes aninhados, instâncias independentes, erros previstos, build determinístico e verificação real no navegador. Conferir CSS, responsividade, foco, teclado, cliques e descarte; snapshots de código gerado não bastam.

## Evolução planejada

- **M1 — interatividade:** estado, derivações, eventos, listas com chaves, limpeza de efeitos e estilos locais.
- **M2 — ambientes e integrações:** adaptadores JS/TS, políticas assíncronas, saída estática quando possível, teste de canvas com seleção compartilhada com um painel DOM e webview real.
- **M3 — ferramentas para agentes:** comparação de sintaxes, edição estruturada e diagnósticos orientados a reparo.
- **M4 — contratos verificáveis:** propriedades delimitadas de estados e ações, com hipóteses e método de verificação declarados.

Compatibilidade deve ser publicada por motor, versão e capacidade. Testar um navegador responsivo ou iframe não comprova suporte a webview. Código externo é uma fronteira de confiança: suas propriedades não são automaticamente conhecidas pelo compilador.

## Referências e avaliação

[Bend](https://bend-lang.com/) e seu [guia](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md) inspiraram a ideia de leis verificáveis. Dobra não adotou Bend como dependência. Validação de tipos, testes, exploração de estados e provas formais oferecem garantias diferentes.

[A2UI Express](https://developers.googleblog.com/fast-reliable-a2ui/) já explora um formato intermediário compacto para geração de UI. Portanto, reduzir sintaxe não é novidade suficiente. Os resultados publicados por outro projeto não demonstram ganhos para Dobra.

[Svelte](https://svelte.dev/docs/svelte/overview) é referência para compilação de componentes. [React](https://react.dev/learn/add-react-to-an-existing-project) é referência de abrangência e adoção incremental, além de baseline de avaliação.

Compararemos tarefas equivalentes de criação e alterações sucessivas. Contaremos guia, contexto, reparos e tentativas malsucedidas, além de bytes transferidos, interação, memória e qualidade. React/TypeScript, Svelte e HTML/CSS/JS mínimo terão papéis distintos nos controles. As três fixtures futuras serão um site, uma aplicação com bastante estado e uma webview real. Ganhos em um eixo não compensam regressões relevantes no outro. Não há benchmarks executados.

## Questões abertas e pedido ao Grok

Já decididos em CORE.md §0.1: stack (TypeScript), parser, regras de espaços/texto, atributos, segurança de URLs, API de exportação e diagnósticos. Permanecem abertos: gramática formal completa, escala de compilação, empacotamento, e matriz de ambientes. Licença decidida: MIT. Os documentos `SPEC.md`, `CORE.md`, `BENCHMARK.md` e `CONTRIBUTING.md` registram a proposta detalhada.

**Pedido ao Grok:** faça uma crítica arquitetural independente. Identifique hipóteses frágeis, ambiguidades e riscos de manutenção. Proponha a menor gramática e o menor transpiler que satisfaçam M0, com exemplos válidos e inválidos e testes de comportamento. Compare alternativas de implementação, explicitando requisitos de escala antes de escolher stack. Preserve a composição livre e o escopo incremental. Separe decisões necessárias agora das futuras e indique como medir se uma linguagem nova se justifica. Não presuma recursos implementados, benchmark favorável, domínio comprado ou licença definida.
