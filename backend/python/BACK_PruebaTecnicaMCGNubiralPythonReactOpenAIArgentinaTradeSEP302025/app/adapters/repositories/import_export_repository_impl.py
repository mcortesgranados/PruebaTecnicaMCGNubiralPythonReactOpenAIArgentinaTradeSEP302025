from sqlalchemy import text
from app.ports.import_export_repository import ImportExportRepository

class ImportExportRepositoryImpl(ImportExportRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def execute_sql(self, sql: str):
        session = self.session_factory()
        try:
            result = session.execute(text(sql))
            # Convierte cada fila en dict usando ._mapping para compatibilidad SQLAlchemy 1.4+
            results = [dict(row._mapping) for row in result]
            return results
        finally:
            session.close()