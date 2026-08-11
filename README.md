# AI Resume Analyzer

An AI-powered career analysis application that combines **ESCO (European Skills, Competences, Qualifications and Occupations) skill and occupation data**, **retrieval-augmented generation (RAG)**, **local LLM inference with Ollama**, and **Streamlit** to explore occupations and skills, answer career questions, and analyze uploaded resumes.

## Overview

The project demonstrates how structured domain knowledge can be combined with vector retrieval and LLMs.

## Architecture
```mermaid
flowchart TD
    ES["📄 ESCO Taxonomy"]
    ES --> ESS["Skills"]
    ES --> ESO["Occupations"]
    ESS --> ESSS["Skill - SKill Relationships"]
    ESS --> ESSO["Skills required in Occupations"]
    ESO --> ESSO

    A["🤖 AI Resume Analyzer"]
    
    A --> B["📚 ESCO Explorer"]
    A --> C["💬 LLM Discussion"]
    A --> D["👤 Resume Analyzer"]

    ES --> B
    B --> E["Occupation Lookup"]
    E --> F["Skills required in Occupation"]

    ES --> ST["Sentence Transformers"]
    ST --> VEC["Vector Store with Skill and Occupation Embeddings"]

    C --> H["User Question"]

    D --> I["Upload CV"]

    H --> J["Document Retrieval"]
    I --> J

    J --> ST

    ST --> ND["New Document Embeddings"]
    ND --> RAG["Extract Occupations and Skills"]
    VEC --> RAG

    RAG --> DS["Find Additional Relevant Occupations and Skills"]
    ES --> DS

    DS --> CX["Create Prompt with Context"]
    RAG --> CX

    OLL["Ollama Model"] --> AN["Generate Answer"]
    CX --> AN
    
    classDef app fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef llmrag fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef io fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;

    class ES,A,B,C,D,DS app;
    class VEC,RAG,OLL,ND llmrag;
    class E,F,H,I,AN io;
```

## Main Features

### ESCO Explorer
- Browse occupations and descriptions.
- Retrieve related skills through ESCO relationships.
- Inspect occupation-skill mappings and URIs.

### LLM Discussion
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


