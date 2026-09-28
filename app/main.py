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

logger.info("Loading main.py")

app = FastAPI(
    title="Zepto Support Assistant"
)


@app.on_event("startup")
def startup():

    logger.info(
        "Application started"
    )

    try:
        ingest_documents()

    except Exception as e:

        logger.exception(
            f"Startup error: {e}"
        )


@app.get("/")
def root():

    try:

        count = collection.count()

        return {

            "service":
                "Zepto Support Assistant",

            "status":
                "healthy",

            "documents_loaded":
                count
        }

    except Exception:

        return {

            "service":
                "Zepto Support Assistant",

            "status":
                "database unavailable",

            "documents_loaded":
                0
        }


@app.get("/stats")
def stats():

    return {

        "documents_loaded":
            collection.count()
    }


@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(request: QueryRequest):

    logger.info(
        f"Question: {request.question}"
    )

    result = graph.invoke(
        {
            "question":
                request.question
        }
    )

    return AnswerResponse(

        answer=result["answer"],

        sources=result["sources"],

        confidence=result["confidence"]
    )