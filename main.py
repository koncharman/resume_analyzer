import streamlit as st
from models.ollama_model import ask_ollama


st.title("AI Resume Analyzer")

st.write("Powered by Ollama + Llama 3.2")


user_input = st.text_area(
    "Enter your question"
)


if st.button("Analyze"):

    if user_input:

        answer = ask_ollama(user_input)

        st.write(answer)