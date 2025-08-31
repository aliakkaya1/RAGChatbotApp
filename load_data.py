# load_data.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load the API key from the .env file
load_dotenv()
print("API Key loaded.")

# Initialize the embedding model from OpenAI
embeddings = OpenAIEmbeddings()

# --- Function to create and save a vector store ---
def create_and_save_vector_store(urls: list[str], index_name: str):
    """Fetches web content, creates embeddings, and saves them to a local FAISS index."""
    print(f"Loading documents from {len(urls)} URLs for '{index_name}'...")
    
    # The loader fetches the content from all URLs
    loader = WebBaseLoader(urls)
    documents = loader.load()
    
    # Split the documents into smaller chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Split documents into {len(docs)} chunks.")
    
    # Create the FAISS vector store from the documents and embeddings
    print("Creating vector store...")
    db = FAISS.from_documents(docs, embeddings)
    
    # Save the vector store locally
    db.save_local(index_name)
    print(f"Vector store '{index_name}' saved successfully.")

# --- Define the knowledge sources for each domain ---
healthcare_links = ["https://en.wikipedia.org/wiki/Influenza", "https://www.who.int/news-room/fact-sheets/detail/influenza-(seasonal)", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2631512/"]
fashion_links = ["https://en.wikipedia.org/wiki/History_of_denim", "https://www.vogue.com/article/what-is-haute-couture", "https://www.voguecollege.com/articles/how-ai-is-shaping-the-fashion-industry-in-2024/"]

# --- Main execution block ---
if __name__ == "__main__":
    create_and_save_vector_store(healthcare_links, "faiss_index_healthcare")
    create_and_save_vector_store(fashion_links, "faiss_index_fashion")