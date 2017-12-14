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
Threshold = 16

def signal_handler(signum, frame):
    raise OSError()

signal.signal(signal.SIGALRM, signal_handler)

def make_packet(filename):
    f = open(filename, "rb")
    packet = []
    while True:
        content = f.read(900)
        if not content:
            break;
        single_packet = {"Type": "SEND", "Seq": len(packet)+1, "Payload": content}
        print(single_packet)
        packet.append(single_packet)
    return packet


if __name__ == "__main__":
    filename = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_SENDER_PORT))

    packet = make_packet(filename)
    
    ptr = 0
    window = 1
    overall_sent = []
    while len(packet) > ptr:
        sent = []
        for i in range(ptr, min(ptr+window, len(packet))):
            sent.append(packet[i]["Seq"])
            sock.sendto(pickle.dumps(packet[i]), (UDP_IP, UDP_AGENT_PORT))
            if packet[i]["Seq"] not in overall_sent:
                overall_sent.append(packet[i]["Seq"])
                print("send\tdata\t#%d,\twinSize = %d" % (packet[i]["Seq"], window))
            else:
                print("resnd\tdata\t#%d,\twinSize = %d" % (packet[i]["Seq"], window))
        signal.alarm(1)
        try:
            while len(sent) > 0:
                recvdata = sock.recv(1024)
                recv_packet = pickle.loads(recvdata)
                if recv_packet["Type"] != "ACK":
                    continue
                if recv_packet["Seq"] in sent:
                    sent.remove(recv_packet[seq])
                print("recv\tack\t#%d" % (recv_packet[Seq]))
            signal.alarm(0)
        except OSError:
            print("time\tout,\t\tthreshold = %d" % (Threshold))
        
        if sent:
            ptr = sent[0] - 1
            window = 1
        else:
            ptr += window
            if window >= threshold:
                window += 1
            else:
                window *= 2
    while True:
        FIN_packet = {"Type": "FIN"}
        sock.sendto(pickle.dumps(FIN_packet), (UDP_IP, UDP_AGENT_PORT))
        print("send\tfin")
        try:
            recvdata = sock.recv(1024)
            recv_packet = pickle.loads(recvdata)
            if recv_packet["Type"] != "FINACK":
                continue 
            print("recv\tfinack")
            signal.alarm(0)
            exit()
        except OSError:
            print("time\tout,\t\tthreshold = %d" % (Threshold))

