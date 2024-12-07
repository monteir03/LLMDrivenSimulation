from flask import Flask, render_template
from flask_socketio import SocketIO
from pprint import pprint
from agents import ObservationAnalysisAgentWithTool, AddingAgent, MixingAgent
from simulation import ContainerBallSimulation
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

simulation = ContainerBallSimulation()

#mode = 'simple GPT'
#mode = 'agents system'
mode = 'agents system with extra measurement of heterogeneity'

global user_started_auto_mode
user_started_auto_mode = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('add_row')
def handle_add_row(json):
    row_num = int(json['rowNum'])
    weight = int(json['weight'])
    simulation.add_balls(row_num, weight)
    socketio.emit('chat_message', {'message': "add_row()"})
    base64_img = simulation.visualize_container_to_base64()
    socketio.emit('update_image', {'base64_img': base64_img})

@socketio.on('shake')
def handle_shake(json):
    shake_times = int(json['shakeTimes'])
    simulation.shake(shake_times)
    socketio.emit('chat_message', {'message': "shake()"})
    base64_img = simulation.visualize_container_to_base64()
    socketio.emit('update_image', {'base64_img': base64_img})

@socketio.on('set_example')
def handle_set_example(json):
    example_num = int(json['exampleNum'])
    simulation.use_example(example_num)
    socketio.emit('chat_message', {'message': "set_example()"})
    base64_img = simulation.visualize_container_to_base64()
    socketio.emit('update_image', {'base64_img': base64_img})

def send_message_to_front_end(message):
    socketio.emit('chat_message', {'message': message})


@socketio.on('user_message')
def handle_user_message(json):
    global user_started_auto_mode
    user_message = json['message']
    response_message = f"Received message: {user_message}"
    # Simplified user message handling, focusing on simulation experimenting. More complex logic or user interaction mechanisms can be added here
    if "Start the Simulation" in user_message:
        user_started_auto_mode = True
    socketio.emit('chat_message', {'message': response_message})

#********this is where the logic is implemented*******

def run_simulation_periodically():
    with ((app.app_context())):
        time.sleep(5)
        while True:
            container_state = simulation.get_container_state()
            user_set_objective = """The objective is to fill and then mix a 10x10 container with 4 rows of light balls, 3 rows of normal balls, 
            and 3 rows of heavy balls. Add rows strategically and use shaking to ensure a homogenous mix."""

            if mode == 'agents system with extra measurement of heterogeneity':
                while not user_started_auto_mode:

                    time.sleep(1)
                    simulation.step_log.clear()

                history_file_path = 'history_json.json'

                # Agents System
                analysis_agent = ObservationAnalysisAgentWithTool(user_set_objective)
                '''
                delta_mixing_index = simulation.step_log[-1]["delta_mixing_index"] if len(simulation.step_log) > 0 else simulation.calculate_mixing_index(simulation.get_container_state())
                delta_mixing_index_text = str(delta_mixing_index)
                '''

                delta_mixing_index = simulation.step_log[-1]["delta_mixing_index"] if len(simulation.step_log) > 0 else simulation.calculate_mixing_index(simulation.get_container_state())
                delta_mixing_index_text = str(delta_mixing_index) if delta_mixing_index is not None else "No change in mixing index"

                #analysis_result = analysis_agent.generate_output(simulation.get_container_state_in_text(), delta_mixing_index_text, model='ollama_llama3')
                analysis_result = analysis_agent.generate_output(container_state, delta_mixing_index_text, model='ollama_llama3')
                if analysis_result is None:
                    analysis_result = "No valid analysis obtained"

                
                decision_agent = DecisionAgent(user_set_objective)
                #decision = decision_agent.generate_output(simulation.get_container_state_in_text(), analysis_result, model='ollama_llama3')
            
                decision = decision_agent.generate_output(container_state, analysis_result, model='ollama_llama3')
                print("this is the decision", decision)
                if not decision or 'action' not in decision:
                    send_message_to_front_end("Invalid decision received, stopping simulation.")
                    break

                experiment_data_structure = {
                    "id": None,
                    "solving_process": [
                        {
                            "id": None,
                            "observation": None,
                            "reasoning": None,
                            "action": None
                        }
                    ],
                    "result": None
                }

                step_data_structure = {"id": None, "observation": analysis_result,
                                       "reasoning": decision, "action": decision['action']}

                # Append the observation, reasoning and action to the history file



                # Agent system decision
                if decision['action'] == 'shake':
                    simulation.shake(1)
                    send_message_to_front_end('shake'  + ". Reason:" + analysis_result)
                    print('Shake')

                elif decision['action'] == 'add_balls':
                    simulation.add_balls(decision['parameters']['row_number'], decision['parameters']['unit_of_weight'])
                    print('Add balls ' + str(decision['parameters']['row_number']) + ' weight: ' + str(
                        decision['parameters']['unit_of_weight']))
                    send_message_to_front_end('add ' + str(decision['parameters']['row_number']) + ' row of balls with ' + ' weight ' + str(
                        decision['parameters']['unit_of_weight'])  + ". Reason:" + analysis_result)

                elif decision['action'] == 'stop':
                    print('Stop')
                    simulation.step_log[-1]["analysis_result"] = analysis_result
                    simulation.step_log[-1]["decision"] = decision
                    send_message_to_front_end('stop' + ". Reason:" + analysis_result)
                    break
            if mode != 'agents system with extra measurement of heterogeneity':
                simulation.step_log[-1]["analysis_result"] = analysis_result
                simulation.step_log[-1]["decision"] = decision
            base64_img = simulation.visualize_container_to_base64()
            socketio.emit('update_image', {'base64_img': base64_img})

        if mode != 'agents system with extra measurement of heterogeneity':
            log_summarization_agent = LogSummarizationAgent(user_set_objective)
            pprint(simulation.step_log)
            decision_log = [{"step": idx, "analysis_result": step["analysis_result"], "decision": step["decision"], "change_of_mixing_index": step["delta_mixing_index"]} for idx, step in enumerate(simulation.step_log)]
            pprint(decision_log)
            log_summary = log_summarization_agent.generate_output(decision_log, model='ollama_llama3')
            print(log_summary)
            send_message_to_front_end("My job is finished, here is the summary of my work: \n")
            send_message_to_front_end(log_summary)
            # TODO: Compare this result with existing history of all the simulation experiments



