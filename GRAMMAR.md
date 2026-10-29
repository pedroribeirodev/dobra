# Dobra — gramática experimental do M0

Esta é a entrega T01: a sintaxe e a superfície HTML do primeiro transpiler. Ela detalha o contrato de [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0), sem acrescentar estado, eventos, imports ou slots. Não há parser ou transpiler implementado nesta entrega. O futuro parser T03 reconhecerá a sintaxe; a validação semântica T04 e a emissão DOM T05 são etapas separadas. **Obter uma AST não significará ter um programa M0 válido nem uma interface executável.**

## 1. Fonte, tokens e posições

- A fonte é texto Unicode. Antes de analisá-la, `CRLF` e `CR` isolado são normalizados para `LF`.
- Fora de texto e strings, os espaços aceitos são `U+0020`, tabulação e `LF`. Não há inserção automática de delimitadores.
- Nomes são sensíveis a maiúsculas. Identificadores usam `[A-Za-z_][A-Za-z0-9_]*`; nomes de componentes começam com `[A-Z]`. Tags HTML são minúsculas. Não há nomes Unicode, namespaces ou resolução de nomes com ponto no M0.
- `component`, `string`, `number`, `boolean`, `true` e `false` são palavras reservadas; não podem ser nomes de props nem referências a props.
- Strings usam apenas aspas duplas e escapes JSON: `\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t` e `\u` seguido de quatro dígitos hexadecimais. Não aceitam quebras de linha literais nem caracteres de controle sem escape. Aspas simples e template strings ficam fora do M0.
- Números têm a forma JSON abaixo. São convertidos para `number` de JavaScript e devem ser finitos; overflow, como `1e999`, é `E006`. Hexadecimal, separadores, `+1`, `.5`, `1.`, `NaN` e `Infinity` não são literais numéricos do M0. `NaN` e `Infinity` sem sinal têm a forma de identificador e serão tratados como referências; sem uma prop correspondente, T04 produzirá `E004`. Não há tipo inteiro nem precisão decimal arbitrária.
- Não há comentários, diretivas, BOM, ponto e vírgula opcional ou vírgula final nas listas de props.

O contrato para T03 exige que todo nó da AST tenha um `span` com `start` e `end`. Cada posição contém `offset`, `line` e `column`: offsets começam em zero; linhas e colunas, em um; o fim é exclusivo. Offsets e colunas contam unidades UTF-16 da fonte normalizada, inclusive no caso de emoji. Tabulação conta como uma coluna. Os spans sempre apontam para a fonte, antes da normalização de texto e da decodificação de strings/entidades. Um diagnóstico em `EOF` terá intervalo vazio no offset igual ao comprimento dessa fonte, com linha e coluna correspondentes.

Diagnósticos usam um caminho relativo à raiz do projeto com `/` como separador. Não incluem caminhos absolutos da máquina. O parser pode interromper no primeiro erro; recuperação com múltiplos erros não é garantia do T03.

## 2. EBNF

Nesta notação, `,` concatena, `|` indica alternativa, `[ ... ]` é opcional e `{ ... }` repete zero ou mais vezes. Textos entre aspas são tokens literais; `? ... ?` define conjuntos de caracteres ou condições especiais. `EOF` é o fim da fonte. Não existe espaço implícito entre termos. `tab` e `lf` representam os caracteres de controle reais, não a barra invertida seguida de uma letra. A barra invertida e as aspas das strings têm produções próprias para evitar ambiguidade de escape na EBNF.

