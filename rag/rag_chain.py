
from models.ollama_model import ask_ollama

from rag.retriever import (
    retrieve_documents,
    format_documents
)

from utils.esco_relations import get_skill_occupations , get_occupation_skills , get_skill_skills


def ask_rag(
    vector_store,
    question,
    skills,
    occupations,
    relations,
    relations_skills
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

    # Expand using ESCO relationships
    for doc in documents:

        # Occupation document
        if doc.metadata["type"] == "occupation":

            occupation_uri = doc.metadata["uri"]

            occupation_skills = get_occupation_skills(
                occupation_uri,
                relations,
                skills
            )

            context += f"\n\nFor Occupation {doc.metadata['name']}, Required ESCO skills:\n"

            for _, skill in occupation_skills.iterrows():
                context += (
                    f"- {skill['preferredLabel']}\n"
                )


        # Skill document
        elif doc.metadata["type"] == "skill":

            skill_uri = doc.metadata["uri"]

            related_occupations = get_skill_occupations(
                skill_uri,
                relations,
                occupations
            )

            context += f"\n\nFor Skill {doc.metadata['name']}, Related ESCO occupations:\n"

            for _, occupation in related_occupations.iterrows():
                context += (
                    f"- {occupation['preferredLabel']}\n"
                )

            related_skills = get_skill_skills(skill_uri,relations_skills,skills)

            context += f"\n\nFor Skill {doc.metadata['name']},Related ESCO skills:\n"

            for _, skill in related_skills.iterrows():
                context += (
                    f"- {skill['preferredLabel']}\n"
                )


    # Create prompt
    prompt = f"""
                You are an AI career advisor.
                
                Use the following ESCO (European Skills, Competences, Qualifications and Occupations) knowledge:
                
                {context}
                
                
                User question:
                {question}
                
                
                Give a practical answer based on the ESCO information. 
                Highlight with bold the skills and occupations found on user question and the given ESCO knowledge.
                """


    # Send to Ollama
    answer = ask_ollama(
        prompt
    )


    return answer