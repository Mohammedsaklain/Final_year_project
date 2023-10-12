import openai

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

exit_words = ("q","Q","quit","QUIT","EXIT")

try:
   with open('output.txt', 'w') as f:
       while True:
           print("Type q, Q, quit, QUIT or EXIT and press Enter to end the chat session")
           query = input("What is your question?> ")
           if query in exit_words:
               print("ENDING CHAT")
               break
           else:
               (res, usage) = GPT(query)
               print(res)
               f.write(res + '\n')
               print("="*20)
               print("You have used %s tokens" % usage)
               print("="*20)
except KeyboardInterrupt:
   print("\nExiting ChatGPT")

  
#In this script, the open function is used to open a file named output.txt in write mode ('w').
#If the file does not exist, it will be created. The write function is then used to write the content of res to the file after each response. 
#The file will be saved in the same directory as your Python script.
