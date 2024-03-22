from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd
from scapy.all import *
import socket
import struct
import json
import time
import argparse
import requests
from urllib.request import urlopen
import numpy as np
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

@app.route('/request', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def responseHandler():
    if request.method == "POST":
        hostname = request.form['request']
        response = jsonify({'result': traceroute(hostname)})
        print("Finished traceroute")
        return response, 200
    else:
        print("Sending client IP")
        response = jsonify({'result': request.remote_addr})
        return response, 200


#geolocation function
def geolocate(host):
    #get IP if not already an IP
    IP = socket.gethostbyname(host)

    #API URL with IP embedded
    url = "http://ipwho.is/" + IP
    response = urlopen(url)

    if(response.getcode() == 200):
        #format to json
        jResponse = json.load(response)
        
        try:
            #extract data
            lat = jResponse["latitude"]
            lng = jResponse["longitude"]
        except(KeyError):
            return str(["NoLat", "NoLng"])

        #return pair
        return str([lat, lng])


    #return str(np.random.rand(2) * 10)

#format response
def formatResponse(response):
    result = " <br> ".join(", ".join(x) for x in response)
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
            response.append(["TTL: " + str(ttl), "Noreply", "*"])
        elif reply.type == 3:
            #destination reached, print the details
            response.append(["TTL: " + str(ttl), "Reached", "Source: " + reply.src])
            return formatResponse(response)
        else:
            #printing the IP address of the intermediate hop
            response.append(["TTL: " + str(ttl), "Intermediate-hop", "Source: " + reply.src, "Coords: " + geolocate(reply.src)])
            
        ttl += 1

        if ttl > max_hops:
            return formatResponse(response)

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