def run_simulation_debug():
    """
    Debugging mode: Runs the simulation logic without Flask or Socket.IO.
    """
    print("Starting simulation in debugging mode...\n")
    
    # not being used now
    user_set_objective = """The objective is to fill and then mix a 10x10 container with 4 rows of light balls, 3 rows of normal balls, 
    and 3 rows of heavy balls. Add rows strategically and use shaking to ensure a homogenous mix."""

    # Initialize agents
    observation_agent = ObservationAnalysisAgentWithTool()
    adding_agent = AddingAgent()
    mixing_agent = MixingAgent()

    while True:
        # Step 1: Get the current container state and mixing index
        #container_state = simulation.get_container_state_in_text()
        container_state = simulation.get_container_minimal_state()
        delta_mixing_index = simulation.step_log[-1]["delta_mixing_index"] if len(simulation.step_log) > 0 else simulation.calculate_mixing_index(simulation.get_container_state())
        delta_mixing_index_text = str(delta_mixing_index) if delta_mixing_index is not None else "No change in mixing index"

        # Step 2: Observation Analysis
        analysis_result = observation_agent.generate_output(container_state, delta_mixing_index_text, model='ollama_llama3')
        if not analysis_result:
            print("No valid analysis obtained. Exiting simulation.")
            break
        
        # Step 3: Decision Making by the Specific Agent
        if "Adding Agent" in analysis_result:
            print("Activating: Adding Agent")
            decision = adding_agent.generate_output(container_state, analysis_result, model='ollama_llama3')
        elif "Mixing Agent" in analysis_result:
            print("Activating: Mixing Agent")
            decision = mixing_agent.generate_output(container_state, analysis_result, model='ollama_llama3')
        else:
            print(f"Unexpected agent suggestion: {analysis_result}. Exiting simulation.")
            break

        if not decision or 'action' not in decision:
            print("Invalid decision received. Exiting simulation.")
            break

        # Step 4: Perform the Action
        if decision['action'] == 'shake':
            simulation.shake(1)
            print("Performed: Shake")
        
        elif decision['action'] == 'add_balls':
            row_number = decision['parameters']['row_number']
            unit_of_weight = decision['parameters']['unit_of_weight']
            simulation.add_balls(row_number, unit_of_weight)
            print(f"Performed: Add {unit_of_weight} balls to row {row_number}")
        
        elif decision['action'] == 'stop':
            print("Performed: Stop")
            print("Simulation completed successfully.")
            break
        else:
            print(f"Unexpected action: {decision['action']}. Exiting simulation.")
            break

        # Step 5: Visualize the current container state (optional: save to a file or display as text)
        print("\nCurrent Container State:")
        for row in simulation.get_container_state():
            print(row)

        # Add a delay to simulate time between steps
        time.sleep(1)



if __name__ == '__main__':
    #run_simulation_thread = threading.Thread(target=run_simulation_periodically)
    #run_simulation_thread.start()
    #socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
    run_simulation_debug()

