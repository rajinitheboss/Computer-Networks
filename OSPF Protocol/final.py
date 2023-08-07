import threading
import math
import time
import random
import socket
import sys

local_IP = '127.0.0.1'
buffersize = 5048

termination = False

def sending_hello(router_ind,neigh_list,udp_socket,hello_interval):
    while True:
        if termination == True:
            break
        msg = 'hello'
        msg = msg + ' ' + str(router_ind)
        for i in range(len(neigh_list)):
            if neigh_list[i] != (-1,-1):
                udp_socket.sendto(msg.encode(),(local_IP,10000+i))
        time.sleep(hello_interval)

def printing_mat(list):
    for i in range(len(list)):
        print(list[i])

def receiving_packets(router_id,neigh_list,udp_socket,local_mat):
    seq_num = list()
    n = len(neigh_list)
    for i in range(n):
        seq_num.append(-1)

    while True:
        if termination == True:
            break
        msg_pair = udp_socket.recvfrom(buffersize)
        msg = msg_pair[0].decode()
        if msg == 'exit':
            break
        port_num = msg_pair[1]
        port = int(port_num[1])
        k = msg.strip().split()
        if k[0] == 'hello':
            recv_id = int(k[1])
            min_cost,max_cost = neigh_list[recv_id]
            cost_to_be_sent = random.randint(min_cost,max_cost)
            new_msg = 'helloreply'+ " "+str(router_id)+" "+str(recv_id)+" "+ str(cost_to_be_sent)
            udp_socket.sendto(new_msg.encode(),(local_IP,10000+recv_id))
        elif k[0] == 'helloreply':
            x = int(k[1])
            y = int(k[2])
            dist = int(k[3])
            local_mat[y][x] = dist
        elif k[0] == 'lsa':
            recv_id = int(k[1])
            seq_num_recv = int(k[2])
            entries = int(k[3])
            if seq_num[recv_id] < seq_num_recv:
                seq_num[recv_id] = seq_num_recv
                for i in range(entries):
                    recv_id2 = int(k[3+(2*i)+1])
                    # if local_mat[recv_id][recv_id2] == -1:
                    #     local_mat[recv_id][recv_id2] = int(k[3+(2*i)+2])
                    # elif local_mat[recv_id][recv_id2] > int(k[3+(2*i)+2]):
                    local_mat[recv_id][recv_id2] = int(k[3+(2*i)+2])
                for i in range(n):
                    if i != recv_id :
                        if neigh_list[i] != (-1,-1):
                            udp_socket.sendto(msg.encode(),(local_IP,10000+i))


def sending_lsa(router_id,neigh_list,udp_socket,local_mat,lsa_interval):
    seq_num = 0
    while True:
        if termination == True:
            break
        msg = 'lsa'
        msg = msg + " " + str(router_id) + " "+ str(seq_num)
        count = 0
        part_of_msg = ''
        for i in range(len(local_mat[router_id])):
            if local_mat[router_id][i] != -1 :
                count = count + 1
                part_of_msg = part_of_msg + str(i) + " " + str(local_mat[router_id][i]) + " "
        msg = msg + " " + str(count) + " " + part_of_msg
        for i in range(len(neigh_list)):
            if neigh_list[i] != (-1,-1):
                udp_socket.sendto(msg.encode(),(local_IP,10000+i))
        seq_num += 1
        time.sleep(lsa_interval)

def dijkstra(matrix, start, end):
    num_vertices = len(matrix)
    shortest_distances = [sys.maxsize] * num_vertices
    visited = [False] * num_vertices
    shortest_distances[start] = 0
    paths = {start: [start]}
    for _ in range(num_vertices):
        current_vertex = -1
        for vertex in range(num_vertices):
            if not visited[vertex] and (current_vertex == -1 or shortest_distances[vertex] < shortest_distances[current_vertex]):
                current_vertex = vertex
        visited[current_vertex] = True
        for neighbor in range(num_vertices):
            distance = matrix[current_vertex][neighbor]
            if distance > 0 and not visited[neighbor]:
                new_distance = shortest_distances[current_vertex] + distance
                if new_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = new_distance
                    paths[neighbor] = paths[current_vertex] + [neighbor]
    return (shortest_distances[end], paths[end])

