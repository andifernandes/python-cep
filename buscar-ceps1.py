from src.viacep_client import buscar_ceps_por_cidade2
from src.database import inserir_cep, inserir_sucesso
from src.database import get_connection

conn = get_connection()

LOGRADOUROS = ["Avenida", "Travessa", "Alameda", "joao", "jose", "maria", "marcio", "marcelo", "lucas"]

for logradouro in LOGRADOUROS:
    
    resultados_cidade = buscar_ceps_por_cidade2("SP", "Sao Paulo", logradouro)

    print("palavra: " + str(logradouro))

    for data in resultados_cidade:
        cep = data["cep"].replace("-", "")
        print(logradouro + " cep: " + str(cep))
        inserir_sucesso(conn, cep, data)

conn.commit()
conn.close()