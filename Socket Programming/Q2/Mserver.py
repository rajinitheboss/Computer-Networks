#https://pythontic.com/modules/socket/udp-client-server-example
import socket
import math

localIP     = "127.0.0.1"
localPort   = int(input("Enter port number"))
bufferSize  = 1024


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    address = bytesAddressPair[1]
    clientMsg = "Recieved: {}".format(message)
    #clientIP  = "Client IP Address: {}".format(address)
    print(clientMsg)
    #print(clientIP)
    arr = message.split()
    if arr[0] == 'add':
        msgtobesent = int(arr[1])+int(arr[2])
        msgtobesent = str(msgtobesent)
        UDPServerSocket.sendto(msgtobesent.encode(),address)
    elif arr[0] == 'mul':
        msgtobesent = int(arr[1]) * int(arr[2])
        msgtobesent = str(msgtobesent)
        UDPServerSocket.sendto(msgtobesent.encode(),address)
    elif arr[0] == 'mod':
        msgtobesent = int(arr[1]) % int(arr[2])
        msgtobesent = str(msgtobesent)
        UDPServerSocket.sendto(msgtobesent.encode(),address)
    elif arr[0] == 'hyp':
        msgtobesent = math.sqrt(int(arr[1])*int(arr[1]) + int(arr[2])*int(arr[2]))
        msgtobesent = str(msgtobesent)
        UDPServerSocket.sendto(msgtobesent.encode(),address)
    else:
        msgtobesent = 'Invalid Command'
        UDPServerSocket.sendto(msgtobesent.encode(),address)
