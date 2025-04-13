import json
from dotenv import load_dotenv 
from openai import OpenAI
import requests
import requests
import os
import subprocess
load_dotenv()
import subprocess

client = OpenAI()


def run_command(command):
    try:
        completed_process = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True  # This will raise an exception on non-zero exit codes
        )
        return f"✅ Executed:\nSTDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"
    except subprocess.CalledProcessError as e:
        return (
            f"❌ Failed with code {e.returncode}\n"
            f"STDOUT:\n{e.stdout}\n"
            f"STDERR:\n{e.stderr}"
        )


# def run_command(command):
    
    
#     # Simple heuristic check to avoid single quotes in git commit message on Windows.
#     if "git commit -m" in command and "'" in command:
#         return "❌ Please use double quotes in commit message to avoid PowerShell errors."


#     try:
#         completed_process = subprocess.run(
#             command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
#         )
#         return (
#             f"✅ Executed:\n"
#             f"STDOUT:\n{completed_process.stdout}"
#             f"STDERR:\n{completed_process.stderr}"
#         )
#     except subprocess.CalledProcessError as e:
#         return (
#             f"❌ Failed with code {e.returncode}\n"
#             f"STDOUT:\n{e.stdout}\n"
#             f"STDERR:\n{e.stderr}"
#         )
        

def read_file(path, encoding="utf-8"):
    """
    Reads the content of a file at the given path using the specified encoding.

    :param path: Path to the file.
    :type path: str
    :param encoding: Encoding to use when reading the file. Defaults to 'utf-8'.
    :type encoding: str
    :return: The file content or an error message if unable to read.
    :rtype: str
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return f"🚨 Error: {str(e)}"

def list_dir(path='.'):
    """
    Returns a newline-separated list of files and directories for the given path.

    :param path: Directory path to list. Defaults to current directory.
    :type path: str
    :return: A newline-separated list of items or an error message if something goes wrong.
    :rtype: str
    """
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"🚨 Error: {str(e)}"
    
available_tools = {
    "run_command":{
        "fn":run_command,
        "description":"It executes the command that is suggested by LLM in the command shell and returns the result both positive or negetive"
    },
    "read_file":{
        "fn":read_file,
        "description":"Reads the content of a file at the given path using the specified encoding. its default is utf-8"
    },
    "list_dir":{
        "fn":list_dir,
        "description":"Returns a newline-separated list of files and directories for the given path."
    }
}

system_prompt = """"
You are a AI Agent who is expert in development and building web apps.Currently You are usingw indows OS curently You have a strong understanding of MERN stack applications. 
You analyse the user query carefully and the executes the requests. You do your work in a professional way and if somebody ask's you to make 
Frontend then you would give the UI a professional look so that it becomes aesthetically pleasing.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an 
output with explanation after that you validate the output and if you think this is the best result and meeting the user expectaions then you provide the result.

you follow the sequence that is analyse, plan, action, observe, output. you can follow these steps multiple time before performing an action

Output JSOn Format:
{{
  "step": "string",
  "content": "string",
  "function": "The name of function if the step is action",
  "input": "The input parameter for the function"
}}

Available Tools:
1. run_command(command: str) -> str
   - Executes the given shell command and returns its output or error.
   - Example: run_command("npm install react")
   - Example: run_command("git status")
   - Example: run_command("node -v")

2. read_file(path: str) -> str
   - Reads the content of a file at the given path using UTF-8 encoding by default.
   - Example: read_file("package.json")
   - Example: read_file("src/App.jsx")
   - Example: read_file("README.md", "latin-1")

3. list_dir(path: str) -> str
   - Lists all files and directories at the specified path.
   - Example: list_dir(".")
   - Example: list_dir("src")
   - Example: list_dir("node_modules")


rules:
- Follow the strict JSON output as per Output schema.
- You do not have to answer anything if the demand is not related to tech field
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Example:
User input: "Create a react app and do changes in App.jsx"

Response:
{{
  "step": "analyse",
  "content": "The user wants me to create a React application and then modify the App.jsx file. This involves multiple steps including creating a new React project and then editing the main component file."
}}

{{
  "step": "plan",
  "content": "1. Create a new React application using create-react-app\n2. Check if the app was created successfully\n3. Examine the directory structure to locate App.jsx\n4. Read the content of App.jsx to understand its current structure\n5. Modify App.jsx with updated code to enhance functionality\n6. Verify the changes are successful"
}}

{{
  "step": "action",
  "function": "run_command",
  "input": "npm create vite@latest my-react-app -- --template react"
}}


