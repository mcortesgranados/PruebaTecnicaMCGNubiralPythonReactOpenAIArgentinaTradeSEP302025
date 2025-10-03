from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v1.import_export_router import import_export_router
from app.adapters.ai.openai_adapter import OpenAIAdapter
from app.adapters.repositories.import_export_repository_impl import ImportExportRepositoryImpl
from app.application.use_cases.import_export.ask_question import AskImportExportQuestion
from app.adapters.db.session import get_db_session

app = FastAPI()

# Allow all origins (development mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection setup
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

openai_adapter = OpenAIAdapter(api_key=openai_api_key)
repo_impl = ImportExportRepositoryImpl(session_factory=get_db_session)
import_export_use_case = AskImportExportQuestion(openai_adapter, repo_impl)

# Make use_case globally discoverable for router dependency
import_export_use_case = import_export_use_case

app.include_router(import_export_router, prefix="/api/v1/import_export", tags=["import_export"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running with CORS enabled!"}