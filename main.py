import os
from openai import OpenAI
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. Load API Key
load_dotenv()
client = OpenAI()

# 2. List of texts to compare
texts = [
    "The Eiffel Tower is in Paris.",
    "The Statue of Liberty is in New York.",
    "Mount Everest is the tallest mountain.",
    "Apple makes iPhones.",
    "Microsoft builds Windows.",
    "Bananas are yellow and healthy.",
    "Coding in Python is fun.",
    "Artificial Intelligence is evolving.",
]

# 3. Get embeddings for each text
embeddings = []
for text in texts:
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embeddings.append(response.data[0].embedding)

# 4. Reduce from 1536D to 2D using PCA
pca = PCA(n_components=2)
import numpy as np

reduced = pca.fit_transform(np.array(embeddings))

# 5. Plot the embeddings
plt.figure(figsize=(10, 6))
for i, text in enumerate(texts):
    x, y = reduced[i]
    plt.scatter(x, y)
    plt.text(x + 0.01, y + 0.01, text, fontsize=9)

plt.title("2D Visualization of Text Embeddings")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.grid(True)
plt.show()



# import json
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = OpenAI()

# system_prompt = """
# You are an AI assistant who is expert in breaking down complex problems and then resolving the user query.

# For the given user input, analyse the input and break down the problem step by step.
# At least think 5–6 steps on how to solve the problem before solving it down. and finally you validate output that you are giving

# The steps are: you get a user input, you analyse, you think, you again think for several times and then return an answer.

# follow these steps in sequence that is analyze, think, output, validate and result
# rules:
# 1. follow strict json output as per output schema
# 2. always perform 1 step at a time and wait for next input 
# 3. carefully analyze query

# output format:
# {{step:"string", content:"string"}}

# Example:
# Input: What is 2 + 2?
# Output: {{ step: "analyze", content: "Alright! The user is interested in a math query and is asking a basic arithmetic operation." }}
# Output: {{ step: "think", content: "To perform the addition, I must go from left to right and add all the operands." }}
# Output: {{ step: "output", content: "4" }}
# Output: {{ step: "validate", content: "Seems like 4 is the correct answer for 2 + 2." }}
# Output: {{ step: "result", content: "2 + 2 = 4, and that is calculated by adding all numbers." }}
# """

# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": "what is 3+4 *5"}
#     ]
# )

# print(response.choices[0].message.content)
