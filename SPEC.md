# Dobra — especificação inicial

**Data:** 28/10/2026 · **Versão:** 0.1 · **Status:** proposta técnica; implementação ainda não iniciada.

## 1. Direção acordada

Criar uma linguagem de UI de propósito geral, destinada à autoria e manutenção por pessoas e agentes. A abrangência pretendida inclui componentes isolados, sites simples, aplicações complexas e interfaces em webviews. Eficiência para LLMs e desempenho no navegador têm o mesmo peso.

A direção é desenvolver o projeto como open source e envolver a comunidade. A primeira entrega será um transpiler pequeno e executável; os recursos da linguagem e as garantias crescerão por etapas. O nome definido é **Dobra**, a extensão de arquivo é `.dobra` e a CLI planejada é `dobra`. O repositório deste projeto é `pedroribeirodev/dobra`. A licença ainda será escolhida. O domínio pretendido é `dobra.build`; sua disponibilidade foi informada pelo fundador, mas a compra ainda não foi confirmada. Nenhum transpiler foi implementado e nenhum ganho foi medido.

Documentos complementares:

- [CORE.md](CORE.md): contrato do primeiro transpiler e direção semântica dos recursos futuros.
- [BENCHMARK.md](BENCHMARK.md): avaliação de correção, tokens, manutenção e desempenho.
- [DIAGNOSTICS.md](DIAGNOSTICS.md): registro dos códigos de diagnóstico.
- [CONTRIBUTING.md](CONTRIBUTING.md): proposta de contribuição, primeiras tarefas e convite em rascunho.

## 2. Problema e hipótese

Agentes precisam coordenar estrutura, estilo, estado e efeitos ao criar ou modificar interfaces. Uma descrição mais previsível, acompanhada de diagnósticos úteis, pode reduzir correções e custo total de autoria. Um compilador pode usar essa estrutura para reduzir trabalho desnecessário no cliente.

Estas são hipóteses a avaliar. Ainda não há dados próprios demonstrando economia de tokens, menos erros ou vantagem de runtime. A sintaxe curta, isoladamente, não comprova nenhuma delas.

O projeto preserva composição livre: componentes são definidos pelo autor; um catálogo visual não limita o que a linguagem pode representar. HTML/CSS e integração com código externo são parte da direção de longo prazo. Compatibilidade é declarada por ambiente e versão, não presumida para todas as webviews.

## 3. Objetivos e critérios de sucesso

| Objetivo | Evidência necessária |
| --- | --- |
| Ter um transpiler funcional | Todos os critérios de M0 abaixo passam; exemplo aberto e inspecionado no navegador. |
| Reduzir custo para agentes | Menor custo total em tarefas equivalentes de criação e manutenção, contando guia, contexto, reparos e falhas. |
| Reduzir custo no cliente | Melhora demonstrada em métricas previamente escolhidas, mantendo funcionalidade e qualidade equivalentes. |
| Sustentar a abrangência pretendida | Fixtures de site, aplicação com estado e webview real executadas nos ambientes publicados. |
| Permitir contribuição independente | Uma pessoa consegue reproduzir exemplos e verificações com instruções e versões documentadas. |

Os dois eixos de eficiência serão avaliados separadamente. Uma regressão relevante no navegador não será compensada por economia de tokens. Limiares experimentais e método de decisão constam em BENCHMARK.md; não são resultados nem promessas comerciais.

## 4. M0 — transpiler mínimo

**Resultado esperado:** um arquivo de componentes vira um módulo JavaScript executável no navegador; um stylesheet associado é emitido sem reescrita. O compilador gera operações DOM, sem depender obrigatoriamente de React ou de um renderer de outro framework.

Fluxo proposto:

```text
Source → Parser → AST → Semantic validation → DOM code generation
                         ↓                         ↓
                    Diagnostics              JS module + CSS
```

### Entrada e saída

As decisões fixadas de gramática, atributos, segurança, API e diagnósticos estão em [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0), que é a fonte canônica do contrato M0.

