from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableSequence

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a facts expert who knows facts about {animal}."),
    ("human", "Tell me {fact_count} facts about {animal}."),
])

format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
# invoke_model = RunnableLambda(lambda prompt: model.invoke(prompt))

# parse_output = RunnableLambda(lambda x: x.content)
