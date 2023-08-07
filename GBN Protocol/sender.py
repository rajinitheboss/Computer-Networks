# NAME: Krishna Sai 
# Roll Number: CS20B044
# Course: CS3205 Jan. 2023 semester
# Lab number: 4
# Date of submission: 05/04/2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.


import threading
import time
import os
import random
import socket
from queue import Queue
import sys


stop_gen_thread = False
stop_recv_thread = False

def generate_packet(pkt_gen_rate,pkt_len,max_buff,sender_buff):
    while True:
        if stop_gen_thread :
            print('Terminating packet generating thread')
            break
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        pkt = ''
        # pkt.append(chr(seq_num % bit_num))
        for i in range(0,pkt_len-1):
            random_alphabet = random.choice(alphabet)
            pkt = pkt + random_alphabet
        if len(sender_buff) < max_buff:
            sender_buff.append(pkt)
        time.sleep(1/pkt_gen_rate)

def recv_pkt(sender_udp,recv_queue):
    print("Nothing for now")
    while True:
        if stop_recv_thread:
            print('terminating the thread which receives ack packets')
            break
        bufferSize = 1024
        bytesAddressPair = sender_udp.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        if message == 'exit()':
            break
        recv_queue.append(message)



if __name__ == "__main__":
    sender_buff= list()
    recv_queue= list()
    debug = False
    if "-d" in sys.argv:
        debug = True
    if "-l" in sys.argv:
        pkt_len = int(sys.argv[sys.argv.index("-l") + 1])
    if "-r" in sys.argv:
        pkt_gen_rate = int(sys.argv[sys.argv.index("-r") + 1])
    if "-b" in sys.argv:
        max_buff = int(sys.argv[sys.argv.index("-b") + 1])
    if "-w" in sys.argv:
        win_size = int(sys.argv[sys.argv.index("-w") + 1])
    if "-n" in sys.argv:
        max_pkts = int(sys.argv[sys.argv.index("-n") + 1])
    if "-s" in sys.argv:
        recv_ip = sys.argv[sys.argv.index("-s") + 1]
    if "-p" in sys.argv:
        recv_port = int(sys.argv[sys.argv.index("-p") + 1])

    local_IP = '127.0.0.1'
    local_port = 22000
    seq_max  = 256
    no_of_pkts_ack = 0
    total_pkt_sent = 0
    rcv_add = (recv_ip,recv_port)
    sender_udp = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    sender_udp.bind((local_IP,local_port))
    print('sender_udp is up and running')
    gen_thread = threading.Thread(target = generate_packet,args=(pkt_gen_rate,pkt_len,max_buff,sender_buff))
    recv_thread = threading.Thread(target = recv_pkt,args = (sender_udp,recv_queue,))
    gen_thread.start()
    recv_thread.start()
    win_buff = list()
    retrans_count = dict()
    for i in range(seq_max):
        retrans_count[i] = 0
    win_timer = list()
    rtt_avg = 0
    seq_num = 0
    head = 0
    next_seq_num = 0
    time.sleep(0.15)
    while True:
        if no_of_pkts_ack == max_pkts:
            sender_udp.sendto(str.encode('exit()'),rcv_add)
            time.sleep(1)
            print('Terminating the sender program as a packet retransmitted 5 times')
            print(f'Packet generate rate is {pkt_gen_rate}')
            print(f'Length of packet is {pkt_len}')
            print(f'Retransmission ratio of packet is {total_pkt_sent/no_of_pkts_ack}')
            print(f'Average RTT value is {rtt_avg}')
            gen_thread.join()
            recv_thread.join()
            sender_udp.close()
            print('maximum packets acknowledged ')
            exit()
        if (next_seq_num - head) % seq_max < win_size:
            if len(sender_buff) != 0:
                msg1 = sender_buff.pop(0)
                msg = chr(seq_num % seq_max + 1) + str(msg1)
                sender_udp.sendto(msg.encode(),rcv_add)
                total_pkt_sent += 1
                win_buff.append(msg)
                win_timer.append(time.time())
                print(f"sent the packet of seq number {seq_num}")
                seq_num = (seq_num + 1) % seq_max
                next_seq_num = (next_seq_num + 1) % seq_max
        if len(recv_queue) != 0:
            ack_pkt = recv_queue.pop(0)
            ack_pkt_seq_num = ord(ack_pkt[0]) - 1
            ack_num = (ack_pkt_seq_num - head + 1) % seq_max
            for i in range(ack_num):
                no_of_pkts_ack += 1 
                win_buff.pop(0)
                start_time = win_timer.pop(0)
                present_time = time.time()
                if debug:
                    print(f'sequence num: {head+i}',end = '  ')
                    print(f'Time Generated ')
                    print(f'RTT : {present_time - start_time}',end = '  ')
                    print(f'Number of attempts : {retrans_count[head + i]}')
                rtt_avg = (rtt_avg*(no_of_pkts_ack-1) + (present_time - start_time)*1000)/no_of_pkts_ack
            temp = head 
            while temp != ack_num:
                retrans_count[temp] = 0
                temp = temp + 1
                temp = temp % seq_max
            head = (ack_pkt_seq_num + 1) % seq_max
            
        if no_of_pkts_ack < 10:
            if len(win_timer) != 0:
                if (time.time() - win_timer[0])*1000 >= 100:
                    print('time out happened')
                    k = len(win_buff)
                    for i in range(k):
                        temp = win_timer.pop(0)
                        retrans_msg = win_buff.pop(0)
                        retrans_count[ord(retrans_msg[0])-1] += 1
                        # print(retrans_count[ord(retrans_msg[0])-1])
                        if retrans_count[ord(retrans_msg[0])-1] == 5:
                            stop_recv_thread = True
                            stop_gen_thread = True
                            sender_udp.sendto(str.encode('exit()'),rcv_add)
                            print('Terminating the sender program as a packet retransmitted 5 times')
                            print(f'Packet generate rate is {pkt_gen_rate}')
                            print(f'Length of packet is {pkt_len}')
                            print(f'Retransmission ratio of packet is {float(total_pkt_sent/no_of_pkts_ack)}')
                            print(f'Average RTT value is {rtt_avg}')
                            time.sleep(1)
                            exit()
                            # gen_thread.join()
                            # recv_thread.join()
                            # sender_udp.close()
                            # print('Terminating the sender program as a packet retransmitted 5 times')
                            # exit()
                        sender_udp.sendto(retrans_msg.encode(),rcv_add)
                        total_pkt_sent +=1
                        win_timer.append(time.time())
                        win_buff.append(retrans_msg)
        else:
            if len(win_timer) != 0:
                if time.time() - win_timer[0] > 2*rtt_avg:
                    print('timeout happened')
                    k = len(win_buff)
                    for i in range(k):
                        temp = win_timer.pop(0)
                        retrans_msg = win_buff.pop(0)
                        retrans_count[ord(retrans_msg[0])-1] += 1
                        if(retrans_count[ord(retrans_msg[0])-1] == 5):
                            stop_recv_thread = True
                            stop_gen_thread = True
                            sender_udp.sendto(str.encode('exit()'),rcv_add)
                            time.sleep(1)
                            print('Terminating the sender program as a packet retransmitted 5 times')
                            print(f'Packet generate rate is {pkt_gen_rate}')
                            print(f'Length of packet is {pkt_len}')
                            print(f'Retransmission ratio of packet is {float(total_pkt_sent/no_of_pkts_ack)}')
                            print(f'Average RTT value is {rtt_avg}')
                            exit()
                            # gen_thread.join()
                            # recv_thread.join()
                            # sender_udp.close()
                            # print('Terminating the sender program as a packet retransmitted 5 times')
                            # exit()
                        sender_udp.sendto(retrans_msg.encode(),rcv_add)
                        total_pkt_sent += 1
                        win_timer.append(time.time())
                        win_buff.append(retrans_msg)