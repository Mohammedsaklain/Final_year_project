** compare to earlier program the model engine and query handling is changed **

import openai

model_engine = "gpt-3.5-turbo"
openai.api_key = "YOUR API"


def GPT(query):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response

exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

try:
    while True:
        print("Type q, Q, quit, QUIT, or EXIT and press Enter to end the chat session")
        query = input("What is your question?> ")
        if query in exit_words:
            print("ENDING CHAT")
            break
        else:
            response = GPT(query)

            # Extract the assistant's reply and usage information
            res = str.strip(response['choices'][0]['message']['content'])
            usage = response['usage']['total_tokens']

            # Print only the assistant's reply
            print(res)
            print("=" * 20)
            print("You have used %s tokens" % usage)
            print("=" * 20)

except KeyboardInterrupt:
    print("\nExiting ChatGPT")

