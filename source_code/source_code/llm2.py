import ollama
from huggingface_hub import InferenceClient
import subprocess

global gpt_call_count
gpt_call_count = 0

client = InferenceClient(api_key="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")

def gpt_model_call(prompt, model='ollama_llama3'):
    model_config = {
        'hugging_face': ("meta-llama/Llama-3.2-1B-Instruct", 2000),
        'ollama_llama3': ("llama3:latest", 5000),  # Example llama3 model from Ollama
        'llama_cpp': ("/Users/gmonteiro/Documents/INESCTEC/code/gemma2b_gguf_2/Gemma2B-Tuned-2.5B-F16.gguf", 128)  # Example llama.cpp model
    }
    model_name, max_tokens = model_config.get(model)

    # This global variable is used to keep track of the number of calls made to the GPT model
    global gpt_call_count
    gpt_call_count += 1  # Increment the call count by 1

    if model == 'ollama_llama3':
        # Combine system message and user prompt for Ollama
        combined_prompt = "System: You are a helpful assistant designed to output JSON. \nUser: " + prompt
        model_output = ollama.chat(model=model_name, messages=[
            {"role": "user", "content": combined_prompt}
        ])
        model_output = model_output["message"]["content"].strip()

    elif model == 'hugging_face':
        combined_prompt = "System: You are a helpful assistant designed to output JSON. \nUser: " + prompt
        messages = [
            {"role": "user", "content": combined_prompt}
        ]

        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens
        )

        model_output = completion.choices[0].message['content']

    elif model == 'llama_cpp':
        # Running llama.cpp model
        combined_prompt = f"System: You are a helpful assistant designed to output JSON. \nUser: {prompt}"
        model_output = infer_llama_cpp(model_path=model_name, prompt=combined_prompt, num_tokens=max_tokens)

    else:
        raise ValueError(f"Model '{model}' does not exist.")

    return model_output

def infer_llama_cpp(model_path, prompt, num_tokens=128):
    """
    Run inference with llama.cpp using llama-cli with a gguf model you can take it from huggig face repo.
    """
    command = [
        "/Users/gmonteiro/Documents/INESCTEC/code/llama.cpp/llama-cli",  # Path to llama-cli executable
        "-m", model_path,  # Model path
        "-p", prompt,  # Prompt to be inferred
        "-n", str(num_tokens)  # Number of tokens to generate
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"llama.cpp failed with error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running llama.cpp: {e}")
        return None

# Example usage:
