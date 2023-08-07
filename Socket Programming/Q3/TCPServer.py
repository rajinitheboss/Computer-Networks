#https://pythontic.com/modules/socket/send
import socket 
import os.path
serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

while (True):
    (connectionSocket, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
    sentence = connectionSocket.recv(1024)
    sentence = sentence.decode()
    sentence = sentence.strip()
    sentence = sentence.split()
    n = int(sentence[1])
    filename = sentence[0]
    filename1 = str('./')+sentence[0]
    if os.path.isfile(filename1):
        f = open(filename,"r")
        string = f.read()
        string = string[::-1]
        string = string[0:n+1]
        string = string[::-1]
        #print("the string that we are returning :" + string)
        connectionSocket.send(string.encode())
    else:
        connectionSocket.send('SORRY!'.encode())
    connectionSocket.close()
