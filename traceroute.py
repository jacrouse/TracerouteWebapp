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
        return jsonify({'result': traceroute(hostname)}), 200
    else:
        return jsonify({'result': request.remote_addr}), 200


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
    return ["testlat", "testlng"]


#format response
def formatResponse(response):
    result = "<br>".join(", ".join(x) for x in response)
    return result

#traceroute function
def traceroute(destination, max_hops=30, timeout=1):
    #try to get IP
    try:
        destination_ip = socket.gethostbyname(destination)
    except:
        return "Something went wrong, is this a real host?"

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
            response.append(["TTL: " + str(ttl), "Noreply", "*"])
        elif reply.type == 3:
            #destination reached, print the details
            #print(f"{ttl}\t{reply.src}")
            response.append(["TTL: " + str(ttl), "Reached", "Source: " + reply.src])
            return formatResponse(response)
        else:
            #printing the IP address of the intermediate hop
            #print(f"{ttl}\t{reply.src}")
            response.append(["TTL: " + str(ttl), "Intermediate-hop", "Source: " + reply.src, "Coords: " + str(geolocate(reply.src))])

        ttl += 1

        if ttl > max_hops:
            return formatResponse(response)