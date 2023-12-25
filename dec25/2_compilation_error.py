#as you said my code is always assumes the that compilation was successful and proceeds to rename and move files, i tried to modify that code and i got confused where to edit that part, can you modify this for it? also whenever i run a code, there are many .eep , .ino.hex, .hex files are there outside of the hexfolder which contains main hex file, can you modify that part also to remove unnecessary hex files other than the main hex file inside the hex folder


import openai
import os
import subprocess

model_engine = "text-davinci-003"
openai.api_key = "your_api_key_here"  # Removed the API Key for security reasons

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
            
            # Compile the .ino file and save the output hex file
            build_path = os.path.join(result_folder, 'build')  # Define a separate build path
            command = f"arduino-cli compile --fqbn {board_fqbn} {file_path} --output-dir {build_path}"
            result = subprocess.run(command, shell=True, capture_output=True)
            
            # Check if the compilation was successful
            if result.returncode != 0:
                print("Compilation failed.")
                print(result.stderr.decode())
                continue  # Go to the next iteration if compilation fails
            
            print(f"Compilation successful for {file_path}")

            hex_file_pattern = os.path.join(build_path, "result.ino.*")
            output_folder = os.path.join(result_folder, 'hex_files') # Define a separate folder for storing hex files
            os.makedirs(output_folder, exist_ok=True)   # Create the folder if it doesn't exist
            
            # Move all related hex and eep files to the output_folder
            for hex_file_path in glob.glob(hex_file_pattern):
                file_name = os.path.basename(hex_file_path)
                new_file_path = os.path.join(output_folder, file_name)
                os.replace(hex_file_path, new_file_path)
                print(f"Moved {file_name} to {output_folder}")

            # Clean up the source .ino file
            os.remove(file_path)

except KeyboardInterrupt:
    print("Process was interrupted by the user.")
