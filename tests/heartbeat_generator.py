# File: tests/heartbeat_generator.py
# Purpose: Generates a single ICMP Echo Request with a randomized, covert log payload
# for Wireshark inspection.

import random
from scapy.all import IP, ICMP, Ether, sendp 
import sys

# --- 1. Define Log Constants (Matches our 32-bit Header Scheme) ---

# Activity Type Codes (4 bits)
ACTIVITY_TYPES = {
    "SCAN": 0b0001,
    "CONN_ATTEMPT": 0b0010,
    "INTERACTION": 0b0011,
}

# Service Type Codes (4 bits)
SERVICE_TYPES = {
    "SSH": 0b0001,
    "HTTP": 0b0010,
    "SMB": 0b0011,
}

# --- 2. Configuration for Test Packet ---

IFACE = "enp1s0"  # **ADJUST THIS to your actual network interface (e.g., 'enp0s3', 'wlan0')**
SOURCE_IP = "192.168.0.45"  # FAKE: The Deception Host that "sends" the log
DEST_IP = "192.168.0.254"   # FAKE: The Plausible Gateway/Log Destination
ICMP_PAYLOAD_SIZE = 48      # Total size of the ICMP data field in bytes (must be >= 4)

def generate_covert_packet(activity="SCAN", service="SSH", attacker_id=10, target_id=50):
    """
    Generates a single ICMP packet with a randomized, self-describing 4-byte
    log header hidden within a larger payload of random noise.
    """
    
    if ICMP_PAYLOAD_SIZE < 4:
        raise ValueError("Payload size must be at least 4 bytes to hold the header.")

    # --- Step A: Encode the 32-Bit Log Header (4 Bytes) ---
    
    # Randomly select a position for the header (in 4-byte blocks)
    # The header takes 4 bytes. We need to leave room for the padding.
    max_offset = (ICMP_PAYLOAD_SIZE // 4) - 1 
    # The Offset Pointer itself is 4 bits, so it can encode max 15 (0b1111)
    offset_blocks = random.randint(0, min(max_offset, 15))
    
    # 4 bits for Offset Pointer (0-15)
    offset_pointer = offset_blocks << 28 

    # 4 bits for Activity Type
    activity_type = ACTIVITY_TYPES.get(activity, 0) << 24
    
    # 4 bits for Service Type
    service_type = SERVICE_TYPES.get(service, 0) << 20
    
    # 4 bits for Reserved/Random Data (Adding some extra randomness here)
    reserved_data = random.randint(0, 15) << 16
    
    # 8 bits for Attacker Host ID
    attacker_octet = (attacker_id & 0xFF) << 8
    
    # 8 bits for Target Host ID (The least significant part of the IP)
    target_octet = target_id & 0xFF
    
    # Combine all 32 bits into a single integer (our log unit)
    log_int = offset_pointer | activity_type | service_type | reserved_data | attacker_octet | target_octet
    
    # Convert the 4-byte integer to actual byte sequence (Big Endian)
    covert_header = log_int.to_bytes(4, byteorder='big')
    
    # --- Step B: Create the Randomized Payload ---
    
    # Create a buffer of pure random bytes (the "noise")
    random_payload = bytearray(random.getrandbits(8) for _ in range(ICMP_PAYLOAD_SIZE))
    
    # --- Step C: Embed the Header using the calculated offset ---
    
    # The offset is the block number * 4 bytes per block
    start_byte_offset = offset_blocks * 4
    
    # Insert the 4-byte header into the randomized payload
    random_payload[start_byte_offset:start_byte_offset + 4] = covert_header
    
    # --- Step D: Construct and Send the Packet using Layer 2 (sendp) ---
    
    # 1. Ethernet Layer (L2): Scapy will automatically determine the Source MAC.
    ether_layer = Ether()
    
    # 2. IP Layer (L3): Source and Destination
    ip_layer = IP(src=SOURCE_IP, dst=DEST_IP)
    
    # 3. ICMP Layer (L4): Type=8 (Echo Request)
    icmp_layer = ICMP(type=8)
    
    # Complete Packet: Ether / IP / ICMP / Payload
    packet = ether_layer / ip_layer / icmp_layer / bytes(random_payload)
    
    print(f"[!] Sending L2 (sendp) ICMP heartbeat from {SOURCE_IP} to {DEST_IP}...")
    print(f"[!] Log Header (Hex): {covert_header.hex()}")
    print(f"[!] Embedded at Byte Offset: {start_byte_offset}")
    
    # Sending at layer 2 (Ethernet)
    sendp(packet, verbose=0, iface=IFACE)
    
    print("\n[+] Packet sent. Check Wireshark for ICMP traffic on the interface.")
    print(f"    Search the ICMP Data field for the repeating sequence: {covert_header.hex()}")


if __name__ == "__main__":
    try:
        # Example Log: Attacker 192.168.0.10 performed a SCAN on target 192.168.0.50
        generate_covert_packet(
            activity="CONN_ATTEMPT", 
            service="SSH",
            attacker_id=10, 
            target_id=50
        )
    except OSError as e:
        if "Permission denied" in str(e) or "Operation not permitted" in str(e):
            print("\n[!!!] ERROR: Raw socket access requires root/administrator privileges.")
            print("      Please run the script using 'sudo python3 heartbeat_generator.py'")
        else:
            print(f"\n[!!!] ERROR: {e}")
    except Exception as e:
        print(f"\n[!!!] An unexpected error occurred: {e}")
