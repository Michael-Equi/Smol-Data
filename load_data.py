import os
import openai
import json

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




filenames = {
    'dataset': 'adult.data.csv',
    'metadata': 'adult.names',
}

content = {}

for data_name in filenames:
    with open(filenames[data_name]) as f:
        content[data_name] = f.read()
    

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

Your first task is to extract the metadata from content given \
belog. In particular, return the following information:

- Summary of what the dataset does:
- Headers: List of column names for the dataset. Do not include \
descriptions of the headers but their names only.

You should ONLY return the fields above, in JSON format and in \
order.


Content you have available:
- Metadata: ```{content['metadata']}```.
"""




response = get_completion(prompt)

print(response)