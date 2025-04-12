from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# In this we are going to learn how to send past conversation history to the model

messages = [
    SystemMessage("You are an expert in social media content strategy."),
    HumanMessage("Give a short tip for creating engaging Instagram posts."),
]

# Create the ChatOpenAI instance using the API key
llm = ChatOpenAI(model="gpt-4")

result = llm.invoke(messages)

print(result.content)