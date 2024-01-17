import openai
import re
import os
import subprocess
import shutil
from glob import glob

# Initializing constants and configurations
model_engine = "gpt-3.5-turbo"
openai.api_key = "api"
result_folder = 'result'
hex_folder = 'hex'

# Helper function to create required folders
def setup_folders():
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    if not os.path.exists(hex_folder):
        os.makedirs(hex_folder)

# Helper function to handle the GPT query
def GPT(query):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to save code to a file
def save_code_to_file(code, file_path):
    with open(file_path, "w") as file:
        file.write(code)
        print(f"Code saved to '{file_path}'")

# Function to clean up files
def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    print("Cleaned up unnecessary files")

# Function to compile and upload code, and handle the resulting HEX file
def compile_and_upload_arduino_code(file_path):
    # Execute Arduino CLI to compile and upload the code
    subprocess.run(['/home/raspberrypi/Arduino/Arduino/arduino-cli', 'compile', '-b', 'arduino:avr:uno', '--output-dir', hex_folder, file_path], check=True)
    
    print("Main HEX file compiled")

    # Find the HEX file in the 'hex' folder
    hex_files = glob(f'{hex_folder}/*.hex')
    if hex_files:
        hex_file_path = hex_files[0]
        # Copy the HEX file directly to the 'hex' folder
        shutil.copy(hex_file_path, os.path.join(hex_folder, 'result.hex'))
        print(f"HEX file '{hex_file_path}' copied to 'hex' folder")

        # Cleanup
        cleanup_files(file_path, hex_file_path)
    else:
        print("Error: HEX file not found.")

# Main function managing the program flow
def main():
    setup_folders()
    exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

    try:
        while True:
            print("Type q, Q, quit, QUIT, or EXIT and press Enter to end the chat session")
            query = input("What is your question?> ")
            if query in exit_words:
                print("ENDING CHAT")
                break
            elif "code" not in query.lower():
                print("Error: Your question does not appear to be a code request.")
            else:
                response = GPT(query)
                # Extract the code block using regular expressions
                code_match = re.search(r'```cpp\n(.*?)\n```', response, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                    file_path = os.path.join(result_folder, "result.ino")
                    save_code_to_file(code, file_path)
                    compile_and_upload_arduino_code(file_path)
                    print("=" * 20)
                else:
                    print("Error: Code block not found in the response.")

    except KeyboardInterrupt:
        print("\nExiting ChatGPT")

# Check if this module is the main run module
if __name__ == "__main__":
    main()
