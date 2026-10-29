# Dobra — orientações de projeto

## Estado atual

- Repositório de desenho e planejamento. O transpiler M0 ainda não foi implementado.
- Leia README.md, SPEC.md e CORE.md antes de propor implementação. Consulte o histórico Git para entender mudanças de decisão.
- Nome definido: Dobra; extensão `.dobra`; CLI planejada `dobra`.
- Eficiência para LLM e desempenho no navegador têm o mesmo peso. Não anunciar ganhos sem evidência reproduzível.
- Licença, stack, gramática exata e matriz de ambientes ainda precisam ser definidas.

## Escopo e decisões

- Priorize o transpiler M0: componentes próprios, props escalares, composição estática, emissão DOM/CSS, montagem e descarte.
- Preserve a abrangência futura: sites, aplicações e webviews; não transformar a linguagem em um catálogo obrigatório de componentes.
- Não ampliar M0 com estado reativo, efeitos, async, SSR ou provas sem registrar a mudança de escopo.
- Questione escolhas de arquitetura e confirme requisitos de escala/distribuição antes de escolher a stack do compilador.
- Mantenha fonte, especificação e corpus de conformidade alinhados. Registre decisões que mudem comportamento observável.

## Implementação e validação

- Variáveis, funções e nomes de arquivos em inglês; comunicação e documentação principal em português do Brasil.
- Faça commits atômicos e descritivos. Preserve alterações de outros contribuidores.
- Build determinístico; erros com código e localização; falhas não devem deixar uma nova saída parcial parecendo válida.
- Montagem e descarte só podem afetar nós da própria montagem. Rejeite ciclos estáticos entre componentes.
- Teste comportamento observável; snapshots do código gerado não bastam para validar semântica DOM.
- Nunca declare uma UI pronta sem abrir no navegador e conferir responsividade, CSS, foco e cliques sem overlays bloqueadores.
- Compatibilidade com webview exige teste em host real e versão registrada.
- Separe checagem de tipos, testes, análise de estados e provas formais. Cada garantia precisa declarar seu alcance.

## Publicação e colaboração

- Não publicar credenciais, dados privados, caminhos locais pessoais ou instruções específicas de uma máquina.
- Não inventar comandos de instalação ou resultados de benchmark. Exemplos de sintaxe sem implementação devem ser identificados como ilustrativos.
- Use CONTRIBUTING.md para tarefas e BENCHMARK.md para avaliações. Atualize o estado do projeto quando um marco for efetivamente concluído.
