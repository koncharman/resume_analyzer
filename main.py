import streamlit as st

from utils.data_loader import (
    load_skills,
    load_occupations,
    load_relations
)

from rag.document_loader import create_esco_documents
from rag.vector_store import create_vector_store
from rag.rag_chain import ask_rag


def get_occupation_skills(
    occupation_uri,
    relations,
    skills
):

    # Find skills connected to occupation
    occupation_relations = relations[
        relations["occupationUri"] == occupation_uri
    ]

    # Get skill URIs
    skill_uris = occupation_relations[
        "skillUri"
    ].tolist()


    # Retrieve skill information
    matched_skills = skills[
        skills["conceptUri"].isin(skill_uris)
    ]

    return matched_skills

# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------------------------
# Load ESCO data
# -------------------------------------------------

@st.cache_data
def load_data():

    skills = load_skills()
    occupations = load_occupations()
    relations = load_relations()

    return skills, occupations, relations


skills, occupations, relations = load_data()


@st.cache_resource
def create_rag_index(skills, occupations):

    documents = create_esco_documents(
        skills,
        occupations
    )

    vector_store = create_vector_store(
        documents
    )

    return vector_store


vector_store = create_rag_index(
    skills,
    occupations
)

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🤖 AI Resume Analyzer")

st.write(
    "ESCO knowledge base + Ollama local LLM"
)


# -------------------------------------------------
# Tabs
# -------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📚 ESCO Explorer",
        "🤖 LLM Discussion",
        "📄 Resume Analyzer"
    ]
)


# =================================================
# TAB 1 - ESCO EXPLORER
# =================================================

with tab1:

    st.header("📚 ESCO Occupation Explorer")


    st.sidebar.header("Dataset information")

    st.sidebar.write(
        f"Skills: {len(skills)}"
    )

    st.sidebar.write(
        f"Occupations: {len(occupations)}"
    )

    st.sidebar.write(
        f"Relations: {len(relations)}"
    )


    occupation_names = sorted(
        occupations["preferredLabel"]
        .dropna()
        .unique()
    )


    selected_occupation = st.selectbox(
        "Choose an occupation",
        occupation_names
    )


    occupation = occupations[
        occupations["preferredLabel"]
        == selected_occupation
    ].iloc[0]

    occupation_uri = occupation["conceptUri"]

    required_skills = get_occupation_skills(
        occupation_uri,
        relations,
        skills
    )

    st.subheader(selected_occupation)


    st.write(
        occupation["description"]
    )


    with st.expander(
        "Occupation information"
    ):

        st.dataframe(
            occupation.to_frame()
        )

        st.subheader("⭐ Required Skills")

        st.dataframe(
            required_skills[
                [
                    "preferredLabel",
                    "description"
                ]
            ]
        )


    with st.expander(
        "Skills preview"
    ):

        st.dataframe(
            skills.head(20)
        )


    with st.expander(
        "Relations preview"
    ):

        st.write(
            relations.columns.tolist()
        )

        st.dataframe(
            relations.head(20)
        )


# =================================================
# TAB 2 - LLM DISCUSSION
# =================================================

with tab2:

    st.header("🤖 Discuss with Ollama")


    st.write(
        "Ask questions about occupations, "
        "skills, careers, or learning paths."
    )


    question = st.text_area(
        "Your question",
        placeholder=
        "Example: What should I learn to become this professional?"
    )

    if st.button("Ask Ollama"):

        if question:

            with st.spinner(
                    "Thinking..."
            ):

                answer = ask_rag(
                    vector_store,
                    question
                )

            st.subheader(
                "Answer"
            )

            st.write(
                answer
            )

        else:
            st.warning(
                "Please enter a question."
            )


# =================================================
# TAB 3 - RESUME ANALYZER
# =================================================

with tab3:

    st.header(
        "📄 Resume Analyzer"
    )


    uploaded_file = st.file_uploader(
        "Upload your CV",
        type=["pdf"]
    )


    if uploaded_file:

        st.success(
            "Resume uploaded."
        )

        st.info(
            "Next step: extract PDF text and compare with ESCO skills."
        )