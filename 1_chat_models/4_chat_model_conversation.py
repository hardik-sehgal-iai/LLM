from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4")

chat_history = []

system_message = SystemMessage("You are a helpful AI assistant.")
chat_history.append(system_message)

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    
    chat_history.append(HumanMessage(content=query)) # Add user message to chat history
    
    result = model.invoke(chat_history) # Invoke the model with the chat history
    response = result.content # Get the response from the model
    chat_history.append(AIMessage(content=response))
    
    print("AI:", response) # Print the AI's response
    
print("Chat history:")
for message in chat_history:
    print(message.content) # Print the entire chat history