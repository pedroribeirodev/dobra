# Dobra

**A language for building interfaces. Designed for humans and agents.**

Dobra é uma proposta de linguagem geral de UI que busca tornar a criação e a manutenção de interfaces mais eficientes para pessoas e agentes, produzindo código web eficiente. A abrangência pretendida vai de componentes isolados e sites simples até aplicações complexas e webviews.

**Status: desenho inicial.** Este repositório contém a especificação e o plano de implementação. O transpiler ainda não existe; sintaxe e APIs são experimentais. Não há pacote publicado, instalação funcional nem ganho de tokens ou runtime demonstrado.

## Começar pelo transpiler

O primeiro marco é pequeno:

```text
.dobra → parser → AST → validação → JavaScript ES modules + CSS
```

M0 aceita componentes próprios, composição estática, props escalares e expressões restritas a literais e leitura de props. A saída monta elementos DOM em uma página existente e oferece descarte explícito. CSS associado é emitido sem reescrita, com escopo global documentado.

Estado reativo, efeitos, interoperabilidade ampla, renderização estática e contratos verificáveis entram em etapas posteriores. O projeto deve preservar composição livre e integração com a plataforma web.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [SPEC.md](SPEC.md) | Direção, requisitos de M0, critérios de aceitação e roadmap. |
| [CORE.md](CORE.md) | Semântica do primeiro transpiler e desenho dos recursos futuros. |
| [BENCHMARK.md](BENCHMARK.md) | Como avaliar custo para LLMs e desempenho no cliente. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Primeiras tarefas e processo de contribuição proposto. |
| [CONTEXT.md](CONTEXT.md) | Contexto autossuficiente para discutir o projeto com outros agentes. |
| [AGENTS.md](AGENTS.md) | Orientações para agentes trabalhando neste repositório. |

## Como avaliar a ideia

Os dois objetivos têm o mesmo peso. A avaliação contará o custo completo de geração e manutenção, incluindo documentação, reparos e falhas, e medirá o código realmente executado no cliente. Melhoras só serão consideradas quando o comportamento, a qualidade visual e a acessibilidade forem equivalentes.

O primeiro marco precisa demonstrar tradução correta e reproduzível. Comparações de superioridade só serão publicadas depois de executar os estudos correspondentes.

## Comunidade e licença

A intenção é desenvolver Dobra como open source com participação da comunidade. A licença de distribuição ainda não foi escolhida; sua definição faz parte da preparação do primeiro lançamento. Até lá, este é um repositório público de planejamento, sem uma concessão de licença open source declarada.

As primeiras contribuições podem discutir a mini-gramática, os exemplos válidos/inválidos, a semântica do código gerado e os critérios de conformidade. Consulte [CONTRIBUTING.md](CONTRIBUTING.md).

## Identidade

- Linguagem: **Dobra**.
- Arquivos: `.dobra`.
- CLI planejada: `dobra`.
- Domínio pretendido: `dobra.build` — compra e ativação ainda não confirmadas.

Referência de estado: 28/10/2026. Não há site ou lançamento anunciados por este documento.
