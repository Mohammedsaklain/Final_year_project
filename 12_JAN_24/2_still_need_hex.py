
import openai
import re
import os
import subprocess

model_engine = "gpt-3.5-turbo"



openai.api_key =  "API"
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

            # Extract the code block using regular expressions
            code_match = re.search(r'```cpp\n(.*?)\n```', response['choices'][0]['message']['content'], re.DOTALL)
            if code_match:
                code = code_match.group(1)

                # Create the 'result' folder if it doesn't exist
                result_folder = "result"
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)

                # Write the code to "result.ino" inside the 'result' folder
                file_path = os.path.join(result_folder, "result.ino")
                with open(file_path, "w") as file:
                    file.write(code)

                print(f"Code saved to '{file_path}'")

                # Change the current working directory to the 'result' folder
                os.chdir(result_folder)

                # Execute Arduino CLI to compile and upload the code
                subprocess.run(['arduino-cli', 'compile', '-b', 'arduino:avr:uno', 'result.ino'], check=True)

                print("Main HEX file compiled")

                # Move the compiled HEX file to the 'hex' folder
                os.rename('result.ino.with_bootloader.hex', '../hex/result.hex')

                print("HEX file moved to 'hex' folder")

                # Change back to the original working directory
                os.chdir("..")

                # Clean up unnecessary files
                os.remove(file_path)

                print("Cleaned up unnecessary files")
                print("=" * 20)

except KeyboardInterrupt:
    print("\nExiting ChatGPT")

