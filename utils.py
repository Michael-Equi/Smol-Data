import os
import openai
from load_data import get_completion


def text_to_html(text):
    prompt = """
Convert the following text to HTML:
```{text}```
    """.format(text=text)

    result = get_completion(prompt)

    return result

if __name__ == '__main__':
    text = """
    # This is a heading

    This is a paragraph.
    """

    html = text_to_html(text)

    print(html)