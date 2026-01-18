import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="bancodedados",
        user="postgres",
        password="senhaforte",
        port=5432
    )
    conn.set_client_encoding("UTF8")
    return conn


def inserir_cep(cep):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO enderecos (cep)
        VALUES (%s)
        ON CONFLICT (cep) DO NOTHING
        """,
        (cep,)
    )

    conn.commit()
    cur.close()
    conn.close()


def buscar_ceps_pendentes(limit=10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT cep FROM enderecos
        WHERE status IS NULL
        LIMIT %s
        """,
        (limit,)
    )

    ceps = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ceps


def atualizar_sucesso(cep, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE enderecos SET
            logradouro = %s,
            complemento = %s,
            bairro = %s,
            localidade = %s,
            uf = %s,
            estado = %s,
            regiao = %s,
            ibge = %s,
            gia = %s,
            ddd = %s,
            siafi = %s,
            status = 'SUCESSO',
            atualizado_em = NOW()
        WHERE cep = %s
        """,
        (
            data.get("logradouro"),
            data.get("complemento"),
            data.get("bairro"),
            data.get("localidade"),
            data.get("uf"),
            data.get("estado"),
            data.get("regiao"),
            data.get("ibge"),
            data.get("gia"),
            data.get("ddd"),
            data.get("siafi"),
            cep
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def atualizar_erro(cep, mensagem):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE enderecos SET
            status = 'ERRO',
            mensagem_erro = %s,
            tentativas = tentativas + 1,
            atualizado_em = NOW()
        WHERE cep = %s
        """,
        (mensagem, cep)
    )

    conn.commit()
    cur.close()
    conn.close()


def inserir_sucesso(conn, cep, data):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO enderecos (
            cep, logradouro, complemento, bairro, localidade,
            uf, estado, regiao, ibge, gia, ddd, siafi,
            status, criado_em, atualizado_em
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            NULL, NOW(), NOW()
        )
        ON CONFLICT (cep) DO NOTHING
        """,
        (
            cep,
            data.get("logradouro"),
            data.get("complemento"),
            data.get("bairro"),
            data.get("localidade"),
            data.get("uf"),
            data.get("estado"),
            data.get("regiao"),
            data.get("ibge"),
            data.get("gia"),
            data.get("ddd"),
            data.get("siafi"),
        )
    )

    inserted = cur.rowcount > 0
    cur.close()
    return inserted
