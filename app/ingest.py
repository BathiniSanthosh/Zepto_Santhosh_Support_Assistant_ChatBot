from pathlib import Path
import logging

from db import collection

logger = logging.getLogger(__name__)

logger.info("Loading ingest.py")


def ingest_documents():

    try:

        if collection is None:
            logger.error(
                "Collection not available"
            )
            return

        if collection.count() > 0:

            logger.info(
                "Documents already exist"
            )

            return

        docs = []
        ids = []
        metadatas = []

        docs_folder = Path("docs")

        if not docs_folder.exists():

            logger.error(
                "docs folder missing"
            )

            return

        for file in docs_folder.glob("*.txt"):

            logger.info(
                f"Reading {file.name}"
            )

            text = file.read_text(
                encoding="utf-8"
            )

            docs.append(text)

            ids.append(file.stem)

            metadatas.append(
                {
                    "source": file.name
                }
            )

        if docs:

            collection.add(
                ids=ids,
                documents=docs,
                metadatas=metadatas
            )

            logger.info(
                f"{len(docs)} documents added"
            )

    except Exception as e:

        logger.exception(
            f"Ingestion failed: {e}"
        )


if __name__ == "__main__":
    ingest_documents()