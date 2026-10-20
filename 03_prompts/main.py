import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from groq_client import generate_response


system_prompt = (
    "Only answer mathematical questions. "
    "For any other question, explain that you can "
    "only answer mathematical questions."
    "give the answer in json format."
)

zero_shot_prompt = (
    "answer only coding questions. other than that say sorry I can only answer coding questions."
    "give the answer in json format."
)

few_shot_prompt = (
    """answer only coding questions. other than that say sorry I can only answer coding questions!. 
    "give the answer in json format."
    """
    
    "example: tell me a joke -> sorry I can only answer coding questions."
    
    "example: program to add two numbers -> def add_numbers(a, b): return a + b"
)

answer = generate_response(
    user_prompt="Hey , program to multiply two numbers",
    system_prompt=few_shot_prompt,
)

print(answer)
