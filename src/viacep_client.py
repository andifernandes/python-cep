import requests
import time

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return None, f"HTTP {response.status_code}"

    data = response.json()

    if data.get("erro"):
        return None, "CEP não encontrado"

    return data, None


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

def consultar_cep2(cep, tentativas=3):
    url = f"https://viacep.com.br/ws/{cep}/json/"

    for tentativa in range(1, tentativas + 1):
        try:
            response = session.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            if data.get("erro"):
                return None, "CEP inexistente"

            return data, None

        except requests.exceptions.Timeout:
            erro = "Timeout ViaCEP"
        except requests.exceptions.RequestException as e:
            erro = str(e)

        print(f"⚠️ {cep} tentativa {tentativa}/{tentativas} falhou: {erro}", flush=True)
        time.sleep(1)  # backoff simples

    return None, erro


def buscar_ceps_por_cidade(uf, cidade, logradouro="Joao"):
    url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()

    if isinstance(data, dict) and data.get("erro"):
        return []

    return [item["cep"].replace("-", "") for item in data if "cep" in item]


def buscar_ceps_por_cidade2(uf, cidade, logradouro="Rua"):
    url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()

    if isinstance(data, dict) and data.get("erro"):
        return []

    return data


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})

def buscar_ceps_por_cidade3(uf, cidade, logradouro):
    url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"
    r = session.get(url, timeout=10)

    if r.status_code != 200:
        return []

    data = r.json()
    return data if isinstance(data, list) else []



session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

def buscar_ceps_por_cidade4(uf, cidade, logradouro):
    url = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data if isinstance(data, list) else []

    except requests.exceptions.RequestException as e:
        # erro de rede / timeout / reset
        print(
            f"[ERRO VIA CEP] {uf}-{cidade} | {logradouro} | {e}",
            flush=True
        )
        time.sleep(1)  # pequeno backoff
        return []