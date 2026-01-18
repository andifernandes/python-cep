import time
from concurrent.futures import ThreadPoolExecutor

from src.viacep_client import buscar_ceps_por_cidade4
from src.database import inserir_sucesso, get_connection


# termos de busca com alta taxa de retorno
LOGRADOUROS = [
    # tipos de via
    "Rua", "Avenida", "Travessa", "Alameda", "Estrada", "Rodovia",
    "Viela", "Largo", "Praca", "Passagem", "Quadra", "Caminho",

    # conectores (ALTÍSSIMO retorno)
    "de", "da", "do", "dos", "das",

    # religiosos / históricos
    "Sao", "Santa", "Santo", "Nossa", "Senhor", "Senhora",
    "Padre", "Dom", "Bispo", "Brasil", "Dom", "Governador"

    # nomes próprios muito comuns
    "Joao", "Jose", "Maria", "Antonio", "Francisco",
    "Carlos", "Paulo", "Pedro", "Lucas", "Marcos",
    "Manoel", "Joaquim", "Luiz", "Miguel", "Daniel",

    # sobrenomes campeões
    "Silva", "Santos", "Oliveira", "Pereira", "Costa",
    "Rodrigues", "Alves", "Lima", "Gomes", "Ribeiro",
    "Martins", "Vieira",

    # termos urbanos frequentes
    "Central", "Industrial", "Comercial",
    "Principal", "Nova", "Velha", "Antiga",
    "Centro", "Jardim", "Parque", "Alto", "Baixo"
]

CIDADES = [
    ("SP", "Sao Paulo"),
    ("RJ", "Rio de Janeiro"),
    ("MG", "Belo Horizonte"),
    ("RS", "Porto Alegre"),
    ("BA", "Salvador"),
]

COMMIT_LOTE = 100


def processar_cidade(uf, cidade):
    inicio = time.perf_counter()

    conn = get_connection()
    total = 0
    lote = 0
    prefixo = f"[{uf}-{cidade}]"

    print(f"{prefixo} 🚀 Iniciando", flush=True)

    for logradouro in LOGRADOUROS:
        print(f"{prefixo} 🔎 Buscando: {logradouro}", flush=True)

        try:
            resultados = buscar_ceps_por_cidade4(uf, cidade, logradouro)
        except Exception as e:
            print(f"{prefixo} ❌ erro inesperado: {e}", flush=True)
            continue

        for data in resultados:
            cep = data["cep"].replace("-", "")

            if inserir_sucesso(conn, cep, data):
                total += 1
                lote += 1

            print(
                f"{prefixo} + CEP inserido: {cep} | total={total}",
                flush=True
            )

            if lote >= COMMIT_LOTE:
                conn.commit()
                print(f"{prefixo} 💾 commit ({lote})", flush=True)
                lote = 0

    conn.commit()
    conn.close()

    fim = time.perf_counter()
    duracao = fim - inicio

    print(
        f"{prefixo} ✅ Finalizado | total={total} | tempo={duracao:.2f}s",
        flush=True
    )

    return total


if __name__ == "__main__":
    inicio_geral = time.perf_counter()
    total_geral = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(processar_cidade, uf, cidade)
            for uf, cidade in CIDADES
        ]

        for future in futures:
            total_geral += future.result()

    fim_geral = time.perf_counter()

    print(
        f"\n🎯 TOTAL GERAL INSERIDO: {total_geral} "
        f"| tempo total={fim_geral - inicio_geral:.2f}s"
    )
