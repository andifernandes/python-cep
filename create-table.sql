CREATE TABLE enderecos (
    cep TEXT PRIMARY KEY,

    -- dados do endereço (quando sucesso)
    logradouro TEXT,
    complemento TEXT,
    unidade TEXT,
    bairro TEXT,
    localidade TEXT,
    uf CHAR(2),
    estado TEXT,
    regiao TEXT,
    ibge TEXT,
    gia TEXT,
    ddd TEXT,
    siafi TEXT,

    -- controle do processamento
    status TEXT,    -- SUCESSO | ERRO
    mensagem_erro TEXT,
    tentativas INTEGER DEFAULT 1,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--comandos para gerenciar banco
SELECT * FROM enderecos;
SELECT cep, status FROM enderecos;
SELECT COUNT(*) FROM enderecos;
truncate table enderecos;

--verificar atividades do banco
SELECT pid, state, query
FROM pg_stat_activity
WHERE datname = current_database();

--finalizar atividades dobanco
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = current_database()
  AND pid <> pg_backend_pid();