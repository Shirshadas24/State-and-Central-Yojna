from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from peft import PeftModel, PeftConfig
import safetensors

FINE_TUNED_MODEL_PATH = os.path.abspath("./fine_tuned_tiny_llama")
BASE_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def load_fine_tuned_model(fine_tuned_path: str):
    print(f"Loading tokenizer from: {fine_tuned_path}")

    if not os.path.isdir(fine_tuned_path):
        print(f"Error: Fine-tuned model directory not found at {fine_tuned_path}")
        print(f"Attempted absolute path: {fine_tuned_path}")
        return None, None

    try:
        tokenizer = AutoTokenizer.from_pretrained(fine_tuned_path)
        
        print(f"Loading base model from Hugging Face Hub: {BASE_MODEL_NAME}")
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            device_map="cpu", 
            torch_dtype=torch.float32,
        )
        
        peft_config = PeftConfig.from_pretrained(fine_tuned_path)
        
        model = PeftModel(model, peft_config)
        
        adapter_model_path = os.path.join(fine_tuned_path, "adapter_model.safetensors")
        if not os.path.exists(adapter_model_path):
            adapter_model_path = os.path.join(fine_tuned_path, "adapter_model.bin")
            if not os.path.exists(adapter_model_path):
                raise FileNotFoundError(f"Neither adapter_model.safetensors nor adapter_model.bin found in {fine_tuned_path}")

        print(f"Loading adapter state dictionary from: {adapter_model_path}")
        if adapter_model_path.endswith(".safetensors"):
            adapter_state_dict = safetensors.torch.load_file(adapter_model_path, device="cpu")
        else: # .bin file
            adapter_state_dict = torch.load(adapter_model_path, map_location='cpu')

        model.load_state_dict(adapter_state_dict, strict=False)

        model.eval()
        
        print("Model and Tokenizer loaded successfully on CPU.")
        return model, tokenizer

    except Exception as e:
        print(f"An error occurred during model loading: {e}")
        return None, None

def generate_chat_response(model, tokenizer, user_input: str, chat_history: list = None, max_new_tokens: int = 150):
    if chat_history is None:
        chat_history = []

    chat_history.append({"role": "user", "content": user_input})

    formatted_chat = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)

    inputs = tokenizer(formatted_chat, return_tensors="pt", padding=True, truncation=True)
    
    inputs = {k: v.to('cpu') for k, v in inputs.items()}

    print(f"\n--- Generating response for input: '{user_input}' ---")
    
    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output_tokens[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    
    chat_history.append({"role": "assistant", "content": response})

    return response

if __name__ == "__main__":
    model, tokenizer = load_fine_tuned_model(FINE_TUNED_MODEL_PATH)

    if model and tokenizer:
        print("\nStarting basic command-line chatbot. Type 'exit' to quit.")
        
        conversation_history = []

        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                print("Chatbot: Goodbye!")
                break
            
            response = generate_chat_response(model, tokenizer, user_input, conversation_history)
            print(f"Chatbot: {response}")
            
    else:
        print("\nFailed to load model and tokenizer. Cannot start chatbot.")