from scapy.all import sniff, IP, conf

def process_packet(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        print(f"Packet: {src} -> {dst}")

def start_sniffing():
    print("Sniffing started (L3 mode)...")

    sniff(
        prn=process_packet,
        store=False,
        L3socket=conf.L3socket
    )

def capture_packet():
    print("Packet capture started...")
    return {"status": "sniffer running"}
