######################################
##                                  ##
##            IP_Tracker            ##
##                                  ##
######################################

#import

import os 
import sys
import csv
import time
import uuid
import subprocess
import folium
import socket
import requests
import colorama
import argparse
import phonenumbers
from geopy.distance import distance
try:
    from phonenumbers import geocoder
    from phonenumbers import carrier
    from opencage.geocoder import OpenCageGeocode
    pass
except:
    pass

# Setting the color combinations
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"


#scan map / ip scapy


def mac(mac):
        
        MAC_URL = 'https://api.maclookup.app/v2/macs/{0}'.format(mac)

        r = requests.get(MAC_URL)
        org = r.json()   

        if org['success'] == False:
            print('wrong format')
            time.sleep(2)
            clear()
            main()
            pass
        else:
            macP = org['macPrefix']
            Comp = org['company']
            adress = org['address']
            country = org['country']
            upt = org['updated']
            

 
        if org['found'] == False:
            print('mac not found')
            time.sleep(2)
            clear()
            main()
            pass
        else:
            print('vendor found')

            print(f"mac prefix : {macP}")
            print(f"Company : {Comp}")
            print(f"address : {adress}")
            print(f"country : {country}")
            print(f"updated : {upt}")

            print('')
            oss()

        
#change mac 

def Mac_switch(interface, mac):
    
    try:
        subprocess.call(['sudo', 'ifconfig', interface, 'ether', mac])
        print(f'Succes / New mac : {mac}')
    except:
        print('Can t change this mac')
        pass

    print('')
    try:
        subprocess.call(['sudo', 'ifconfig', interface, 'up'])
    except:
        print('error on proccess 3')
    
    print('')
    oss()
    

#var ip 

clear = lambda:os.system('clear')

def CalcDistance(ip1, ip2):
    req_1 = requests.get('http://ip-api.com/json/' + ip1)
    req_2 = requests.get('http://ip-api.com/json/' + ip2)

    req_a = req_1.json()
    req_b = req_2.json()

    lat1, lng1 = req_a['lat'], req_a['lon']
    lat2, lng2 = req_b['lat'], req_b['lon']

    print('distance : ', distance((lat1, lng1),(lat2, lng2)).km, 'Km')

    #save 

    a = distance((lat1, lng1),(lat2, lng2)).km

    print('')
    questr = input('[0]-Exit / [1]-Save / Back : ')
    if questr == '0':
        sys.exit()
    elif questr == '1':
        quest = input('Name file : ')
        Modul_2(quest, ip1, ip2, a)
        q = input('[0]-Exit / Back : ')
        if q == '0':
            sys.exit()
        else:
            clear()
            main
    else:
        clear()
        main()

def IpDetail(ip):
    
    request = requests.get('http://ip-api.com/json/' + ip + '?fields=status,message,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,query,asname')
    org = request.json()
    if org['status'] == 'fail':
        print('Ip not found')
        time.sleep(1)
        clear()
        main()
    else:
        print('ip found')
        print('')
        print(f"Ip Address: {ip}")
        print(f"City: {org['city']}, {org['regionName']}, {org['country']}")
        print(f"Zip: {org['zip']}")
        print(f"XY: lat : {org['lat']}, lng : {org['lon']}")
        print(f"Timezone: {org['timezone']}")
        print(f"Isp: {org['isp']}")
        print(f"Proxy: {org['proxy']}")
        print(f"Cellular Co: {org['mobile']}")

    #save

        ipz = ip
        city = org['city'], org['regionName'], org['country']
        Zip = org['zip']
        X = org['lat']
        Y = org['lon']
        Time = org['timezone']
        Isp = org['isp']
        proxy = org['proxy']
        cellular = org['mobile']

        print('')
        questr = input('[0]-Exit / [1]-Save / Back : ')
        if questr == '0':
            sys.exit()
        elif questr == '1':
            quest = input('Name file : ')
            Modul_1(quest, ipz, city, Zip, X, Y, Time, Isp, proxy, cellular)
            q = input('[0]-Exit / Back : ')
            if q == '0':
                sys.exit()
            else:
                clear
                main()
        else:
            clear
            main()

def UrlDetail(url):   
    ip_add = socket.gethostbyname(url)
    
    IpDetail(ip_add)

def getNameHostIp(ip):
    try:
        
        host = socket.gethostbyaddr(ip)[0]
        print(f'ip : {ip},  Name : {host}')
    except socket.herror:
        return "No domain found"
    
def getApiName():
    api = requests.get('654155a35ce62e6a8a6049d8-502936ccc45d')
    print(api)

def MapIp(ip):
    request = requests.get('http://ip-api.com/json/' + ip + '?fields=status,message,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,query,asname')
    org = request.json()
    X = org['lat']
    Y = org['lon']
    quest = input('Name Map : ')
    Map_1(quest,X,Y)
      
#var phone number 

