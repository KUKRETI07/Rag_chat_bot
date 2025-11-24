import os
from dotenv import load_dotenv

# LangChain imports (compatible with the fixed versions)
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables
load_dotenv()

# Global variable to store the chain 
rag_chain = None

def initialize_rag():
    global rag_chain
    
    pdf_path = "combined_handbook.pdf"
    if not os.path.exists(pdf_path):
        print(f"Warning: {pdf_path} not found. RAG will not work.")
        return

    print("Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=60
    )
    chunks = text_splitter.split_documents(documents)

    print("Creating embeddings...")
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"}
    )

    print("Creating Vector Store...")
    persist_directory = "./chroma_db_handbook"
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="handbook_data"
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    print("Initializing LLM...")
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Warning: MISTRAL_API_KEY not found in environment variables.")
        api_key = "dummy_key"  # to prevent crash on init
    
    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.1,
        api_key=api_key
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert assistant for the company handbook. "
                "Answer the user's question only based on the provided context:\n\n{context}"
            ),
            ("human", "{input}")
        ]
    )

    document_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    print("RAG Pipeline Ready!")

def run_llm(prompt: str) -> str:
    global rag_chain
    if rag_chain is None:
        initialize_rag()
        if rag_chain is None:
            return "Error: RAG pipeline is not initialized. Please check server logs."
    
    try:
        response = rag_chain.invoke({"input": prompt})
        return response["answer"]
    except Exception as e:
        return f"Error running RAG: {str(e)}"

# Optional: initialize on module load
# initialize_rag()
