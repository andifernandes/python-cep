from concurrent.futures import ThreadPoolExecutor
from src.viacep_client import buscar_ceps_por_cidade2
from src.database import inserir_sucesso, get_connection

LOGRADOUROS = [
    "Rua", "Avenida", "Travessa", "Alameda", "Estrada", "Rodovia", "Praca",
    "de", "da", "do", "dos", "das",
    "Sao", "Santa", "Santo",
    "Nossa", "Senhor", "Senhora",
    "Joao", "Jose", "Maria", "Antonio", "Francisco",
    "Carlos", "Paulo", "Pedro", "Lucas", "Marcos",
    "Silva", "Santos", "Oliveira", "Pereira", "Costa",
]

CIDADES = [
    ("SP", "Sao Paulo"),
    ("RJ", "Rio de Janeiro"),
    ("MG", "Belo Horizonte"),
    ("RS", "Porto Alegre"),
]

COMMIT_LOTE = 100


def processar_cidade(uf, cidade):
    conn = get_connection()
    total = 0
    lote = 0
    prefixo = f"[{uf}-{cidade}]"

    print(f"{prefixo} 🚀 Iniciando", flush=True)

    for logradouro in LOGRADOUROS:
        resultados = buscar_ceps_por_cidade2(uf, cidade, logradouro)

        for data in resultados:
            cep = data["cep"].replace("-", "")
            inserir_sucesso(conn, cep, data)

            total += 1
            lote += 1

            print(f"{prefixo} + CEP inserido: {cep} | total={total}", flush=True)

            if lote >= COMMIT_LOTE:
                conn.commit()
                print(f"{prefixo} 💾 commit ({lote})", flush=True)
                lote = 0

    conn.commit()
    conn.close()

    print(f"{prefixo} ✅ Finalizado | total={total}", flush=True)
    return total


if __name__ == "__main__":
    total_geral = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(processar_cidade, uf, cidade)
            for uf, cidade in CIDADES
        ]

        for future in futures:
            total_geral += future.result()

    print(f"\n🎯 TOTAL GERAL INSERIDO: {total_geral}")
