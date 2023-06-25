import os
import openai
import pandas as pd
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



def get_prompt_data(metadata_filename, dataset_filename, num_samples=20):
    with open(metadata_filename) as f:
        metadata = f.read()
        

    prompt = f'''
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

    Your first task is to extract the metadata from raw text. \
    You should ONLY return the fields described below, in JSON \
    format and in order. The keys of the JSON object should be \
    the names of the fields. For example, if the field is called \
    "name" and the value is "John", then the JSON object should \
    be ```{{"name": "some data"}}```.

    - summary: Summary of what the dataset does. It should be \
    extensive, covering all important information from the text. \
    - headers: List of column names for the dataset. Do not include \
    descriptions of the headers but their names only.



    Content you have available: \
    - Metadata: ```{metadata}```.
    '''




    response_json = get_completion(prompt)
    data = json.loads(response_json)


    df = pd.read_csv(dataset_filename)

    data['subset'] = df.sample(n=num_samples).values.tolist()

    return data



if __name__ == '__main__':
    data = get_prompt_data('adult.names', 'adult.data.csv')

    print(json.dumps(data, indent=4))