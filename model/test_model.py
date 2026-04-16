import os
import json
from analyze_document import analyze_document

def run_test():
    """
    Simple testing framework designed to locally instantiate the model orchestrations.
    We are piping in one of the existing sample files to test extraction, embeddings, and NLP.
    """
    
    # Locate one of our baseline AI/ML sample references mapped inside sample_data natively.
    test_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'sample_data', 
        'reference_articles', 
        'article2.txt'
    ))
    
    print(f"[*] Commencing integrated AI testing framework.")
    print(f"[*] Targeting test file payload: {test_file}\n")
    print("[*] Instantiating Transformers, initializing NLP layers... (May take a few moments)\n")
    
    result = analyze_document(test_file)
    
    print("\n============== EVALUATION RESULTS ==============\n")
    print(json.dumps(result, indent=2))
    print("\n================================================")

if __name__ == "__main__":
    run_test()
