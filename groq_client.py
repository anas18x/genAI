import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_response(
    user_prompt : str,
    system_prompt : str | None = None,
    max_completion_tokens: int = 300,
    messages : list[dict] | None = None   
) -> str :
    
    messages = []
    
    if system_prompt:
        messages.append({
            "role" : "system",
            "content" : system_prompt
        })
        
    
    messages.append({
        "role" : "user",
        "content" : user_prompt
    })
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format = {"type": "json_object"},
        messages=messages,
        max_completion_tokens=max_completion_tokens,
    )    
    
    content = response.choices[0].message.content

    if content is None:
        raise ValueError("The model returned no text response")

    return content