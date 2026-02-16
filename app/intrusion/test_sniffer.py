import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.intrusion.packet_sniffer import start_sniffing

start_sniffing()
