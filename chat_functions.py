# -*- coding: utf-8 -*-
from Tkinter import *
from socket import *
import urllib
import re


def GetExternalIP():
    url = "http://checkip.dyndns.org"
    request = urllib.urlopen(url).read()
    return str(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request))

def GetInternalIP():
    return str(gethostbyname(getfqdn()))

def FilteredMessage(EntryText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(EntryText)-1,-1,-1):
        if EntryText[i]!='\n':
            EndFiltered = EntryText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return ''

def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText+'\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

def LoadMyEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            LineNumber = float(ChatLog.index('end'))-1.0
            #Trying to get emojis to work
            '''
            if "/shrug" in EntryText:
                EntryText =  "¯\_(ツ)_/¯"
            else:
                EntryText = u'\U0001f63b'
            '''
            ChatLog.insert(END, "YOU: " + EntryText)
            ChatLog.tag_add("YOU", LineNumber, LineNumber+0.4)
            ChatLog.tag_config("YOU", foreground="#AA3939", font=("Courier", 12, "bold"), justify = "right")
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


def LoadOtherEntry(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            try:
                LineNumber = float(ChatLog.index('end'))-1.0
            except:
                pass
            ChatLog.insert(END, "OTHER: " + EntryText)
            ChatLog.tag_add("OTHER", LineNumber, LineNumber+0.6)
            ChatLog.tag_config("OTHER", foreground="#255E69", font=("Courier", 12, "bold"))
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
