import os
import sys
from dotenv import load_dotenv

load_dotenv()

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_script_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.rag_pipeline import RAGPipeline
from app.chat_handler import ChatHandler
from app.response_formatter import ResponseFormatter

def main():
    print("Initializing SoochnaGPT Chatbot...")
    
    try:
        rag_pipeline = RAGPipeline()
    except FileNotFoundError as e:
        print(f"Initialization Error: {e}")
        print("Please ensure you have run 'python scripts/data_preparation.py' to generate chunked documents.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during RAG pipeline initialization: {e}")
        sys.exit(1)

    chat_handler = ChatHandler()
    response_formatter = ResponseFormatter()

    print("\nSoochnaGPT is ready! Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        chat_handler.add_message("user", user_input)

        raw_response = rag_pipeline.query(user_input)
        
        formatted_response = response_formatter.format_response(raw_response)

        chat_handler.add_message("assistant", formatted_response)

        print(f"SoochnaGPT: {formatted_response}")

if __name__ == "__main__":
    main()