from llm import gpt_model_call
import json
import re

RESET = "\033[0m"  # Reset to default color
# Define color codes
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"



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


class AddingAgent:
    """
    The Adding Agent is responsible only for adding balls to the container.
    """
    def __init__(self):
        self.prompt_template = """You are the Adding Agent in a multi-agent system.

### Task:
You are responsible for adding rows of balls to a 10x10 container matrix.
There are 3 types of balls:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
The container's gravity causes balls to settle at the lowest empty rows, and the total capacity is 10 rows. 

### Objective:
Ensure the container has exactly:
  - **4 number of rows with 1**
  - **3 number of rows with 2**
  - **3 number of rows with 3**

### Action Rules:
**Do not add more than three rows of the same value at once.**
**Do not add more than 10 rows in total.** 

### Action Format:
{
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": <int>,
    "unit_of_weight": <int>
  },
  "reason_for_an_action": "str"
}

# Example Shots:
### Input 
The container state is:
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]

have this information in consideration:
{'number_of_rows_of_**1**_to_add': 0, 'number_of_rows_of_**2**_to_add': 3, 'number_of_rows_of_**3**_to_add': 0}

Add rows to achieve **respecting the rows left to add** to achieve the objectives.

### Output
Provide the answer in a JSON format only without extra characters inside of it:

{
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 2
  },
  "reason_for_an_action": "The container is missing normal balls to meet the objective of 3 rows of weight 2."
}

### Input 
The container state is:
 [0 0 0 0 0 0 0 0 0 0]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]

have this information in consideration:
{'number_of_rows_of_**1**_to_add': 1, 'number_of_rows_of_**2**_to_add': 0, 'number_of_rows_of_**3**_to_add': 0}

Add rows to achieve **respecting the rows left to add** to achieve the objectives.

###Output:
Provide the answer in a JSON format only without extra characters inside of it:

{
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 2
  },
  "reason_for_an_action": "The container is missing one row 1 balls"
}

### Input:
The container state is:
[0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]

have this information in consideration:
{'number_of_rows_of_**1**_to_add': 0, 'number_of_rows_of_**2**_to_add': 0, 'number_of_rows_of_**3**_to_add': 3}

Add rows to achieve **respecting the rows left to add** to achieve the objectives.

###Output:
Provide the answer in a JSON format only without extra characters inside of it:

{
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 3
  },
  "reason_for_an_action": "The container is missing light and heavy balls to meet the objective of 4 rows of weight 1 and 3 rows of weight 3."
}

### Input:
The container state is:
{{input_text}}

have this information in consideration:
{{update_info}}


Add rows to achieve **respecting the rows left to add** to achieve the objectives.

### Output:
Provide the answer in a JSON format only without extra characters inside of it:
"""

    def generate_output(self, input_text, update_info, analysis_insights, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{update_info}}", update_info)
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Adding Agent Working{RESET}")
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Input Adding Agent:{RESET}")
        print(f"{RED}***********************{RESET}")
        print(input_text)
        print(update_info)

        try:

            text_output = gpt_model_call(self.prompt, model=model)
            print("the text output before json", text_output)
            text_output = extract_and_clear_json_str(text_output)
            print("the text output after json", text_output)
        except Exception as e:
            print(f"Error: {e}")
            return None

        try:
            # Parse the text output into a JSON object
            result_json = json.loads(text_output)
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            return None

        # Write the JSON data to a file
        with open('adding_agent_decision.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print(f"{BLUE}Result:{RESET}\n")
        print(f"{BLUE}***********************{RESET}") 
        print(input_text)
        return result_json


class MixingAgent:
    """
    The Mixing Agent is responsible for deciding whether to shake or stop the process.
    """
    def __init__(self):
        self.prompt_template = """You are the Mixing Agent in a multi-agent system. 

        
You are responsible for adding rows of balls to a 10x10 container matrix.
There are 3 types of balls:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
The container's gravity causes balls to settle at the lowest empty rows, and the total capacity is 10 rows. 

### Objective:
You will receive as input the current state of the container represented as a 10x10 matrix and external insights about it.
With that information, you will perform your share or stop action to achieve a well-mixed distribution of balls. You should answer in the output format that is given to you.
You should answear in the output format.

### Actions:
1. **Shake the Container**:
   - If the container has exactly 10 rows filled, you can shake it to mix balls of different weights.
   - Output Format: {"action": "shake", "parameters": {}}

2. **Stop**:
   - If the container has exactly 10 rows filled and the distribution of balls is well mixed, you should stop the process.
   - Output Format: {"action": "stop", "parameters": {}}

### Action Rules:
- If the container has exactly 10 rows filled:
  - The action **"add_balls"** must not be used.
  - Decide between **"shake"** or **"stop"** based on the mixing state and insights provided.

# Output Format
For example, you provide the output in this format after you receive the input (matrix and insights):
Input example:
// Current state of the container, with exactly 10 rows filled.
Output example:
{"reason_for_an_action": "", "action": "shake", "parameters": {}}

### Input:
You shall pay attention to the following insights: {{analysis_insights}}
The container state is:
{{input_text}}

You should now finish the output, and only generate one action. Generate only the JSON Output Format:

###Output:
"""


    def generate_output(self, input_text, analysis_insights, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        #self.prompt = self.prompt.replace("{{agent_objective}}", self.agent_objective)
        self.prompt = self.prompt.replace("{{analysis_insights}}", analysis_insights)
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Mixing Agent Working{RESET}")
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Input Mixing Agent:{RESET}")
        print(f"{RED}***********************{RESET}")
        print(self.prompt)

        try:
            text_output = gpt_model_call(self.prompt, model=model)
            text_output = extract_and_clear_json_str(text_output)
        except Exception as e:
            print(f"Error: {e}")
            return None

        try:
            # Parse the text output into a JSON object
            result_json = json.loads(text_output)
        except json.JSONDecodeError as json_err:
            print(f"JSON Decode Error: {json_err}")
            return None

        # Write the JSON data to a file
        with open('mixing_agent_decision.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print(f"{BLUE}Result:{RESET}\n")
        print(f"{BLUE}***********************{RESET}")
        print(input_text)
        return result_json


class ObservationAnalysisAgentWithTool:
    """the output of the observation analysis agent is a summarized observation of the current situation"""
    def __init__(self):
        self.prompt_template = """You are the Observation Agent in a multi-agent system. Your task is to analyze the state of the container and determine which agent should be activated: the Adding Agent or the Mixing Agent.



### Context:
- The container is a 10x10 matrix filled from the bottom (row 1) to the top (row 10).
- There are 3 types of balls with different weights:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
- **0** indicates an empty cell in the matrix.

### Your Task:
The matrix is **complete: There are not 0 in the matrix**.
The matrix is **incomplete: There are 0 in the matrix**.
If the container is incomplete you call **Adding Agent**.
If the container is complete you call the **Mixing Agent**.


### Example Shots:
### Input 
1.
The container state is:
[
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
]

Now, add rows of balls in order to achieve the objectives:

### Output 
Provide the answer in a JSON format only:

{
  "state": incomplete,
  "agent_to_call": "Adding Agent"
}

2.
### Input 
The container state is:
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]


Now, add rows of balls in order to achieve the objectives:

### Output
Provide the answer in a JSON format only:

{
  "state": incomplete,
  "agent_to_call": "Adding Agent"
}

3.
### Input 
The container state is:
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [3 3 3 3 3 3 3 3 3 3]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]

Now, add rows of balls in order to achieve the objectives:

### Output
Provide the answer in a JSON format only:

{
  "state": complete,
  "agent_to_call": "Mixing Agent"
}

### Input:
{{input_text}}

### Output:
Provide the answer in a JSON format only:
"""


    def generate_output(self, input_text, model):
        #self.prompt = self.prompt_template.replace("{{agent_objective}}", self.agent_objective)

        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        #self.prompt = self.prompt.replace("{{delta_mixing_index}}", delta_mixing_index)
        # Print with green color
        print(f"\n\n{GREEN}***********************{RESET}")
        print(f"{GREEN}Observation Agent Working (Using Tool){RESET}")
        print(f"{GREEN}***********************{RESET}")
        print(f"{GREEN}Input Observation Agent:\n{RESET}")
        print(f"{GREEN}***********************{RESET}")
        print(input_text)

        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None
        print(f"{BLUE}Result:{RESET}\n")
        print(f"{BLUE}***********************{RESET}")
        print(text_output)
        return text_output

