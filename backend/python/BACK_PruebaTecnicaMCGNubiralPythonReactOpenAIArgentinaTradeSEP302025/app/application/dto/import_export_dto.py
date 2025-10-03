from pydantic import BaseModel

class ImportExportQuestionRequest(BaseModel):
    question: str