```ebnf
module           = ws, component, { ws, component }, ws, EOF ;
component        = "component", required-ws, component-name, ws,
                   "(", ws, [ parameters ], ")", ws,
                   "{", ws, element, ws, "}" ;
parameters       = parameter, { ws, ",", ws, parameter }, ws ;
parameter        = identifier, ws, ":", ws, scalar-type ;
scalar-type      = "string" | "number" | "boolean" ;

element          = "<", tag-name, attributes, ws, "/>"
                 | "<", tag-name, attributes, ws, ">",
                   { child }, "</", tag-name, ws, ">" ;
attributes       = { required-ws, attribute } ;
attribute        = attribute-name, ws, "=", ws, attribute-value ;
attribute-value  = string | interpolation ;
child            = element | interpolation | text ;
interpolation    = "{", ws, expression, ws, "}" ;
expression       = string | number | "true" | "false" | identifier ;

component-name   = upper, { letter | digit | "_" } ;
html-name        = lower, { lower | digit | "-" } ;
tag-name         = component-name | html-name ;
attribute-name   = identifier | html-name ;
identifier       = (letter | "_"), { letter | digit | "_" } ;
letter           = upper | lower ;
upper            = ? U+0041–U+005A: A–Z ? ;
lower            = ? U+0061–U+007A: a–z ? ;
digit            = ? U+0030–U+0039: 0–9 ? ;
nonzero-digit    = ? U+0031–U+0039: 1–9 ? ;
hex-digit        = digit | ? U+0061–U+0066: a–f ? | ? U+0041–U+0046: A–F ? ;

number           = [ "-" ], ("0" | nonzero-digit, { digit }),
                   [ ".", digit, { digit } ],
                   [ ("e" | "E"), [ "+" | "-" ], digit, { digit } ] ;
string           = double-quote, { string-char | escape }, double-quote ;
escape           = backslash, (double-quote | backslash | "/" | "b" | "f" | "n" | "r" | "t"
                   | "u", hex-digit, hex-digit, hex-digit, hex-digit) ;
double-quote     = ? U+0022 ? ;
backslash        = ? U+005C ? ;
string-char      = ? qualquer caractere exceto U+0000–U+001F, U+0022 e U+005C ? ;
text             = (text-char | entity), { text-char | entity } ;
text-char        = ? qualquer caractere exceto <, {, } e & ? ;
entity           = "&lt;" | "&gt;" | "&amp;" | "&lbrace;" | "&rbrace;" ;

tab              = ? U+0009 ? ;
lf               = ? U+000A ? ;
ws               = { " " | tab | lf } ;
required-ws      = (" " | tab | lf), ws ;
EOF              = ? fim da fonte ? ;
```

As seguintes restrições complementam a EBNF:

1. O nome de uma tag de fechamento deve ser igual ao da abertura. Ausência ou troca de fechamento é `E001`; não há fechamento HTML implícito.
2. Um módulo tem pelo menos um componente. Cada corpo tem exatamente uma raiz, que é um elemento HTML ou uso de componente. Corpo vazio é `E001`; duas raízes são `E008`. Texto ou interpolação isolados não substituem a raiz.
3. Tags HTML vazias da tabela da seção 4 exigem `/>`: `<input />` é válido; `<input></input>` é uma forma fora do M0 (`E006`). Uma abertura sem fechamento como `<input>` é `E001`. Tags não vazias também podem ser escritas como `<div />`.
4. Componentes próprios aceitam props e não aceitam filhos/slots. `<Card />` e `<Card></Card>` são formas equivalentes; o par pode conter somente espaços descartáveis. Texto, interpolação ou elementos entre as tags de um componente são `E006`.
5. Atributos HTML têm nomes na forma `html-name`; props de componentes têm nomes na forma `identifier`. A lista HTML e a declaração de props limitam quais nomes são aceitos. Não há `className`, spread, atributo abreviado nem atributo sem valor: use `disabled={true}`.
6. Declarações de componentes, props declaradas e atributos de uma mesma abertura não podem repetir nomes. Duplicações e props fornecidas sem declaração são recursos fora do contrato (`E006`), a verificar em T04.
7. Nomes e literais são tokens completos. `trueValue` é uma referência, não `true` seguido de texto. Expressões como `name.trim()`, `count + 1`, `obj.name`, arrays, objetos, ternários, atribuições e chamadas são `E006`.

O futuro lexer/parser poderá aceitar uma tag ou um nome de atributo com forma correta antes de T04 verificar a lista fechada. Não poderá avaliar expressões como JavaScript para tentar validá-las.

`E001` identifica estrutura malformada: delimitador ausente, string não terminada, escape JSON inválido, atributo sem valor, dois atributos sem espaço entre eles, vírgula final, nome que viola a forma lexical ou `}` cru em texto. `E006` identifica um recurso reconhecível fora do subconjunto: uma expressão com operação/chamada, string com aspas simples, comentário, import, entidade não admitida, filhos de componente ou elemento vazio escrito com par de tags. A primeira falha encontrada determina o diagnóstico; exemplos com múltiplas falhas não prometem uma lista completa. `E008` se aplica quando aparece uma segunda raiz após uma primeira raiz completa.

