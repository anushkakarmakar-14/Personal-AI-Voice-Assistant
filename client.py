from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)