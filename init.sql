CREATE TABLE IF NOT EXISTS estudos (
    id SERIAL PRIMARY KEY,
    materia VARCHAR(100) NOT NULL,
    data DATE NOT NULL,
    duracao INTEGER NOT NULL,
    observacoes TEXT
);