| Caso isolado, no contexto correspondente | Diagnóstico previsto |
| --- | --- |
| Fonte vazia; EOF antes de fechar string, interpolação, tag ou corpo | `E001` |
| `<p>` fechado por `</div>`; `}` cru no texto | `E001` |
| Prop declarada sem `:`; atributo sem `=` ou valor; atributos sem espaço entre eles | `E001` |
| Vírgula final em `component Card(name: string,)` | `E001` |
| Literal numérico malformado `01`, `1.` ou `1e` | `E001` |
| BOM inicial, comentários (`//`, `/* ... */`, `<!-- ... -->`) ou `import` | `E006` |
| Tipo fora do M0, como `Date`, `string[]` ou `string?` | `E006` |
| Aspas simples, template string, número hexadecimal, separador numérico, `+1` ou `.5` | `E006` |
| Número que excede o intervalo finito, como `1e999` | `E006` |
| `<input></input>`; filhos em `<Card>texto</Card>` | `E006` |
| Entidade desconhecida, como `&nbsp;`, ou `&` isolado | `E006` |
| Segundo elemento na raiz após uma primeira raiz completa | `E008` |

A detecção de um recurso fora do subconjunto não exige interpretá-lo. A mesma fonte normalizada, com o mesmo caminho relativo, deverá produzir a mesma AST ou diagnóstico, sem IDs aleatórios, timestamps ou variação na ordem de visita.

## 3. Texto, strings e entidades

Texto entre tags segue um algoritmo por trecho contíguo, separado por elementos e interpolações:

1. Dividir o trecho em linhas por `LF`.
2. Descartar linhas compostas apenas de espaços e tabulações.
3. Em cada linha restante, converter sequências de espaços/tabulações em um único espaço. Remover espaços no início das linhas posteriores à primeira linha original e no fim das linhas anteriores à última linha original.
4. Juntar as linhas restantes com um espaço.
5. Decodificar as cinco entidades da tabela uma única vez. Entidade desconhecida ou `&` sem entidade válida gera `E006`.

Essa ordem preserva um espaço literal ao lado de uma interpolação na mesma linha. Não insere espaços entre trechos separados por nós. Um trecho descartado não produz nó de texto. A normalização não considera o CSS: `white-space: pre` não recupera indentação removida da fonte.

| Fonte no corpo de um elemento | Valor de texto ou sequência de nós |
| --- | --- |
| `Olá, {name}!` | texto `"Olá, "`, interpolação `name`, texto `"!"` |
| `A   B` | texto `"A B"` |
| `A` + quebra de linha + `  B` | texto `"A B"` |
| quebra de linha + `  A` + quebra de linha | texto `"A"` |
| `<span>A</span><span>B</span>` | dois elementos; nenhum espaço inserido entre eles |
| `{first} {last}` | duas interpolações; o trecho composto só de espaço é descartado; use `{first}{" "}{last}` para separá-las |
| `&lt;b&gt;&lbrace;x&rbrace;&lt;/b&gt;` | texto `"<b>{x}</b>"`, sem nova análise de marcação |
| `&amp;lt;` | texto `"&lt;"`, sem segunda decodificação |

O atributo literal `title="A &amp; B"` usa os escapes JSON e depois decodifica entidades uma vez. Não aplica a normalização de espaços de texto. Já expressões string, como `title={"A &amp; B"}` e `{"&lt;"}`, usam somente escapes JSON: os valores são respectivamente `"A &amp; B"` e `"&lt;"`. Uma prop recebida de JavaScript também não passa por decodificação de entidades.

Interpolação de string produz texto literal; `number` usa `String(n)` e `boolean` usa `"true"` ou `"false"`. Não há interpretação de string como HTML. Para espaços ou quebras de linha intencionais, uma expressão string como `{" "}` ou `{"\n"}` mantém o valor, sujeito à apresentação normal do CSS.

## 4. Superfície HTML fechada

Esta tabela é a lista completa de tags HTML do M0. Elementos próprios, cuja tag começa em maiúscula, são definidos pelo autor e não compõem um catálogo visual obrigatório. O alvo inicial de produto são interfaces de CRM/ERP, mas M0 serve para provar tradução e montagem estática: esta lista não representa todas as necessidades desses produtos. Tabelas, outras tags e atributos poderão entrar por propostas com casos de conformidade. Editores visuais no estilo Figma permanecem uma direção futura; integrações Canvas pertencem ao trabalho de ambientes e adaptadores de M2, não acrescentam um renderer ao M0.

