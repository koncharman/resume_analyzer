# AI Resume Analyzer

An AI-powered career analysis application that combines **ESCO (European Skills, Competences, Qualifications and Occupations) skill and occupation data**, **retrieval-augmented generation (RAG)**, **local LLM inference with Ollama**, and **Streamlit** to explore occupations and skills, answer career questions, and analyze uploaded resumes.

## Overview

The project demonstrates how structured domain knowledge can be combined with vector retrieval and LLMs.

## Architecture
```mermaid
flowchart TD

    A["🤖 AI Resume Analyzer"]

    A --> B["📚 ESCO Explorer"]
    A --> C["💬 Career Assistant"]
    A --> D["📄 Resume Analyzer"]

    B --> E["Occupation Lookup"]
    E --> F["Skill Relationships"]
    F --> G["ESCO Knowledge"]

    C --> H["User Question"]

    D --> I["Upload CV"]
    I --> J["Resume Parsing"]
    J --> K["Extracted Skills"]

    G --> L["RAG Pipeline"]
    H --> L
    K --> L

    L --> M["Document Loader"]
    M --> N["Embeddings"]
    N --> O["Vector Store"]
    O --> P["Retriever"]

    P --> Q["Relevant ESCO Context"]
    Q --> R["Prompt Construction"]
    R --> S["🦙 Ollama"]
    S --> T["Career Recommendations"]

    classDef app fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef rag fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef llm fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;

    class A,B,C,D app;
    class L,M,N,O,P,Q,R rag;
    class S,T llm;
```

## Main Features

### ESCO Explorer
- Browse occupations and descriptions.
- Retrieve related skills through ESCO relationships.
- Inspect occupation-skill mappings and URIs.

### RAG Career Assistant
Ask natural-language career questions. The system retrieves relevant ESCO documents first, formats them into context, and then asks Ollama to answer using that retrieved knowledge.

### Resume Analyzer
Upload a CV and analyze it against ESCO knowledge for:
- detected skills;
- related occupations;
- skill gaps;
- recommended skills;
- possible career directions.


## ESCO Data

Expected source files (create data/ and retrieve data from ESCO):

```text
skill_en.ods
occupations_en.ods
occupationSkillRelations.ods
skillSkillRelations_en.ods
```

## Ollama

Example model:

```text
llama3.2:3b
```

Pull it with:

```bash
ollama pull llama3.2:3b
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run main.py
```

## Testing

```bash
python -m pytest -v
```

## Technologies

- Python
- Streamlit
- pandas
- ESCO
- LangChain
- sentence-transformers
- vector retrieval
- Ollama
- pytest


