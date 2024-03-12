from flask import Flask, jsonify, request
import pandas as pd
from scapy.all import *
import socket
import struct
import time
import argparse
import requests
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

@app.route('/request', methods=['GET', 'POST'])
def responseHandler():
    if request.method == "POST":
        hostname = request.form['request']
        tracerouteResult = traceroute(hostname)
        return jsonify({'result': ''.join(str(x) for x in tracerouteResult)})
    else:
        return ""


#geolocation function
def geolocate(host):
    """
    #get IP if not already an IP
    IP = socket.gethostbyname(host)

    #API URL with IP embedded
    
    
    url = "https://api.geoapify.com/v1/ipinfo?ip=" + IP + "&apiKey=59050c64726a4da1a7d50e726172d4a3"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    response = requests.get(url, headers=headers)

    if(response.status_code == 200):
        #format to json
        json = response.json()
        
        #extract data
        lat = json["location"]["latitude"]
        lng = json["location"]["longitude"]

        #return pair
        return {host: [lat, lng]}

    """
    return {"testHost": ["testLat", "testLng"]}

#traceroute function
def traceroute(destination, max_hops=30, timeout=1):
    destination_ip = socket.gethostbyname(destination)
    port = 33434
    ttl = 1

    response = []

    while True:
        #creating the IP and UDP headers
        ip_packet  = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)

        #combining the headers
        packet = ip_packet / udp_packet
        
        #sending the packet and receive a reply
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            #no reply, print * for timeout
            #print(f"{ttl}\t*")
            response.append([destination, ttl, 'noreply', '*'])
        elif reply.type == 3:
            #destination reached, print the details
            #print(f"{ttl}\t{reply.src}")
            response.append([destination, ttl, 'reached', reply.src])
            return response
        else:
            #printing the IP address of the intermediate hop
            #print(f"{ttl}\t{reply.src}")
            response.append([destination, ttl, 'intermediate-hop', reply.src, geolocate(reply.src)])

        ttl += 1

        if ttl > max_hops:
          return response