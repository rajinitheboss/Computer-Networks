'''

    Name: Krishna Sai Kottakota
    Roll Number: CS20B044
    Course: CS3205 Jan-May 2023 semester
    Lab number: 2
    Date of submission: 01/03/2023
    I confirm that the source file is entirely written by me without
    resorting to any dishonest means.

'''

import os                                               # Importing necessary packages
import socket
import math
import sys
import time
import multiprocessing.process

localIP = '127.0.0.1'
buffersize = 1024

filename = sys.argv[2]                                   #getting file name and k from arguments
k = int(sys.argv[1])
fp = open(filename,'r')                                  #opening the input file with filepointer fp
IPmap = dict()
ADSmap = dict()
while True:                                              # reading through the input file 
    x = fp.readline().strip()   
    if x == 'END_DATA':                                  # if the line is 'END_DATA' the break                         
        break
    elif x == 'List_of_ADS1':                            # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]]= 1
    elif x == 'List_of_ADS2':                           # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]] = 2
    elif x == 'List_of_ADS3':                           # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]] = 3
    elif x == 'List_of_ADS4':                           # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]] = 4
    elif x == 'List_of_ADS5':                           # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]] = 5
    elif x == 'List_of_ADS6':                           # reading the next 5 lines and storing the IP addresses 
        for i in range(5):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()
            dom = add[0].split('.')
            ADSmap[str(dom[1])+'.'+dom[2]]= 6
    elif x == 'BEGIN_DATA':                                 # reading the next 10 lines and storing the IP addresses
        for i in range(10):
            y = fp.readline().strip()
            add = y.split(' ')
            IPmap[add[0].strip()] = add[1].strip()



NRpointer = open("NR.output",'w')                        # opening different outputfiles in write mode
Rootpointer = open('RDS.output','w')
TLDpointer = open('TDS.output','w')
ADSpointer = open('ADS.output','w')



