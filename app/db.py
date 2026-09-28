import logging
import chromadb

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("Loading db.py")

try:

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="zepto_docs"
    )

    logger.info("ChromaDB connected")

except Exception as e:

    logger.exception(
        f"Database initialization failed: {e}"
    )

    collection = None