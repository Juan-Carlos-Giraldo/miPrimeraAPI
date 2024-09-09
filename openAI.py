from dotenv import load_dotenv
import os
import openai

openai.api_key = "sk-wWiSDXVNEbtn0_NglMCEaQVblS06tOyhB7IPOaNzI9T3BlbkFJvR9JNZfFD4O9AW-sSrpcuSk99peKuHo6iqjyJT4QIA"

prompt = "Translate the following English text to French: 'Hello, how are you?'"

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=60
)

print(response.choices[0].text.strip())