- Extensão definida: `.dobra`. A sintaxe pública permanece experimental.
- Um módulo contém componentes nomeados, composição estática e props escalares obrigatórias: `string`, `number` e `boolean`.
- Expressões aceitas inicialmente: literais e referências a props. Chamadas, atribuições e JavaScript arbitrário ficam fora desse subconjunto e produzem diagnóstico.
- A primeira gramática deve ser familiar, baseada em marcação semelhante a HTML, e publicada como experimental. O corpus de conformidade acompanha sua evolução.
- Componentes compostos no M0 podem estar no mesmo módulo. Resolução de pacotes e imports gerais pertencem às expansões.
- A composição estática deve formar um grafo sem ciclos. Referência recursiva direta ou indireta entre componentes é erro de compilação, com o caminho do ciclo no diagnóstico.
- CSS associado é global e explícito no M0. O compilador o preserva; não anuncia isolamento automático antes de implementar e verificar essa transformação.
- Cada componente exporta uma operação de montagem que recebe raiz e props e devolve `dispose`. O nome exato das exportações será fixado com a gramática e a API do primeiro pacote.
- Props são capturadas na montagem. Não há API de atualização reativa no M0.
- Diagnósticos têm código estável, severidade, mensagem, arquivo e intervalo de origem. A CLI deve distinguir compilação bem-sucedida de erro; erro não pode deixar uma nova saída parcial apresentada como válida.

Exemplo de autoria **ilustrativo, ainda não executável**:

```text
component Greeting(name: string) {
  <section class="greeting">
    <h1>Olá, {name}</h1>
    <a href="#details">Saiba mais</a>
  </section>
}
```

### Histórias e requisitos P0

| ID | Necessidade | Aceitação observável |
| --- | --- | --- |
| R01 | Como autor, compor componentes próprios | Dois componentes aninhados e duas instâncias do mesmo componente exibem as props correspondentes. |
| R02 | Como integrador, montar em página existente | Nós anteriores na raiz permanecem intactos; cada montagem possui somente os nós que criou. |
| R03 | Como integrador, descartar uma montagem | `dispose` remove seus nós; chamadas repetidas não falham nem removem outras montagens. |
| R04 | Como autor, preservar semântica HTML | Texto é texto; atributos booleanos falsos são ausentes; valores de inputs e atributos suportados refletem as props. |
| R05 | Como agente, localizar um erro | Sintaxe inválida, componente desconhecido, prop obrigatória ausente, referência inexistente e ciclo de composição recebem posição e código úteis. |
| R06 | Como mantenedor, reproduzir o build | Mesma fonte, CSS, versão e configuração produzem os mesmos bytes, sem timestamps ou IDs aleatórios. |
| R07 | Como usuário, navegar e interagir | Links e controles HTML nativos funcionam com mouse e teclado; não há overlay bloqueando cliques no exemplo. |
| R08 | Como contribuidor, verificar a tradução | Corpus público cobre casos aceitos e rejeitados; comportamento do DOM é verificado além de snapshots do código gerado. |

Critérios adicionais de conclusão:

- [ ] Tabela documentada de elementos, atributos, expressões e tipos suportados; recursos fora do subconjunto geram diagnóstico explícito.
- [ ] Validação de props na fronteira pública de montagem, pois chamadas JavaScript podem fornecer valores incorretos; falha não deixa montagem parcial anexada à raiz.
- [ ] Fixture com CSS responsivo verificada em 360, 768 e 1440 pixels de largura; inspeção de conflitos CSS, foco, overflow e cliques.
- [ ] Saída inspecionável, exemplo reproduzível, instruções reais de instalação/build e versões registradas.
- [ ] Arquitetura não exige conhecer de antemão um catálogo de componentes de produto.
- [ ] O relatório do marco declara exatamente os navegadores executados. Webview só entra nesse relatório se testada em host real.

M0 não inclui estado reativo, handlers de eventos da linguagem, operações assíncronas gerenciadas, SSR, hidratação ou provas formais. A interação do exemplo usa os comportamentos nativos do HTML. Essa delimitação permite entregar o transpiler antes de implementar um framework completo.

## 5. Evolução incremental

