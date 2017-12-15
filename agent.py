import os
import sys
import pickle
import math
import socket
from threading import Timer
import signal
import random

UDP_IP = "127.0.0.1"
UDP_SENDER_PORT = 53000
UDP_AGENT_PORT = 53100
UDP_RECEIVER_PORT = 53200
Drop_Rate = 1 # %

if __name__ == "__main__":
    Drop_Rate = int(sys.argv[1])
    random.seed()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_AGENT_PORT))
    recved_n = 0
    droped_n = 0
    while True:
        recvdata = sock.recv(1024)
        recv_packet = pickle.loads(recvdata)
        if recv_packet["Type"] in "SEND":
            recved_n += 1
            print("get\tdata\t#%d" % recv_packet["Seq"])

            if random.randint(1,100) <= Drop_Rate:
                droped_n += 1
                print("drop\tdata\t#%d,\tloss rate = %.4f" % (recv_packet["Seq"], float(droped_n)/float(recved_n)))
            else:
                sock.sendto(pickle.dumps(recv_packet), (UDP_IP, UDP_RECEIVER_PORT))
                print("fwd\tdata\t#%d,\tloss rate = %.4f" % (recv_packet["Seq"], float(droped_n)/float(recved_n)))
        elif recv_packet["Type"] == "ACK":
            print("get\t%s\t#%d" % (recv_packet["Type"].lower(), recv_packet["Seq"]))
            sock.sendto(pickle.dumps(recv_packet), (UDP_IP, UDP_SENDER_PORT))
            print("fwd\t%s\t#%d" % (recv_packet["Type"].lower(), recv_packet["Seq"]))
        elif recv_packet["Type"] == "FINACK":
            print("get\tfinack")
            sock.sendto(pickle.dumps(recv_packet), (UDP_IP, UDP_SENDER_PORT))
            print("fwd\tfinack")
        elif recv_packet["Type"] == "FIN":
            print("get\tfin")
            sock.sendto(pickle.dumps(recv_packet), (UDP_IP, UDP_RECEIVER_PORT))
            print("fwd\tfin")

