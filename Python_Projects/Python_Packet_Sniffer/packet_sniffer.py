# Import necessary libraries
from scapy.all import sniff, IP, TCP, UDP  # Used for packet sniffing
import psutil  # Used for monitoring active network connections
import time  # Used to add delays for better readability

# Function to handle sniffed packets
def packet_handler(packet):
    """
    Processes each captured packet and extracts important details.
    Checks if the packet contains an IP layer and determines its protocol (TCP/UDP).
    """
    if IP in packet:
        proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
        print(f"Packet: {proto} | Src: {packet[IP].src} -> Dst: {packet[IP].dst}")

# Function to monitor active network connections
def monitor_connections():
    """
    Retrieves and displays a list of active network connections on the system.
    Filters connections that are in the 'ESTABLISHED' state.
    """
    print("\n[*] Active Network Connections:")
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "ESTABLISHED":
            print(f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port} [{conn.status}]")

# Main execution block
if __name__ == "__main__":
    print("[*] Starting Network Sniffer... Press Ctrl+C to stop.")

    try:
        while True:
            # Sniff network packets for 5 seconds, capturing up to 10 packets at a time
            sniff(prn=packet_handler, store=False, count=10, timeout=5)  
            
            # Monitor active network connections every 5 seconds
            monitor_connections()
            
            # Adds a 5-second delay before the next iteration to prevent flooding
            time.sleep(5)  

    except KeyboardInterrupt:
        # Gracefully handle script termination when user presses Ctrl+C
        print("\n[*] Stopping Network Sniffer...")

