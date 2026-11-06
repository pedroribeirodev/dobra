# Contribuindo com Dobra

*[English summary below](#english-summary).* Participar implica aceitar o [Código de Conduta](CODE_OF_CONDUCT.md). Vulnerabilidades seguem [SECURITY.md](SECURITY.md), nunca issue pública.

**Status em 28/10/2026:** repositório de planejamento da linguagem Dobra; transpiler ainda não implementado. Licença: MIT ([LICENSE](LICENSE)). Ainda não há pacote instalável ou resultados de desempenho.

## Como queremos trabalhar

- Entregar primeiro o transpiler M0 descrito em [SPEC.md](SPEC.md), com um caminho pequeno que qualquer contribuidor consiga reproduzir.
- Manter especificação, exemplos, corpus de conformidade e implementação versionados juntos.
- Receber contribuições de implementação, exemplos que quebram a tradução, compatibilidade de ambientes, documentação e medições reproduzíveis.
- Discutir mudanças de semântica em propostas curtas: problema, exemplo, comportamento esperado, alternativas, compatibilidade e forma de verificar.
- Vincular cada recurso novo a um caso observável. Código aceito pelo parser precisa ter significado publicado.
- Tratar sintaxe e APIs iniciais como experimentais, registrando mudanças incompatíveis e como migrar exemplos.

## Primeiras tarefas, na ordem das dependências

| Tarefa | Entrega | Depende de |
| --- | --- | --- |
| T01 — mini-gramática M0 | Contrato experimental em [GRAMMAR.md](GRAMMAR.md): tokens, componentes, texto/espaços, props, expressões e exemplos válidos/inválidos | Contrato M0 |
| T02 — corpus e harness | Casos de conformidade e projeto mínimo de navegador que consome a saída | T01 |
| T03 — parser e AST | Nós com intervalos de origem e diagnósticos de sintaxe | T01 |
| T04 — validação semântica | Referências, tipos escalares, props obrigatórias, componentes e rejeição de ciclos | T03 |
| T05 — emissão DOM | Módulos determinísticos com montagem/descarte; cópia do CSS associado | T02, T04 |
| T06 — revisão no navegador | Evidência de texto/atributos, duas montagens independentes, descarte, teclado, cliques e CSS | T05 |
| T07 — reprodução por terceiro | Instruções e comandos realmente executados em ambiente limpo | T06 |

T01 está documentada; T02 e T03 são as próximas entregas e podem avançar em paralelo a partir desse contrato. A gramática não substitui o corpus executável nem significa que o parser existe. Cada PR deve ter escopo definido e informar qual comportamento muda, como foi verificado e quais limitações permanecem. Não se exige uma nova prova formal para contribuir ao M0.

## Relatos de bugs e propostas

Um relato de bug deve incluir versão, ambiente, entrada mínima, saída observada, resultado esperado e passos para reproduzir. Reduzir o exemplo costuma ser mais útil que anexar uma aplicação inteira. Não incluir dados privados ou credenciais nos exemplos.

Uma proposta de sintaxe deve incluir pelo menos um exemplo de criação e um de alteração posterior. Comparações de tamanho devem contar tokens com método declarado; quantidade de caracteres não é evidência suficiente.

Uma proposta de otimização deve preservar o contrato funcional e visual e seguir [BENCHMARK.md](BENCHMARK.md). Resultados negativos e casos de regressão também são contribuições úteis. Evitar slogans de superioridade antes de executar comparações equivalentes.

## Governança e decisões

- **Quem decide:** por enquanto o projeto tem um único mantenedor, [@pedroribeirodev](https://github.com/pedroribeirodev), que aprova mudanças de contrato e faz merge. Essa regra deve mudar quando houver mais mantenedores, e a mudança será registrada aqui.
- **Fonte da verdade:** CORE.md §0.1 e GRAMMAR.md definem o contrato do M0. Issues, discussões, comentários e mensagens de chat não mudam o contrato até que um PR atualize esses documentos.
- **Fluxo de uma proposta:** ideias começam nas Discussions. Uma proposta formal usa o template de issue e recebe `status: needs-decision`. O mantenedor marca `status: accepted` ou `status: declined` com justificativa. Só depois de aceita, um PR altera o contrato, junto com os casos de corpus e uma nota de migração.
- **Escopo:** recursos de marcos futuros recebem `out-of-scope: M0` e ficam abertos para reavaliação, sem implementação antes do marco.
- **Merge:** a `main` aceita mudanças só por PR, com a CI passando e todas as conversas resolvidas. O [CODEOWNERS](.github/CODEOWNERS) pede a revisão do mantenedor automaticamente. Enquanto houver um único mantenedor, a aprovação não é obrigatória; ela passa a ser quando o projeto tiver contribuidores regulares.

## Contribuições com ferramentas de IA

Dobra é feita para pessoas e agentes, e contribuições com ajuda de IA são bem-vindas. Valem as mesmas regras de qualquer PR, e mais estas:

- Uma pessoa abre o PR e responde por todo o conteúdo, inclusive o que não escreveu.
- Comandos, saídas, medições e resultados de teste precisam ter sido realmente executados. Saída inventada leva ao fechamento do PR.
- Prefira PRs pequenos e focados. PRs grandes e genéricos, ou várias variações do mesmo PR, podem ser fechados sem revisão detalhada.
- Não cole no PR prompts com dados privados ou credenciais.

## Labels

| Label | Uso |
| --- | --- |
| `milestone: M0` … `milestone: M4` | Marco ao qual o trabalho pertence. |
| `type: proposal`, `type: task`, `bug` | Tipo da issue, aplicado pelos templates. |
| `status: needs-decision` / `accepted` / `declined` | Estado de uma proposta. |
| `out-of-scope: M0` | Recurso válido, mas fora do marco atual. |
| `area: grammar` / `corpus` / `compiler` / `docs` | Parte do projeto afetada. |
| `benchmark` | Medição ou alegação de ganho; segue BENCHMARK.md. |
| `good first issue`, `help wanted` | Boas portas de entrada. |

## Preparação do primeiro lançamento

- Licença MIT adicionada em [LICENSE](LICENSE). Nome e repositório já estão definidos: Dobra, `pedroribeirodev/dobra`.
- Publicar estado real de implementação e limitações. A abertura pode começar na fase de desenho; um exemplo executável amplia a utilidade do convite a implementadores.
- Disponibilizar SPEC, CORE, tarefas pequenas e um canal de discussão.
- Quando M0 existir, adicionar instalação, exemplo, comando de build, comando de verificação e ambientes realmente testados.
- Manter um roteiro público de marcos e registrar decisões em propostas/PRs. Detalhes de governança podem crescer com o grupo de mantenedores.

## Convite em rascunho

> Estamos desenhando Dobra, uma linguagem geral de UI para autoria por pessoas e agentes, com dois objetivos: reduzir o custo de gerar e manter interfaces e produzir código web eficiente.
>
> A proposta é desenvolver o projeto como open source. O primeiro marco é um transpiler pequeno: componentes e props virando JavaScript e CSS. Estado, integrações e contratos verificáveis serão acrescentados progressivamente.
>
> Buscamos pessoas interessadas em compiladores, frontend, ferramentas para agentes e testes de compatibilidade. A especificação inicial está escrita; o transpiler ainda será construído. Contribuições à gramática, ao corpus de conformidade e aos exemplos são as primeiras oportunidades.
>
> Ainda não demonstramos vantagem de tokens ou runtime. Queremos medir isso publicamente, com comparações reproduzíveis e espaço para resultados que contrariem a hipótese.

Repositório: [pedroribeirodev/dobra](https://github.com/pedroribeirodev/dobra). Antes de divulgar o convite, vincular tarefas abertas. Este convite é um rascunho; não foi enviado à comunidade.

## English summary

Dobra is in the specification phase: the transpiler does not exist yet, and no token or performance gains have been demonstrated. Main documents are in Brazilian Portuguese; issues and PRs are welcome in Portuguese or English.

- **Start here:** the M0 contract is [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0). Open tasks are tracked as issues labeled `type: task`, in the dependency order of the table above (T01–T07).
- **Proposals:** discuss ideas in Discussions first, then use the proposal issue template. Only the maintainer accepts or declines; the contract changes only through a PR that updates CORE/GRAMMAR, corpus cases and migration notes.
- **Scope:** M0 is static (components, scalar props, composition, mount/dispose). State, events, async, SSR and proofs are later milestones and get `out-of-scope: M0`.
- **Claims:** token or performance claims must follow [BENCHMARK.md](BENCHMARK.md). Character counts are not evidence.
- **AI-assisted contributions** are welcome. A human opens the PR, is accountable for all of it, and only reports commands and results that were actually run.
- **Conduct and security:** follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
