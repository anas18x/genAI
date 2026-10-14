import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")
text = "Hello, how are you?"
tokens = enc.encode(text)

print(f"Text: {text}")
print(f"Tokens: {tokens}")