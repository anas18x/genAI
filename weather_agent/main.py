import json

import requests
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

from pydantic import BaseModel, Field
from typing import Optional


system_prompt = """
you are an AI weather assistant named "WeatherBot". Your primary role is to provide accurate and up-to-date weather information to users based on their queries. You should respond in a friendly and informative manner, ensuring that the user receives the weather details they are looking for.
other than providing weather information, you should not answer any other questions. If the user asks a question that is not related to weather, politely inform them that you can only provide weather information.


Rules:
1. Return exactly ONE valid JSON object per response.
2. Never explain your reasoning outside the JSON object.
3. Use only these steps: START, PLAN, TOOL, OBSERVE, OUTPUT.
4. Follow this sequence:
   START -> PLAN -> TOOL -> OBSERVE -> OUTPUT.
5. After START, return PLAN on the next API call.
6. After PLAN, return TOOL with the city as input.
7. After receiving OBSERVE, return OUTPUT using the tool result.
8. Never invent weather data.
9. Never use native function/tool calling. Always return a JSON object
   using the specified step format. For calling the weather function,
   return {"step":"TOOL","tool":"get_weather","input":"Delhi"}.
    


JSON formats:
{"step":"START","content":"..."}
{"step":"PLAN","content":"..."}
{"step":"TOOL","tool":"get_weather","input":"Delhi"}
{"step":"OUTPUT","content":"..."}

Available actions (these are NOT native function calls):
1. get_weather: fetches current weather for a city.
To use it, return exactly:
{"step":"TOOL","tool":"get_weather","input":"<city name>"}

JSON formats:
{"step":"START","content":"..."}
{"step":"PLAN","content":"..."}
{"step":"TOOL","tool":"get_weather","input":"Delhi"}
{"step":"OUTPUT","content":"..."}

You must return each step as a normal JSON text response,
not as a native function call.

For a weather request, return START once, PLAN once,
then TOOL with the requested city.
After receiving OBSERVE, return OUTPUT with the weather result.

Do not repeat START or PLAN.
Never invent weather data.

example:
START : what is the weather of Delhi?
PLAN:{"step":"PLAN", "content":"seem like user is asking for the weather of Delhi"}
PLAN:{"step":"PLAN", "content":"check if you have tool available to get the weather of Delhi"}
PLAN:{"step":"PLAN", "content":"use the tool to get the weather of Delhi"}
PLAN:{"step":"TOOL", "tool":"get_weather", "input":"Delhi"}
PLAN:{"step":"OBSERVE", "tool":"get_weather", "output":"The weather is Delhi is Partly cloudy +30°C"}
OUTPUT:{"step":"OUTPUT", "content":"The weather is Delhi is Partly cloudy +30°C"}

"""

class OutputFormat(BaseModel):
    step: str = Field(
        ...,
        description="Current step: START, PLAN, TOOL, OBSERVE, OUTPUT."
    )
    content: Optional[str] = Field(default=None, description="Message content.")
    tool: Optional[str] = Field(default=None, description="Tool name.")
    input: Optional[str] = Field(default=None, description="Tool input.")

def getWeather(city : str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code==200:
        return f"The weather is {city} is {response.text}"
    
    return "Unable to get weather information."


messageHistory = [
    {"role": "system", "content": system_prompt},
]

user_prompt = input("Enter your prompt: ")
messageHistory.append({"role": "user", "content": user_prompt})


client = Groq(api_key=api_key)

available_tools = {
    "get_weather": getWeather
}

while(True):
    response = client.chat.completions.parse(
    model="openai/gpt-oss-20b",
    response_format=OutputFormat,
    messages=messageHistory,
   )
    
    raw_result = response.choices[0].message.content
    messageHistory.append({"role":"assistant", "content":raw_result})
    
    parsed_result = response.choices[0].message.parsed
    # print("DEBUG:", type(parsed_result), parsed_result)
    
    if parsed_result.step == "START":
        print("🔥",parsed_result.content)
        continue
    
    if parsed_result.step == "PLAN":
        print("📝",parsed_result.content)
        continue

    if parsed_result.step == "TOOL":
        tool_name = (parsed_result.tool or "").split(".")[-1]
        tool_input = parsed_result.input
        
        print(f"🛠️ Using tool: {tool_name} with input: {tool_input}")
        tool_response = available_tools[tool_name](tool_input)
        print(f"🛠️ Tool response: {tool_response}")
        
        messageHistory.append({
        "role": "user",
        "content": json.dumps({
            "step": "OBSERVE",
            "tool": tool_name,
            "output": tool_response
        })
    })
        continue

    if parsed_result.step == "OUTPUT":
        print("✅",parsed_result.content)
        break