def Location_number(Num):   
    key = 'ac2d813ef9674414b5dfb748f89fbaca'
    phone = phonenumbers.parse(Num)
    location = geocoder.description_for_number(phone,lang='fr')  
    isp = carrier.name_for_number(phone,"fr")
    geo = OpenCageGeocode(key)
    lat_lng = str(location)
    res = geo.geocode(lat_lng)
    
    print(location)
    print(isp)
    print(res)

#map 

def Map_1(NameMap, lat, long):
    FILE = 'data/' + NameMap + '.html'
    map = folium.Map(location=[lat, long], zoom_start=4)
    folium.Marker([lat, long],popup='yourLocation').add_to((map))
    map.save(FILE)
    print('Map Saved !')
    v = input('[0]-Exit / back : ')
    if v == '0':
        sys.exit()
    else: 
        clear()
        main()

#save in csv

def Modul_1(NameFile, ip, city, Zip, X, Y, Timezone, Isp, proxy, cellular):
    e = 'data/' + NameFile + '.txt'
    file = open(e, 'w+')

    file.write(f'ip : {ip} ' + '\n')
    file.write(f'city : {city}  '+ '\n')
    file.write(f'zip : {Zip} '+ '\n')
    file.writelines(f'XY : lat : {X}, long {Y} '+ '\n')
    file.write(f'timezone : {Timezone}  '+ '\n')
    file.write(f'isp : {Isp}'+ '\n')
    file.write(f'proxy : {proxy}'+ '\n')
    file.write(f'cellular : {cellular}'+ '\n')
    print('Info Saved !')
    file.close()
   
def Modul_2(NameFile, ip1, ip2, Dist):
    a = 'data/' + NameFile + '.txt'
    file = open(a, 'w+')

    file.write(f"ip_1 : {ip1} \n")
    file.write(f"ip_2 : {ip2} \n")
    file.write(f"Distance : {Dist}km \n")

    print('Info Saved !')
    file.close()

#remover

def remove():
    try: 
        m = input('Name File : ')
        os.system('rm data/'+ m)
        print('Remove Succes !')
        time.sleep(2)
        clear()
        main()
    except:
        print('Rm error retry')
        remove()

#use

def mac_change():
    q = input('New mac : ')
    i = input('Interface name : ')
    Mac_switch(i,q)

def mac_lookup():
    c = input("Mac address : ")
    mac(c)


def Phone_info():
    v = input('Number : ')
    Location_number(v)

def Map_use():
    ip = input('Ip : ')
    MapIp(ip)

def IP_Location():  
    try:        
        ip_add = input("Enter IP: ")
        IpDetail(ip_add)
    except:
        time.sleep(1)
        clear()
        main()
    
def IP_Calc():
    #try:
        ip1 = input('ip [1] : ')
        ip2 = input('ip [2] : ')

        dist = CalcDistance(ip1, ip2)
        print('')
        print(f"Distance : {str(dist)}km / 1 -> 2")
        print('')
        oss()
    #except:
        print('error on modul')

def IP_Url():
    try:
        url = input('Url : ')
        UrlDetail(url)
        print('')
        oss()
    except:
        print('error on URL')

def GethostName():
    quest = input('Ip : ')
    getNameHostIp(quest)

    print('')
    oss()

def oss():
    questr = input('[0]-Exit / Back : ')
    if questr == '0':
        sys.exit()
    else:
        clear()
        main()


def main():
    clear()
    id = socket.gethostname()
    mac = uuid.getnode()
    macString=':'.join(("%012X" % mac) [i:i+2] for i in range(0,12,2))
    print('[0]-Exit')
    print(colorama.Fore.CYAN+"""
_________________________________________________________

███╗   ██╗███████╗████████╗ ██████╗  ██████╗ ██╗     
████╗  ██║██╔════╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██╔██╗ ██║█████╗     ██║   ██║   ██║██║   ██║██║     
██║╚██╗██║██╔══╝     ██║   ██║   ██║██║   ██║██║     
██║ ╚████║███████╗   ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
""")
    print(colorama.Fore.LIGHTYELLOW_EX+'MAC: ' + '['+macString+']'+' ID: '+'['+id+']')
    print(colorama.Fore.LIGHTCYAN_EX+'_________________________________________________________')
    print(colorama.Fore.LIGHTYELLOW_EX+"""
[1] - Ip info               [5] - Mac address info 
[2] - Link info             [6] - Mac address changer
[3] - 2 ip distance         [7] - Remove file
[4] - Ip map   
""")
    
    quest = input('- Mode : ')

    if quest == '1':
        IP_Location()
    
    elif quest == '2':
        IP_Url()

    elif quest == '3':
        IP_Calc()
    
    elif quest == '4':
        Map_use()
    
    elif quest == '5':
        mac_lookup()
    
    elif quest == '7':
        remove()
    
    elif quest == '6':
        mac_change()
        #Phone_info()
        
    

    elif quest == '0':
        sys.exit()

    else: 
        print('Retry')
        clear
        main()
    
#main

if __name__ == "__main__":
    main()
    
