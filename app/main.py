import logging

from fastapi import FastAPI

from models import (
    QueryRequest,
    AnswerResponse
)

from graph import graph
from ingest import ingest_documents
from db import collection

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zepto Support Assistant"
)


@app.on_event("startup")
def startup():

    logger.info(
        "Application startup initiated"
    )

    try:

        ingest_documents()

        count = collection.count()

        logger.info(
            f"Documents loaded: {count}"
        )

    except Exception as e:

        logger.exception(
            f"Startup error: {e}"
        )


@app.get("/")
def root():

    try:

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

        return {
            "documents_loaded": collection.count()
        }

    except Exception:

        return {
            "documents_loaded": 0
        }


@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(request: QueryRequest):

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
