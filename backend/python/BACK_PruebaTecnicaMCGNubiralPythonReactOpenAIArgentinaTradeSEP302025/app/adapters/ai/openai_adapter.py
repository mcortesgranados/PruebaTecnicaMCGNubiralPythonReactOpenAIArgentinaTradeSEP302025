import openai
import re

class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def extract_select_sql(self, text: str) -> str:
        """
        Busca la primera línea que comienza con SELECT (ignorando espacios y comentarios).
        Si falta el FROM argentina_import_export, lo agrega al final del SELECT.
        Hace post-procesado para agregar GROUP BY si es necesario.
        """
        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("select"):
                # Si ya tiene un FROM, retorna tal cual
                if "from" in line.lower():
                    sql = line
                else:
                    sql = f"{line} FROM argentina_import_export"
                # POSTPROCESADO: Añade GROUP BY si es necesario
                sql = self.add_group_by_if_needed(sql)
                print(f"SQL generado: {sql}")
                return sql
        return ""

    def add_group_by_if_needed(self, sql: str) -> str:
        """
        Si hay funciones de agregación y columnas no agregadas, añade GROUP BY automáticamente.
        """
        # Chequea si ya tiene GROUP BY
        if "group by" in sql.lower():
            return sql

        # Busca el SELECT ... FROM ... (ignora el WHERE y demás por simplicidad)
        select_match = re.match(r"select\s+(.*?)\s+from\s+.*", sql, re.IGNORECASE)
        if not select_match:
            return sql  # No se puede parsear bien

        select_columns = select_match.group(1)
        columns = [col.strip() for col in select_columns.split(",")]

        # Detecta columnas no agregadas (sin paréntesis)
        group_by_columns = []
        for col in columns:
            # Si no contiene función de agregación (sum, count, avg, min, max)
            if not re.search(r"\b(sum|count|avg|min|max)\s*\(", col, re.IGNORECASE):
                # Si tiene un alias (AS), toma solo la parte antes de AS
                base_col = col.split(" as ")[0].strip()
                group_by_columns.append(base_col)

        # Si hay columnas para GROUP BY y hay alguna función de agregación
        if group_by_columns and any(re.search(r"\b(sum|count|avg|min|max)\s*\(", col, re.IGNORECASE) for col in columns):
            sql += " GROUP BY " + ", ".join(group_by_columns)
        return sql

    def generate_sql(self, question: str) -> str:
        prompt = (
            "Tabla disponible y su esquema:\n"
            "argentina_import_export(\n"
            "  id_registro INT AUTO_INCREMENT PRIMARY KEY,\n"
            "  fecha DATE NOT NULL,\n"
            "  operacion VARCHAR(20) DEFAULT NULL, -- solo puede ser 'impo' o 'expo'\n"
            "  clae2 VARCHAR(20) DEFAULT NULL,\n"
            "  clae3 VARCHAR(20) DEFAULT NULL,\n"
            "  clae6 VARCHAR(20) DEFAULT NULL,\n"
            "  letra VARCHAR(1) DEFAULT NULL,\n"
            "  empresas DOUBLE DEFAULT NULL,\n"
            "  total_fob DOUBLE DEFAULT NULL,\n"
            "  total_cif DOUBLE DEFAULT NULL\n"
            ")\n"
            "Reglas IMPORTANTES para la consulta SQL:\n"
            "- Usa solo los campos listados.\n"
            "- Si usas funciones de agregación como SUM, COUNT, AVG, etc. y también incluyes columnas no agregadas, SIEMPRE incluye la cláusula GROUP BY con esas columnas.\n"
            "- No incluyas comas extra antes de FROM.\n"
            "- No generes comentarios, explicaciones ni texto adicional.\n"
            "- La consulta debe ser completamente válida para MySQL con ONLY_FULL_GROUP_BY habilitado.\n"
            "- Si la pregunta pide comparar importaciones y exportaciones por año, incluye ambas columnas en el GROUP BY.\n"
            "- Si la pregunta es ambigua, asume la agregación y agrupación más natural según la pregunta.\n"
            "Ejemplos:\n"
            "1. Total de exportaciones por año:\n"
            "SELECT YEAR(fecha) AS anio, SUM(total_fob) AS total_exportaciones FROM argentina_import_export WHERE operacion = 'expo' GROUP BY anio;\n"
            "2. Total de importaciones por clae2:\n"
            "SELECT clae2, SUM(total_fob) AS total_importaciones FROM argentina_import_export WHERE operacion = 'impo' GROUP BY clae2;\n"
            "3. Total exportaciones e importaciones por año:\n"
            "SELECT YEAR(fecha) AS anio, operacion, SUM(total_fob) AS total FROM argentina_import_export GROUP BY anio, operacion;\n"
            "Pregunta: " + question
        )
        try:
            print("Enviando prompt a OpenAI...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un experto en SQL. Devuelve solo el SQL, sin texto adicional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                timeout=30
            )
            print("Respuesta recibida de OpenAI.")
            raw_sql = response.choices[0].message.content.strip()
            sql = self.extract_select_sql(raw_sql)
            if not sql:
                raise ValueError("No se generó una consulta SELECT válida.")
            return sql
        except Exception as e:
            print(f"Error generando SQL: {e}")
            raise RuntimeError(f"Error generando SQL: {e}")