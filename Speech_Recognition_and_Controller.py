import tkinter as tk
from PIL import ImageTk,Image

import speech_recognition as sr
import pyttsx3
import serial
import time
import socket

#Establishing connection with ESP8266
esp_ip = "192.168.50.163"
esp_port = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((esp_ip, esp_port))

#Function to send data to ESP8266
def send(message):
    try:
        sock.sendall(message.encode() + b'\n')
    except KeyboardInterrupt:
        print("Closing connection")
    finally:
        pass

#Function to decide with command to send
def listen_for_commands(c):
    global Flag
    try:
        print(f"Command recognized: {c}")
        if "forward" in c:
            print('Forward')
            send('w')
            
        elif "backward" in c:
            print('Backward')
            send('d')

        elif "left" in c:
            print('Left')
            send('a')

        elif "right" in c:
            print('Right')
            send('d')

        elif "off" in c:
            print ('Deactivate')            
            Flag=False

        else:
            print('Invalid Command')
    except sr.UnknownValueError:
        print("Sorry, I did not understand the audio.")
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")

#Function to activate speach recognition
def StartVoice():
    
    global Flag
    Flag=True
    while Flag:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Voice Commands Activated....")
                audio = r.listen(source)
                command = r.recognize_google(audio)

                listen_for_commands(command)

        except Exception as e:
            print("Error; {0}".format(e))

#Defining funtions of each button
def on_click(event):
    item = canvas.find_withtag("current")[0]
    
    if item == Up:
        print("Up")
        send('f')
    elif item == Down:
        print("Down")
        send('b')
    elif item == Left:
        print("Left")
        send('l')
    elif item == Right:
        print("Right")
        send('r')
    elif item == Voice:
        print('Voice')
        StartVoice()
    elif item == Stop:
        print('Stop')
        send('s')


#Creating GUI        
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=500, bg='white')
canvas.pack()

bg=Image.open('Background.png')
rebg=bg.resize((600,500),Image.LANCZOS)
i=ImageTk.PhotoImage(rebg)
canvas.create_image(0,0,image=i,anchor='nw')

canvas.create_text(300, 30, text = "VoBOT", font = ("Arial", 30),fill='white')
Up = canvas.create_polygon(300, 100, 250, 200, 350, 200, fill='red',width=10)
Down = canvas.create_polygon(250, 370, 300, 470, 350, 370, fill='red')
Left = canvas.create_polygon(200, 335, 100, 285, 200, 235, fill='red')
Right = canvas.create_polygon(400, 235, 400, 335, 500, 285, fill='red')
Voice = canvas.create_oval(350, 235, 250, 335,fill='yellow')
canvas.create_text(300, 285, text = "Voice", font = ("Arial", 15))
Stop = canvas.create_oval(10, 490, 110, 390,fill='pink')
canvas.create_text(60, 440, text = "Stop", font = ("Arial", 15))


canvas.tag_bind(Up, '<ButtonPress-1>', on_click)
canvas.tag_bind(Down, '<ButtonPress-1>', on_click)
canvas.tag_bind(Left, '<ButtonPress-1>', on_click)
canvas.tag_bind(Right, '<ButtonPress-1>', on_click)
canvas.tag_bind(Voice, '<ButtonPress-1>', on_click)
canvas.tag_bind(Stop, '<ButtonPress-1>', on_click)




root.mainloop()

