import pandas as pd
import json
import time
import datetime
import csv
from scapy.all import *
from urllib.request import urlopen

globalClientIP = "167.99.0.220"
globalClientCoords = "[40.7127837 -74.0059413]"
globalHostList = ["webtan.impress.co.jp", "news.mn", "mail.ru", "ftp.sjtu.edu.cn", "sbu.ac.ir", "redfishportorford.com", "www.redfishportorford.com"]

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
    #columns are TTL, Status, Source, Coords, Date
    #status can be "Origin", "Intermediate", or "Reached"
    response = []

    #creating the IP and TCP headers
    ip_packet  = IP(dst=destination, ttl=(1,max_hops), id=RandShort())
    tcp_packet = TCP(flags=0x2)

    #combining the headers
    packet = ip_packet / tcp_packet
    
    #sending the packet and receive a reply
    s,r = sr(packet, timeout=timeout, verbose=0)

    #get start time
    now = datetime.utcnow().strftime("%m/%d/%Y-%H:%M:%S.%f")[:-3]
    response.append(['0', "Origin", globalClientIP, globalClientCoords, now])

    for send,receive in s:
        #get date and time in UTC
        now = datetime.utcnow().strftime("%m/%d/%Y-%H:%M:%S.%f")[:-3]
        
        if receive.src == destination_ip:
            #destination reached, print the details
            response.append([str(send.ttl), "Reached", receive.src, geolocate(receive.src), now])
            return response
        else:
            #printing the IP address of the intermediate hop
            response.append([str(send.ttl), "Intermediate", receive.src, geolocate(receive.src), now])
    return response


def main():
    try:
        #check if file exists, if not create it
        if not os.path.exists("recordedRoutes.csv"):
            with open("recordedRoutes.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                fields = ["TTL", "Status", "Source", "Coords", "Date"]
                writer.writerow(fields)
    
        #while loop to record each traceroute and export to csv
        while(True):
            for host in globalHostList:
                entry = traceroute(host)
                df = pd.DataFrame(entry)
                df.to_csv("recordedRoutes.csv", mode='a', header=False, index=False)
                time.sleep(5)
            time.sleep(7200)

    except(KeyboardInterrupt):
        exit()


if __name__ == "__main__":
    main()
