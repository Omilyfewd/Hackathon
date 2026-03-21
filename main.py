import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

try:
    response = completion(
        model="gemini/gemini-3.1-flash-lite-preview",
        messages=[{"role": "user", "content": "Write a 3-line poem about automation."}]
    )
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error occurred: {e}")



