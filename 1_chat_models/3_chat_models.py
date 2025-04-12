from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables from .env file
load_dotenv()

# Prepare the conversation messages
messages = [
    SystemMessage("You are an expert in social media content strategy."),
    HumanMessage("Give a short tip for creating engaging Instagram posts."),
]

# Initialize and invoke the OpenAI model (GPT-4)
llm_openai = ChatOpenAI(model="gpt-4")
result_openai = llm_openai.invoke(messages)

# Initialize and invoke the Google Gemini model
llm_google = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

result_google = llm_google.invoke(messages)

# Print results from both models
print("Answer from OpenAI:\n", result_openai.content)
print("Answer from Google:\n", result_google.content)
