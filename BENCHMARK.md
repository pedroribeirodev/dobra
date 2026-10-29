# Dobra — protocolo de benchmark

**Status:** proposta de avaliação; nenhum benchmark executado e nenhum ganho demonstrado.
**Objetivo:** testar, com igual peso decisório, eficiência para LLMs e desempenho no cliente.
**Escopo:** autoria e manutenção de interfaces gerais, incluindo componentes próprios e interoperabilidade JS/TS. Os marcos seguem [SPEC.md](SPEC.md).

## 0. Fases incrementais para um projeto open source

- **M0 — transpiler:** validar tradução, diagnósticos úteis e saída determinística em um exemplo pequeno com componentes próprios, props e composição estática. Abrir a saída no navegador e verificar conteúdo, montagem/descarte, CSS e interação nativa de links e controles HTML; estado reativo e handlers da linguagem entram em M1.
- O contrato de M0 é funcional: a mesma entrada/configuração produz a mesma saída e o exemplo preserva a semântica esperada. Registrar limitações, casos aceitos e rejeitados de maneira reproduzível.
- M0 pode registrar bytes, tempo e tokens para conferir os instrumentos; não precisa superar React e não sustenta alegação de desempenho.
- **M1/M2 — cobertura:** ampliar exemplos, interatividade, interoperabilidade e cenários de patches conforme a linguagem estabiliza. A comunidade pode contribuir fixtures e contraexemplos segundo contratos públicos.
- **Avaliação comparativa, transversal aos marcos:** executar ensaios somente sobre recursos já suportados; executar o estudo completo abaixo após a cobertura das três fixtures em M2. As três fixtures são plano futuro, não requisitos para entregar o primeiro transpiler.
- Versionar protocolo, datasets sintéticos e critérios junto ao projeto; contribuições novas exigem contratos equivalentes, sem alterar retroativamente a avaliação já registrada.
- Este documento define o protocolo; instrumentos e resultados ainda não foram produzidos.

## 1. Hipóteses e registro prévio

- H1: a linguagem reduz o custo total de geração e manutenção até atingir o mesmo contrato funcional e visual.
- H2: o compilador melhora métricas do cliente sem degradar funcionalidade, acessibilidade ou portabilidade.
- H3: os ganhos persistem em alterações sucessivas, componentes próprios e integração com bibliotecas externas.
- Registrar antes das medições: versões, configurações, hardware, hosts, tarefas, sementes, limites, métricas primárias e margens.
- Os tamanhos e limiares abaixo são hipóteses iniciais, não requisitos confirmados nem resultados.
- Calibrar cargas em um piloto separado; congelar o protocolo antes da amostra usada para decidir.
- Manter dois eixos de aprovação independentes. Economia de tokens não compensa regressão relevante no cliente, ou vice-versa.

## 2. Fixtures e cargas propostas

| Fixture | Contrato e interações | Escalas iniciais, calibráveis |
| --- | --- | --- |
| `content-site` | Site predominantemente estático; navegação, busca/filtro local, menu móvel e formulário interativos; conteúdo acessível sem depender da ativação das interações. | 1/10/50 páginas; 20/200/2.000 itens de busca; 1/3/8 regiões interativas. |
| `workspace-app` | Aplicação com rotas, lista, filtros, seleção, edição, estados assíncronos, cancelamento, respostas fora de ordem e recuperação de erros. | 100/1.000/10.000 registros; 20/100/500 linhas visíveis; sequências de 10/50/200 ações; atrasos de 50/300/1.500 ms. |
| `embedded-webview` | Interface hospedada em uma webview real; navegação, teclado, foco, ciclo de suspensão/retomada e troca de mensagens tipadas com o host. | 50/500/5.000 registros; sessões de 1/5/15 min; rajadas de 1/10/50 mensagens por segundo. |

- Cobrir pelo menos três larguras de viewport e estados vazios, carregando, sucesso e erro pertinentes a cada fixture.
- Incluir CSS próprio, SVG, componente definido pelo usuário e integração JS/TS; catálogo fechado não satisfaz o escopo.
- A aplicação deve incluir uma biblioteca externa funcionalmente equivalente em todos os candidatos.
- Na lista, compartilhar dados, algoritmo e política de virtualização; medir mudanças de algoritmo como experimento separado.
- Na webview, registrar host/engine, versão, dispositivo e integração nativa; usar, por exemplo, WKWebView no host macOS disponível.
- Uma medição em WKWebView não sustenta conclusão sobre Android WebView ou todos os ambientes embarcados.
- Browser responsivo, emulação de dispositivo ou iframe não substituem webview real.
- Sem host real disponível, marcar esse estrato como não avaliado e limitar explicitamente a conclusão de portabilidade.

