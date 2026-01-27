CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    foto_data BYTEA NOT NULL,  -- Aquí se guarda la foto original
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);