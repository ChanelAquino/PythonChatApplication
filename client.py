# -*- coding: utf-8 -*-

import thread
import tkMessageBox
from tkFileDialog import askopenfilename
from chat_functions import *
from Tkinter import *
from PIL import ImageTk, Image
import os
#---------------------------------------------------#
#---------INITIALIZE CONNECTION VARIABLES-----------#
#---------------------------------------------------#
WindowTitle = 'Pychat Client'
HOST = gethostname()
PORT = 9002
s = socket(AF_INET, SOCK_STREAM)

#---------------------------------------------------#
#------------------ MOUSE EVENTS -------------------#
#---------------------------------------------------#
def ClickAction():
    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    LoadMyEntry(ChatLog, EntryText)

    #Scroll to the bottom of chat windows
    ChatLog.yview(END)

    #Erace previous message in Entry Box
    EntryBox.delete("0.0",END)


    if '/pin' in EntryText:
        s.send("Your partner is sending an emojo... /pin")#do image stuff
        #LoadMyEntry(ChatLog, "Please enter the path to your image:")
        
        root = Toplevel() #instead of making a new tk, you are supposed to do this to make a new window
        img = ImageTk.PhotoImage(Image.open("pin.png"))#makes it okay to open all types of images instead of just gifs
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop()
        """root = Tk()
        img = ImageTk.PhotoImage(Image.open("1.png"))
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop()
        tkMessageBox.showinfo(title="Image Transfer", message="Click OK to Select Image")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        LoadMyEntry(ChatLog, "You selected " + filename)
        s.send(filename)
        fp = Image.open(filename)
        LoadMyEntry(ChatLog, "Starting image transfer...")
        while True:
            strng = s.recv(512)
            if not strng:
                break
            fp.write(strng)
        fp.close()
        LoadMyEntry(ChatLog, " Sending side stopped, problem must be on HOST side")"""
    else:
         s.send(EntryText) #Just send the message
    if '/smile' in EntryText:
        s.send("Your partner is sending an emojo... /smile")#do image stuff
        #LoadMyEntry(ChatLog, "Please enter the path to your image:")
        
        root = Toplevel()
        img = ImageTk.PhotoImage(Image.open("smile.png"))
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop() 
    else:
        s.send(EntryText) #Just send the message
    if '/mad' in EntryText:
        s.send("Your partner is sending an emojo... /mad")#do image stuff
        #LoadMyEntry(ChatLog, "Please enter the path to your image:")
        
        root = Toplevel()
        img = ImageTk.PhotoImage(Image.open("mad.png"))
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop() 
    else:
        s.send(EntryText) #Just send the message
    if '/barf' in EntryText:
        s.send("Your partner is sending an emojo... /barf")#do image stuff
        #LoadMyEntry(ChatLog, "Please enter the path to your image:")
        
        root = Toplevel()
        img = ImageTk.PhotoImage(Image.open("barf.png"))
        panel = Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        root.mainloop() 
    else:
        s.send(EntryText) #Just send the message
#---------------------------------------------------#
#----------------- KEYBOARD EVENTS -----------------#
#---------------------------------------------------#
def PressAction(event):
	EntryBox.config(state=NORMAL)
	ClickAction()
def DisableEntry(event):
	EntryBox.config(state=DISABLED)


#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#

#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#716664")

#Create a Chat window
ChatLog = Text(base, bd=0, bg="#42737E", height="8", width="50", font="Helvetica",)
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create the Button to send message
SendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#8DB85D", activebackground="#8DB85D", justify="center",
                    command=ClickAction)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="#CC7967",width="29", height="5", font="Courier")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
SendButton.place(x=128, y=401, height=90)
EntryBox.place(x=6, y=401, height=90, width=265)


#---------------------------------------------------#
#----------------CONNECTION MANAGEMENT--------------#
#---------------------------------------------------#

def ReceiveData():
    try:
        s.connect((HOST, PORT))
        LoadConnectionInfo(ChatLog, '[ Succesfully connected ]\n-------------------------------------')
    except:
        LoadConnectionInfo(ChatLog, '[ Unable to connect ]')
        return

    while 1:
        try:
            data = s.recv(1024)
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            LoadOtherEntry(ChatLog, data)
            #if base.focus_get() == None:
            #    FlashMyWindow(WindowTitle)
            #    playsound('notif.wav')

        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
    s.close()


thread.start_new_thread(ReceiveData,())

base.mainloop()
