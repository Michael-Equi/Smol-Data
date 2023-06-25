import openai
import dotenv
import os
from prompts import EXECUTOR_PROMPT
import traceback

dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORG")

class Executor():
    def __init__(self, data_description, data_location):
        self.data_location = data_location
        self.data_description = data_description

    def generate_code(self, steps):
        messages = [{"role": "system", "content": EXECUTOR_PROMPT(self.data_description, self.data_location)}]
        messages.append({"role": "user", "content": steps})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
            )
        text = response["choices"][0]["message"]["content"]
        return text
    
    def execute(self, code):
        env = {}
        try:
            exec(code, env)
            print("Code executed succesfully")
            return env
        except Exception as e:
            print(f"An error occurred: {e}")
            return e, traceback.print_exc()


steps = """
step 1: Load the dataset into a suitable format, e.g., a pandas DataFrame
step 2: Handle any missing data (e.g., replace '?' by NaN, drop rows with missing data, or impute missing values)
step 3: Calculate the frequency distribution of the different work classes and education levels
step 4: Calculate the cross-tabulation (contingency table) between work class and education level [report]
step 5: Calculate the Pearson's Chi-squared test statistic and p-value to determine the dependence between work class and education level [report]
step 6: Calculate the Cramér's V coefficient to measure the strength of the association between work class and education level [report]
"""

code = """```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Step 1: Load the dataset into a pandas DataFrame
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
column_names = ["Age", "Work Class", "fnlwgt", "Education", "Education Num", "Marital Status",
                "Occupation", "Relationship", "Race", "Sex", "Capital Gain", "Capital Loss",
                "Hours per Week", "Native Country", "Income"]
df = pd.read_csv(url, header=None, names=column_names, sep=',\s', na_values=["?"], engine='python')

# Step 2: Handle missing data
df = df.dropna()

# Step 3: Calculate the frequency distribution of work classes and education levels
work_class_freq = df['Work Class'].value_counts()
education_freq = df['Education'].value_counts()

# Step 4: Calculate the cross-tabulation between work class and education level
crosstab = pd.crosstab(df['Work Class'], df['Education'])

# Report results
print("Cross-tabulation:\n", crosstab)

# Step 5: Calculate the Pearson's Chi-squared test statistic and p-value
chi_stat, p_value, _, _ = chi2_contingency(crosstab)

# Report results
print("Chi-squared test statistic: ", chi_stat)
print("p-value: ", p_value)

# Step 6: Calculate the Cramér's V coefficient
n = crosstab.sum().sum()
min_dim = min(crosstab.shape) - 1
cramers_v = np.sqrt(chi_stat / (n * min_dim))

# Report results
print("Cramér's V coefficient: ", cramers_v)
```"""

if __name__ == "__main__":
    data_description = "This is a dataset from the 1994 consensus"
    data_location = "data/adult.data.csv"
    executor =  Executor(data_description, data_location)
    # print(executor.generate_code(steps))
    code = code.strip('```')
    print(code)
 