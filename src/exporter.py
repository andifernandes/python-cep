# src/exporter.py
import json
import xml.etree.ElementTree as ET
from src.database import get_connection
from xml.dom import minidom
import csv
import os


def buscar_enderecos_sucesso():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT cep, logradouro, complemento, bairro, localidade, uf,
               estado, regiao, ibge, gia, ddd, siafi
        FROM enderecos
        WHERE status = 'SUCESSO'
    """)

    colunas = [desc[0] for desc in cur.description]
    dados = [dict(zip(colunas, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()
    return dados


def exportar_json(caminho="output/enderecos.json"):
    dados = buscar_enderecos_sucesso()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def exportar_xml(caminho="output/enderecos.xml"):
    dados = buscar_enderecos_sucesso()
    root = ET.Element("enderecos")

    for item in dados:
        e = ET.SubElement(root, "endereco")
        for k, v in item.items():
            child = ET.SubElement(e, k)
            child.text = "" if v is None else str(v)

    rough_string = ET.tostring(root, "utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(caminho, "wb") as f:
        f.write(pretty_xml)


def exportar_csv(caminho="output/enderecos.csv"):
    dados = buscar_enderecos_sucesso()

    if not dados:
        return

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=dados[0].keys(),
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(dados)


def exportar_ceps_entrada(caminho="data/ceps_entrada.csv"):
    dados = buscar_enderecos_sucesso()

    if not dados:
        return

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["cep"])

        for item in dados:
            writer.writerow([item["cep"]])


def exportar_ceps_sucesso(caminho="data/ceps_sucesso.csv"):
    dados = buscar_enderecos_sucesso()

    if not dados:
        print("⚠️ Nenhum CEP com sucesso encontrado para exportar")
        return

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["cep", "status"])

        for item in dados:
            writer.writerow([item["cep"], 200])

    print(f"✅ CEPs exportados com sucesso: {len(dados)} → {caminho}")