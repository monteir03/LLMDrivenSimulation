import ollama
global gpt_call_count
gpt_call_count = 0

def gpt_model_call(prompt, model='ollama_llama3'):

    model_config = {
        'gpt-3.5': ("gpt-3.5-turbo-0125", 2700), 
        'gpt-4': ("gpt-4-0125-preview", 2700), #2700 is the max tokens for gpt-4  so is not needed a model with more than that.
        'Llama_2_70B_HF': ('meta-llama/Llama-2-70b-hf', 2000),
        'Mixtral_8x7B_Instruct': ("mistralai/Mixtral-8x7B-Instruct-v0.1", 4048),
        'WizardCoder-Python-34B-V1.0': ("WizardLM/WizardCoder-Python-34B-V1.0", 2000),
        'ollama_llama3': ("llama3:latest", 4000) # Example llama3 model from ollama
    }
    model_name, max_tokens = model_config.get(model)

      # this global variable is used to keep track of the number of calls made to the GPT-4 model
    global gpt_call_count
    gpt_call_count += 1   # increment the call count by 1

    

    if model in ['ollama_llama3']:
        # Combine system message and user prompt for ollama
        combined_prompt = "System: You are a helpful assistant designed to output JSON. \nUser: " + prompt
        model_output = ollama.chat(model=model_name, messages=[
            {"role": "user", "content": combined_prompt}
        ])
        model_output = model_output["message"]["content"].strip()
    else:
        print("model don't exist yet")
    return model_output
