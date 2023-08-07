#https://pythontic.com/modules/socket/send
import socket
serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

filename = input("Enter the filename : ")

sizeneeded = input("Enter the size of file needed :")

message = '{f1} {f2}'.format(f1 = filename , f2 = str(sizeneeded))

clientSocket.send(message.encode())

modifiedSentence = clientSocket.recv(1024)
recvmsg = modifiedSentence.decode()
if recvmsg == 'SORRY!':
    print('server says that the file does not exist.')
else:
    nwfile = filename+'1'
    f = open(nwfile,'w')
    f.write(recvmsg)
clientSocket.close()