## 3. Baselines e controles de equivalência

- Baseline principal: implementação idiomática React + TypeScript, com configuração de produção e recursos estáticos quando cabíveis.
- Baseline de compilação: implementação idiomática Svelte, com a mesma semântica, dados, assets e comportamento observável.
- Referência inferior de custo: HTML/CSS/JavaScript mínimo na fixture estática; não exigir sua reimplementação manual de toda aplicação complexa.
- A2UI Express/json-render só entram em subexperimentos de composição declarativa compatível; não tratá-los como equivalentes automáticos a autoria geral.
- Usar versões fixas e públicas disponíveis no ambiente; registrar bibliotecas, flags de produção e saídas geradas.
- Igualar renderização inicial, entrega de conteúdo, compressão, cache, rede, fontes, imagens e política de carregamento por cenário.
- Não conceder otimizações manuais a apenas um candidato. Manter orçamento de revisão e correção equivalente.
- Distinguir dois ensaios: custo da autoria por LLM e custo do artefato aceito executado no cliente.
- Uma referência otimizada manualmente pode orientar desempenho, mas seu custo de autoria não é comparável ao de uma execução da LLM.
- Publicar cada comparação nominalmente; ganho sobre React não significa ganho sobre Svelte, HTML mínimo ou todo frontend.

## 4. Ensaio de geração e manutenção por LLM

- Usar modelos realmente disponíveis; fixar identificação, versão quando exposta, parâmetros, orçamento e ferramentas.
- Aplicar a mesma tarefa semântica, assets, dados e critérios de aceitação a cada linguagem; permitir ferramentas equivalentes.
- Incluir o guia completo necessário à linguagem nova e o contexto equivalente das demais; não omitir esse custo.
- Medir cenário frio e sequência com contexto reutilizado separadamente; explicitar cache e eventual amortização do guia.
- Contabilizar tokens de entrada e saída em todas as chamadas, instruções, histórico, documentação, mensagens de ferramenta e reparos.
- Registrar tokens de raciocínio quando o provedor os expuser; marcar o que não for observável, sem estimar como zero.
- Reportar tokens brutos, tokens cobrados/com cache, custo monetário e tempo; menor cobrança por cache não equivale a menos tokens.
- Usar contagem do provedor quando disponível; declarar tokenizer e método em contagens locais, sem comparar caracteres como tokens.
- Definir orçamento máximo de tokens, tempo e tentativas antes de começar; esgotamento é falha, não exclusão da amostra.
- Registrar sucesso na primeira tentativa, sucesso final, reparos, violações e recursos consumidos em todas as tentativas malsucedidas.
- Reportar taxa de sucesso e custo total da campanha, além do custo condicionado ao sucesso; nenhuma média apenas dos aprovados.

### Sequência de patches

1. Criar a fixture a partir do mesmo briefing e contrato de aceitação.
2. Alterar layout responsivo preservando comportamento e conteúdo.
3. Adicionar um estado assíncrono e modificar uma interação já existente.
4. Extrair/reutilizar um componente e integrar uma chamada JS/TS com falha controlada.
5. Aplicar uma mudança transversal de estilo e uma correção funcional identificada por cenário reproduzível.

- Entregar o repositório resultante da etapa anterior, com o mesmo regime de contexto; não regenerar silenciosamente do zero.
- Registrar tamanho do patch, arquivos tocados, alterações fora do pedido, regressões e custo acumulado da sequência.
- IDs estáveis e diffs menores são métricas diagnósticas; não substituem correção nem economia de tokens.

## 5. Medições no navegador e na webview

- **Entrega:** bytes HTML/CSS/JS transferidos e descomprimidos; separar inicial, interação e rotas adicionais, incluindo dependências.
- **Runtime:** custo de parse/execução, ativação/hidratação quando houver, tarefas longas e trabalho de atualização após cada ação.
- **Experiência:** tempo até conteúdo principal e até primeira interação funcional; latência de cenários de entrada, filtro, seleção e navegação.
- **Interação:** distribuição por cenário, incluindo p50/p95 quando a amostra comportar; usar INP apenas quando a ferramenta e o contexto o suportarem adequadamente.
- **Memória:** base, pico e retenção após sequências repetidas; informar método, coleta de lixo controlada quando possível e diferenças de observabilidade entre engines.
- **Estabilidade:** falhas, travamentos, perda de estado, listeners/recursos retidos e comportamento após suspensão/retomada.
- Medir cold/warm separadamente, fixar condições e alternar a ordem dos candidatos para reduzir efeitos de aquecimento e carga do host.
- Manter latência de rede/API idêntica por semente; não atribuir ao framework economia causada por backend ou dados diferentes.
- Medir tempo e memória de compilação como custo adicional de desenvolvimento, sem confundi-los com performance do cliente.

