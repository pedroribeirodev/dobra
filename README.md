# Dobra

*A UI language for people and AI agents to write and maintain interfaces. Spec phase: nothing is implemented yet.*

Dobra é uma linguagem de UI para pessoas e agentes de IA escreverem e manterem interfaces, compilada para JavaScript e CSS sem depender de React.

> **Status: fase de especificação.** O transpiler ainda não existe. Não há pacote, instalação funcional nem benchmarks executados. Nenhum ganho de tokens ou de desempenho foi demonstrado. Sintaxe e APIs são experimentais.

## Exemplo (ilustrativo, transpiler ainda não existe)

```text
component Greeting(name: string) {
  <section class="greeting">
    <h1>Olá, {name}</h1>
    <a href="#detalhes">Saiba mais</a>
  </section>
}
```

O tipo de JavaScript que o M0 deve gerar, seguindo o contrato de [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0):

```js
// ilustrativo: a saída real será definida pela implementação
export function mountGreeting(root, props) {
  if (typeof props?.name !== "string") throw new DobraPropError("name", "string");
  const section = document.createElement("section");
  section.setAttribute("class", "greeting");
  const h1 = document.createElement("h1");
  h1.append(document.createTextNode("Olá, "), document.createTextNode(props.name));
  const a = document.createElement("a");
  a.setAttribute("href", "#detalhes");
  a.append(document.createTextNode("Saiba mais"));
  section.append(h1, a);
  root.append(section);
  let mounted = true;
  return function dispose() {
    if (!mounted) return;
    mounted = false;
    section.remove();
  };
}
```

## Por que existe

Agentes precisam coordenar estrutura, estilo, estado e efeitos ao criar e alterar interfaces. A hipótese é que uma linguagem com semântica previsível e diagnósticos precisos reduza o custo total de autoria, incluindo guia, contexto, reparos e falhas, e que o compilador gere código leve no navegador. É só uma hipótese. A primeira pergunta a responder é se Dobra custa menos para um agente do que TSX nas mesmas tarefas, mesmo contando o guia da linguagem. O piloto que responde isso está em [BENCHMARK.md §8](BENCHMARK.md#8-piloto-antecipado-de-custo-para-agentes-no-subconjunto-m0).

## Roadmap

- **M0, agora:** transpiler mínimo com componentes, props escalares, composição estática, montagem/descarte e diagnósticos.
- **M1:** interatividade, com estado local, eventos, listas com chave e estilos locais.
- **M2:** ambientes e integrações, com adaptadores JS/TS, async, saída estática e webview real.
- **M3:** otimização para agentes, com comparação de sintaxes, edição estruturada e diagnósticos orientados a reparo.
- **M4:** contratos verificáveis, com propriedades delimitadas de estados e ações.

Detalhes em [SPEC.md §5](SPEC.md#5-evolução-incremental).

## Como ajudar

Primeiras tarefas, na ordem de [CONTRIBUTING.md](CONTRIBUTING.md):

1. **T01, mini-gramática M0:** tokens, texto/espaços, props, expressões e exemplos válidos e inválidos.
2. **T02, corpus e harness:** casos `.dobra` + `.expected.json` e um projeto mínimo de navegador que consome a saída.
3. **T03, parser e AST:** parser recursivo descendente em TypeScript, com intervalos de origem e diagnósticos de sintaxe.
4. **T06, revisão no navegador:** testes de comportamento para texto, atributos, montagens independentes, descarte, teclado e cliques.

Exemplos que quebram a tradução e resultados negativos também são contribuições úteis.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [SPEC.md](SPEC.md) | Direção, requisitos do M0 e roadmap. |
| [CORE.md](CORE.md) | Contrato canônico do M0 (§0.1) e semântica futura. |
| [BENCHMARK.md](BENCHMARK.md) | Como avaliar custo para agentes e desempenho no cliente. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Tarefas T01–T07 e processo de contribuição. |
| [DIAGNOSTICS.md](DIAGNOSTICS.md) | Registro dos códigos de diagnóstico. |
| [CONTEXT.md](CONTEXT.md) | Contexto do projeto para conversar com agentes. |
| [AGENTS.md](AGENTS.md) | Orientações para agentes neste repositório. |

## Licença

[MIT](LICENSE) © 2026 Pedro Ribeiro.
