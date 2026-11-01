"""Valida o ias.json antes de publicar. Uso: python3 validar.py [ias.json]
Sai com código 1 se encontrar problema (o app não carregaria o arquivo)."""
import json
import re
import sys

arq = sys.argv[1] if len(sys.argv) > 1 else "ias.json"
erros = []
try:
    d = json.load(open(arq, encoding="utf-8"))
except Exception as e:
    print(f"JSON inválido: {e}")
    sys.exit(1)

if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d.get("atualizado", ""))):
    erros.append("campo 'atualizado' deve ser AAAA-MM-DD")
for k in ("cotacaoReserva", "iof"):
    if not isinstance(d.get(k), (int, float)):
        erros.append(f"campo '{k}' deve ser número")

cats = {c.get("id") for c in d.get("categorias", [])}
if not cats:
    erros.append("sem categorias")
ias = d.get("ias", [])
if len(ias) < 10:
    erros.append(f"só {len(ias)} IAs (esperado 25+)")
ids = set()
for ia in ias:
    n = ia.get("id", "?")
    for k in ("id", "nome", "categoria", "site", "resumo"):
        if not isinstance(ia.get(k), str) or not ia.get(k):
            erros.append(f"{n}: falta '{k}'")
    if n in ids:
        erros.append(f"{n}: id repetido")
    ids.add(n)
    if ia.get("categoria") not in cats:
        erros.append(f"{n}: categoria '{ia.get('categoria')}' não existe")
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(ia.get("cor", ""))):
        erros.append(f"{n}: cor inválida")
    planos = ia.get("planos", [])
    if not planos:
        erros.append(f"{n}: sem planos")
    for p in planos:
        if not p.get("nome"):
            erros.append(f"{n}: plano sem nome")
        if p.get("brl") is None and p.get("usd") is None:
            erros.append(f"{n}/{p.get('nome')}: plano sem preço (brl ou usd)")
        for k in ("brl", "usd"):
            if p.get(k) is not None and (not isinstance(p[k], (int, float)) or p[k] < 0 or p[k] > 20000):
                erros.append(f"{n}/{p.get('nome')}: {k} fora do normal ({p[k]})")
    for k in ("comoUsar", "fortes", "limites", "tags", "prompts"):
        if not isinstance(ia.get(k, []), list):
            erros.append(f"{n}: '{k}' deve ser lista")

if erros:
    print("PROBLEMAS:\n- " + "\n- ".join(erros))
    sys.exit(1)
print(f"OK: {len(ias)} IAs, atualizado em {d['atualizado']}")
