# this is tehe experimenting file.
import ollama
import threading
import json
import re

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
#call_count = 0

# Define a function that modifies the global variable
def increment_call_count():
#   global call_count  # Use the global variable call_count, not a new local one -> this test can perturb the real code ! WATHOUT???
    #call_count += 1  # Increment the global variable by 1
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

    print(completion.choices[0].message['content'])



def extract_json_str(texto):
    # Localiza a primeira ocorrência de '{' e a última de '}'
    inicio = texto.find('{')
    fim = texto.rfind('}')

    # Verifica se foi encontrada uma estrutura plausível de objeto JSON
    if inicio == -1 or fim == -1 or inicio > fim:
        raise ValueError("Nenhum objeto JSON válido encontrado no texto.")
    
    # Extrai apenas a parte que representa o objeto JSON
    json_str = texto[inicio:fim+1]

    # Agora, ao invés de fazer o parse, simplesmente retorne a string
    return json_str


def clear_invalid_json(json_str):
    # Remove comentários do tipo // até o fim da linha
    json_str = re.sub(r'//[^\n]*', '', json_str)

    # Remove comentários do tipo /* ... */
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    # Opcional: Remover espaços desnecessários após remover comentários
    json_str = json_str.strip()

    return json_str

def extract_and_clear_json_str(texto):
    # Localiza a primeira ocorrência de '{' e a última de '}'
    inicio = texto.find('{')
    fim = texto.rfind('}')

    # Verifica se foi encontrada uma estrutura plausível de objeto JSON
    if inicio == -1 or fim == -1 or inicio > fim:
        raise ValueError("Nenhum objeto JSON válido encontrado no texto.")
    
    # Extrai apenas a parte que representa o objeto JSON
    json_str = texto[inicio:fim+1]

    # Remove comentários do tipo // até o fim da linha
    json_str = re.sub(r'//[^\n]*', '', json_str)

    # Remove comentários do tipo /* ... */
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    # Remove espaços extras
    json_str = json_str.strip()

    return json_str

def test_json():

    test_str = """{
  "name": "Alice", // The user's name
  "age": 30, // The user's age
  /* This is a block comment that is not allowed in JSON */
  "country": "Wonderland"
}
"""
    output = extract_and_clear_json_str(test_str)


    try:
        # Parse the text output into a JSON object
        result_json = json.loads(output)
        print("it worked")
    except json.JSONDecodeError as json_err:
        print(f"JSON Decode Error: {json_err}")
        return None
    
    print(result_json)
    
    return result_json


if __name__ == "__main__":
    test_json()

    