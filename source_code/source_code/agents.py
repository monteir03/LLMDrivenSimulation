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
        self.prompt_template = """You are the Adding Agent in a multi-agent system. Your decisions must be supported by insights provided by an Observation Agent.

### Context:
You are responsible for adding rows of balls to a 10x10 container matrix.
There are 3 types of balls:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
The container's gravity causes balls to settle at the lowest empty rows, and the total capacity is 10 rows. 

### Objective:
Ensure the container has exactly:
  - **4 rows of weight 1**
  - **3 rows of weight 2**
  - **3 rows of weight 3**

### Action Rules:
- If the container has fewer than 10 rows filled **"add_balls"** until the container is completely filled with 10 rows.
- Ensure the total number of rows does not exceed 10.
- the number_of_rows_to_add can be 1, 2 or 3 per action.

### Action:
1. **Add Balls**:
Output Format: 
     
{"reason_for_an_action": "str",
  "light_balls_remaining": <int>,
  "normal_balls_remaining": <int>,
  "heavy_balls_left": <int>,
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": <int>,
    "unit_of_weight": <int>
  }
}

# Follow the  Examples

### Input 
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

### Output **"Only the JSON object without extra characters outside of it."**:

{
  "reason_for_an_action": "The container is missing normal balls to meet the objective of 3 rows of weight 2.",
  "light_balls_remaining": 0,
  "normal_balls_remaining": 3,
  "heavy_balls_left": 0,
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 2
  }
}


### Input 
The container state is:
[
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
]

Now, add rows of balls in order to achieve the objectives:

###Output **"Only the JSON object without extra characters outside of it."**:

{
  "reason_for_an_action": "The container is missing light and heavy balls to meet the objective of 4 rows of weight 1 and 3 rows of weight 3.",
  "light_balls_left": 1,
  "normal_balls_left": 0,
  "heavy_balls_left": 3,
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 2
  }
}

### Input:
The container state is:
{{input_text}}

Now, add rows of balls in order to achieve the objectives:

### Output **"Only the JSON object without extra characters outside of it."**:
"""

    def generate_output(self, input_text, analysis_insights, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{analysis_insights}}", analysis_insights)
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Adding Agent Working{RESET}")
        print(f"{RED}***********************{RESET}")
        print(f"{RED}Input Adding Agent:{RESET}")
        print(f"{RED}***********************{RESET}")
        print(input_text)

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
        self.prompt_template = """You are the Mixing Agent in a multi-agent system. Your decisions must be supported by insights provided by an Observation Agent.

### Context:
There is a container structured as a 10x10 matrix that's completely filled. 
Your task is to mix three types of balls—heavy, normal, and light—to achieve a well-mixed distribution. Each cell in the matrix represents the weight of the ball at that position:
There are 3 different types of balls with diferent weights:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
In the matrix a row is empty if it is made by empty cells represented by number 0:
- 0 indicates an empty cell.
The gravity has an effect on balls, and its direction is from row 10 to row 1. So row 1 is the bottom row and row 10 is the top row.
The container is filled row by row from the bottom to the top.
The container can hold up to exactly **10 rows** of balls. The process ends when all rows are filled, and the distribution of balls is well mixed.

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
- The container is considered "full" if **all 10 rows** are completely filled with balls (i.e., no zeroes in the entire 10x10 matrix).
- If there is **at least one empty cell 0** anywhere in the matrix, or if fewer than 10 rows contain balls, the container is considered "not full."
- If the container is not full, the correct agent to call is the "Adding Agent."
- If the container is full, the correct agent to call is the "Mixing Agent."

### Your Task:
1. Check if the container is full or not:
   - **Full**: All 10 rows are filled with no empty cells (no zeroes).
   - **Not Full**: If there is at least one empty cell or fewer than 10 rows of balls.
2. If the container is not full, the correct agent to call is the **Adding Agent**.
3. If the container is full, the correct agent to call is the **Mixing Agent**.

### Important Clarification:
- A completely empty container (all zeroes) is clearly not full, as it contains no balls.

### Step-by-Step Logic for Determining Fullness:
1. Read the entire 10x10 matrix.
2. Check every cell. If **any cell is 0**, then `is_full = false`.
3. If no cells are 0 (meaning all cells have 1, 2, or 3), then `is_full = true`.
4. If `is_full = true`, `agent_to_call = "Mixing Agent"`.
5. If `is_full = false`, `agent_to_call = "Adding Agent"`.

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

