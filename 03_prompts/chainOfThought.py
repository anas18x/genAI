import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


system_prompt= """u are a coding expert. answer the question step by step and then give the final answer. if the question is not related to coding, say sorry I can only answer coding questions.

Return every response as a valid JSON object with these keys:
- "STEP": "START", "PLANNING", or "END"
- "content": your response as a string

All responses must follow this JSON format.

STEP = START
1: understand the question and identify the key components.

STEP = PLANNING
1: break down the problem into smaller parts and solve each part.
2: combine the solutions of the smaller parts to arrive at the final answer.
3: review the final answer to ensure it is correct.

STEP = END
1: provide the final answer in a clear and concise manner.

example: program to add two numbers -> def add_numbers(a, b): return a + b
steps for the example:

STEP = START
1: understand the question and identify the key components.

STEP = PLANNING
1: break down the problem into smaller parts and solve each part
2: plan the solution and write the code.
3: test the code with different inputs to ensure it works correctly.
4: review the final answer to ensure it is correct.

STEP = END
1: provide the final answer in a clear and concise manner.

"""

print("\n\n")

message_history = [
    {"role": "system", "content": system_prompt},
]

user_prompt = input("Enter your prompt: ")
message_history.append({"role": "user", "content": user_prompt})

while True:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        messages=message_history,
        # max_completion_tokens=300,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role":"assistant", "content":raw_result})
    
    parsed_result = json.loads(raw_result)
    
    if parsed_result.get("STEP") == "START":
        print("starting to solve the problem...")
        print(parsed_result.get("content"))
        continue
    
    if parsed_result.get("STEP") == "PLANNING":
        print("planning the solution...")
        print(parsed_result.get("content"))
        continue
    
    if parsed_result.get("STEP") == "END":
        print(" 🤖 ",parsed_result.get('content'))
        break
    

