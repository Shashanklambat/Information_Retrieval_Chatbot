# This will handle everything to do with the Vector Database
# This will Create, Read, Update and Delete (CRUD)

import os
import faiss
from the_extractor import get_file_contents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


current_dir         = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_FILE_NAME = "vector_db.index"
VECTOR_DB_FILE_PATH = os.path.join(current_dir, VECTOR_DB_FILE_NAME)

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=200,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

embeddings = OllamaEmbeddings(model='all-minilm')
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)


def create_n_save_vector_db() -> None:
    file_contents = get_file_contents()
    
    texts = text_splitter.create_documents(file_contents)
    
    vector_store.add_documents(texts)
    vector_store.save_local(VECTOR_DB_FILE_NAME)


# Always create and save the vector database
create_n_save_vector_db()
print("Vector Database Created")
new_vector_db = FAISS.load_local(VECTOR_DB_FILE_PATH, embeddings, allow_dangerous_deserialization=True)


def similarity_search(query: str) -> list:
    return new_vector_db.similarity_search(query)