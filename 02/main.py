
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# Create the API client
client = Groq(api_key=api_key)

# Send a prompt to the model
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "hey this is Anas, can you tell me a joke?"
        }
    ],
    max_completion_tokens=300,
)

# Print the generated response
print(response.choices[0].message.content)
