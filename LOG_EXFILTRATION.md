# 📡 Covert Log Exfiltration

To ensure logs are transferred without alerting an intelligent attacker, Ansanet uses a **Heartbeat Steganography** technique. Log data is covertly embedded in the network's background noise, specifically within randomized ICMP Echo Request (Ping) packets.

These packets will, in turn, be read by a listener in promiscuous mode, so as to conceal itself in the network.

**Channel Specification: Minimal Binary Logging**

Each critical log event is encoded into a 4-byte (32-bit) minimal log unit. This unit is randomized and self-describing, meaning its position within the packet payload changes every time it is sent.

| Field            | Size (Bits) | Description                                                                                               | Encoding                                                                |
| ---------------- | ----------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Offset Pointer   | 4           | Defines where the remaining 28 bits of data start within the packet payload (in 4-byte block increments). | 0000 to 1111 (0 to 15 blocks)                                           |
| Header Type      | 4           | The category of the event recorded.                                                                       | 0000 (No Operation), 0001 (Scan), 0010 (Connection), 0011 (Interaction) |
| Target Service   | 4           | The service or port being targeted.                                                                       | 0001 (SSH), 0010 (HTTP), 0011 (SMB), Random (if Header Type is 0000)    |
| Reserved Data    | 4           | Placeholder for future flags (currently random bits).                                                     | Random 4-bit integer                                                    |
| Attacker Host ID | 8           | The last octet of the Attacker's IP address.                                                              | 0 to 255                                                                |
| Target Host ID   | 8           | The last octet of the Deception Host's IP address.                                                        | 0 to 255                                                                |

**Stealth Strategy: Randomization**

In order to make it harder for an attacker to detect these transmissions, some packets will be generated without a new event being recorded, in which case the Header Type will be No Operation (`0000`).

Placement: The 4-byte header is placed at a position defined by the Offset Pointer, which is regenerated randomly for every packet.

Padding: The remainder of the ICMP data payload is filled with cryptographically random bytes, ensuring the log header is indistinguishable from the noise.

Destination: Logs are sent to a Plausible Silent IP (e.g., a simulated gateway or external DNS server) to avoid generating tell-tale ICMP Destination Unreachable messages.
