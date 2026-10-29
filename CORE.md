# Dobra — núcleo semântico

Data: 28/10/2026. Documento de decisões; não descreve uma linguagem implementada nem resultados medidos. Nome definido: Dobra; arquivos `.dobra` e CLI planejada `dobra`. A sintaxe experimental está em [GRAMMAR.md](GRAMMAR.md); a implementação do compilador permanece pendente. Leia [SPEC.md](SPEC.md) para os requisitos e a ordem dos marcos. Direção confirmada: open source, comunidade e evolução incremental começando pelo transpiler.

## 0. M0: primeiro transpiler executável

- Uma saída inicial: JavaScript ES modules e CSS, sem dependência obrigatória de React. HTML estático como artefato de build é evolução posterior; o M0 não promete zero JavaScript.
- Entrada mínima: componentes definidos pelo autor, props escalares obrigatórias (`string`, `number`, `boolean`), composição estática de componentes/elementos HTML e expressões restritas a literais e leitura de props. Não executar JavaScript arbitrário para avaliar uma expressão.
- Props são valores capturados na montagem, validados na fronteira pública antes de anexar novos nós. M0 não possui atualização de props, estado reativo, loops dinâmicos, efeitos, eventos próprios, async, SSR, hidratação ou provas. Links e formulários preservam o comportamento nativo do HTML.
- API observável mínima: montar uma árvore em um elemento raiz e descartar essa montagem. `mount` possui apenas os nós que criou; `dispose` remove apenas esses nós e é idempotente. Irmãos pré-existentes não são apagados.
- A saída usa operações DOM que distinguem texto, atributos e propriedades. Texto de props nunca vira HTML executável; atributos booleanos e valores de inputs precisam de tratamento correto.
- Cada chamada de montagem cria novas instâncias. Não há reconciliação nem promessa de preservação de foco/estado entre duas montagens; isso evita simular uma atualização por descarte silencioso.
- CSS mantém sua semântica nativa. Para reduzir escopo, o M0 emite o stylesheet associado como CSS global explicitamente documentado; isolamento automático completo pertence a uma etapa seguinte. O autor continua livre para usar CSS completo.
- Transpilar duas vezes a mesma entrada/configuração produz os mesmos bytes. Artefatos não incluem timestamps ou IDs aleatórios; fixtures recebem nomes estáveis.
- Erros de sintaxe, componente não definido, prop obrigatória ausente, referência inválida ou ciclo direto/indireto de composição bloqueiam a emissão bem-sucedida e indicam arquivo e posição. O diagnóstico de ciclo identifica seu caminho; M0 não admite recursão de componentes nem valida antecipadamente todo comportamento CSS/HTML.
- Critério executável: dois componentes aninhados com props de texto/número/booleano, instâncias independentes e CSS responsivo; montar no browser, conferir DOM/textos, usar teclado e clicar links/controles nativos, descartar e preservar os irmãos da raiz. Executar também os cinco casos de erro acima, incluindo ciclos diretos e indiretos, e a repetição determinística do build.
- A mesma fixture pode servir de smoke test em webview, mas não declara compatibilidade universal sem uma matriz de motores/versões realmente executada.
- Para colaboração: mini-especificação desse subconjunto, exemplos, diagnósticos e corpus de conformidade versionados junto ao compilador. Novas propostas entram com semântica e fixtures, antes de acrescentar features.

### 0.1 Decisões fixadas para o M0

Contrato canônico do M0, detalhado pela [gramática experimental T01](GRAMMAR.md). SPEC.md e CONTEXT.md apontam para esta seção em vez de repeti-la. As decisões valem para o M0 e podem mudar por proposta com corpus e migração.

**Componentes e raiz**

- Tag com inicial maiúscula é componente do mesmo módulo; tag minúscula é elemento HTML. Um nome que não segue essa regra gera diagnóstico.
- Cada componente tem exatamente um nó raiz. Mais de uma raiz gera `E008`. Filhos/slots ficam fora do M0.

**Texto, espaços e entidades**

