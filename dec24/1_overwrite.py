# save inside a result folder

import openai
import os

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

result_folder = 'result'
if not os.path.exists(result_folder):
    os.makedirs(result_folder)  # Create the result directory if it doesn't exist

exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

try:
    while True:
        query = input()
        if query in exit_words:
            break  # Ends the chat without printing "ENDING CHAT"
        else:
            answer = GPT(query)
            print(answer)  # Only prints the answer
            
            # Define the path to the .ino file within the result folder
            file_path = os.path.join(result_folder, 'result.ino')
            
            # Write the answer to the result.ino file in the result folder
            with open(file_path, 'w') as file:  # Use 'w' mode to overwrite the existing content
                file.write(answer + "\n")  # File only logs the answer.

except KeyboardInterrupt:
    print()  # Prints a new line for clean exit
