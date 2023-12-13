#In this code, the output is stored in result.txt file and no other print lines are there, even in the beginning

import openai

model_engine = "text-davinci-003"
openai.api_key = "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"

def GPT(query):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=1024,
        temperature=0.5,
    )
    
    return response['choices'][0]['text'].strip()

exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

try:
    while True:
        query = input()  # Removed the prompt to make it cleaner
        if query in exit_words:
            break  # Ends the chat without printing "ENDING CHAT"
        else:
            answer = GPT(query)
            print(answer)  # Only prints the answer
            
            with open('result.txt', 'a') as file:  # Changed file name to 'result.txt'
                file.write(answer + "\n")  # File only logs the answer.
except KeyboardInterrupt:
    print()  # Prints a new line for clean exit
