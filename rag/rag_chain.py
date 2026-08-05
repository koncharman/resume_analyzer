
from models.ollama_model import ask_ollama

from rag.retriever import (
    retrieve_documents,
    format_documents
)


def ask_rag(
    vector_store,
    question
):
    """
    Complete RAG pipeline:
    question -> retrieval -> Ollama
    """


    # Retrieve ESCO information
    documents = retrieve_documents(
        vector_store,
        question
    )


    # Convert documents to context
    context = format_documents(
        documents
    )


    # Create prompt
    prompt = f"""
                You are an AI career advisor.
                
                Use the following ESCO knowledge:
                
                {context}
                
                
                User question:
                {question}
                
                
                Give a practical answer based on the ESCO information.
                """


    # Send to Ollama
    answer = ask_ollama(
        prompt
    )


    return answer