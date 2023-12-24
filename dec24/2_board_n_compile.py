#in this code the output generated will be compiled and created a hex file 

import openai
import os
import subprocess

model_engine = "text-davinci-003"
openai.api_key = "sk-9886O6ZF5PRBD4jetS6T3BlbkFJZA7YxNxxlXoOLOFpQE6"

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
            break  # Ends the loop
        else:
            answer = GPT(query)
            print(answer)  # Only prints the answer
            
            # Define the path to the .ino file within the result folder
            file_path = os.path.join(result_folder, 'result.ino')
            
            # Write the answer to the result.ino file in the result folder
            with open(file_path, 'w') as file:  # Use 'w' mode to overwrite the existing content
                file.write(answer + "\n")  # File writes the answer.
            
            # Prompt the user to enter the Arduino board's fully qualified board name
            board_name = input("Enter your Arduino board's fully qualified board name: ")
            
            # Compile the .ino file using the Arduino IDE command-line interface with user provided board name
            compile_command = f'arduino-cli compile --fqbn {board_name} {file_path} --output-dir {result_folder}'
            try:
                subprocess.run(compile_command, shell=True, check=True)
                print("Compilation successful")
            except subprocess.CalledProcessError as e:
                print(f"Compilation failed with the following error: {e}")

except KeyboardInterrupt:
    print()  # Prints a new line for clean exit

