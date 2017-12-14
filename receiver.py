import os
import sys
import pickle
import math
import socket
from threading import Timer
import signal

UDP_IP = "127.0.0.1"
UDP_SENDER_PORT = 53000
UDP_AGENT_PORT = 53100
UDP_RECEIVER_PORT = 53200
Buffer = 32
Buffer_content = []

def flush_buffer(f, Buffer_content):
    for i in range(0,len(Buffer_content)):
        f.write(Buffer_content[i]["Payload"])
    return

def make_ack_packet(n):
    return {"Type": "ACK", "Seq": n}

if __name__ == "__main__":
    filename = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_RECEIVER_PORT))
    f = open(filename, "wb")
    next_seq = 1

    while True:
        recvdata = sock.recv(1024)
        recv_packet = pickle.loads(recvdata)
        if recv_packet["Type"] == "FIN":
            print("recv\tfin")
            fin_packet = {"Type": "FINACK"}
            print("send\tfinack")
            sock.sendto(pickle.dumps(fin_packet), (UDP_IP, UDP_AGENT_PORT))
            flush_buffer(f, Buffer_content)
            Buffer_content = []
            print("flush")
            break
        else:
            if recv_packet["Seq"] == next_seq and len(Buffer_content) < Buffer:
                Buffer_content.append(recv_packet)        
                print("recv\tdata\t#%d" % recv_packet["Seq"])
                pac = make_ack_packet(next_seq)
                sock.sendto(pickle.dumps(pac), (UDP_IP, UDP_AGENT_PORT))
                print("send\tack\t#%d" % next_seq)
                next_seq += 1
            else:
                print("drop\tdata\t#%d" % recv_packet["Seq"])
                pac = make_ack_packet(next_seq-1)
                sock.sendto(pickle.dumps(pac), (UDP_IP, UDP_AGENT_PORT))
                print("send\tack\t#%d" % (next_seq-1))
                if recv_packet["Seq"] == next_seq:
                    flush_buffer(f, Buffer_content)
                    Buffer_content = []
                    print("flush")



