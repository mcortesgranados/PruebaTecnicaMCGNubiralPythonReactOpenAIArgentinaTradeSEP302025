from abc import ABC, abstractmethod

class ImportExportRepository(ABC):
    @abstractmethod
    def execute_sql(self, sql: str) -> list[dict]:
        pass