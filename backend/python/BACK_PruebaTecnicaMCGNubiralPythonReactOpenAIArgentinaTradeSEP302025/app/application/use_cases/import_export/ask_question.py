class AskImportExportQuestion:
    def __init__(self, ai_adapter, repo):
        self.ai_adapter = ai_adapter
        self.repo = repo

    def execute(self, question: str):
        sql = self.ai_adapter.generate_sql(question)
        if not sql.strip().lower().startswith("select"):
            raise ValueError("Solo se permiten consultas SELECT.")
        return self.repo.execute_sql(sql)