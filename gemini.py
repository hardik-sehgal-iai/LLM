from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = "AIzaSyC_YJqLoQ_mB6ihe3FBqoZE1OCstS9F-Tw"

client = genai.Client(api_key=gemini_api_key)

def run_command(command): 
    result = os.system(command=command)
    return result

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File written successfully to {path}"

available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "write_file": {
        "fn": write_file,
        "description": "Takes the file path and content as parameter and write the content in the given file path"
    }
}


chat = client.chats.create(
    model="gemini-2.0-flash", 
    config=types.GenerateContentConfig(
        response_mime_type= 'application/json',
        system_instruction="""
        You are a coding assistant specialized in coding. Your job is to complete all the task given to you in a step by step and structured manner. You are a great problem solver. whenever a problem statement or a task is given to you, you first observe the problem statement, then you analyze the problem statement, and you divide the problem in steps which are actionable and necessary, than you execute it.
        For the given user query you can use the list of available tools: 
        - run_command: Takes the command as an input to execute it on system and returns the output
        - write_file: Takes the file path and content as parameter and write the content in the given file path

        Rules: 
        - always perform one step at a time
        - The only valid steps are: "observe", "analyze", "divide", "execute", and "output"
        - After "observe", "analyze", and "divide" steps, you must move to the next step
        - After "execute" steps, you should move to either another "execute" step or "output"
        - The final step should always be "output" which completes the task

        Output JSON Format:        
        {"step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"}
        follow the json output format
        
        Example: 
        User Query: create a new js file and write a function to add two numbers?
        Output: { "step": "observe", "content": "The user is asking to create a new js file with add function init" }
        Output: { "step": "analyze", "content": "There are two tasks which user wants me to do. From the available tools I should call run_command" }
        Output: { "step": "divide", "content": "First task is to create a new js file and Second task is to write a function which adds two numbers in the created file" }
        Output: { "step": "execute", "function": "run_command", "content": "creating new js file", "input": "touch add.js" }
        Output: { "step": "execute", "function": "write_file", "content": "writing function to add two numbers in the created file", "input": {
            "path": "./add.js",
            "content": "function add(a,b) {\n return a + b \n}"
        } }
        Output: { "step": "output", "content": "Successfully completed the task of creating a new file and writing an add function init" }
        
        For simple greetings or non-task conversations, you should just use observe followed immediately by output.
        """
    )
)

# Main conversation loop
while True:
    user_text = input("You: ")
    if user_text.lower() in ["exit", "quit", "bye"]:
        break
    
    # Flag to track if the inner loop completed normally
    completed = False
    # Maximum number of iterations to prevent infinite loops
    max_iterations = 10
    iterations = 0
    
    # Processing loop for a single user message
    while iterations < max_iterations:
        iterations += 1
        
        try:
            response = chat.send_message(user_text)
            print(response.text)
            
            # Try to parse the JSON response
            try:
                parsed_output = json.loads(response.text)
            except json.JSONDecodeError:
                print("Error: Could not parse response as JSON")
                break
            
            step = parsed_output.get("step", "")
            
            # Handle each step type
            if step == "observe":
                print(f"👀: {parsed_output.get('content')}")
                # Continue to next iteration - get next step from AI
                
            elif step == "analyze":
                print(f"🧠: {parsed_output.get('content')}")
                # Continue to next iteration - get next step from AI
                
            elif step == "divide":
                print(f"🧠: {parsed_output.get('content')}")
                # Continue to next iteration - get next step from AI
                
            elif step == "execute":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                print(f"🛠️: Executing {tool_name} with input: {tool_input}")
                
                if tool_name in available_tools:
                    try:
                        if isinstance(tool_input, dict):
                            output = available_tools[tool_name]["fn"](**tool_input)
                        else:
                            output = available_tools[tool_name]["fn"](tool_input)
                        
                        # Send result back to AI
                        user_text = f"Tool execution result: {output}"
                        print(f"Tool result: {output}")
                    except Exception as e:
                        print(f"Error executing tool: {e}")
                        user_text = f"Error executing tool: {e}"
                else:
                    print(f"Unknown tool: {tool_name}")
                    user_text = f"Unknown tool: {tool_name}"
                    
            elif step == "output":
                print(f"🤖: {parsed_output.get('content')}")
                print("Type exit to stop this chat")
                completed = True
                break
                
            elif step == "respond":  # This wasn't in your original steps but appears in the output
                print(f"🗣️: {parsed_output.get('response', parsed_output.get('content', 'No response content'))}")
                # For a greeting, we'll just exit the inner loop
                completed = True
                break
                
            else:
                print(f"Unknown step: {step}")
                # Exit the inner loop if we get an unknown step
                break
                
        except Exception as e:
            print(f"Error processing response: {e}")
            break
    
    # Check if we hit the iteration limit
    if iterations >= max_iterations and not completed:
        print("Warning: Maximum number of iterations reached. Starting fresh with next input.")
        # Send a reset message to the AI
        try:
            chat.send_message("Let's start fresh. Please respond only with valid steps as defined in your instructions.")
        except Exception:
            pass
