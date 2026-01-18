import csv
from src.database import buscar_ceps_pendentes, atualizar_sucesso, atualizar_erro
from src.viacep_client import consultar_cep2

ceps = buscar_ceps_pendentes(limit=100)

with open("data/ceps_entrada.csv", "a", newline="", encoding="utf-8") as f_ok, \
     open("data/ceps_erro.csv", "a", newline="", encoding="utf-8") as f_err:

    writer_ok = csv.writer(f_ok)
    writer_err = csv.writer(f_err)

    for cep in ceps:
        data, erro = consultar_cep2(cep)

        if erro:
            atualizar_erro(cep, erro)
            writer_err.writerow([cep, erro])
        else:
            atualizar_sucesso(cep, data)
            writer_ok.writerow([cep])
