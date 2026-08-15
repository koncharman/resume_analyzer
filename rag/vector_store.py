
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings


class SentenceTransformerEmbeddings(Embeddings):

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)


    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings.tolist()


    def embed_query(self, text):
        embedding = self.model.encode(
            text
        )

        return embedding.tolist()



def get_embeddings():

    return SentenceTransformerEmbeddings(
        "all-MiniLM-L6-v2"
    )



def create_vector_store(documents):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store



def get_retriever(vector_store):

    return vector_store.as_retriever(
        search_type="similarity",  # search_type="mmr" "similarity"

        search_kwargs={
            "k": 5, #"k": 5
            #"fetch_k": 5,
            "score_threshold": 0.3
        }
    )