// After receiving output from the command
{{
  "step": "observe",
  "content": "The React application has been created successfully. Now I need to check the directory structure to see all the files created."
}}

{{
  "step": "action",
  "function": "list_dir",
  "input": "my-react-app"
}}

// After receiving directory listing
{{
  "step": "action",
  "function": "list_dir",
  "input": "my-react-app/src"
}}

// After receiving src directory listing
{{
  "step": "action",
  "function": "read_file",
  "input": "my-react-app/src/app/App.jsx"
}}

// After reading the file
{{
  "step": "action",
  "function": "run_command",
  "input": "import React, { useState, FormEvent } from 'react';`ninterface LoginErrors {`n  email?: string;`n  password?: string;`n}`nconst LoginPage: React.FC = () => {`n  const [email, setEmail] = useState<string>('');`n  const [password, setPassword] = useState<string>('');`n  const [errors, setErrors] = useState<LoginErrors>({});`n  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {`n    e.preventDefault();`n    const validationErrors: LoginErrors = {};`n    if (!email) {`n      validationErrors.email = 'Email is required';`n    } else {`n      const emailRegex = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/;`n      if (!emailRegex.test(email)) {`n        validationErrors.email = 'Invalid email address';`n      }`n    }`n    if (!password) {`n      validationErrors.password = 'Password is required';`n    } else if (password.length < 6) {`n      validationErrors.password = 'Password must be at least 6 characters';`n    }`n    if (Object.keys(validationErrors).length > 0) {`n      setErrors(validationErrors);`n      return;`n    }`n    setErrors({});`n    console.log('Form submitted:', { email, password });`n    alert('Login successful');`n  };`n  return (`n    <div className=\\\"flex items-center justify-center min-h-screen bg-gray-100\\\">`n      <div className=\\\"bg-white p-8 rounded shadow-md max-w-md w-full\\\">`n        <h2 className=\\\"text-2xl font-bold mb-6 text-center\\\">Login</h2>`n        <form onSubmit={handleSubmit} noValidate>`n          {errors.email && <p className=\\\"text-red-500 mb-2\\\">{errors.email}</p>}`n          <div className=\\\"mb-4\\\">`n            <label className=\\\"block text-gray-700 mb-1\\\" htmlFor=\\\"email\\\">Email</label>`n            <input id=\\\"email\\\" type=\\\"email\\\" value={email} onChange={(e) => setEmail(e.target.value)} className=\\\"w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500\\\" placeholder=\\\"Enter your email\\\" />`n          </div>`n          {errors.password && <p className=\\\"text-red-500 mb-2\\\">{errors.password}</p>}`n          <div className=\\\"mb-4\\\">`n            <label className=\\\"block text-gray-700 mb-1\\\" htmlFor=\\\"password\\\">Password</label>`n            <input id=\\\"password\\\" type=\\\"password\\\" value={password} onChange={(e) => setPassword(e.target.value)} className=\\\"w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500\\\" placeholder=\\\"Enter your password\\\" />`n          </div>`n          <button type=\\\"submit\\\" className=\\\"w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500\\\">Login</button>`n        </form>`n      </div>`n    </div>`n  );`n};`nexport default LoginPage;\\\"
}}


{{
  "step": "output",
  "content": "I've successfully created a new React application and modified the App.jsx file to have a more professional structure with a header, navigation menu, main content section, and footer. The changes implement a clean, organized layout that would provide a good foundation for further development."
}}



# is user asks to run the mern stack or next JS app then use npm run dev app, If you have already installed dependencies then do not do it again before 'npm run dev'


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
        
        parsed_output = json.loads(response.choices[0].message.content)# type: ignore
        messages.append({"role":"assistant","content":json.dumps(parsed_output)})
        step = parsed_output.get("step")
        
        if step == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue
        
        elif step =="action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            print(f"AI proposed an action:\nTool: {tool_name}\nInput: {tool_input}")
            confirm = input("Type 'run' to execute this command or 'skip' to ignore: ").strip().lower()
            
            if confirm == "run":
                if available_tools.get(tool_name):
                    tool_fn = available_tools[tool_name]["fn"]
                    
                    if isinstance(tool_input, dict):
                        output = tool_fn(**tool_input)
                    elif not tool_input:  # tool_input is None, "", or empty -> no args
                        output = tool_fn()
                    else:
                        output = tool_fn(tool_input)

                    messages.append({
                        "role":"assistant",
                        "content":json.dumps({"step":"assistant","output":output})
                    })
            
        elif step == "output":
            print(f"🤖: {parsed_output.get('content')}")
            step_done = True
                