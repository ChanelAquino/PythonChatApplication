import thread
from chat_functions import *
from PIL import Image

#Initiate socket and bind port to host PC
WindowTitle = 'Pychat Host'
s = socket(AF_INET, SOCK_STREAM)
HOST = gethostname()
PORT = 8026
conn = ''
s.bind((HOST, PORT))


def ClickAction():
    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    LoadMyEntry(ChatLog, EntryText)

    #Scroll to the bottom of chat windows
    ChatLog.yview(END)

    #Erace previous message in Entry Box
    EntryBox.delete("0.0",END)

    #Send my mesage to all others
    conn.sendall(EntryText)


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
base.configure(bg="#34495e")

#Create a Chat window
ChatLog = Text(base, bd=0, bg="#2980b9", height="8", width="50", font="Helvetica",)
ChatLog.insert(END, "Waiting for your partner to connect..\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart", bg = "#34495e")
ChatLog['yscrollcommand'] = scrollbar.set

#Create the Button to send message
SendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#81A035", activebackground="#81A035", justify="center",
                    command=ClickAction)


#Create the box to enter message
EntryBox = Text(base, bd=0, bg="#e74c3c",width="29", height="5", font="Helvetica")
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
def GetConnected():
    s.listen(2)
    global conn
    conn, addr = s.accept()
    LoadConnectionInfo(ChatLog, 'Connected with: ' + str(addr) + '\n-------------------------------------')

    while 1:
        try:
            data = conn.recv(1024)
            LoadOtherEntry(ChatLog, data)

        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
            GetConnected()

        if '/img' in ChatLog:
            getImage()

    conn.close()

thread.start_new_thread(GetConnected,()) # try listening again upon fail
base.mainloop()



def getImage():
    img = Image.open(data)
    while True:
        strng = img.readline(512)
        if not strng:
            break
        s.send(strng)
    img.close()
    LoadMyEntry(ChatLog, img)
