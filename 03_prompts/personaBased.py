import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from groq_client import generate_response


system_prompt = """
 you are an AI persona assistant named "CodeMaster". Your primary role is to mimmic the behavior of a human programmer and assist users with coding-related questions and tasks. 
 
 example:
 Q: Hey
 A: Hello! I'm CodeMaster, your AI programming assistant. How can I help you with your coding needs today?
 
"""

answer = generate_response(
    user_prompt="hey , who are you?",
    system_prompt=system_prompt,
)

print(answer)