## 6. Correção, qualidade visual e acessibilidade

- Aceitação funcional comum: mesmas ações, resultados, regras de estado e tratamento das falhas previstas.
- Checar visualmente os mesmos estados e viewports; usar referência comum e revisão cega quando praticável.
- Verificar overflow, legibilidade, hierarquia, posicionamento, conflitos CSS, overlays e clique real nos controles.
- Avaliar teclado, ordem/foco visível, nomes acessíveis, semântica e contraste; auditoria automática complementa revisão humana.
- Falha em requisito obrigatório reprova aquela execução, mesmo que o artefato carregue rapidamente.
- Reportar qualidade junto das métricas de custo; retirar conteúdo, funcionalidades ou acessibilidade não constitui otimização válida.

## 7. Smoke, evidência e decisão

- **Smoke:** uma execução por fixture e cenário para validar instrumentos e contratos; resultados servem ao diagnóstico, sem conclusão de superioridade.
- **Piloto:** repetições limitadas para estimar variância, custo e cargas viáveis; publicar seu papel exploratório separadamente.
- **Estudo:** definir tamanho amostral com a variância do piloto e o efeito mínimo relevante; parear tarefas/sementes e randomizar a ordem.
- Não contar centenas de eventos da mesma execução como centenas de amostras independentes; respeitar agrupamento por tarefa/execução.
- Reportar dispersão e intervalos de confiança, inclusive para falhas; amostra insuficiente produz resultado inconclusivo.
- Publicar por fixture, escala, modelo e host, com valores absolutos e relativos. Não usar média agregada para ocultar regressões.
- **Margens propostas para calibração:** 15% de redução em tokens totais por campanha; 10% na métrica primária do cliente; até 5% de regressão nas métricas protegidas, com tolerância absoluta previamente definida para valores próximos de zero.
- Selecionar previamente uma métrica primária do cliente por fixture: JS entregue para a estática; latência da interação principal para a aplicação; latência de interação/ponte para a webview.
- Uma referência com zero JS impede alegar redução percentual desse valor; avaliar paridade absoluta e registrar ausência de ganho nesse cenário.
- **Sucesso por comparação:** aceitação preservada, sucesso da LLM não inferior dentro da margem registrada e benefício relevante nos dois eixos, sustentado pelos intervalos de confiança e guardrails.
- Uma vantagem apenas em parte das fixtures autoriza uma conclusão restrita àquelas condições, não superioridade geral.
- **Falsificação:** ganho desaparece ao incluir guia/reparos; taxa de falha cresce; patches acumulam regressões; runtime/bytes/memória pioram além da margem; ou interoperabilidade/host real quebra o contrato.
- **Inconclusivo:** intervalos incluem ausência de ganho relevante ou ambiente necessário não foi avaliado; não reinterpretar como aprovação.
- Preservar dados brutos, versões, prompts não sensíveis, configurações, logs de falha e scripts de medição para reprodução futura.

## 8. Piloto antecipado de custo para agentes no subconjunto M0

Objetivo: testar cedo se a sintaxe de Dobra reduz custo para agentes, antes de investir em M1. É um piloto exploratório (§7); não sustenta alegação de superioridade.

- **Candidatos:** Dobra; TSX; HTML com template literal em JavaScript; e TSX compilado pelo mesmo emissor DOM de Dobra. Esse último isola o efeito da sintaxe do efeito do compilador.
- **Tarefas:** criação e alteração de componentes estáticos com props escalares e composição, dentro do que o M0 suporta.
- **Custo do guia:** contar os tokens do guia de Dobra em todo cenário frio, como em §4.
- **Reparo:** injetar erros conhecidos e contar tokens e tentativas até o agente corrigir usando apenas o diagnóstico. Registrar sucesso, reparos e falhas dentro do orçamento.
- **Critério de parada:** se o custo total de Dobra não for menor que o de TSX, nem no ensaio de reparo, revisar a tese antes de iniciar M1. Margens e orçamento seguem §7 e são registrados antes da execução.
