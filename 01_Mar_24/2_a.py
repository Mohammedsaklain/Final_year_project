import tkinter as tk

def ard_uno_board():
    print("AU uno selected")
    button_ard_uno.config(bg="lightblue")  # Change color when button is pressed

def ard_nano_board():
    print("AU nano selected")
    button_ard_nano.config(bg="lightblue")  # Change color when button is pressed

def esp_32_board():
    print("esp-32 selected")
    button_esp.config(bg="lightblue")  # Change color when button is pressed
    
def escape():
    print("ENDING CHAT")

root = tk.Tk()
root.geometry("480x320")
root.configure(bg="#FBFBD0")  # background color

message = tk.Label(root, text="Welcome To CodeGen Assist", font=("TimesNewRoman", 20))
message.pack()

prompt = tk.Label(root, text=" Select Board ")
prompt.place(x=0,y=55)


button_ard_uno = tk.Button(root, text="Arduino Uno", width=10, height=1, command=ard_uno_board)
button_ard_uno.configure(bg="lightgreen")
button_ard_uno.place(x=0, y=74)

button_ard_nano = tk.Button(root, text="Arduino nano", width=10, height=1, command=ard_nano_board)
button_ard_nano.configure(bg="lightgreen")
button_ard_nano.place(x=0, y=99)

button_esp = tk.Button(root, text="esp-32", width=10, height=1, command=esp_32_board)
button_esp.configure(bg="lightgreen")
button_esp.place(x=0, y=124)


button_exit = tk.Button(root, text="QUIT", width=10, height=1, command=escape)
button_exit.configure(bg="red")
button_exit.place(x=400, y=62)

prompt = tk.Label(root, text="Enter your prompt")
prompt.pack()

input_box = tk.Text(root, height=1.5, width=38)
input_box.pack()

root.mainloop()

