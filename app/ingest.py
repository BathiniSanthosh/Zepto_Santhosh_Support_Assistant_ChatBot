from pathlib import Path
import logging

from db import collection

logger = logging.getLogger(__name__)

logger.info("Loading ingest.py")


def ingest_documents():

    try:

        if collection is None:
            logger.error(
                "Collection unavailable"
            )
            return

        current_count = collection.count()

        logger.info(
            f"Current collection count: {current_count}"
        )

        if current_count > 0:
            logger.info(
                "Documents already exist in Chroma"
            )
            return

        project_root = Path(__file__).parent

        docs_folder = project_root / "docs"

        logger.info(
            f"Looking for docs in: {docs_folder}"
        )

        if not docs_folder.exists():

            logger.error(
                f"Docs folder not found: {docs_folder}"
            )

            return

        txt_files = list(
            docs_folder.glob("*.txt")
        )

        logger.info(
            f"Found {len(txt_files)} txt files"
        )

        docs = []
        ids = []
        metadatas = []

        for file in txt_files:

            logger.info(
                f"Reading {file.name}"
            )

            text = file.read_text(
                encoding="utf-8"
            ).strip()

            if not text:
                logger.warning(
                    f"{file.name} is empty"
                )
                continue

            docs.append(text)

            ids.append(file.stem)

            metadatas.append(
                {
                    "source": file.name
                }
            )

        if not docs:

            logger.warning(
                "No documents loaded"
            )

            return

        collection.add(
            ids=ids,
            documents=docs,
            metadatas=metadatas
        )

        logger.info(
            f"{len(docs)} documents inserted"
        )

        logger.info(
            f"Collection count after insert: {collection.count()}"
        )

    except Exception as e:

        logger.exception(
            f"Ingestion failed: {e}"
        )


if __name__ == "__main__":
    ingest_documents()
