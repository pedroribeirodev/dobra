# Dobra — registro de diagnósticos

Códigos estáveis do compilador. Um código publicado não muda de significado; quando deixa de ser emitido, passa a `obsoleto` e não é reutilizado. Contrato em [CORE.md §0.1](CORE.md#01-decisões-fixadas-para-o-m0). Nenhum código é emitido ainda: o compilador não foi implementado.

| Código | Severidade | Significado | Status |
| --- | --- | --- | --- |
| E001 | erro | Sintaxe inválida (por exemplo, tag não fechada ou fechamento trocado) | ativo |
| E002 | erro | Componente desconhecido | ativo |
| E003 | erro | Prop obrigatória ausente em uso interno | ativo |
| E004 | erro | Referência inexistente | ativo |
| E005 | erro | Ciclo de composição, direto ou indireto, com o caminho do ciclo | ativo |
| E006 | erro | Recurso fora do subconjunto M0: expressão não suportada, tag ou atributo fora da lista, `on*`, URL com esquema não permitido | ativo |
| E007 | erro | Tipo incompatível em uso estático de prop | ativo |
| E008 | erro | Componente com mais de um nó raiz | ativo |

Erros de execução na montagem (`DobraPropError`) não são diagnósticos de compilação e não usam esta numeração.
