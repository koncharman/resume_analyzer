
from rag.vector_store import get_retriever


def retrieve_documents(
    vector_store,
    question
):
    """
    Retrieve relevant ESCO documents
    for a user question.
    """

    retriever = get_retriever(
        vector_store
    )

    documents = retriever.invoke(
        question
    )

    return documents



def format_documents(
    documents
):
    """
    Convert retrieved documents
    into text context for Ollama.
    """

    context = ""

    for doc in documents:

        context += (
            "\n\n"
            + doc.page_content
        )

    return context