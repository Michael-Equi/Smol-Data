import os
import openai
import pandas as pd

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


ds = pd.read_csv('adult.data.csv')

headers = ds.head()

task = f"""
What does each of the columns mean?
"""

prompt = f"""
You are an expert data scientist specializing in databases. \
You have extensive knowledge and experience in managing, \
analyzing, and optimizing databases. Your goal is to assist \
users with any database-related tasks and provide expert \
guidance. When interacting with the agent, make your orders \
clear and concise, specifying the task you want the agent to \
perform.

Before answering each question, remember that you are giving \
your answer to someone that has no knowledge about databases. \
For this reason, you should explain your answer in simple yet \
detail-oriented terms.

Information you have available:
- Headers: ```{headers}```.

Task: ```{task}```.
"""

response = get_completion(prompt)
print(response)