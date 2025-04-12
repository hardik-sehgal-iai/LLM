from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a facts expert who knows facts about {animal}."),
    ("human", "Tell me {fact_count} facts about {animal}."),
])

# LCEL chain (Prompt → Model → Output Parser)
chain = prompt_template | model | StrOutputParser()

result = chain.invoke({"animal": "cat", "fact_count": 3})
print(result)