| Grupo | Tags |
| --- | --- |
| Estrutura | `main`, `header`, `footer`, `nav`, `section`, `article`, `aside`, `div` |
| Texto | `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `p`, `span`, `strong`, `em`, `small`, `code`, `pre`, `blockquote` |
| Listas | `ul`, `ol`, `li` |
| Navegação e mídia | `a`, `img` |
| Formulários | `form`, `label`, `input`, `button`, `select`, `option`, `textarea`, `fieldset`, `legend` |
| Separadores | `br`, `hr` |

As únicas tags vazias desta lista são `img`, `input`, `br` e `hr`. SVG, custom elements, `script`, `style`, `iframe`, `object`, `embed`, `link`, `meta` e quaisquer outras tags ficam fora do M0 (`E006`). CSS continua em arquivo associado, global e preservado pelo futuro emissor; não existe bloco de estilo na gramática `.dobra`.

Os atributos globais são `id`, `class`, `title`, `lang`, `dir`, `role`, `tabindex` e `hidden`. Também são aceitos nomes `aria-*` e `data-*` com sufixo não vazio formado por minúsculas, dígitos e hífens, iniciado por letra minúscula. Essa forma aberta dos dois prefixos é parte explícita da lista; ela não valida a semântica de cada nome ARIA.

Além dos globais, cada tag aceita somente os atributos abaixo. Tags ausentes da tabela aceitam apenas globais.

| Tag | Atributos específicos |
| --- | --- |
| `a` | `href`, `target`, `rel`, `download` |
| `img` | `src`, `alt`, `width`, `height`, `loading` |
| `ol` | `start`, `reversed` |
| `form` | `action`, `method`, `autocomplete`, `novalidate` |
| `label` | `for` |
| `input` | `type`, `name`, `value`, `checked`, `disabled`, `placeholder`, `required`, `readonly`, `min`, `max`, `step`, `minlength`, `maxlength`, `multiple`, `autocomplete` |
| `button` | `type`, `name`, `value`, `disabled` |
| `select` | `name`, `value`, `disabled`, `required`, `multiple` |
| `option` | `value`, `selected`, `disabled`, `label` |
| `textarea` | `name`, `value`, `disabled`, `placeholder`, `required`, `readonly`, `rows`, `cols`, `minlength`, `maxlength` |
| `fieldset` | `disabled`, `name` |

O contrato de emissão, a implementar após T04, distingue:

- **Propriedades DOM:** `value`, `checked`, `disabled` e `selected`. O emissor atribuirá à propriedade correspondente nos elementos onde a tabela permite seu uso. `value` exige `string`; `checked`, `disabled` e `selected` exigem `boolean`. Uma prop `number` não pode alimentar `value`, mesmo que o navegador pudesse convertê-la. A lista não inclui `li.value`, cuja semântica numérica exigiria uma regra diferente.
- **Booleanos de presença:** `hidden`, `reversed`, `novalidate`, `required`, `readonly` e `multiple` exigem `boolean` e usarão presença/ausência do atributo para `true`/`false`. Os booleanos atribuídos como propriedades (`checked`, `disabled`, `selected`) também terão seu atributo inicial presente para `true` e ausente para `false`, além da atribuição da propriedade. Isso não pressupõe que uma propriedade como `checked` reflita automaticamente seu atributo. Não é válido codificar falsidade como a string `"false"`.
- **Demais atributos:** usam `setAttribute` com representação textual do escalar. Em particular, `aria-*` e `data-*` recebem `"true"` e `"false"` para valores booleanos, sem regra de presença.
- **URLs:** `href`, `src` e `action` exigem `string` e estão sujeitos à política descrita a seguir. Tipo incompatível em uso estático de uma prop ou atributo gera `E007`; valor de URL proibido gera `E006` para literal.

A montagem futura definirá primeiro os atributos comuns, incluindo `input.type`, construirá os filhos e só então atribuirá `value`; assim, as opções de um `select` já existirão quando seu valor for definido. A ordem textual dos atributos não deve mudar esse resultado. Se houver `select.value` e `option.selected`, o valor de `select` será aplicado por último e definirá a seleção final conforme o comportamento nativo. O atributo inicial `selected` representa o padrão da opção; sua propriedade de seleção atual pode diferir após a aplicação de `select.value` ou uma interação do usuário.

Em `textarea`, `value` e conteúdo não vazio são mutuamente exclusivos (`E006`); espaços descartados pelo algoritmo de texto não contam como conteúdo. Sem `value`, seu conteúdo fornece o texto inicial. Depois da montagem, controles mantêm o comportamento nativo: M0 não reaplica props após interação ou reset de formulário. O valor efetivo dos inputs obedece à normalização nativa do tipo escolhido; Dobra não promete manter uma string que o próprio controle rejeite ou normalize.

`input.type` exige `string`. O tipo `file`, comparado sem distinguir maiúsculas de minúsculas, fica fora do M0 para não introduzir uma propriedade `value` que recuse atribuições não vazias. Um literal com esse tipo gera `E006`; uma prop que resolva para esse tipo deverá gerar `DobraPropError` na montagem, antes de criar nós. Outros valores de `type` mantêm seu significado e fallback nativos; não há eventos próprios ou API de arquivos no M0.

### URLs no M0

A checagem opera sobre o valor final da string: escapes e entidades de atributos literais já terão sido decodificados; strings em expressões e props não ganham outra decodificação. O mesmo procedimento valerá na compilação para literais e na montagem para valores vindos de props. Ele rejeita valores; não os corrige, remove caracteres ou troca o destino.

1. Rejeitar controles `U+0000–U+001F` e `U+007F`, barra invertida em qualquer posição e espaço `U+0020` no início ou no fim.
2. Reconhecer um esquema somente no início pela forma `[A-Za-z][A-Za-z0-9+.-]*:`. Comparar seu nome sem distinguir maiúsculas de minúsculas. Aceitar somente `http`, `https`, `mailto` e `tel`; rejeitar qualquer outro, incluindo `javascript` e `data`.
3. Sem esquema, aceitar fragmentos iniciados por `#` e referências relativas. Para M0, uma referência relativa não começa com `//` e não contém `:` antes do primeiro `/`, `?` ou `#`. Caminhos iniciados por `/`, `./`, `../`, uma consulta `?page=2` e string vazia estão incluídos. Referências de rede como `//example.com` ficam fora do subconjunto inicial.

