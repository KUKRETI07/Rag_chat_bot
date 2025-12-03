import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from dotenv import load_dotenv
from typing import Optional

# --- Configuration & Globals ---
load_dotenv()
PERSIST_DIRECTORY = "./chroma_db_handbook"
PDF_PATH = "combined_handbook.pdf"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" 

rag_chain: Optional[create_retrieval_chain] = None


def get_embeddings_model():
    """Initializes and returns the low-memory HuggingFaceEmbeddings model."""
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"}
    )


def initialize_rag():
    """
    Optimized initialization: checks for persistence first to avoid OOM.
    """
    global rag_chain

    if rag_chain is not None:
        print("RAG Pipeline already initialized.")
        return

    embeddings = get_embeddings_model()
    vector_store = None

    # --- CRITICAL DEPLOYMENT DEBUG CHECK ---
    print(f"DEBUG: Checking for persistence directory: {PERSIST_DIRECTORY}")
    
    # 1. ATTEMPT TO LOAD FROM PERSISTENCE (LOW MEMORY PATH)
    # Check if the directory exists AND contains files
    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print(f"DEBUG: Directory contents found: {os.listdir(PERSIST_DIRECTORY)[:3]}...")
        print(f"Loading existing Vector Store from: {PERSIST_DIRECTORY}...")
        try:
            vector_store = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=embeddings,
                collection_name="handbook_data"
            )
            print("Vector Store loaded successfully from disk (Low Memory Path).")
        except Exception as e:
            print(f"Error loading Chroma from disk: {e}. Proceeding to re-create.")

    # 2. CREATE NEW VECTOR STORE (HIGH MEMORY PATH - Only if load failed)
    if vector_store is None:
        print(f"Vector Store not found or failed to load. Creating new store...")
        # ... (Rest of the high-memory PDF loading and embedding steps)
        # IF THIS CODE RUNS, YOU WILL LIKELY OOM!
        
        if not os.path.exists(PDF_PATH):
            print(f"FATAL ERROR: {PDF_PATH} not found. Cannot build RAG.")
            return

        print("Loading and splitting PDF...")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=60
        )
        chunks = text_splitter.split_documents(documents)
        
        # This is the OOM-causing line if run on Render free tier
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY,
            collection_name="handbook_data"
        )
        
        vector_store.persist() 
        print("New Vector Store created and persisted (HIGH MEMORY USED).")
        
    # --- 3. Initialize LLM and Final Chain (Low Memory) ---
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
         print("Warning: MISTRAL_API_KEY not found.") 
         api_key = "dummy_key"
         
    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.1,
        api_key=api_key
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert assistant... context:\n\n{context}"),
        ("human", "{input}")
    ])

    document_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    print("✅ RAG Pipeline Ready!")


def run_llm(prompt: str) -> str:
    # ... (Keep this function as is)
    global rag_chain
    if rag_chain is None:
        return "Error: RAG pipeline is not initialized. Check server logs for deployment failure."
    # ... (rest of run_llm logic)
    try:
        response = rag_chain.invoke({"input": prompt})
        return response["answer"]
    except Exception as e:
        print(f"Error during RAG invocation: {str(e)}") 
        return f"An internal error occurred while processing your request: {str(e)}"
