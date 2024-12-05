from llm import gpt_model_call
import json

# Red color ANSI escape code
RED = "\033[91m"
RESET = "\033[0m"  # Reset to default color

# Define color codes
GREEN = "\033[92m"
RESET = "\033[0m"  # Reset to default color

class SimpleDecisionAgent:
    '''action: add_balls, shake, stop, each action has it's parameters
     add_balls: row_number, unit_of_weight ;
     shake: no parameters; -> meaning shake action is 1 shake.
     stop: no parameters; -> meaning stop action is 1 stop.

     '''
    
    def __init__(self):
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]



Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.   

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
The goal is to mix the balls of different weights by strategically adding rows and utilizing the shaking action to achieve a homogenous distribution of all types of balls within the container.
In total, you need add 4 rows of light balls, 3 rows of normal balls, and 3 rows of heavy balls to complete the process. The container must be filled with exactly 10 rows of balls by the end of the process.

You will receive the input of the current container state and need to provide an action to perform as action in output.
For example:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
{"action": "", "parameters": {}} //You should decide an action in JSON format.

You should now finish the output:
Input:
{{input_text}}
Output:"""


    def generate_output(self, input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        print(input_text)#
        print("***********************")
        print("Simple GPT Working")
        print("***********************")
        try:
            text_output = gpt_model_call(self.prompt, model=model)
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
        with open('simple_decision_agent.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print(text_output)
        return result_json


class SituationAnalysisAgent:
    '''
    this is more like a observation agent'''
    def __init__(self):
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]


Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
The goal is to mix the balls of 3 different weights by strategically adding rows and utilizing the shaking action to achieve a homogenous distribution of all types of balls within the container.
In total, you need add 4 rows of light balls, 3 rows of normal balls, and 3 rows of heavy balls to complete the process. The container must be filled with exactly 10 rows of balls by the end of the process.

You will receive the input of the current container state and please concisely describe the current situation in terms of:
- The current state of the container.
- The number of rows filled and how many more rows are required to complete the process.
- Describing the 2-dimensional distribution of the different types of balls in the container.
- Make an conclusion about whether the types of the balls are well mixed or not.
- Highlight one important aspects of the current situation to achieve the objective described above.

For example, you provide the summarized description in this format after you receive the input:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
// Your summarized description of the current situation within 60 words.

You should now finish the output:
Input:
{{input_text}}
Output:"""


    def generate_output(self, input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        print("***********************")
        print("Analysis Agent Working")
        print("***********************")

        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print(text_output)
        return text_output


class DecisionAgent:
    """the output of the decision agent is a JSON object that contains the action to be taken"""
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are the Decision Agent in a multi-agent system. Your decisions must be supported by insights provided by an Observation Agent.

### Problem Context:
The task is to mix three types of balls—heavy, normal, and light—in a container structured as a 10x10 matrix. Each cell in the matrix represents the weight of the ball at that position:
- '0' indicates an empty cell.
- '1' indicates a light ball (weight 1).
- '2' indicates a normal ball (weight 2).
- '3' indicates a heavy ball (weight 3).
The gravity has effect on balls and its direction is from row 10 to row 1. So the row 1 is the bottom row and row 10 is the top row.
The container is filled row by row from the bottom to the top.

The container can hold up to exactly **10 rows** of balls. The process ends when all rows are filled and the distribution of balls is well mixed.

### Actions:
Based on the container's state, you can take one of three actions:
1. **Add Balls**:
   - If the container has fewer than 10 rows filled, you can add rows of balls, either 1, 2, or 3 rows at a time, of the same type.
   - The total number of rows must not exceed 10.
   - Format: {"action": "add_balls", "parameters": {"row_number": <int>, "unit_of_weight": <int>}}

2. **Shake the Container**:
   - If the container has exactly 10 rows filled, you can shake it to mix balls of different weights.
   - Format: {"action": "shake", "parameters": {}}

3. **Stop**:
   - If the container has exactly 10 rows filled and the distribution of balls is well mixed, you should stop the process.
   - Format: {"action": "stop", "parameters": {}}

### Decision Rules:
- If the container has fewer than 10 rows filled:
  - Decide to **"add_balls"** until the container is completely filled with 10 rows.
  - Ensure the total number of rows does not exceed 10.

- If the container has exactly 10 rows filled:
  - The action **"add_balls"** must not be used.
  - Decide between **"shake"** or **"stop"** based on the mixing state and insights provided.

- Ensure decisions strictly follow these rules and align with insights from the Observation Agent.

### Insights Provided:
{{analysis_insights}}

### Objective:
{{agent_objective}}

You shall pay attention to the following insights: {{analysis_insights}}

You shall pay attention to the following:
- If the container is not full, you should decide to "add_balls" until it is full.
- If the container is full, adding more balls is not allowed. Only "shake" or "stop" actions can be performed.
- Ensure the decision respects the container's current state and the mixing index insights.


For example, you provide the output in this format after you receive the input:
Input:
// 10 rows of balls with their weight number representing the current state of the container, the bottom row is at the bottom of the matrix.
Output:
{"reason_for_an_action": "", "action": "", "parameters": {}} //You should decide an action in JSON format.

You should now finish the output, and only generate 1 action:
Input:
The container state is:
{{input_text}}

### Output Example:
{"reason_for_an_action": "<brief reason>", "action": "<action>", "parameters": {}}
"""


    def generate_output(self, input_text, analysis_insights, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{agent_objective}}", self.agent_objective)
        self.prompt = self.prompt.replace("{{analysis_insights}}", analysis_insights)
        print(f"{RED}***********************")
        print("Decision Agent Working")
        print("***********************")
        print("Input Decision Agent:\n")
        print("***********************")
        print(f"{RESET}")
        print(self.prompt)

        try:
            text_output = gpt_model_call(self.prompt, model=model)
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
        with open('decision.json', 'w') as file:
            json.dump(result_json, file, indent=4)
        print("Result:\n")
        print("***********************")
        print(text_output)
        return result_json


class ObservationAnalysisAgentWithTool:
    """the output of the observation analysis agent is a summarized observation of the current situation"""
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are the Observation Agent in a multi-agent system. Your task is to analyze the container's state and provide insights to help the Decision Agent.

### Context:
- The container is a 10x10 matrix filled row by row from **bottom (row 1)** to **top (row 10)**.
- Ball types: 
- '0': Empty cell, '1': Light (weight 1), '2': Normal (weight 2), '3': Heavy (weight 3).

### Task:
Summarize the container state:
1. How many rows are filled?
2. How many rows of light, normal, and heavy balls are still required?
3. Is the container full (`true/false`)?
4. Describe the ball distribution (e.g., even, uneven).
5. What happened to the mixing index after the last shake? 
   - Negative or zero: Recommend stopping.
   - Positive: Highlight improvement.

### Rules:
- The container is **not full** if fewer than 10 rows are filled.
- The container is **full** if exactly 10 rows are filled.

### Example Matrix:
The container state is represented as a 10x10 matrix:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9:  [0 0 0 0 0 0 0 0 0 0]
row 8:  [0 0 0 0 0 0 0 0 0 0]
row 7:  [0 0 0 0 0 0 0 0 0 0]
row 6:  [0 0 0 0 0 0 0 0 0 0]
row 5:  [0 0 0 0 0 0 0 0 0 0]
row 4:  [1 1 1 1 1 1 1 1 1 1]
row 3:  [1 1 1 1 1 1 1 1 1 1]
row 2:  [1 1 1 1 1 1 1 1 1 1]
row 1:  [1 1 1 1 1 1 1 1 1 1]

Objective:
{{agent_objective}}

### Output Format:
Provide the analysis in this JSON format:
{
  "rows_filled": 4,
  "number_of_rows_required": {
    "light_ball": 0,
    "normal_ball": 3,
    "heavy_ball": 3
  },
  "is_full": false,
  "distribution": "Uneven, only light balls in the container.",
  "change_of_mixing_index": 0.02,
  "important_aspect": "Continue adding normal and heavy balls."
}

### Input:
The container state is:
{{input_text}}
The change of mixing index is:
{{delta_mixing_index}}

### Output:
"""

    def generate_output(self, input_text, delta_mixing_index, model):
        if delta_mixing_index is None:
            delta_mixing_index = "No change in mixing index available"
        else:
            delta_mixing_index = str(delta_mixing_index)
    
        self.prompt = self.prompt_template.replace("{{agent_objective}}", self.agent_objective)
        self.prompt = self.prompt.replace("{{input_text}}", input_text)
        self.prompt = self.prompt.replace("{{delta_mixing_index}}", delta_mixing_index)
        # Print with green color
        print(f"\n\n{GREEN}***********************{RESET}")
        print(f"{GREEN}Observation Agent Working (Using Tool){RESET}")
        print(f"{GREEN}***********************{RESET}")
        print(f"{GREEN}Input Observation Agent:\n{RESET}")
        print(f"{GREEN}***********************{RESET}")
        print(self.prompt)

        try:
            text_output = gpt_model_call(self.prompt, model=model)

        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print("***********************")
        print(text_output)
        return text_output



class LogSummarizationAgent:
    def __init__(self, agent_objective):
        self.agent_objective = agent_objective
        self.prompt_template = """You are a ball mixing machine operator. This machine mixes three types of balls—heavy, normal, and light—within a container. All balls are identical in size but differ in weight. The mixing process takes place in a two-dimensional container designed as a 10x10 matrix, allowing for 10 rows of 10 balls each.

Types of Balls:
- Heavy Ball: Weight of 3 units.
- Normal Ball: Weight of 2 units.
- Light Ball: Weight of 1 unit.

Container Specifications:
- The container is structured into a 10x10 matrix, accommodating up to 100 balls in 10 rows, with each row holding 10 balls.
- The container is filled from the bottom row to the top row.
- The container is represented as a 10x10 matrix, with each cell containing a number representing the weight of the ball in that position.
- '0' indicates an empty cell.
- '1' indicates a light ball.
- '2' indicates a normal ball.
- '3' indicates a heavy ball.
- Initially, the container is empty, and the container state has the following format:
row 10: [0 0 0 0 0 0 0 0 0 0]
row 9: [0 0 0 0 0 0 0 0 0 0]
row 8: [0 0 0 0 0 0 0 0 0 0]
row 7: [0 0 0 0 0 0 0 0 0 0]
row 6: [0 0 0 0 0 0 0 0 0 0]
row 5: [0 0 0 0 0 0 0 0 0 0]
row 4: [0 0 0 0 0 0 0 0 0 0]
row 3: [0 0 0 0 0 0 0 0 0 0]
row 2: [0 0 0 0 0 0 0 0 0 0]
row 1: [0 0 0 0 0 0 0 0 0 0]



Actions:
(1) Adding Balls:
- You can add one or more rows of balls, but exclusively of one type during each action.
- You can only add 1 row or 2 rows of balls in each action.
- You can perform the add action in this format: {"action": "add_balls", "parameters":{"row_number": "", "unit_of_weight": ""}}, row_number is an integer between 1 and 10, and unit_of_weight is an integer between 1 and 3.

(2) Shaking the Container:
- After each shake, gravity may cause heavier balls to switch positions with lighter balls immediately below them.
- The shaking action helps to mix the balls of different weights.
- You can perform the shake action in this format: {"action": "shake", "parameters":{}}.

(3) Stop:
- You terminate the process if the distribution of balls is well mixed and the container has 10 rows of balls.
- You can perform the stop action in this format: {"action": "stop", "parameters":{}}.

Objective:
{{agent_objective}}


You operated the machine and now need to summarize the actions taken during the mixing process concisely for each step. The detailed log of the actions taken by you during the mixing process, including the following information:
{{input_text}}

Now, please provide a summary of the actions taken in the log in a text report, summarizing each step with its main reason concisely within 8 words, in the following form:
{
    "step_summary": [
        {
            "step": ,
            "action": "",
            "summary": ""
            "change_of_mixing_index": ""
        }
        ...
    ]}
"""


    def generate_output(self,input_text, model):
        self.prompt = self.prompt_template.replace("{{input_text}}", str(input_text))
        self.prompt = self.prompt.replace("{{agent_objective}}", self.agent_objective)
        print("***********************")
        print("Summarization Agent Working")
        print("***********************")
        print("Input Summarization Agent:\n")
        print("***********************")
        print(self.prompt)
        try:
            text_output = gpt_model_call(self.prompt, model=model)
        except Exception as e:
            print(f"Error: {e}")

            return None
        print("Result:\n")
        print("***********************")
        print(text_output)
        return text_output
