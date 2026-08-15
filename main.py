import streamlit as st

from utils.data_loader import (
    load_skills,
    load_occupations,
    load_relations,
    load_skill_relations
)

from utils.esco_relations import get_skill_occupations , get_occupation_skills , get_skill_skills
from utils.pdf_reader import extract_pdf_text


from rag.document_loader import create_esco_documents
from rag.vector_store import create_vector_store
from rag.rag_chain import ask_rag


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
    relations_skills= load_skill_relations()
    return skills, occupations, relations , relations_skills


skills, occupations, relations , relations_skills = load_data()


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
        f"Occupation-Skill Relations: {len(relations)}"
    )


    st.sidebar.write(
        f"Skill-Skill Relations: {len(relations_skills)}"
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



    with st.expander(
        "Occupation information"
    ):

        st.dataframe(
            occupation.to_frame()
        )



    with st.expander(
        "Related Skills"
    ):
        st.dataframe(
            required_skills[
                [
                    "preferredLabel",
                    "altLabels",
                    "description"
                ]
            ]
        )


    with st.expander(
        "Related Skills Type"
    ):
        occupation_relations = relations[
            relations["occupationUri"]
            == occupation_uri
            ]

        st.write(
            occupation_relations.columns.tolist()
        )

        st.dataframe(
            occupation_relations
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
                    question,
                    skills,
                    occupations,
                    relations,
                    relations_skills,
                    context_input=question
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

    st.header("📄 Resume Analyzer")

    st.write(
        "Upload a PDF resume. The app will extract its text, "
        "retrieve relevant ESCO skills and occupations, and "
        "ask Ollama to produce a career analysis."
    )

    uploaded_file = st.file_uploader(
        "Upload your CV",
        type=["pdf"],
        key="resume_uploader",
    )

    if uploaded_file is not None:

        st.success(f"Uploaded: {uploaded_file.name}")

        try:
            resume_text = extract_pdf_text(uploaded_file)

        except ValueError as error:
            st.error(str(error))
            resume_text = ""

        except Exception as error:
            st.error(
                f"An unexpected error occurred while reading the PDF: "
                f"{error}"
            )
            resume_text = ""

        if resume_text:

            st.info(
                f"Extracted approximately "
                f"{len(resume_text.split())} words."
            )

            with st.expander("Preview extracted CV text"):
                st.text_area(
                    "Extracted text",
                    value=resume_text,
                    height=350,
                    disabled=True,
                    label_visibility="collapsed",
                )

            analysis_type = st.selectbox(
                "Choose analysis type",
                [
                    "Complete CV analysis",
                    "Suggest suitable occupations",
                    "Identify skills",
                    "Identify missing skills",
                    "Create a learning roadmap",
                    "Generate interview questions",
                ],
                key="resume_analysis_type",
            )

            target_occupation = st.text_input(
                "Target occupation (optional)",
                placeholder=(
                    "Example: AI engineer, data scientist, "
                    "software developer"
                ),
                key="target_occupation",
            )

            additional_request = st.text_area(
                "Additional request (optional)",
                placeholder=(
                    "Example: Focus on skills I should learn "
                    "during the next six months."
                ),
                key="resume_additional_request",
            )

            if st.button(
                    "Analyze CV",
                    key="analyze_resume_button",
                    type="primary",
            ):

                target_text = (
                    target_occupation.strip()
                    if target_occupation.strip()
                    else "No specific target occupation was provided."
                )

                request_text = (
                    additional_request.strip()
                    if additional_request.strip()
                    else "No additional instructions were provided."
                )

                rag_question = f"""
            A CV-Resume was analyzed. 
            Use the previous ESCO information to do what is asked in the following information.
            
            Requested analysis:
            {analysis_type}

            Target occupation:
            {target_text}

            Additional user request:
            {request_text}
            
            Resume:
            {resume_text}
            """

                try:
                    with st.spinner(
                            "Retrieving ESCO knowledge and analyzing CV..."
                    ):

                        answer = ask_rag(
                            vector_store,
                            rag_question,
                            skills,
                            occupations,
                            relations,
                            relations_skills,
                            context_input=resume_text,
                            add_relations=False
                        )

                    st.subheader("Analysis")

                    st.markdown(answer)

                except Exception as error:
                    st.error(
                        "The CV analysis failed. Make sure Ollama "
                        "is running and the selected model is installed."
                    )

                    with st.expander("Technical error"):
                        st.exception(error)

