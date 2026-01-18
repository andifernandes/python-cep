from src.viacep_client import buscar_ceps_por_cidade3
from src.database import inserir_sucesso, get_connection
import time

# abre UMA conexão
conn = get_connection()

LOGRADOUROS = [
    # tipos de via
    "Rua", "Avenida", "Travessa", "Alameda", "Estrada", "Rodovia", "Viela", "Largo", "Praca",

    # artigos / conectores (MUITO eficientes)
    "de", "da", "do", "dos", "das",

    # nomes extremamente comuns
    "Sao", "Santa", "Santo",
    "Nossa", "Senhor", "Senhora",

    # nomes comuns
    "Joao", "Jose", "Maria", "Antonio", "Francisco", "Carlos", "Paulo", "Pedro",
    "Lucas", "Mateus", "Marcos", "Marcelo", "Rafael", "Daniel", "Bruno",
    "Ana", "Beatriz", "Julia", "Mariana", "Carolina",

    # sobrenomes comuns
    "Silva", "Santos", "Oliveira", "Pereira", "Costa", "Rodrigues", "Alves", "Lima",
]

CIDADES = [
    ("SP", "Sao Paulo"),
    ("RJ", "Rio de Janeiro"),
    ("MG", "Belo Horizonte"),
    ("RS", "Porto Alegre"),
]

TOTAL_SUCESSO = 0
LIMITE = 10_000

for uf, cidade in CIDADES:
    if TOTAL_SUCESSO >= LIMITE:
        break

    print(f"\n🏙️ Cidade: {cidade} - {uf}")

    for logradouro in LOGRADOUROS:
        if TOTAL_SUCESSO >= LIMITE:
            break

        print(f"🔎 Buscando logradouro: {logradouro}")

        resultados_cidade = buscar_ceps_por_cidade3(uf, cidade, logradouro)
        time.sleep(0.2)

        for data in resultados_cidade:
            if TOTAL_SUCESSO >= LIMITE:
                break

            cep = data["cep"].replace("-", "")
            print(f"{uf}/{cidade} | {logradouro} -> CEP: {cep}")

            inserir_sucesso(conn, cep, data)
            TOTAL_SUCESSO += 1

# commit único
conn.commit()
conn.close()

print(f"\n✅ Total de CEPs inseridos com SUCESSO: {TOTAL_SUCESSO}")
