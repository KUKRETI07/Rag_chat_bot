import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

print("Importing rag...")
try:
    from backend.rag import initialize_rag, run_llm
    print("Import successful.")
    print("Initializing RAG...")
    initialize_rag()
    print("RAG Initialized.")
    print("Testing LLM...")
    response = run_llm("What is the handbook about?")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
