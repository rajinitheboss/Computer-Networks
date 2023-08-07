# NAME: Krishna Sai 
# Roll Number: CS20B044
# Course: CS3205 Jan. 2023 semester
# Lab number: 4
# Date of submission: 05/04/2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.


import time
import os
import socket
from queue import Queue
import threading
import numpy as np
import sys

def recv_pkt(recv_udp,drop_prob,pkt_queue,max_seq,debug):      # function which takes care of receiving part of receiver
    bufferSize = 1024
    while True:                                                 # runs a while loop which receives packets from the sender
        next_exp_num = 0                                            # using recv udp
        bytesAddressPair = recv_udp.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        if message == 'exit()':
            break
        if debug:                                               # printing things if it is debug mode
            print(f'Seq Number {seq_recieved}',end = '  ')
            print(f'Time recieived {time.time()}', end = '  ')
        if np.random.random() > drop_prob:
            pkt_queue.append(message)
            if debug:
                print(f'Packet dropped : False')
        else:
            if debug:
                print(f'Packet dropped : True')

if __name__ == "__main__":  
    debug = False                                        #extracting required values from the system arguments
    if "-d" in sys.argv:
        debug = True
    if "-p" in sys.argv:
        local_port = int(sys.argv[sys.argv.index("-p") + 1])
    if "-n" in sys.argv:
        max_pkts = int(sys.argv[sys.argv.index("-n") + 1])
    if "-e" in sys.argv:
        drop_prob = float(sys.argv[sys.argv.index("-e") + 1])
    # drop_prob = float(input('Random Drop Probability: '))
    # local_port = int(input('enter the port number for receiver: '))
    # max_pkts = int(input('Enter the maximum nuber of acknowledgements after which can be terminated: '))
    pkt_queue = list()
    local_IP = '127.0.0.1'
    max_seq = 256
    recv_udp = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    recv_udp.bind((local_IP,local_port))
    recv_thread = threading.Thread(target = recv_pkt,args=(recv_udp,drop_prob,pkt_queue,max_seq,debug,)) #threading the receiving function 
    first = True
    next_exp_num = 0
    last_ack = 0 
    sender_add = ('127.0.0.1',22000)
    pkts_ack = 0
    recv_thread.start()

    while True:
        if len(pkt_queue) != 0:                                     # whenever the receiver receives the packet it starts
            pkt = pkt_queue.pop(0)                                  # to process the packet and try to find the sequence number
            seq_recieved = ord(pkt[0]) - 1                          # in that packet 
            if seq_recieved == next_exp_num:
                next_exp_num = (next_exp_num + 1) % max_seq
                msg_to_sender = chr(seq_recieved + 1) + 'Acknowledged' # sending acknowledgement
                pkts_ack +=1
                recv_udp.sendto(str.encode(msg_to_sender),sender_add)
                last_ack = seq_recieved
                if first:
                    first = False
            else:
                if not first:
                    msg_to_sender = chr(last_ack + 1) + 'Acknowledged'
                    recv_udp.sendto(str.encode(msg_to_sender),sender_add)
        if pkts_ack >= max_pkts:
            print('Terminating Reciever since it acknowledged maximum number of packets')
            recv_udp.sendto(str.encode('exit()'),sender_add)
            time.sleep(1)
            recv_thread.join()
            exit()

