# Final_year_project
This file was created on 12-10-2023 at 10:37


Please use different API KEY, this key is no longer accessible

- 1. Set up the required modules and API keys.

- 2. Create a function called GPT that uses OpenAI's GPT-3 engine to generate a response based on the input query.

- 3. Create a result folder if it doesn't exist.

- 4. Start an input loop to select the board type ("Arduino Uno" or "Arduino Nano").

- 5. Based on the selected board type, set the corresponding board_fqbn and break the loop.

- 6. Start an infinite loop to receive queries from the user.

- 7. If the user input matches any of the exit words ("q", "Q", "quit", "QUIT", "EXIT"), exit the loop and end the chat.

- 8. If the input is not an exit word, use the GPT function to get a response based on the input query and print the response.

- 9. Define the path to the .ino file within the result folder and write the response to the result.ino file within the result folder.

- 10. Compile the .ino file and save the output hex file in a separate build path.

- 11. Check if the compilation was successful, print an error message if it failed, and continue to the next iteration.

- 12. If the compilation was successful, move the related hex and eep files to a separate folder for storing hex files.

- 13. Clean up the source .ino file after completion of each iteration.

- 14. Handle the interruption of the process by the user (if keyboard interruption occurs).


<img src="code_diagram.drawio.png" alt="drawing" style="width:200px;"/>

      

