
from models.ollama_model import ask_ollama

import re

from rag.retriever import (
    retrieve_documents,
    format_documents
)

from utils.esco_relations import get_skill_occupations , get_occupation_skills , get_skill_skills


def sent_split(text):
    split_text = re.split(r'[.,;:·]+', text)#\n

    split_text = [
        part.strip()
        for part in split_text
        if part.strip()
    ]

    return split_text


def ask_rag(
    vector_store,
    question,
    skills,
    occupations,
    relations,
    relations_skills,
    context_input=None,
):
    """
    Complete RAG pipeline:
    question -> retrieval -> Ollama
    """
    documents=[]
    for text in sent_split(context_input):

        # Retrieve ESCO information
        documents_temp = retrieve_documents(
            vector_store,
            text
        )
        documents.extend(documents_temp)

    documents = list(
        {
            doc.metadata["uri"]: doc
            for doc in documents
        }.values()
    )
    # Convert documents to context
    context = format_documents(
        documents
    )

    context="Found ESCO Occupations and Skills:\n\n"+context

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

            context += f"\n\nFor Occupation {doc.metadata['name']}, Related ESCO skills:\n"

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
            #'''
            related_skills = get_skill_skills(skill_uri,relations_skills,skills)

            context += f"\n\nFor Skill {doc.metadata['name']},Related ESCO skills:\n"

            for _, skill in related_skills.iterrows():
                context += (
                    f"- {skill['preferredLabel']}\n"
                )
            #'''


    # Create prompt
    prompt = f"""
                You are an AI career advisor.
                
                Use the following Found and Related European Skills, Competences, Qualifications and Occupations (ESCO) knowledge (ESCO Skills and Occupations):
                Highlight the ESCO Occupations and ESCO Skills with bold.
                {context}
                
                User input:
                {question}
                
                """


    # Send to Ollama
    answer = ask_ollama(
        prompt
    )


    return answer
