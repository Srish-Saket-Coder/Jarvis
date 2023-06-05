import os
import openai
from api_keys import openai_api_key

openai.api_key = os.getenv(openai_api_key)

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Write an email to my boss for resigination",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
print(response)
