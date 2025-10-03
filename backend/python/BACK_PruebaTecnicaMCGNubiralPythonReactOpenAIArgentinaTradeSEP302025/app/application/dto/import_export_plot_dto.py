from pydantic import BaseModel
from typing import Optional

class ImportExportPlotRequest(BaseModel):
    question: str
    x: str
    y: str
    chart_type: Optional[str] = "bar"