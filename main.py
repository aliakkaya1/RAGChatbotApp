# main.py

# --- 1. Imports: All your tools go at the top ---
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# --- NEW IMPORTS START HERE ---
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# --- NEW IMPORTS END HERE ---


# --- 2. Initializations: Set up your main variables ---
load_dotenv()
app = FastAPI()
embeddings = OpenAIEmbeddings()
# --- NEW CODE START HERE ---
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# --- NEW CODE END HERE ---


# --- 3. Data Contracts: Define API input/output rules ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    source: str | None


# --- 4. Load Vector Stores on Startup ---
print("Loading vector stores...")
if not os.path.exists("faiss_index_healthcare") or not os.path.exists("faiss_index_fashion"):
    print("ERROR: Vector store indexes not found. Please run load_data.py first.")
    healthcare_db = None
    fashion_db = None
else:
    healthcare_db = FAISS.load_local("faiss_index_healthcare", embeddings, allow_dangerous_deserialization=True)
    fashion_db = FAISS.load_local("faiss_index_fashion", embeddings, allow_dangerous_deserialization=True)
    print("Vector stores loaded successfully.")


# --- 5. Core Logic Functions ---
# --- NEW CODE START HERE ---
def detect_domain(query: str) -> str:
    """
    Uses an LLM to classify the user's query into 'healthcare' or 'fashion'.
    """
    prompt = ChatPromptTemplate.from_template(
        "You are a domain classifier. Classify the following user query into one of "
        "two domains: 'healthcare' or 'fashion'. Respond with only the single word "
        "domain name.\n\nQuery: {query}"
    )
    
    chain = prompt | llm | StrOutputParser()
    domain = chain.invoke({"query": query}).lower()
    
    if "healthcare" in domain:
        return "healthcare"
    elif "fashion" in domain:
        return "fashion"
    else:
        return "general"
# --- NEW CODE END HERE ---
# Add this function in main.py, below the detect_domain function

def retrieve_docs(db: FAISS, query: str, k: int = 3) -> str:
    """
    Retrieves the top-k most relevant document chunks from the specified vector store.
    """
    # Create a retriever from the vector store to search for relevant documents
    # The 'k' parameter specifies how many results to return.
    retriever = db.as_retriever(search_kwargs={"k": k})
    
    # Invoke the retriever to get the documents
    docs = retriever.invoke(query)
    
    # Format the retrieved documents into a single string to use as context
    return "\n\n".join([doc.page_content for doc in docs])
# Add this function in main.py, below the retrieve_docs function

def generate_answer(query: str, context: str, domain: str) -> str:
    """
    Generates a final answer using the LLM with a domain-specific prompt and context.
    """
    # 1. Define custom prompts for each domain
    # These templates instruct the AI on how to behave and what information to use.
    healthcare_prompt_template = """
    You are a helpful assistant specializing in healthcare. 
    Answer the user's query based ONLY on the provided context. 
    If the context does not contain the answer, state that you cannot answer with the available information.

    Context: {context}

    Query: {query}

    Answer:
    """

    fashion_prompt_template = """
    You are a knowledgeable fashion advisor. 
    Answer the user's query based ONLY on the provided context. 
    If the context does not contain the answer, state that you cannot answer with the available information.

    Context: {context}

    Query: {query}

    Answer:
    """

    # 2. Select the appropriate prompt based on the detected domain
    prompt_str = healthcare_prompt_template if domain == "healthcare" else fashion_prompt_template
    
    prompt = ChatPromptTemplate.from_template(prompt_str)
    
    # 3. Create the final chain that combines the prompt, LLM, and output parser
    chain = prompt | llm | StrOutputParser()
    
    # 4. Invoke the chain with the query and retrieved context to get the answer
    answer = chain.invoke({
        "context": context,
        "query": query
    })

    return answer
# --- 6. API Endpoint ---
# Replace your old chat_handler function with this one

@app.post("/chat", response_model=ChatResponse)
def chat_handler(request: ChatRequest):
    # First, check if the vector stores are loaded and ready.
    if healthcare_db is None or fashion_db is None:
        return ChatResponse(answer="Server is not ready, vector stores are missing.", source="server_error")

    query = request.query
    print(f"Received query: {query}")

    # 1. Detect the domain of the query
    domain = detect_domain(query)
    print(f"Detected domain: {domain}")

    # Handle queries that don't fit a domain
    if domain == "general":
        return ChatResponse(answer="I can only answer questions about healthcare and fashion.", source="N/A")

    # 2. Select the correct DB and retrieve context
    if domain == "healthcare":
        db = healthcare_db
        source_used = "Healthcare Documents"
    else: # domain == "fashion"
        db = fashion_db
        source_used = "Fashion Documents"
    
    context = retrieve_docs(db, query)
    print(f"Retrieved context: {context[:500]}...") # Log the first 500 chars

    # 3. Generate the final answer
    answer = generate_answer(query, context, domain)
    print(f"Generated answer: {answer}")

    # Return the final response, fulfilling the API contract
    return ChatResponse(answer=answer, source=source_used)