import json
from conexion_db import ConexionDB


class AuthDAO:
    def __init__(self):
        self.db = ConexionDB().get_connection()

    def registrar_usuario(self, username, passphrase, log_json):
        cursor = self.db.cursor()
        try:
            # Insertar en tabla rígida
            cursor.execute(
                "INSERT INTO usuarios_voz (username, passphrase_text) VALUES (%s, %s) RETURNING id",
                (username, passphrase)
            )
            u_id = cursor.fetchone()[0]
            # Insertar log dinámico (JSONB)
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (u_id, json.dumps(log_json))
            )
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error en registro: {e}")
            self.db.rollback()
            return False
        finally:
            cursor.close()

    def verificar_login(self, username, frase_dicha, confianza, latencia):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, passphrase_text, intentos_fallidos FROM usuarios_voz WHERE username = %s",
                       (username,))
        user = cursor.fetchone()

        if not user: return "USER_NOT_FOUND"

        u_id, pass_correcta, intentos = user

        if frase_dicha == pass_correcta:
            # ÉXITO: Guardamos log con confianza y latencia
            log = {"status": "OK", "confianza": confianza, "latencia": f"{latencia}s"}
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = 0 WHERE id = %s", (u_id,))
            cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                           (u_id, json.dumps(log)))
            self.db.commit()
            return "SUCCESS"
        else:
            # FALLO: Guardamos intentos restantes en el JSONB
            intentos_restantes = 3 - (intentos + 1)
            log = {"status": "FAIL", "frase_intentada": frase_dicha, "intentos_restantes": intentos_restantes}
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = intentos_fallidos + 1 WHERE id = %s", (u_id,))
            cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                           (u_id, json.dumps(log)))
            self.db.commit()
            return "WRONG_PHRASE"

    def obtener_auditoria(self):
        cursor = self.db.cursor()
        # Consulta que "bucea" en el JSONB
        query = """
            SELECT u.username, l.resultado_json->>'status', l.resultado_json
            FROM log_accesos_voz l
            JOIN usuarios_voz u ON l.usuario_id = u.id
            WHERE l.resultado_json->>'status' = 'FAIL'
            OR (l.resultado_json->>'confianza')::float < 0.6;
        """
        cursor.execute(query)
        return cursor.fetchall()