def calculating_shortest_path(router_id,local_mat,outfile,spf_interval):
    current_time = 0
    while True:
        time.sleep(spf_interval)
        current_time += spf_interval
        outfile.write(f"Routing table for node number {router_id} at time {current_time}\n")
        outfile.write(f"Destination,path,cost\n")
        for i in range(len(local_mat)):
            if i != router_id:
                dist,path = dijkstra(local_mat,router_id,i)
                outfile.write(f'{i},')
                for i in range(len(path)):
                    outfile.write(f"{path[i]} ")
                outfile.write(",")
                outfile.write(f"{dist}\n")
        if current_time > 30:
            break
    outfile.close()

if __name__ == "__main__":

    hello_interval = 1
    lsa_interval = 5
    spf_interval = 15
    node_identifier = 0
    input_list = sys.argv[1:]
    inputfile = ''
    i = 0
    while i < len(input_list):
        if input_list[i] == '-i':
            node_identifier = int(input_list[i+1])
            i += 2
        elif input_list[i] == '-f':
            inputfile = input_list[i+1]
            i += 2
        elif input_list[i] == '-o':
            outputfile = input_list[i+1]
            i += 2
        elif input_list[i] == '-h':
            hello_interval = int(input_list[i+1])
            i += 2
        elif input_list[i] == '-a':
            lsa_interval = int(input_list[i+1])
            i += 2
        elif input_list[i] == '-s':
            spf_interval = int(input_list[i+1])
            i += 2
    inpointer = open(inputfile,'r')
    k = inpointer.readline().strip()
    k = k.split()
    n = int(k[0])
    no_of_links = int(k[1])
    matrix = list()
    temp_dict = dict()
    for line in inpointer:
        k = line.strip().split()
        x = int(k[0])
        y = int(k[1])
        min_cost = int(k[2])
        max_cost = int(k[3])
        temp_dict[(x,y)] = (min_cost,max_cost)
        temp_dict[(y,x)] = (min_cost,max_cost)
    for i in range(n):
        temp = list()
        for j in range(n):
            t = tuple()
            t = (i,j)
            if t in temp_dict:
                temp.append(temp_dict[(i,j)])
            else:
                temp.append((-1,-1))
        matrix.append(temp)

    thread_list1 = list()
    thread_list2 = list()
    thread_list3 = list()
    t = 1
    printing_local_mat = list()
    outlist = list()
    outthread = list()
    socket_list = list()
    for i in range(n):
        udp_socket = socket.socket(socket.AF_INET,type = socket.SOCK_DGRAM)
        udp_socket.bind((local_IP,10000+i))
        socket_list.append(udp_socket)
        t1 = threading.Thread(target = sending_hello, args = (i,matrix[i],udp_socket,hello_interval,))
        thread_list1.append(t1)
        local_mat = list()
        for _ in range(n):
            temp = list()
            for _ in range(n):
                temp.append(-1)
            local_mat.append(temp)
        t2 = threading.Thread(target = receiving_packets, args = (i,matrix[i],udp_socket,local_mat,))
        thread_list2.append(t2)
        t3 = threading.Thread(target = sending_lsa, args = (i,matrix[i],udp_socket,local_mat,lsa_interval,))
        thread_list3.append(t3)
        k1 = threading.Thread(target = printing_mat, args = (local_mat,))
        printing_local_mat.append(k1)
        # if i == node_identifier:
        file_name = outputfile + '-' +str(i)+'.csv'
        outfile = open(file_name, 'w')
        t = threading.Thread(target = calculating_shortest_path, args = (i,local_mat, outfile,spf_interval,))
        outlist.append(outfile)
        outthread.append(t)
    for i in range(len(thread_list2)):
        print(f"starting receiving thread for node {i}")
        thread_list2[i].start()
    for i in range(len(thread_list1)):
        time.sleep(1)
        print(f"starting thread for sending hello for node {i}")
        thread_list1[i].start()
    time.sleep(5)
    for i in range(len(thread_list3)):
        print(f"starting thread for sending lsa for node{i}")
        thread_list3[i].start()
        time.sleep(1)
    for i in range(n):
        outthread[i].start()
    for i in range(n):
        outthread[i].join()
    print('closing all the file pointers for the outputfiles ')
    termination = True
    print('Sending messages to all threads to terminate')
    final_socket = socket.socket(socket.AF_INET,type = socket.SOCK_DGRAM)
    final_socket.bind((local_IP,11000))
    for i in range(n):
        final_socket.sendto('exit'.encode(),(local_IP,10000+i))
    for i in range(n):
        thread_list2[i].join()
    final_socket.close()
    for i in range(n):
        socket_list[i].close()
    print('All Threads are terminated and closing the program')