Exemplos aceitos: `https://example.com`, `HTTP://example.com`, `mailto:team@example.com`, `tel:+5511999999999`, `#details`, `/customers`, `../customers` e `?page=2`. Exemplos rejeitados: `javascript:alert(1)`, `data:text/html,x`, `//example.com`, `javascript` com uma tabulação antes de `:`, e espaço antes de um esquema. A política limita esquemas e formas ambíguas; não é uma lista de domínios confiáveis nem uma garantia sobre o conteúdo do destino.

Qualquer atributo `on*` é proibido, mesmo que pareça um atributo HTML conhecido. `style` inline também está fora da lista. Essa lista define a capacidade do M0; não valida sozinha acessibilidade, regras completas de conteúdo HTML nem segurança do CSS fornecido pelo autor.

## 5. Props, composição e validação

Props são escalares obrigatórios: `string`, `number` e `boolean`. Não há valor padrão, prop opcional, coerção entre tipos, filhos ou atualização reativa. Valores são literais ou referências a props do componente que contém o uso. Declarações podem aparecer antes ou depois de seus usos no mesmo módulo.

T04 deverá verificar componentes desconhecidos (`E002`), props ausentes (`E003`), referências fora do escopo (`E004`), ciclos diretos/indiretos (`E005`), restrições HTML e de recursos (`E006`) e tipos incompatíveis em props ou atributos (`E007`). Uma string com aparência de número não satisfaz uma prop `number`; uma prop `number` não satisfaz um atributo que exige `string`. T03 não deverá alegar que verificou essas propriedades apenas por construir a AST.

A fronteira pública futura é `mountX(root, props) => dispose`, conforme CORE. Tipos inválidos, números não finitos e URLs proibidas vindos de JavaScript são erros de montagem, antes de anexar nós; não são diagnósticos de compilação. Estas regras ainda não equivalem a uma implementação de `mount`.

## 6. Exemplos de criação e alteração

Criação: compor dois cartões com todas as classes de props escalares.

```text
component Card(name: string, count: number, enabled: boolean) {
  <article class="card" data-enabled={enabled}>
    <h2>{name}</h2>
    <p>Itens: {count}</p>
    <input type="checkbox" checked={enabled} aria-label="Ativo" />
  </article>
}

component Dashboard() {
  <main class="dashboard">
    <Card name="Primeiro" count={1} enabled={true} />
    <Card name="Segundo" count={2} enabled={false} />
  </main>
}
```

Alteração posterior: acrescentar um destino obrigatório ao cartão. A declaração e os dois usos mudam juntos; o restante da estrutura permanece igual.

