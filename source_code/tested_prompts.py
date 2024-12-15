Adding_prompts ={
"2": """You are the Adding Agent in a multi-agent system. Your decisions must be supported by insights provided by an Observation Agent.

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
  "rows_of_1_left_to_add": <int>,
  "rows_of_2_left_to_add": <int>,
  "rows_of_3_left_to_add": <int>,
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

Add rows to achieve **respecting the rows left to add** to achieve the objectives.

### Output
Provide the answer in a JSON format only without extra characters inside of it:

{
  "rows_of_1_left_to_add": 0,
  "rows_of_2_left_to_add": 3,
  "rows_of_3_left_to_add": 0,
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
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]

Add rows to achieve **respecting the rows left to add** to achieve the objectives.

###Output:
Provide the answer in a JSON format only without extra characters inside of it:

{
  "rows_of_1_left_to_add": 1,
  "rows_of_2_left_to_add": 0,
  "rows_of_3_left_to_add": 3,
  "action": "add_balls",
  "parameters": {
    "number_of_rows_to_add": 3,
    "unit_of_weight": 2
  },
  "reason_for_an_action": "The container is missing light and heavy balls to meet the objective of 4 rows of weight 1 and 3 rows of weight 3."
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


Add rows to achieve **respecting the rows left to add** to achieve the objectives.

###Output:
Provide the answer in a JSON format only without extra characters inside of it:

{
  "rows_of_1_left_to_add": 0,
  "rows_of_2_left_to_add": 0,
  "rows_of_3_left_to_add": 3,
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


Add rows to achieve **respecting the rows left to add** to achieve the objectives.

### Output:
Provide the answer in a JSON format only without extra characters inside of it:
""" ,"2": """ You are the Adding Agent in a multi-agent system.

### Task:
You are responsible for adding rows of balls to a 10x10 container matrix.
There are 3 types of balls:
  - **1** = light ball (weight 1)
  - **2** = normal ball (weight 2)
  - **3** = heavy ball (weight 3)
The container's gravity causes balls to settle at the lowest empty rows, and the total capacity is 10 rows. 

### Objective:
container must end with exactly this number of rows:
  - four rows of **1**
  - three rows of **2**
  - three rows of **3**

### Action Rules:
**Do not add more than three rows of the same value at once.**
**Do not add more than 10 rows in total.** 

# Example Shots:"""}



observation_prompts = {"1":"""You are the Observation Agent in a multi-agent system. Your task is to analyze the state of the container and determine which agent should be activated: the Adding Agent or the Mixing Agent.



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
Provide the answer in a JSON format only:"""}