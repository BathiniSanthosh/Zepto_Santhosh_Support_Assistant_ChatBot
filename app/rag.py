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

        question_lower = question.lower().strip()

        if any(topic in question_lower for topic in BLOCKED_TOPICS):

            return {
                "answer": (
                    "I am a Zepto Support Assistant. "
                    "Please ask questions about Zepto orders, "
                    "refunds, deliveries, subscriptions, payments, "
                    "or customer support."
                ),
                "sources": [],
                "confidence": 0.0
            }

        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:

            return {
                "answer": (
                    "Sorry, I could not find relevant information "
                    "in the Zepto knowledge base."
                ),
                "sources": [],
                "confidence": 0.0
            }

        sources = [
            meta.get("source", "unknown")
            for meta in metadatas
            if meta
        ]

        return {
            "answer": documents[0],
            "sources": sources,
            "confidence": 0.90
        }

    except Exception as e:

        logger.exception("Retrieval failed")

        return {
            "answer": f"An unexpected error occurred: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }