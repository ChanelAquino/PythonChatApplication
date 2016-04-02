# -*- coding: utf-8 -*-

from Tkinter import *
from chat import *
from PIL import *
import thread
import tkMessageBox
from tkFileDialog import askopenfilename



HOST = gethostname()
PORT = 9003
s = socket(AF_INET, SOCK_STREAM)

def onClick():
    messageText = messageFilter(textBox.get("0.0",END)) #filter

    if "/shrug" in messageText :
        messageText =  "¯\_(ツ)_/¯"
        s.send(messageText)

    elif "/creep" in messageText :
        messageText = "( ͡° ͜ʖ ͡°)"
        s.send(messageText) #Just send the message
    elif "/smile" in messageText :
        messageText = "•ᴗ•"
        s.send(messageText) #Just send the message
    elif "/what" in messageText :
        messageText = "ლ(ಠ_ಠლ)"
        s.send(messageText) #Just send the message
    elif "/img" in messageText :
        s.send("Your partner is sending an image... /img")#do image stuff
        tkMessageBox.showinfo(title="Image Transfer", message="Click OK to Select Image")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        Image.open(filename).show()
    else:
        s.send(messageText) #send over socket

    displayLocalMessage(chatBox, messageText) #display local
    chatBox.yview(END) #auto-scroll
    textBox.delete("0.0",END) #clear the input box

def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def ReceiveData():
    try:
        s.connect((HOST, PORT))
        getConnectionInfo(chatBox, '[ Connected! ]\n-------------------------------------')
    except:
        getConnectionInfo(chatBox, '[ Cannot connect ]')
        return

    while 1:
        try:
            data = s.recv(1024)
        except:
            getConnectionInfo(chatBox, '\n [ Your partner left.] \n')
            break
        if data != '':
            displayRemoteMessage(chatBox, data)

        else:
            getConnectionInfo(chatBox, '\n [ Your partner left. ] \n')
            break
    s.close()


#Base Window
base = Tk()
base.title("Pychat Client")
base.geometry("400x450")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#716664")

#Chat
chatBox = Text(base, bd=0, bg="#689099", height="8", width="20", font="Helvetica",)
chatBox.insert(END, "Waiting for your partner to connect..\n")
chatBox.config(state=DISABLED)
sb = Scrollbar(base, command=chatBox.yview, bg = "#34495e")
chatBox['yscrollcommand'] = sb.set

#Send Button
sendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onClick)

#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="29", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)

#Put everything on the window
sb.place(x=370,y=5, height=350)
chatBox.place(x=15,y=5, height=350, width=355)
sendButton.place(x=255, y=360, height=80, width=130)
textBox.place(x=15, y=360, height=80, width=250)

thread.start_new_thread(ReceiveData,())
base.mainloop()
