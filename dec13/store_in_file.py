#IN this code, the output is stored in the text file named result.txt and also the output is printed on to the console

import openai
import datetime

model_engine = "text-davinci-003"
openai.api_key = "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"

def GPT(query):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=1024,
        temperature=0.5,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']
exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

try:
    while True:
        print("Type q, Q, quit, QUIT or EXIT and press Enter to end the chat session")
        query = input("What is your question?> ")
        if query in exit_words:
            print("ENDING CHAT")
            break
        else:
            (res, usage) = GPT(query)
            print(res)
            print("="*20)
            print("You have used %s tokens" % usage)
            print("="*20)
            
            with open('result.txt', 'a') as file:
                file.write(f"Time: {datetime.datetime.now()}\n")
                file.write(f"Question: {query}\n")
                file.write(f"Response: {res}\n")
                file.write(f"Tokens used: {usage}\n")
                file.write("="*30 + "\n")
except KeyboardInterrupt:
    with open('result.txt', 'a') as file:
        file.write(f"Time: {datetime.datetime.now()} - Chat session was terminated by user\n")
    print("\nExiting ChatGPT")

