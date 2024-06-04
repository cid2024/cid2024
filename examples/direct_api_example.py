from openai import OpenAI

model_name = "gpt-4o"
proj_api_key = "YOUR_API_KEY_HERE"

client = OpenAI(
    api_key=proj_api_key,
)

completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print(completion.choices[0].message)
