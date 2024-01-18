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
board_settings = {
    "arduino uno": "arduino:avr:uno",
    "arduino nano": "arduino:avr:nano",
    "esp32": "esp32:esp32:esp32"
}

# Helper function to create required folders
def setup_folders():
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    if not os.path.exists(hex_folder):
        os.makedirs(hex_folder)

# Helper function to handle the GPT query
def GPT(query, board_type):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        user="user-" + board_type  # This will track user context based on board type
    )
    return response['choices'][0]['message']['content'].strip()

# Function to save code to a file
def save_code_to_file(code, file_path):
    with open(file_path, "w") as file:
        file.write(code)
    print(f"Code saved to '{file_path}'")

# Function to clean up files selectively, retaining certain types
def cleanup_files(directory, keep=('.ino', '.hex')):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(keep):
                os.remove(os.path.join(root, file))
    print("Cleaned up unnecessary files")

# Function to compile and upload code
def compile_and_upload_arduino_code(file_path, board_type):
    board = board_settings.get(board_type.lower())
    if not board:
        print(f"Error: Board type '{board_type}' not recognized.")
        return

    compile_command = [
        '/home/raspberrypi/Arduino/Arduino/arduino-cli', 
        'compile', 
        '-b', board, 
        '--output-dir', hex_folder, 
        file_path
    ]
    subprocess.run(compile_command, check=True)

    # Find and copy the HEX file
    hex_files = glob(f'{hex_folder}/*.hex')
    if hex_files:
        hex_file_path = hex_files[0]
        shutil.copy(hex_file_path, os.path.join(hex_folder, 'result.hex'))
        print(f"HEX file '{hex_file_path}' copied to 'hex' folder")
        
        # Cleanup
        cleanup_files(hex_folder)
    else:
        print("Error: HEX file not found.")

# Main function managing the program flow
def main():
    setup_folders()
    exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

    board_type = input("Please enter the board type (Arduino Uno, Arduino Nano, ESP32): ").strip().lower()
    if board_type not in board_settings:
        print("Error: Invalid board type entered.")
        return

    try:
        while True:
            print("Type q, Q, quit, QUIT, or EXIT and press Enter to end the chat session")
            query = input("Type your command (e.g., 'write code to blink LED at pin 7'): ")
            if query in exit_words:
                print("ENDING CHAT")
                break

            full_query = f"Write code for an {board_type} to {query}"
            response = GPT(full_query, board_settings[board_type])

            code_match = re.search(r'```cpp\n(.*?)\n```', response, re.DOTALL)
            if code_match:
                code = code_match.group(1)
                file_path = os.path.join(result_folder, "result.ino")
                save_code_to_file(code, file_path)
                compile_and_upload_arduino_code(file_path, board_type)
                print("=" * 20)
            else:
                print("Error: Code block not found in the response.")

    except KeyboardInterrupt:
        print("\nExiting program")

# Check if this module is the main run module
if __name__ == "__main__":
    main()