- Regra no estilo JSX: linhas formadas só por espaços são descartadas; sequências internas de espaços, tabulações e quebras de linha viram um único espaço.
- Entidades aceitas: `&lt;`, `&gt;`, `&amp;`, `&lbrace;` e `&rbrace;`. Outras entidades geram diagnóstico.
- Um `number` vira texto com `String(n)`. `NaN` e `Infinity` (positivo ou negativo) são rejeitados na montagem.

**Elementos, atributos e propriedades**

- O M0 aceita a lista fechada de tags e atributos HTML de [GRAMMAR.md §4](GRAMMAR.md#4-superfície-html-fechada), que guiará o corpus T02. O que estiver fora da lista gera `E006`.
- `value`, `checked`, `disabled` e `selected` são atribuídos como propriedades DOM. `value` exige string nas tags suportadas; as outras três exigem boolean. Os demais atributos usam `setAttribute`, sujeitos às regras de presença abaixo.
- Atributos booleanos do HTML seguem presença: `false` remove o atributo. `aria-*` e `data-*` recebem os textos `"true"` ou `"false"`.
- Na inicialização, `checked`, `disabled` e `selected` sincronizam propriedade e presença do atributo. Interações, agrupamentos de controles e mudanças posteriores seguem o comportamento nativo do HTML; não há controle reativo no M0.
- Propriedades são aplicadas após atributos e filhos. `select.value` tem precedência sobre a seleção inicial das opções; `textarea` não combina `value` com conteúdo. `input type="file"` fica fora do M0. Casos de normalização nativa e conflitos estão definidos em GRAMMAR.md.

**Segurança**

- Atributos `on*` são rejeitados.
- URLs aceitam apenas `http:`, `https:`, `mailto:`, `tel:`, fragmento (`#...`) e caminhos relativos ao documento ou à raiz. Literais são verificados na compilação; valores vindos de props, na montagem. A checagem ocorre após decodificar a fonte e rejeita controles, barras invertidas e referências `//host`; o algoritmo está em GRAMMAR.md §4.

**API exportada**

- Cada componente exporta `mountX(root, props)`, em que `X` é o nome do componente, e a chamada devolve `dispose`.
- As props são validadas antes de criar qualquer nó. Uma prop inválida lança `DobraPropError` sem anexar nada à raiz.
- A montagem insere seu nó no fim de `root`. `dispose` remove apenas esse nó e é idempotente.
- Prop ausente em uso interno é diagnóstico de compilação (`E003`); valor inválido vindo de JavaScript é `DobraPropError` na montagem.

**Diagnósticos e build**

- Os códigos `E001`–`E008` estão registrados em [DIAGNOSTICS.md](DIAGNOSTICS.md), com status. Um código publicado não é reutilizado com outro significado.
- O build é determinístico: a entrada é normalizada para LF antes da análise, e diagnósticos e artefatos usam caminhos relativos à raiz do projeto.

**Implementação**

- Compilador em TypeScript, com parser recursivo descendente escrito à mão e AST com intervalos de origem (offset, linha e coluna).
- O corpus de conformidade é formado por pares `.dobra` + `.expected.json`, independentes da implementação, para sobreviver a uma troca futura de stack.

As seções 1–9 são direção do núcleo futuro e registram pontos de extensão. Não são critérios de entrega do M0 nem motivo para bloquear seu primeiro transpiler.

### 0.2 Direção de produto e caminho para editores

Decisão de 28/10/2026: CRM/ERP é o primeiro cenário de validação de webapps. Dobra continua sendo uma linguagem geral de UI, com um caminho de evolução para editores visuais com interação contínua. Esse requisito não declara suporte ou desempenho equivalentes aos de um editor existente.

- O M0 mantém a saída JavaScript ES modules + CSS com operações DOM. Reatividade granular é a direção de M1: atualizar os consumidores de um estado preservando identidade, foco e ciclo de vida. Seus ganhos dependem de testes e medições.
- Componentes são definidos pelo autor. Tabelas, formulários e fluxos de CRUD pertencem a bibliotecas; não delimitam a linguagem.
- O modelo de estado e as regras de domínio futuros devem ser independentes dos nós DOM. Uma seleção poderá alimentar um painel HTML e uma superfície gráfica por adaptadores explícitos. Recursos de renderização ficam sob responsabilidade do adaptador.
- Uma região externa tem proprietário e ciclo de vida definidos. Dobra não modifica os descendentes ou recursos controlados pelo adaptador; o descarte da região libera os listeners, tarefas e recursos que ela criou. O contrato deve permitir notificar alterações e limpar a integração.
- Parser e validação ficam separados da emissão DOM. Preservar essa separação não exige construir uma representação universal de renderização no M0.
- A integração prevista em M2 pode hospedar uma superfície canvas com motor gráfico próprio, mantendo menus e formulários em HTML. Canvas, WebGL/WebGPU, Workers e Wasm serão escolhidos por necessidade e ambiente; não são dependências obrigatórias. Componentes HTML/CSS não são automaticamente convertíveis em desenhos canvas.

O teste de evolução em [SPEC.md §5](SPEC.md#5-evolução-incremental) deverá exercitar seleção compartilhada entre canvas e painel DOM, atualizações em ambas as direções e descarte independente. Essa verificação pertence a M2, após o estado e os eventos de M1, e não amplia o escopo do M0.

## 1. Abrangência e unidade de composição

- A unidade básica é um componente definido pelo autor, com entradas tipadas, saídas/eventos e composição de filhos. Não há catálogo obrigatório de componentes visuais.
- Elementos HTML, SVG e capacidades do ambiente devem ser acessíveis. Canvas, bibliotecas externas e recursos específicos de webviews entram por integrações explícitas, sem exigir uma nova primitiva de linguagem para cada biblioteca.
- O núcleo descreve estrutura, estado e comportamento. Roteamento, design systems, formulários e acesso a dados são bibliotecas sobre esse núcleo; nenhuma delas deve ser condição para montar um componente.
- O mesmo componente pode ser montado em parte de uma página existente ou compor uma aplicação inteira. A integração recebe um elemento raiz e devolve um identificador para descarte; no M0 esse identificador é a função `dispose` (§0.1). Atualização pelo identificador é posterior ao M0.
- “Universal” significa uma base comum com capacidades declaradas por ambiente. Não significa que uma API nativa exista em todos os motores ou que toda biblioteca web funcione em qualquer webview.

## 2. Identidade e ciclo de vida

- A identidade de uma instância combina o local de montagem, o tipo do componente e uma chave explícita quando houver coleção dinâmica. Uma chave identifica uma entidade entre irmãos; não é o índice visual da lista.
- Reordenar uma coleção com chaves preserva estado, foco e identidade dos elementos correspondentes quando sua espécie não muda. Remover a chave ou trocar o tipo descarta a instância anterior.
- Chaves duplicadas geram diagnóstico; desenvolvimento deve falhar de modo visível, e a compilação deve rejeitá-las quando puder demonstrar a duplicação.
- Identificadores usados por agentes para localizar nós no código são distintos das chaves de instâncias em execução. Um ID de edição não pode alterar silenciosamente a preservação de estado.
- Descartar uma instância remove assinaturas e listeners pertencentes a ela, executa limpezas e invalida entregas assíncronas pendentes. A operação de descarte deve ser idempotente.

## 3. Estado, valores derivados e atualização

- Estado pertence a um escopo explícito: instância, árvore compartilhada ou serviço externo. Estado global implícito entre requisições de servidor é proibido.
- No núcleo verificável, valores observáveis mudam por operações da linguagem. Mutações arbitrárias em objetos importados não devem ser tratadas como automaticamente reativas.
- Valores derivados são funções puras de entradas e estado: não escrevem estado, não fazem IO e não alteram o DOM. Cache e eliminação de recomputações devem preservar o valor observável.
- Dependências de uma derivação são as leituras observáveis da sua avaliação atual. Dependências anteriores que deixaram de ser lidas são removidas. Escritas não devem causar avaliações recursivas parcialmente concluídas.
- Uma ação síncrona agrupa suas escritas em uma atualização. Leituras feitas pela própria ação enxergam suas escritas; derivados usados nessas leituras refletem os valores atuais. O DOM é atualizado após a ação, antes dos efeitos posteriores à atualização.
- Um `await` encerra o trecho síncrono: a continuação inicia outra atualização. Não há atomicidade implícita entre rede, servidor e interface.
- Ciclos demonstráveis entre derivações são rejeitados. Ciclos descobertos apenas em execução produzem diagnóstico identificável, sem permitir um loop infinito silencioso.

## 4. Eventos e efeitos

- Eventos têm payload tipado e executam handlers de forma síncrona até o primeiro ponto assíncrono. Operações dependentes do gesto do usuário e controle da ação padrão do evento precisam permanecer nesse trecho síncrono.
- Efeitos conectam estado a sistemas externos: DOM imperativo, timers, assinaturas, rede e armazenamento. Exigem um proprietário de ciclo de vida e admitem função de limpeza.
- A limpeza anterior ocorre antes da próxima execução do mesmo efeito e também no descarte. Não deve depender de uma renderização futura para acontecer.
- O efeito comum executa depois da atualização do DOM. Leitura de geometria e ajuste antes da pintura exigem uma capacidade específica, com custo e ordem documentados; não são o comportamento de todo efeito.
- Erros de efeitos e handlers assíncronos chegam a um mecanismo explícito de tratamento. Falhas não podem desaparecer porque uma Promise foi descartada.
- Ordenação entre efeitos independentes não é contrato de negócio. Uma dependência real deve ser expressa por dados ou sequenciamento explícito.

## 5. Ações assíncronas: políticas separadas

| Política | Semântica proposta | Caso decisivo de avaliação |
|---|---|---|
| `single` | Por instância da ação, nova invocação enquanto há execução ativa não inicia trabalho e devolve um resultado explícito de ocupação. | Dois cliques no mesmo ciclo iniciam apenas uma execução. |
| `latest` | A nova execução invalida a entrega das anteriores e solicita seu cancelamento quando o adaptador permite. Só a execução ainda atual pode publicar resultado/erro em seu recurso gerenciado. | Respostas fora de ordem preservam o resultado da consulta mais recente. |
| `parallel` | Todas as execuções podem publicar em destinos próprios; não existe um único resultado mutável compartilhado implícito. | Duas tarefas independentes mantêm seus IDs e resultados. |

- A política é declarada por ação; não há um padrão que tente adivinhar a intenção. A validação rejeita uma ação assíncrona gerenciada sem política.
- Argumentos são capturados na invocação como valores do núcleo. Referências a objetos externos mutáveis exigem um contrato de adaptador e não fornecem a mesma garantia de snapshot.
- Cancelar invalida futuras entregas locais e solicita interrupção cooperativa. Não desfaz efeitos já ocorridos em um servidor, arquivo ou serviço externo.
- `latest` não torna mutações externas seguras: a invalidação protege apenas a publicação gerenciada na UI. Efeitos externos exigem sua própria política de identidade, repetição e compensação.
- O estado de recurso distingue `idle`, `pending`, `success`, `error` e `cancelled`, e contém um ID de execução. Dados anteriores podem ser preservados separadamente durante uma atualização; não ficam indistinguíveis de dados atuais.
- O bloqueio de `single` é estabelecido antes de iniciar o trabalho e liberado na conclusão, falha ou confirmação de encerramento do trabalho local após cancelamento. Solicitar cancelamento ou invalidar a entrega à UI, isoladamente, não libera o bloqueio. Isso não garante exclusão mútua de operações no servidor. Desabilitar um botão é apresentação; a proteção também pertence à ação.

## 6. Estilos e liberdade visual

- CSS completo é parte da superfície de autoria, incluindo media queries, variáveis, animações, seletores e layout personalizado. Tokens e componentes de design são conveniências opcionais.
- Estilos locais são o padrão proposto. Seletores globais, fontes, camadas e regras que afetam conteúdo externo precisam de intenção explícita.
- A transformação de isolamento deve ter semântica publicada, especialmente para especificidade, filhos projetados, portais, pseudo-elementos e variáveis herdadas. Não prometer transparência antes de definir esses casos.
- Portais preservam propriedade e ciclo de vida do componente, mas obedecem à árvore DOM real para herança e layout. O compilador não deve fingir que CSS herdado atravessa essa mudança de posição.
- CSS externo e manipulação imperativa do DOM tornam parte do resultado opaca. Contrastes, sobreposições, cliques, foco, responsividade e leitura por tecnologia assistiva exigem avaliação no ambiente real.

## 7. Integração JS/TS e fronteiras de confiança

- Imports externos declaram entradas, saídas, efeitos conhecidos, ambiente permitido e descarte quando aplicável. Tipos estáticos não validam respostas de rede nem objetos desconhecidos em execução.
- Dados externos que entrem em um contrato verificado passam por validação de runtime. Um adaptador deve transformar falhas de validação em um resultado tratável, com localização útil para o agente.
- Integrações imperativas possuem uma região DOM delimitada. O runtime não deve reconciliar simultaneamente os mesmos descendentes que a biblioteca externa controla.
- Código externo permanece utilizável mesmo quando opaco. Nesse caso, otimizações e garantias dependentes do seu comportamento são suspensas naquela fronteira e identificadas no relatório do compilador.
- Acesso a capacidades de webview passa por um adaptador tipado e pelo ciclo de vida da instância. O componente define um fallback ou uma falha explícita para ambientes sem a capacidade.

## 8. Estático, servidor e cliente

- São modos de execução da mesma semântica. Uma árvore comprovadamente estática pode gerar apenas HTML/CSS; interatividade declarada não pode ser eliminada para atingir uma meta de tamanho.
- Renderização de servidor usa contexto por requisição. Referências ao DOM, recursos nativos e efeitos exclusivos do cliente não executam durante essa etapa.
- Transferência de estado do servidor para o cliente aceita um formato tipado e serializável, com codificação segura para HTML. Funções, handles nativos e referências ao DOM não atravessam essa fronteira como dados.
- Ativação no cliente deve preservar estrutura, estado inicial e identidade combinados com o servidor. Divergências produzem diagnóstico, e a estratégia de recuperação deve ser definida antes de declarar suporte a hidratação.
- Incluir no contrato a interação ocorrida antes da ativação: navegação e formulários nativos podem funcionar progressivamente; replay de eventos arbitrários é uma capacidade separada, não uma garantia implícita.
- Saídas para webviews declaram o motor/versão mínimo e capacidades necessárias. Navegador de desktop não é substituto suficiente para a avaliação em uma webview real.

## 9. Contratos e limites de verificação

- Separar quatro mecanismos nos diagnósticos: validação estrutural/tipos, exploração de estados finitos, assertions/testes de execução e provas formais. Aprovar um mecanismo não equivale a aprovar os outros.
- O primeiro subconjunto verificável pode cobrir integridade de referências, ações tipadas, estados e transições declaradas. Garantias devem indicar hipótese, propriedade, fronteira e método utilizado.
- A garantia de um modelo de estado só cobre a aplicação executada se a tradução e o runtime preservarem sua semântica. Até demonstrar essa relação, relatar “modelo verificado”, não “aplicação provada”.
- Uma lei escrita pelo autor não é uma implementação: o compilador precisa rejeitar a violação ou exigir evidência, nunca mudar silenciosamente o comportamento para satisfazer o enunciado.
- Contratos de referência devem ter proteção contra edição junto com a solução durante avaliações. Alterar a lei para acomodar um erro não conta como tarefa bem-sucedida.

## 10. Decisões mínimas antes de cada expansão

1. Fixar a identidade por instância e o comportamento de chaves, desmontagem, foco e portais.
2. Fixar a ordem observável de ações, derivações, atualização do DOM e efeitos; definir erros e ciclos.
3. Fixar o conjunto de valores do núcleo e as regras de mutação, igualdade, snapshots e serialização.
4. Fixar `single`, `latest` e descarte com exemplos de respostas atrasadas; distinguir cancelamento local de reversão externa.
5. Fixar o mecanismo de isolamento CSS e os limites de propriedade DOM para integrações.
6. Publicar capacidades por alvo e o significado exato de cada diagnóstico de verificação.

O M0 precisa apenas da semântica descrita na seção 0, da gramática de seu subconjunto e do formato de saída. As decisões 1–6 acima antecedem os marcos que introduzirem os respectivos recursos. A sintaxe pode evoluir mediante corpus e migração explícita; uma representação curta não basta para demonstrar menor custo total de geração ou execução.
