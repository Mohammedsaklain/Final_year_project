#In this script, I’ve changed filename = f'output_{timestamp_str}.txt' to filename = f'output_{timestamp_str}.ino' 
#to save the output with a .ino extension.##import openai


import datetime

model_engine = "text-davinci-003"
openai.api_key = "YOUR API KEY HERE"

def GPT(query):
   response = openai.Completion.create(
       engine=model_engine,
       prompt=query,
       max_tokens=1024,
       temperature=0.5,
   )
   return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']

def extract_code(response):
    # Split the response into lines
    lines = response.split('\n')
    
    # Find the lines that start and end the code block
    start_line = lines.index('```') + 1
    end_line = lines.index('```', start_line)
    
    # Extract the code lines and join them back into a single string
    code = '\n'.join(lines[start_line:end_line])
    
    return code

exit_words = ("q","Q","quit","QUIT","EXIT")

N = 5  # Change this to the number of prompts per file you want
prompt_count = 0

try:
   while True:
       print("Type q, Q, quit, QUIT or EXIT and press Enter to end the chat session")
       query = input("What is your question?> ")
       if query in exit_words:
           print("ENDING CHAT")
           break
       else:
           (res, usage) = GPT(query)
           res = extract_code(res)
           print(res)
           # Get the current date and time
           now = datetime.datetime.now()
           # Format as a string
           timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
           # Create a filename with the timestamp and .ino extension
           if prompt_count % N == 0:
               filename = f'output_{timestamp_str}.ino'
           # Write the output to the file
           with open(filename, 'a') as f:
               f.write(res + '\n')
           print("="*20)
           print("You have used %s tokens" % usage)
           print("="*20)
           prompt_count += 1
except KeyboardInterrupt:
   print("\nExiting ChatGPT")
