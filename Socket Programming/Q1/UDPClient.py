#https://pythontic.com/modules/socket/udp-client-server-example





import socket

serverAddressPort   = ("127.0.0.1", 30535)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while True:
    msgFromClient = input("Enter a message :")
    if msgFromClient == "exit":
        break
    bytesToSend         = str.encode(msgFromClient)
    k = UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    #Wait on recvfrom()
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    #Wait completed
    msg = "Message from Server: {}".format(msgFromServer[0].decode())
    print(msg)
