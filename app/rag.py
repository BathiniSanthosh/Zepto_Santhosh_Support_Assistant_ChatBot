import logging

from db import collection

logger = logging.getLogger(__name__)

BLOCKED_TOPICS = {
    "python",
    "java",
    "cricket",
    "football",
    "movie",
    "netflix",
    "weather",
    "ai"
}


def retrieve(question: str):

    try:

        if collection is None:

            return {
                "answer": "Knowledge base unavailable.",
                "sources": [],
                "confidence": 0.0,
            }

        question_lower = question.lower().strip()

        if any(
            topic in question_lower
            for topic in BLOCKED_TOPICS
        ):
            return {
                "answer": (
                    "I am a Zepto Support Assistant. "
                    "Please ask questions related to Zepto services."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        count = collection.count()

        logger.info(
            f"Documents in collection: {count}"
        )

        if count == 0:

            return {
                "answer": (
                    "Knowledge base is empty. "
                    "No documents have been loaded yet."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        results = collection.query(
            query_texts=[question],
            n_results=min(3, count)
        )

        logger.info(
            f"Query results: {results}"
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        if not documents:

            return {
                "answer": (
                    "Sorry, I could not find relevant information "
                    "in the Zepto knowledge base."
                ),
                "sources": [],
                "confidence": 0.0,
            }

        answer = "\n\n".join(documents)

        sources = list(
            set(
                meta.get("source", "unknown")
                for meta in metadatas
                if meta
            )
        )

        return {
            "answer": answer,
            "sources": sources,
            "confidence": 0.90,
        }

    except Exception as e:

        logger.exception(
            f"Retrieval failed: {e}"
        )

        return {
            "answer": f"Error: {str(e)}",
            "sources": [],
            "confidence": 0.0,
        }
