#Pychat built with help from -- source of original github work

WindowTitle = 'Pychat Host'
s = socket(AF_INET, SOCK_STREAM)
HOST = gethostname()
PORT = 9000
conn = ''
s.bind((HOST, PORT))
