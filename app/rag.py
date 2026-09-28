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
                "confidence": 0.0
            }

        if collection.count() == 0:
            return {
                "answer": (
                    "Knowledge base is empty. "
                    "Please load documents first."
                ),
                "sources": [],
                "confidence": 0.0
            }

        question_lower = question.lower().strip()

        if any(
            topic in question_lower
            for topic in BLOCKED_TOPICS
        ):
            return {
                "answer": (
                    "I am a Zepto Support Assistant. "
                    "Please ask Zepto-related questions only."
                ),
                "sources": [],
                "confidence": 0.0
            }

        results = collection.query(
            query_texts=[question],
            n_results=min(3, collection.count())
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

        if len(documents) == 0:
            return {
                "answer": (
                    "Sorry, I could not find relevant "
                    "information in the knowledge base."
                ),
                "sources": [],
                "confidence": 0.0
            }

        answer = "\n\n".join(documents)

        sources = []

        for meta in metadatas:
            if meta and "source" in meta:
                sources.append(meta["source"])

        return {
            "answer": answer,
            "sources": list(set(sources)),
            "confidence": 0.90
        }

    except Exception as e:

        logger.exception(
            f"Retrieval error: {e}"
        )

        return {
            "answer": f"Error: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }
