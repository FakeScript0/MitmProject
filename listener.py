import scapy.all as scapy
def listen_packets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyze_packets)
    #prn = callback function
def analyze_packets(packet):
    packet.show()
listen_packets("eth0")
