import logging

from fastapi import FastAPI

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

    count = 0

    if collection is not None:
        count = collection.count()

    return {
        "status": "healthy",
        "documents_loaded": count
    }


@app.get("/stats")
def stats():

    count = 0

    if collection is not None:
        count = collection.count()

    return {
        "documents_loaded": count
    }
