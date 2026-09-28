import logging

from fastapi import FastAPI

from models import (
    QueryRequest,
    AnswerResponse
)

from graph import graph
from ingest import ingest_documents
from db import collection

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("Loading main.py")

app = FastAPI(
    title="Zepto Support Assistant"
)


@app.on_event("startup")
def startup():

    logger.info("Application startup initiated")

    try:

        ingest_documents()

        count = 0

        if collection is not None:
            count = collection.count()

        logger.info(
            f"Documents loaded into ChromaDB: {count}"
        )

    except Exception as e:

        logger.exception(
            f"Startup error: {e}"
        )


@app.get("/")
def root():

    try:

        count = 0

        if collection is not None:
            count = collection.count()

        return {
            "service": "Zepto Support Assistant",
            "status": "healthy",
            "documents_loaded": count
        }

    except Exception as e:

        logger.exception(
            f"Health check failed: {e}"
        )

        return {
            "service": "Zepto Support Assistant",
            "status": "database unavailable",
            "documents_loaded": 0
        }


@app.get("/stats")
def stats():

    try:

        count = 0

        if collection is not None:
            count = collection.count()

        return {
            "documents_loaded": count
        }

    except Exception as e:

        logger.exception(
            f"Stats endpoint failed: {e}"
        )

        return {
            "documents_loaded": 0
        }


@app.get("/debug")
def debug():

    from pathlib import Path

    try:

        docs_folder = Path(__file__).parent / "docs"

        txt_files = []

        if docs_folder.exists():

            txt_files = [
                file.name
                for file in docs_folder.glob("*.txt")
            ]

        count = 0

        if collection is not None:
            count = collection.count()

        return {
            "docs_folder_exists": docs_folder.exists(),
            "docs_folder_path": str(docs_folder),
            "files_found": txt_files,
            "files_count": len(txt_files),
            "collection_count": count
        }

    except Exception as e:

        logger.exception(
            f"Debug endpoint failed: {e}"
        )

        return {
            "error": str(e)
        }


@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(request: QueryRequest):

    try:

        logger.info(
            f"Question received: {request.question}"
        )

        result = graph.invoke(
            {
                "question": request.question
            }
        )

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )

    except Exception as e:

        logger.exception(
            f"Ask endpoint failed: {e}"
        )

        return AnswerResponse(
            answer=f"Error: {str(e)}",
            sources=[],
            confidence=0.0
        )