for i in range(0,10):
    pid = os.fork()                                       # Creating child process using fork
    if pid == 0:                                          # pid = 0 for child process and going inside for child process
        if i == 0:                                        # creating root server when i = 0
            UDPRoot = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
            UDPRoot.bind((localIP,k+54))
            print("Root DNS server is up and running")
            while True:
                Rootmsg = UDPRoot.recvfrom(1024)          # receiving query from local DNS server 
                domain = Rootmsg[0].decode().strip()      
                message = domain 
                domain = domain.split('.')
                if message == 'kill':
                    bytestosend = str.encode('kill')
                    UDPRoot.sendto(bytestosend,(localIP,k+55))
                    UDPRoot.sendto(bytestosend,(localIP,k+56))
                    UDPRoot.close()
                    exit()
                if len(domain) != 3:                      # sending 'sorry' when the domain is not in format
                    sendtoaddress = Rootmsg[1]
                    bytestosend = 'sorry'.encode()
                    UDPRoot.sendto(bytestosend,sendtoaddress)
                    Rootpointer.write(f'Query asked : {message}\nResponse given : sorry\n')
                    continue
                if domain[2] == 'com':                     # checking the TDS for the given domain 
                    sendtoaddress = Rootmsg[1]
                    bytestosend = (IPmap['TDS_com'] + ' ' + str(k+55)).encode()
                    servIP = str(IPmap['TDS_com'])
                    UDPRoot.sendto(bytestosend,sendtoaddress)
                    Rootpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+55)}\n')
                elif domain[2] == 'edu':
                    sendtoaddress = Rootmsg[1]
                    bytestosend = (IPmap['TDS_edu'] + ' ' + str(k+56)).encode()
                    UDPRoot.sendto(bytestosend,sendtoaddress)
                    servIP = str(IPmap['TDS_edu'])
                    Rootpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+56)}\n')
                else:
                    sendtoaddress = Rootmsg[1]
                    bytestosend = 'sorry'.encode()
                    UDPRoot.sendto(bytestosend,sendtoaddress)
                    Rootpointer.write(f'Query asked : {message}\nResponse given : sorry\n')
        elif i == 1:                                      # creating TDS_com server when i = 1     
            time.sleep(1)
            UDPTLD = socket.socket(family = socket.AF_INET,type = socket.SOCK_DGRAM)
            UDPTLD.bind((localIP,k+55))
            print("TLD_com is up and running")
            while True:
                bytesAddressPair = UDPTLD.recvfrom(buffersize)
                message = bytesAddressPair[0].decode().strip()
                address = bytesAddressPair[1]
                if message == 'kill':                   # closing the socket and exiting the process 
                    bytestosend = str.encode('kill')
                    UDPTLD.sendto(bytestosend,(localIP,k+57))
                    UDPTLD.sendto(bytestosend,(localIP,k+58))
                    UDPTLD.sendto(bytestosend,(localIP,k+59))
                    UDPTLD.close()
                    exit()
                TLDmsg = message.split('.')
                key = str(TLDmsg[1]) + '.' + str(TLDmsg[2])
                x = ADSmap.get(key)
                if x is None:
                    bytestosend = 'sorry'.encode()
                    UDPTLD.sendto(bytestosend,address)
                    TLDpointer.write(f'Query asked : {message}\nResponse given : sorry\n')
                else:                                           # checking to which ADS the query belong 
                    if x == 1:
                        bytestosend = (IPmap[key]+' '+str(k+57)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+57)}\n')
                    elif x == 2:
                        bytestosend = (IPmap[key]+' '+str(k+58)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+58)}\n')
                    elif x == 3:
                        bytestosend = (IPmap[key]+' '+str(k+59)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+59)}\n')
        elif i == 2:                                      # creating TDS_edu server when i = 2
            time.sleep(2)
            UDPTLD = socket.socket(family = socket.AF_INET,type = socket.SOCK_DGRAM)
            UDPTLD.bind((localIP,k+56))
            print("TLD_edu is up and running")
            while(True):
                bytesAddressPair = UDPTLD.recvfrom(buffersize)
                message = bytesAddressPair[0].decode().strip()
                address = bytesAddressPair[1]
                if message == 'kill':                       # closing the socket and exiting the process 
                    bytestosend = str.encode('kill')
                    UDPTLD.sendto(bytestosend,(localIP,k+60))
                    UDPTLD.sendto(bytestosend,(localIP,k+61))
                    UDPTLD.sendto(bytestosend,(localIP,k+62))
                    UDPTLD.close()
                    exit()
                TLDmsg = message.split('.')
                key = str(TLDmsg[1]) + '.' + str(TLDmsg[2])
                x = ADSmap.get(key)
                if x is None:
                    bytestosend = 'sorry'.encode()
                    UDPTLD.sendto(bytestosend,address)
                    TLDpointer.write(f'Query asked : {message}\nResponse given : sorry\n')
                else:
                    if x == 4:
                        bytestosend = (IPmap[key]+' '+str(k+60)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+60)}\n')
                    elif x == 5:
                        bytestosend = (IPmap[key]+' '+str(k+61)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+61)}\n')
                    elif x == 6:
                        bytestosend = (IPmap[key]+' '+str(k+62)).encode()
                        UDPTLD.sendto(bytestosend,address)
                        servIP = str(IPmap[key])
                        TLDpointer.write(f'Query asked : {message}\nResponse given : {servIP} {str(k+62)}\n')
                    else:
                        bytestosend = 'sorry'.encode()
                        UDPTLD.sendto(bytestosend,address)
        elif i in list(range(3,9)):                       #creaing 6 ADS servers when i is in between 3 to 8 
            time.sleep(i)
            UDPADS = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
            UDPADS.bind((localIP,k+56+i-2))
            print(f'ADS server number {i-2} is up and running')
            while(True):
                bytesAddressPair = UDPADS.recvfrom(buffersize)
                message = bytesAddressPair[0].decode().strip()
                address = bytesAddressPair[1]
                if message == 'kill':                       # closing the socket and exiting the process 
                    UDPADS.close()
                    exit()
                x = IPmap.get(message)
                if x is None:
                    bytestosend = 'sorry'.encode()
                    ADSpointer.write(f'Query asked : {message}\nResponse given : sorry\n')
                else:
                    bytestosend = x.encode()
                    ADSpointer.write(f'Query asked : {message}\nResponse given : {x} {address[1]}\n')
                UDPADS.sendto(bytestosend,address)
        elif i == 9:                                       #creating local DNS server when i = 9
            time.sleep(9)
            local_dns = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
            local_dns.bind((localIP,k+53))
            print('local DNS is up and running')
            while(True):
                bytesAddressPair = local_dns.recvfrom(buffersize)  #recieving message from client 
                message = bytesAddressPair[0].decode().strip()
                address = bytesAddressPair[1]
                RootIP = '127.0.0.1'
                Rootport = k+54
                bytesToRoot         = str.encode(message)
                RootAddressPort   = ("127.0.0.1", Rootport)
                if message == 'kill':                               # telling all the servers to terminate
                    local_dns.sendto(bytesToRoot,RootAddressPort)
                    exit()
                local_dns.sendto(bytesToRoot, RootAddressPort)      # sending the request to Root DNS
                msgFromRoot = local_dns.recvfrom(buffersize)
                msgfromRoot =msgFromRoot[0].decode().strip()
                if msgfromRoot == 'sorry':                          # sending sorry to client if the domain is not present 
                    bytestoclient = str.encode('sorry')
                    local_dns.sendto(bytestoclient,address)
                    NRpointer.write(f'Query asked :{message}\nResponse given : bye\n') #writing into NR.output
                else:
                    temp = msgfromRoot.split(' ')
                    TLDAddressPort = ('127.0.0.1',int(temp[1]))
                    bytestoTLD = str.encode(message)
                    local_dns.sendto(bytestoTLD,TLDAddressPort)     #sending the query to TDS server 
                    msgFromTLD = local_dns.recvfrom(buffersize)     # recieving from TDS server
                    msgfromTLD = msgFromTLD[0].decode()
                    if msgfromTLD == 'sorry':
                        bytestoclient = str.encode('sorry')
                        local_dns.sendto(bytestoclient,address)
                        NRpointer.write(f'Query asked :{message}\nResponse given : bye\n')
                    else:
                        p = msgfromTLD.strip().split()
                        ADSPort = int(p[1].strip())
                        ADSAddressPort = ((localIP,ADSPort))
                        bytestoADS = str.encode(message)
                        local_dns.sendto(bytestoADS,ADSAddressPort) # sending the query to ADS server 
                        msgFromADS = local_dns.recvfrom(buffersize) # receiving from the ADS server
                        msgfromADS = msgFromADS[0].decode()
                        if msgfromADS == 'sorry':
                            bytestoclient = str.encode('sorry')
                            local_dns.sendto(bytestoclient,address)
                            NRpointer.write(f'Query asked :{message}\nResponse given : bye\n')
                        else:
                            bytestoclient = str.encode(msgfromADS)
                            local_dns.sendto(bytestoclient,address)
                            NRpointer.write(f'Query asked :{message}\nResponse given : {msgfromADS} {address[1]}\n')
        exit()                      # exiting the child process in every iteration
time.sleep(10)                                            # Running client program in parent process 
UDPClient = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
local_dnsAddress = ((localIP,k+53))
while True:
    IPrequired = input('Enter Server name :')
    if(IPrequired == 'bye'):
        bytestolocal_dns = str.encode('kill')
        UDPClient.sendto(bytestolocal_dns,local_dnsAddress)
        NRpointer.close()                                   # closing all the pointers 
        TLDpointer.close()
        Rootpointer.close()
        ADSpointer.close()
        print('All Server Processes are killed. Exiting.')
        exit()
    bytestolocal_dns = IPrequired.encode()
    UDPClient.sendto(bytestolocal_dns,local_dnsAddress)     # sending the query to local DNS server 
    msgFromServer = UDPClient.recvfrom(buffersize)          # receiving queries from the local DNS server
    actualmessage = msgFromServer[0].decode().strip()
    if actualmessage == 'sorry':
        print("No DNS Record Found")
    else:
        print('DNS Mapping: '+actualmessage)