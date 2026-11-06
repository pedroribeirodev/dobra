# Política de segurança / Security policy

[Português](#português) · [English](#english)

## Português

### Estado

Dobra está em fase de especificação. Ainda não há pacote, versão publicada nem compilador executável, então não há versões com suporte de segurança. Mesmo assim, o contrato já define garantias de segurança e falhas nele são relevantes.

### O que relatar

- Formas de contornar a política de URLs do M0 (por exemplo, um esquema `javascript:` aceito) descrita em GRAMMAR.md e CORE.md §0.1.
- Formas de introduzir atributos `on*`, HTML executável a partir de texto ou props, ou outra execução de código não prevista.
- Quando o compilador existir: leitura ou escrita fora do projeto, saída parcial apresentada como válida e falhas semelhantes.

Ambiguidades do contrato sem impacto de segurança podem ser abertas como issue pública.

### Como relatar

Use o [relato privado de vulnerabilidades do GitHub](https://github.com/pedroribeirodev/dobra/security/advisories/new). **Não abra issue, PR ou discussão pública** com detalhes exploráveis. Inclua a seção do contrato afetada, uma entrada mínima e o impacto esperado.

O projeto é mantido por voluntários. As respostas são feitas no melhor esforço possível, sem prazo garantido. A correção e a divulgação serão coordenadas com quem relatou, e o crédito será dado se a pessoa quiser.

## English

### Status

Dobra is in the specification phase. There is no package, published release or runnable compiler yet, so no versions receive security support. Even so, the contract already defines security guarantees, and flaws in it matter.

### What to report

- Ways to bypass the M0 URL policy (for example, an accepted `javascript:` scheme) described in GRAMMAR.md and CORE.md §0.1.
- Ways to introduce `on*` attributes, executable HTML from text or props, or any other unintended code execution.
- Once the compiler exists: reads or writes outside the project, partial output presented as valid, and similar failures.

Contract ambiguities with no security impact can be opened as a public issue.

### How to report

Use [GitHub private vulnerability reporting](https://github.com/pedroribeirodev/dobra/security/advisories/new). **Do not open a public issue, PR or discussion** with exploitable details. Include the affected contract section, a minimal input and the expected impact.

The project is maintained by volunteers. Responses are best effort, with no guaranteed timeline. Fixes and disclosure will be coordinated with the reporter, and credit will be given if they want it.