```text
component Card(name: string, count: number, enabled: boolean, href: string) {
  <article class="card" data-enabled={enabled}>
    <h2><a href={href}>{name}</a></h2>
    <p>Itens: {count}</p>
    <input type="checkbox" checked={enabled} aria-label="Ativo" />
  </article>
}

component Dashboard() {
  <main class="dashboard">
    <Card name="Primeiro" count={1} enabled={true} href="#first" />
    <Card name="Segundo" count={2} enabled={false} href="#second" />
  </main>
}
```

O CSS responsivo pertence ao corpus/harness T02, em arquivo associado. Estes exemplos definem fontes e comportamento esperado; não afirmam que a emissão ou a navegação já foi executada.

## 7. Pares válidos e inválidos por diagnóstico

Cada bloco abaixo é um módulo independente. “Válido” significa que satisfaz o contrato ilustrado; futuros testes de parser só comprovarão a parte sintática. Os exemplos semânticos inválidos são sintaticamente reconhecíveis e só poderão ser rejeitados pela validação T04. Nenhum resultado de compilação está sendo apresentado nesta entrega.

### E001 — sintaxe inválida

Válido:

```text
component Greeting() { <p>Olá</p> }
```

Inválido, fechamento diferente da abertura:

```text
component Greeting() { <p>Olá</div> }
```

### E002 — componente desconhecido

Válido:

```text
component Card() { <article /> }
component Page() { <Card /> }
```

Inválido, `Missing` não foi declarado:

```text
component Page() { <Missing /> }
```

### E003 — prop obrigatória ausente

Válido:

```text
component Card(name: string) { <p>{name}</p> }
component Page() { <Card name="Ana" /> }
```

Inválido, falta `name` no uso:

```text
component Card(name: string) { <p>{name}</p> }
component Page() { <Card /> }
```

### E004 — referência inexistente

Válido:

```text
component Greeting(name: string) { <p>{name}</p> }
```

Inválido, `missing` não pertence ao escopo:

```text
component Greeting(name: string) { <p>{missing}</p> }
```

### E005 — ciclo de composição

Válido, grafo sem ciclo:

```text
component Leaf() { <span /> }
component Branch() { <Leaf /> }
component Tree() { <Branch /> }
```

Inválido, ciclo direto `Loop → Loop`:

```text
component Loop() { <Loop /> }
```

Inválido, ciclo indireto `First → Second → First`:

```text
component First() { <Second /> }
component Second() { <First /> }
```

### E006 — recurso fora do subconjunto

Válido, referência simples e URL permitida:

```text
component Greeting(name: string) { <a href="#details">{name}</a> }
```

Inválido, chamada de método:

```text
component Greeting(name: string) { <p>{name.trim()}</p> }
```

Também são exemplos independentes inválidos: `<video />` (tag fora da lista), `<p style="color:red" />` (atributo fora da lista), `<button onclick="run()" />` (`on*`) e `<a href="javascript:alert(1)" />` (URL proibida), quando usados como raiz de um componente. Os exemplos com chamada e entidades não suportadas podem ser rejeitados pelo parser; as restrições HTML/URL pertencem a T04.

### E007 — tipo incompatível

Válido, `number` fornecido como número:

```text
component Count(value: number) { <p>{value}</p> }
component Page() { <Count value={2} /> }
```

Inválido, string fornecida à prop `number`:

```text
component Count(value: number) { <p>{value}</p> }
component Page() { <Count value="2" /> }
```

### E008 — mais de uma raiz

Válido, os dois elementos têm uma raiz comum:

```text
component Pair() { <div><p>A</p><p>B</p></div> }
```

Inválido, dois elementos na raiz do corpo:

```text
component Pair() { <p>A</p><p>B</p> }
```

## 8. Limites desta entrega

Não há sintaxe para imports, eventos, estado, loops, condicionais, funções, objetos, arrays, CSS embutido ou slots. A gramática não é uma licença para aceitar JavaScript arbitrário. Novas formas precisam de decisão registrada e casos de conformidade antes da implementação.

T01 não conclui M0. O corpus completo com expectativas semânticas e harness (T02), parser e AST (T03), validação semântica (T04), emissão (T05), testes no navegador (T06) e reprodução por terceiro (T07) continuam sendo entregas próprias. Nenhuma compatibilidade de navegador/webview, ganho de tokens ou desempenho é demonstrada por este documento.
