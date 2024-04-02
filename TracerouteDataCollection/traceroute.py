import pandas as pd
import json
import time
from scapy.all import *
from urllib.request import urlopen

globalClientIP = "167.99.0.220"

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


#traceroute function
def traceroute(destination, max_hops=30, timeout=1):
    #try to get IP
    try:
        destination_ip = socket.gethostbyname(destination)
    except:
        return "Something went wrong, is this a real host?"

    #this will be added to data frame later
    #columns are TTL, Source, 
    response = ()

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
            response.append(str(send.ttl), "Reached", "Source: " + receive.src])
            return response
        else:
            #printing the IP address of the intermediate hop
            response.append(["TTL: " + str(send.ttl), "Intermediate-hop", "Source: " + receive.src, "Coords: " + geolocate(receive.src)])

    return response


def main():
    try:
        hosts = ["google.com", "yahoo.com"]
        while(True):
            for host in hosts:
                print(traceroute(host))
            print("Finished, restarting in 5 seconds")
            time.sleep(5)

    except(KeyboardInterrupt):
        exit()



if __name__ == "__main__":
    main()
