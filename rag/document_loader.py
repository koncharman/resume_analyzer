
from langchain_core.documents import Document


def create_esco_documents(
    skills,
    occupations
):
    """
    Convert ESCO skills and occupations
    into separate LangChain documents.
    """

    documents = []


    # -----------------------------
    # Occupation documents
    # -----------------------------

    for _, occupation in occupations.iterrows():

        text=occupation['preferredLabel']
        '''
        text = f"""
Occupation:
{occupation['preferredLabel']}

Alternative labels:
{occupation.get('altLabels', '')}

Description:
{occupation['description']}
"""
        '''



        documents.append(
            Document(
                page_content=text,
                metadata={
                    "type": "occupation",
                    "name": occupation["preferredLabel"],
                    "uri": occupation["conceptUri"]
                }
            )
        )


    # -----------------------------
    # Skill documents
    # -----------------------------

    for _, skill in skills.iterrows():

        text=skill['preferredLabel']

        '''
        text = f"""
        Skill:
        {skill['preferredLabel']}
        
        Alternative labels:
        {skill.get('altLabels', '')}
        
        Description:
        {skill['description']}
        """
        '''



        documents.append(
            Document(
                page_content=text,
                metadata={
                    "type": "skill",
                    "name": skill["preferredLabel"],
                    "uri": skill["conceptUri"]
                }
            )
        )


    return documents