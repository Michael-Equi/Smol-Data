import openai
import dotenv
import os
import re

dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORG")

from prompts import EXAMPLE_DATA, CONTROLLER_SYSTEM_PROMPT

class Controller:

    def __init__(self) -> None:
        self.state = [
            {"role": "system", "content": CONTROLLER_SYSTEM_PROMPT},
        ]
        self.hypothesis_buffer = []

    def load_data(self) -> None:
        # Adds information about the dataset to the state
        self.data_description = EXAMPLE_DATA

    def plan(self, user_request) -> None:
        # Generate a plan for testing the data
        self.state.append({"role": "user", "content": f"You are provided the following data:\n\n{self.data_description}\n\nYour client requests the following insight(s):\n{user_request}"})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.state
            )
        text = response["choices"][0]["message"]["content"]
        print(text)

        # Split the text by newline character to get each line separately
        lines = text.split('\n')

        # Initialize an empty list to hold the steps
        steps = []

        # Regular expression pattern for "step x: "
        step_pattern = re.compile("step \d+: ", re.IGNORECASE)

        # Loop through each line
        for line in lines:
            # Check if the line starts with 'step'
            if line.startswith('step'):
                # Remove the "step x: " part from the line, then strip leading/trailing whitespace and add to the list of steps
                step = step_pattern.sub("", line).strip()
                steps.append(step)

        print(steps)

    def reflect(self) -> None:
        # Adds to hypothesis buffer
        pass

if __name__ == "__main__":
    controller = Controller()
    controller.load_data()
    controller.plan("What is the relationship between work class and eduction?")