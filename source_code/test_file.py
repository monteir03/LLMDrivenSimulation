# this is tehe experimenting file.
import ollama
import threading

# ollama testing
def test_ollama3_inference(prompt):
    # Combine system message and user prompt for ollama
    combined_prompt = "System: You are a helpful assistant designed to output JSON. Always Output only the json object.\nUser: " + prompt
    
    # Make the call to ollama
    response = ollama.chat(model='llama3:latest', messages=[
        {"role": "user", "content": combined_prompt}
    ])
    
    # Extract the response content
    model_output = response["message"]["content"].strip()
    return model_output



# threading testing
def test_ollama3_inference(prompt):
    # Combine system message and user prompt for ollama
    combined_prompt = "System: You are a helpful assistant designed to output JSON.\nUser: " + prompt
    
    # Make the call to ollama
    response = ollama.chat(model='llama3:latest', messages=[
        {"role": "user", "content": combined_prompt}
    ])
    
    # Extract the response content
    model_output = response["message"]["content"].strip()
    print("\nOllama3 Inference Result:\n-------------------------")
    print(model_output)


#*****testing global variables******#
call_count = 0

# Define a function that modifies the global variable
def increment_call_count():
#   global call_count  # Use the global variable call_count, not a new local one -> this test can perturb the real code ! WATHOUT???
    call_count += 1  # Increment the global variable by 1
    print(f"Call count after increment: {call_count}")
   
#####_______ testing with hugging face inference API _______#####
from huggingface_hub import InferenceClient

def huggingface_test():
    # my toekn: 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
    client = InferenceClient(api_key="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")

    messages = [
    	{
    		"role": "user",
    		"content": "What is the capital of France?"
    	}
    ]

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-1B-Instruct", 
    	messages=messages, 
    	max_tokens=500
    )

    print(completion.choices[0].message)

