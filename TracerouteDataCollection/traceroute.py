import pandas as pd
import json
import time
import datetime
import csv
from scapy.all import *
from urllib.request import urlopen

globalClientIP = "167.99.0.220"
globalClientCoords = "[40.7127837 -74.0059413]"
globalHostList = ["borysov.com.ua", "romapass.it", "tver.ru", "yenicagaascilik.meb.k12.tr"]

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
    #columns are Target, TTL, Status, Source, Coords, Time
    #status can be "Origin", "Intermediate", or "Reached"
    #round trip time is stored in the data entry where the packet is "Reached" if there is one
    response = []

    #creating the IP and TCP headers
    ip_packet  = IP(dst=destination, ttl=(1,max_hops), id=RandShort())
    tcp_packet = TCP(flags=0x2)

    #combining the headers
    packet = ip_packet / tcp_packet

    #get start time
    now = datetime.now()

    #sending the packet and receive a reply
    s,r = sr(packet, timeout=timeout, verbose=0)

    startTime = s[0][0].sent_time
    
    #add point of origin to data
    response.append([destination, '0', "Origin", globalClientIP, globalClientCoords, "-1"])

    for send,receive in s:
        if receive.src == destination_ip:
            #destination reached, print the details
            response.append([destination, str(send.ttl), "Reached", receive.src, geolocate(receive.src), str((receive.time - startTime) * 1000)])
            return response
        else:
            #printing the IP address of the intermediate hop
            response.append([destination, str(send.ttl), "Intermediate", receive.src, geolocate(receive.src), "-1"])

    
    return response


def main():
    try:
        #check if file exists, if not create it
        if not os.path.exists("recordedRoutes.csv"):
            with open("recordedRoutes.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                fields = ["Destination", "TTL", "Status", "Source", "Coords", "Latency"]
                writer.writerow(fields)
    
        #while loop to record each traceroute and export to csv
        while(True):
            for host in globalHostList:
                entry = traceroute(host)
                df = pd.DataFrame(entry)
                df.to_csv("recordedRoutes.csv", mode='a', header=False, index=False)
                time.sleep(5)
            time.sleep(20)

    except(KeyboardInterrupt):
        exit()


if __name__ == "__main__":
    main()
