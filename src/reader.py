import os
import pandas as pd

from src.viacep_client import consultar_cep
from src.database import atualizar_sucesso, atualizar_erro


CAMINHO_ENTRADA = "data/ceps_entrada.csv"
CAMINHO_SUCESSO = "data/ceps_sucesso.csv"
CAMINHO_ERRO = "data/ceps_erro.csv"


def garantir_pasta():
    os.makedirs("data", exist_ok=True)


def ler_ceps_csv(caminho, limite=10_000):
    df = pd.read_csv(caminho, dtype=str)
    df = df.head(limite)

    # espera coluna chamada "cep"
    if "cep" not in df.columns:
        raise ValueError("CSV precisa conter a coluna 'cep'")

    return df["cep"].str.replace("-", "").tolist()


def processar_ceps(ceps):
    registros_sucesso = []
    registros_erro = []

    for i, cep in enumerate(ceps, start=1):
        print(f"🔎 [{i}/{len(ceps)}] Consultando CEP {cep}", flush=True)

        data, erro = consultar_cep(cep)

        if erro:
            atualizar_erro(cep, erro)
            registros_erro.append({
                "cep": cep,
                "erro": erro
            })
        else:
            atualizar_sucesso(cep, data)
            registros_sucesso.append(data)

    return registros_sucesso, registros_erro


def salvar_csv(dados, caminho):
    if not dados:
        return

    df = pd.DataFrame(dados)
    df.to_csv(caminho, index=False, sep=";", encoding="utf-8")


if __name__ == "__main__":
    garantir_pasta()

    print("📥 Lendo CSV de entrada...")
    ceps = ler_ceps_csv(CAMINHO_ENTRADA)

    print(f"🚀 Iniciando validação de {len(ceps)} CEPs")
    sucesso, erro = processar_ceps(ceps)

    print("💾 Salvando arquivos de saída...")
    salvar_csv(sucesso, CAMINHO_SUCESSO)
    salvar_csv(erro, CAMINHO_ERRO)

    print("\n✅ PROCESSO FINALIZADO")
    print(f"✔ Sucessos: {len(sucesso)}")
    print(f"❌ Erros: {len(erro)}")
