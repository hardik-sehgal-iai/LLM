import json
from dotenv import load_dotenv 
from openai import OpenAI
import requests
import requests
import os

load_dotenv()

client = OpenAI()


def get_weather(city: str):
    print("tool called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"  # Use valid format
    response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds

    print("response", response)
    if response.status_code == 200:
        return f"The Weather of {city} is {response.text.strip()}"
    
    return "Something went wrong"

def calculate_area(length: float, width: float):
    print("tool called: calculate_area", length, width)
    return f"Area is {length * width} square units"

def run_command(command):
    print("tool called: run command", command)
    result = os.system(command=command)
    return "✅ Executed" if result == 0 else f"❌ Failed with code {result}"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "calculate_area":{
        "fn":calculate_area,
        "description": "Takes length and width as input and returns the area of a rectangle"
    },
    "run_command":{
        "fn":run_command,
        "description":"Takes a command as input to execute on system and returns output "
    }
}


system_prompt = """
You are a helpful AI Assistant specialized in resolving user queries.
You operate in a Start, Plan, Act, Observe mode.

for the given user query and given tools, plan the step by step exectution, based on the planning select the relevant tool from the available tool
and based on the tool selection you perform an action to call the tool. wait for the observation and based on the observation from the tool call to resolve user query

Output JSOn Format:
{{
  "step": "string",
  "content": "string",
  "function": "The name of function if the step is action",
  "input": "The input parameter for the function"
}}

Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - calculate_area: Takes length and width as input. Example Input: { "length": 5, "width": 3 }
    - run_command : Takes a command as input to execute on system and returns output 

example:
User Query: What is the weather of new york?

Output: {{ "step": "plan", "content": "The user is interested in weather data of New York" }}
Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "12 Degree Cel" }}
Output: {{ "step": "output", "content": "The weather for New York seems to be 12 degrees." }}

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

"""
messages = [
    {"role": "system", "content": system_prompt}
]


while True:
    user_query = input("User -> ").strip().lower()

    if user_query in ["bye", "exit", "quit"]:
        print("👋 Goodbye!")
        break

    messages.append({ "role": "user", "content": user_query })

    step_done = False  # Track if output step is completed

    while not step_done:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=messages # type: ignore
        )

        parsed_output = json.loads(response.choices[0].message.content)  # type: ignore
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        step = parsed_output.get("step")

        if step == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue

        elif step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name):
                tool_fn = available_tools[tool_name]["fn"]

                if isinstance(tool_input, dict):
                    output = tool_fn(**tool_input)
                else:
                    output = tool_fn(tool_input)

                messages.append({
                    "role": "assistant",
                    "content": json.dumps({"step": "observe", "output": output})
                })

        elif step == "output":
            print(f"🤖: {parsed_output.get('content')}")
            step_done = True
