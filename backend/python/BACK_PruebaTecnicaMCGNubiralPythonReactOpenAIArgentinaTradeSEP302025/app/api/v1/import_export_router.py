from fastapi import APIRouter, HTTPException, Depends
from app.application.dto.import_export_dto import ImportExportQuestionRequest
from app.application.use_cases.import_export.ask_question import AskImportExportQuestion
from starlette.concurrency import run_in_threadpool

import_export_router = APIRouter()

def get_use_case():
    # Lazy import to avoid circular dependencies
    from app.main import import_export_use_case
    return import_export_use_case

@import_export_router.post("/query")
async def query_import_export(
    request: ImportExportQuestionRequest,
    use_case: AskImportExportQuestion = Depends(get_use_case)
):
    try:
        # This will run the blocking code in a thread, freeing up the event loop
        results = await run_in_threadpool(use_case.execute, request.question)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))