from flask import Flask
import pandas as pd
from scapy.all import *
import socket
import struct
import time
import argparse

app = Flask(__name__)

@app.route('/request', methods=['GET', 'POST'])
def request(host):
    return "helo"


# Traceroute Function
def traceroute(destination, max_hops=30, timeout=2):
    destination_ip = socket.gethostbyname(destination)
    port = 33434
    ttl = 1

    response = []

    while True:
        # Creating the IP and UDP headers
        ip_packet  = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)

        # Combining the headers
        packet = ip_packet / udp_packet
        
        # Sending the packet and receive a reply
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            # No reply, print * for timeout
            # print(f"{ttl}\t*")
            response.append([destination, ttl, 'noreply', '*'])
        elif reply.type == 3:
            # Destination reached, print the details
            # print(f"{ttl}\t{reply.src}")
            response.append([destination, ttl, 'reached', reply.src])
            return response
        else:
            # Printing the IP address of the intermediate hop
            # print(f"{ttl}\t{reply.src}")
            response.append([destination, ttl, 'intermediate-hop', reply.src])

        ttl += 1

        if ttl > max_hops:
          return response