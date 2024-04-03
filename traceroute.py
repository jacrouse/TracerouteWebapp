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

globalClientIP = ""

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

@app.route('/request', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def responseHandler():
    if request.method == "POST":
        global globalClientIP
        globalClientIP = request.remote_addr
        hostname = request.form['request']
        response = jsonify({'result': traceroute(hostname, 50, 2)})
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

    response = []

    #creating the IP and TCP headers
    ip_packet  = IP(dst=destination, ttl=(1,max_hops), id=RandShort())
    tcp_packet = TCP(flags=0x2)

    #combining the headers
    packet = ip_packet / tcp_packet
    
    #sending the packet and receive a reply
    s,r = sr(packet, timeout=timeout, verbose=0)
    response.append(["TTL: " + '0', "Origin", "Source: " + globalClientIP, "Coords: " + geolocate(globalClientIP)])

    for send,receive in s:
        if receive.src == destination_ip:
            #destination reached, print the details
            response.append(["TTL: " + str(send.ttl), "Reached", "Source: " + receive.src])
            return formatResponse(response)
        else:
            #printing the IP address of the intermediate hop
            response.append(["TTL: " + str(send.ttl), "Intermediate-hop", "Source: " + receive.src, "Coords: " + geolocate(receive.src)])

    return formatResponse(response)

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
