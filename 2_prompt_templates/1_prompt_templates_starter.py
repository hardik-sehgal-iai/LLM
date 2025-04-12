from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(model="gpt-4")

template = "Write a {tone} email to {company} expressing interest in the {position} position. Mentioning {skills} as a key strength. keep it to 4 lines max"

prompt_template = ChatPromptTemplate.from_template(template)

prompt = prompt_template.invoke({
    "tone": "friendly",
    "company": "Google",
    "position": "Software Engineer",
    "skills": "Python, JavaScript"
})

result = llm.invoke(prompt)
print(result.content)

# print(prompt)