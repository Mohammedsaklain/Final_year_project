from guizero import App, Text, TextBox, PushButton, Picture
def ard_uno_board():
       print("AU R3 selected")
       button_ard_uno.bg ="green"
def ard_nano_board():
        print("AU nano selected")
        button_ard_nano.bg="green"
def escape():
        print("ENDING CHAT")
app = App(title="Hello") # indexname
app.bg = "#FBFBD0" #background clor
message = Text(app, text="Welcome To CodeGen Assist",font="TimesNewRoman",size=20)# text widget
button_ard_uno=PushButton(app, ard_uno_board,text="Arduino Uno")
button_ard_uno.bg="lightgreen"
button_ard_nano=PushButton(app, ard_nano_board,text="Arduino nano")
button_ard_nano.bg="lightgreen"
button_exit = PushButton(app, escape, text="QUIT")
prompt = Text(app,"Enter your prompt")
input_box = TextBox(app, text=" ", height=5,width=40, multiline=True,scrollbar=True)
input_box.bg = "white"
button_exit.bg="red"
app.display()
