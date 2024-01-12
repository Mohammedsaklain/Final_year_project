

#as you said my code is always assumes the that compilation was successful and proceeds to rename and move files, i tried to modify that code and i got confused where to edit that part, can you modify this for it? also whenever i run a code, there are many .eep , .ino.hex, .hex files are there outside of the hexfolder which contains main hex file, can you modify that part also to remove unnecessary hex files other than the main hex file inside the hex folder

import glob
import openai
import os
import subprocess


model_engine = "gpt-3.5-turbo"
openai.api_key = "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"
# Removed the API Key for security reasons

def GPT(query):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response


result_folder = 'result'
if not os.path.exists(result_folder):
    os.makedirs(result_folder)  # Create the result directory if it doesn't exist

exit_words = ("q", "Q", "quit", "QUIT", "EXIT")

while True:
    board = input("Which board do you want to use? (Arduino Uno/Arduino Nano): ")
    if board.lower() == "arduino uno":
        board_fqbn = "arduino:avr:uno"
        break
    elif board.lower() == "arduino nano":
        board_fqbn = "arduino:avr:nano"
        break
    else:
        print("Invalid board selection. Please try again.")


# Define the path to the .ino file within the result folder
file_path = os.path.join(result_folder, 'result.ino')

try:
    while True:
        query = input("Enter your command: ").strip()
        if query in exit_words:
            break
        else:
            answer = GPT(query)
            assistant_message = answer['choices'][0]['message']['content']
            code_start_index = assistant_message.find("```cpp")
            code_end_index = assistant_message.find("```", code_start_index + 1)

            if code_start_index != -1 and code_end_index != -1:
                code_part = assistant_message[code_start_index + 5:code_end_index].strip()
                print(code_part[1:])  # Exclude the initial 'p' when printing the code block
            else:
                print("No code block found in the response.")

            # Write the answer to the result.ino file in the result folder
            with open(file_path, 'w') as file:
                file.write(answer['choices'][0]['message']['content'] + "\n")

            # Compile the .ino file and save the output hex file
            build_path = os.path.join(result_folder, 'build')
            command = f"arduino-cli compile --fqbn {board_fqbn} {file_path} --output-dir {build_path}"

            try:
                result = subprocess.run(command, shell=True, capture_output=True, check=True)
                print(f"Compilation successful for {file_path}")

                # Clean up unnecessary hex files
                hex_file_pattern = os.path.join(build_path, "result.ino.hex")
                output_folder = os.path.join(result_folder, 'hex_files')
                os.makedirs(output_folder, exist_ok=True)

                # Move the main hex file to the output_folder
                main_hex_file_path = os.path.join(build_path, "result.ino.hex")
                new_file_path = os.path.join(output_folder, "result.ino.hex")
                os.replace(main_hex_file_path, new_file_path)
                print(f"Moved result.ino.hex to {output_folder}")

                # Clean up the source .ino file
                os.remove(file_path)

            except subprocess.CalledProcessError as e:
                print("Compilation failed.")
                print(e.stderr.decode())

except KeyboardInterrupt:
    print("Process was interrupted by the user.")