| Marco | Incremento | Evidência para avançar |
| --- | --- | --- |
| M0 — tradução | Parser, validação, emissão DOM/CSS, montagem/descarte e diagnósticos | Corpus e fixture de navegador aprovados. |
| M1 — interatividade | Estado local, derivações, eventos, listas com chaves, limpeza de efeitos e semântica de estilos locais | Atualizações preservam identidade; remover componentes libera recursos; cenários de foco e clique passam. |
| M2 — ambientes e integrações | Adaptadores JS/TS, políticas assíncronas, saída estática onde possível e integração com webview real | Fixtures de site, aplicação e host embarcado passam; fronteiras e versões suportadas estão publicadas. |
| M3 — otimização para agentes | Comparação de sintaxes, operações estruturadas de edição e diagnósticos orientados a reparo | Menor custo total demonstrado sem perda de qualidade; mudanças incompatíveis têm migração. |
| M4 — contratos verificáveis | Propriedades específicas de estados e ações, com método e fronteiras declarados | Casos positivos e contraexemplos demonstram cada garantia; tradução/runtime entram no argumento de confiança. |

As medições começam em M0 como instrumentação. Ensaios comparativos podem ocorrer a cada marco com tarefas já suportadas. O estudo completo das três fixtures depende da cobertura de M2. Provas formais gerais, renderers nativos sem webview e um ecossistema completo de roteamento/pacotes não condicionam o primeiro transpiler.

## 6. Decisões de arquitetura e alternativas

| Decisão proposta | Motivo e limite |
| --- | --- |
| Começar por tradução para DOM | Torna explícito o custo do código emitido; exige definir corretamente texto, atributos e propriedade dos nós. |
| Não usar React como dependência obrigatória da saída | Mantém autonomia para otimizar o runtime. Um adaptador ou backend React pode ser explorado depois; emitir JSX sozinho não demonstraria ganho no cliente. |
| Separar análise de emissão | Permite acrescentar saída HTML estática e outras estratégias sem redefinir a semântica da fonte. Evitar uma IR muito genérica antes dos casos reais. |
| Preservar CSS global no M0 | Entrega comportamento nativo com pouco escopo. Isolamento exige decisões próprias sobre especificidade, composição e portais. |
| Manter interoperabilidade como requisito de direção | A abrangência depende de código e bibliotecas externos. Garantias não atravessam automaticamente fronteiras opacas. |
| Sintaxe experimental antes de sintaxe definitiva | Permite aprender com parser, exemplos e agentes sem prometer estabilidade prematura. |

## 7. Questões abertas e dependências

| Questão | Quando resolver | Responsabilidade |
| --- | --- | --- |
| Linguagem de implementação do compilador e parser | Decidido: TypeScript, parser recursivo descendente escrito à mão ([CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0)); empacotamento segue aberto | Engenharia + usuário |
| Espaços/texto, mapeamento de atributos e API de exportação | Decidido em [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0); gramática formal completa entra com o T01 | Engenharia; proposta curta e exemplos |
| Orçamento de tempo/memória e tamanho dos projetos | Antes de escolher stack e fixar metas; cargas de BENCHMARK.md são hipóteses calibráveis | Usuário + engenharia |
| Licença de distribuição e registro do domínio pretendido | Antes do primeiro lançamento como open source e da ativação do site | Fundador/mantenedores |
| Matriz mínima de navegadores/webviews | Antes de declarar suporte; ampliações por evidência | Mantenedores + contribuidores |
| Qual subconjunto merece verificação formal | M4, com base em falhas reais e custo de prova | Comunidade de linguagem/verificação |

Não há prazo de entrega informado. Os marcos são ordenados por dependências e evidência, sem estimativa de calendário artificial.

## 8. Referências e fundamento

- [Bend](https://bend-lang.com/) e [guia oficial](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md): inspiração para contratos e provas; não é dependência escolhida para este compilador.
- [A2UI Express — anúncio oficial](https://developers.googleblog.com/fast-reliable-a2ui/): demonstra uma abordagem de formato intermediário para geração de UI; seus resultados não medem nossa linguagem nem performance de runtime web.
- [Svelte — documentação](https://svelte.dev/docs/svelte/overview): precedente de componentes declarativos compilados para JavaScript.
- [React — adoção incremental](https://react.dev/learn/add-react-to-an-existing-project) e [identidade de estado](https://react.dev/learn/preserving-and-resetting-state): referências para integração gradual e comportamento observável a tratar explicitamente.

Referências consultadas em 28/10/2026. Decisões técnicas deste documento são propostas do projeto, não garantias derivadas dessas referências.
