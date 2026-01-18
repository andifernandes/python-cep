# Software Python Console para tratamento de CEPs Brasil com Pandas

Este projeto é um **software em Python executado via console** para **coleta, validação, persistência e exportação de CEPs do Brasil**, utilizando a **API pública ViaCEP**, **PostgreSQL**, **paralelismo com threads** e **Pandas** para leitura de dados em CSV.

O sistema foi desenvolvido com foco em **performance, organização de código, controle de erros, logs e reprocessamento**, atendendo aos requisitos de um teste técnico.

---

## 📌 Funcionalidades

### ✅ Coleta massiva de CEPs
- Busca CEPs por **UF, cidade e logradouros**
- Lista otimizada de termos com alta taxa de retorno
- Integração com a API ViaCEP

### ⚡ Paralelismo
- Processamento concorrente com `ThreadPoolExecutor`
- Uma thread por cidade
- Controle individual de tempo e volume por thread

### 💾 Persistência em banco
- Banco de dados: **PostgreSQL**
- Controle de status:
  - `SUCESSO`
  - `ERRO`
  - `PENDENTE`
- Commit em lote para melhor performance
- Evita duplicidade de CEPs

### 🔁 Validação de CEPs
- Reprocessa CEPs pendentes
- Atualiza status conforme retorno da API
- Trata:
  - Timeouts
  - Erros de rede
  - CEPs inválidos

### 📄 Exportação de dados
Exportação dos CEPs válidos para:
- JSON (identado)
- XML (identado)
- CSV completo (endereços)
- CSV apenas com CEPs válidos (`data/ceps_sucesso.csv`)
- CSV de erros (`data/ceps_erro.csv`)

### 📊 Logs e métricas
- Log por cidade
- Log por thread
- Tempo de execução por cidade
- Tempo total do processamento
- Quantidade de CEPs inseridos por cidade

---

## 🧠 Arquitetura do Projeto
```plaintext
python-cep/
│
├── src/
│ ├── database.py # Conexão e operações no banco
│ └── exporter.py # Exportação JSON, XML e CSV
│ └── processor.py # Gera numeros de cep aleatório
│ └── reader.py # Leitura de CSV com Pandas
│ ├── viacep_client.py # Cliente da API ViaCEP
│
├── data/
│ ├── ceps_entrada.csv # CEPs para validação
│ ├── ceps_sucesso.csv # CEPs válidos (status 200)
│ └── ceps_erro.csv # CEPs com erro
│
├── output/
│ ├── enderecos.json
│ ├── enderecos.xml
│ └── enderecos.csv
│
├── buscar-ceps1.py # buscador versão 1
├── buscar-ceps2.py # buscador versão 2
├── buscar-ceps3.py # buscador versão 3
├── buscar-ceps4.py # buscador versão 4 (paralelo com threds)
├── buscar-ceps5.py # buscador versão 5 (paralelo com threds e resultados comparados) (final)
├── cep-exportador.py # Exportação JSON, XML e CSV
├── cep-gerador.py # Gerador de CEPs
├── cep-verificador.py # Validação de CEPs pendentes
├── create-table.sql # Modelo de dados
├── requirements.txt
└── README.md
```

---

## 🚀 Buscador Paralelo

- Executa busca concorrente por cidade
- Commit em lote
- Logs detalhados por thread

### Exemplo de saída:
```plaintext
📊 RESUMO POR CIDADE
[SP-Sao Paulo] ✅ total=2544 | tempo=478.84s
[RJ-Rio de Janeiro] ✅ total=2361 | tempo=456.65s
[MG-Belo Horizonte] ✅ total=2078 | tempo=420.59s
[RS-Porto Alegre] ✅ total=1899 | tempo=414.96s
[BA-Salvador] ✅ total=2482 | tempo=499.52s

🎯 TOTAL GERAL INSERIDO: 11364 | tempo total=499.52s
```

---

## 📥 Leitura de CSV com Pandas

O projeto atende ao requisito de leitura de **10.000 CEPs via CSV** utilizando a biblioteca Pandas.

Exemplo:

```python
import pandas as pd

df = pd.read_csv("data/ceps_entrada.csv", sep=";")
print(df.head())


🧪 Tratamento de Erros

Timeout da API ViaCEP

Erros de rede

Retentativas com backoff

Registro de erros em CSV

Exemplo (data/ceps_erro.csv):

cep;erro
20535030;Timeout ViaCEP


⚙️ Tecnologias Utilizadas

Python 3.10+
Requests
Pandas
PostgreSQL
psycopg2
concurrent.futures
ViaCEP API

📦 Instalação
pip install -r requirements.txt

Buscar CEPs (paralelo):
python buscar-ceps5.py

Validar CEPs pendentes:
python cep-verificador.py

Exportar dados:
from src.exporter import (
    exportar_json,
    exportar_xml,
    exportar_csv,
    exportar_ceps_entrada()
    exportar_ceps_sucesso
)

exportar_json()
exportar_xml()
exportar_csv()
exportar_ceps_entrada()
exportar_ceps_sucesso()


✅ Conclusão
Este projeto demonstra:
Integração com API externa
Processamento concorrente
Persistência em banco de dados
Tratamento robusto de erros
Exportação de dados
Uso de Pandas para leitura de CSV

Aplicável a cenários de engenharia de dados, backend e processamento em lote.
