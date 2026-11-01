# Como atualizar os preços (rotina automática)

Este arquivo descreve a rotina semanal que mantém o `ias.json` em dia.
O app Android **Guia de IAs** baixa o `ias.json` deste repositório toda vez que abre.

## Regras

1. Para cada IA do `ias.json`, confira os planos e preços **atuais** (pesquisa na web; prefira a página oficial de preços e, para o Brasil, valores em R$ cobrados oficialmente).
2. Campos de preço de cada plano:
   - `brl`: preço oficial em reais por mês (só quando a empresa cobra em R$ no Brasil).
   - `usd`: preço em dólares por mês. Se só existir em dólar, deixe sem `brl`: o app converte pela cotação do dia + IOF.
   - `0` em `brl` = plano grátis.
3. Mude só o que tiver fonte confiável. Na dúvida, mantenha o valor e acrescente na `obs` "(verifique)".
4. Planos novos ou extintos: adicione/remova o plano. IA nova muito famosa pode entrar; não remova IAs sem motivo forte.
5. Sempre que algo mudar, atualize `"atualizado"` (AAAA-MM-DD) e, se quiser, `cotacaoReserva` (cotação USD/BRL recente).
6. Rode `python3 validar.py` antes de publicar. Só faça commit se der OK.
7. Mensagem de commit: `Preços atualizados em AAAA-MM-DD: <resumo curto das mudanças>`.
8. Se nada mudou, não faça commit.

## Formato

Mantenha a estrutura existente (chaves, categorias e formatação com 2 espaços). Não use crases nem `${` nos textos.
