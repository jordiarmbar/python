-- Eliminar tablas si existen para reiniciar la práctica (opcional)
-- DROP TABLE IF EXISTS log_accesos_voz;
-- DROP TABLE IF EXISTS usuarios_voz;

-- 1. Tabla de Usuarios (Datos Relacionales Estáticos)
-- Almacena la configuración base del usuario y su frase secreta
CREATE TABLE IF NOT EXISTS usuarios_voz (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passphrase_text TEXT NOT NULL, -- Frase secreta transcrita por la IA
    intentos_fallidos INT DEFAULT 0,
    bloqueado_hasta TIMESTAMP NULL -- Para la gestión de bloqueo dinámico
);

-- 2. Tabla de Logs de Acceso (Datos Objeto-Relacionales Dinámicos)
-- Utiliza JSONB para evitar una tabla llena de valores NULL ineficientes.
CREATE TABLE IF NOT EXISTS log_accesos_voz (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios_voz (id) ON DELETE CASCADE,
    fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- La columna resultado_json actuará como una "bolsa dinámica".
    -- Guardará status, confianza, latencia, o motivos de error según el caso.
    resultado_json JSONB NOT NULL
);

-- Comentario: JSONB permite indexación y búsquedas ultrarrápidas.