import openai
from guizero import App, Text, PushButton

model_engine = "gpt-3.5-turbo"
openai.api_key = "YOUR API"  # Replace with your actual API key

def GPT(query):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response

def send_prompt():
    prompt = text_box.value
    response = GPT(prompt)

    # Extract the assistant's reply and usage information
    res = str.strip(response['choices'][0]['message']['content'])
    usage = response['usage']['total_tokens']

    code_display.value = res
    token_usage.value = f"Tokens used: {usage}"

app = App(title="ChatGPT Assistant")

text_box = Text(app, text="Enter your question:", width=40)
text_box.textsize = 14

code_display = Text(app, text="", width=40, height=10, multiline=True)
code_display.textsize = 12

token_usage = Text(app, text="", width=40)

send_button = PushButton(app, text="Ask ChatGPT", command=send_prompt)

app.display()
