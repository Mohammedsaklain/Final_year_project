
import openai
import re
import os
import subprocess
import shutil
from glob import glob

model_engine = "gpt-3.5-turbo"

openai.api_key =  "api"

def GPT(query):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

result_folder = 'result'
hex_folder = 'hex'

if not os.path.exists(result_folder):
    os.makedirs(result_folder)

if not os.path.exists(hex_folder):
    os.makedirs(hex_folder)

try:
    while True:
        print("Type q, Q, quit, QUIT, or EXIT and press Enter to end the chat session")
        query = input("What is your question?> ")
        if query in exit_words:
            print("ENDING CHAT")
            break
        else:
            response = GPT(query)

            # Extract the code block using regular expressions
            code_match = re.search(r'```cpp\n(.*?)\n```', response, re.DOTALL)
            if code_match:
                code = code_match.group(1)

                file_path = os.path.join(result_folder, "result.ino")
                with open(file_path, "w") as file:
                 file.write(code)

                print(f"Code saved to '{file_path}'")

                # Execute Arduino CLI to compile and upload the code
                subprocess.run(['/home/raspberrypi/Arduino/Arduino/arduino-cli', 'compile', '-b', 'arduino:avr:uno', '--output-dir', '../hex', file_path], check=True)


                print("Main HEX file compiled")

                # Find the HEX file in the 'hex' folder
                hex_files = glob('../hex/*.hex')
                if hex_files:
                    hex_file_path = hex_files[0]

                    # Copy the HEX file directly to the 'hex' folder
                    shutil.copy(hex_file_path, os.path.join(hex_folder, 'result.hex'))

                    print(f"HEX file '{hex_file_path}' copied to 'hex' folder")

                    # Clean up unnecessary files
                    os.remove(file_path)
                    os.remove(hex_file_path)

                    print("Cleaned up unnecessary files")
                    print("=" * 20)
                else:
                    print("Error: HEX file not found.")

except KeyboardInterrupt:
    print("\nExiting ChatGPT")

