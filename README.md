
# DNS Spoofer

This Python script is a simple DNS spoofing tool that modifies DNS responses for a specific domain, redirecting traffic to a specified IP address. The script uses `netfilterqueue` to intercept packets and `scapy` to manipulate and inject malicious DNS responses.

## How It Works

- The script intercepts DNS queries using `netfilterqueue`.
- It checks if the query is for the target domain (`www.vulnweb.com`).
- If a match is found, the DNS response is spoofed, and the query is redirected to the attacker’s IP (in this example: `192.168.1.5`).
- The modified packet is then sent back to the victim.

## Prerequisites

- **Kali Linux** or any Linux distribution with root access.
- Python 3.x installed.
- `iptables` for creating packet queues.
- `netfilterqueue` and `scapy` Python libraries.

### Installing Dependencies

1. **Install `scapy`**:
   ```bash
   sudo pip install scapy
   ```

2. **Install `netfilterqueue`** (ensure the required system libraries are installed):
   ```bash
   sudo apt-get install libnetfilter-queue-dev
   sudo pip install netfilterqueue --break-system-packages
   ```

## Running the Script

### Step 1: Set up iptables

Use `iptables` to forward DNS packets to a queue (queue number `0` in this example). This allows the script to intercept the packets.

```bash
sudo iptables -I FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 0
```

To spoof packets on your local machine, use this iptables rule:
```bash
sudo iptables -I OUTPUT -p udp --dport 53 -j NFQUEUE --queue-num 0
sudo iptables -I INPUT -p udp --sport 53 -j NFQUEUE --queue-num 0
```

### Step 2: Run the Python Script

```bash
sudo python3 dns_spoofer.py
```

### Step 3: Clean Up iptables Rules (Optional)

After running the script, reset your iptables rules to their original state:

```bash
sudo iptables --flush
```

## Script Breakdown

- **process_packet(packet)**: This function processes each packet intercepted by `netfilterqueue`. It checks if the packet contains a DNS response and modifies it if the target domain (`www.vulnweb.com`) is found.
- **scapy.IP(packet.get_payload())**: Converts the packet payload into a Scapy packet for easier manipulation.
- **scapy.DNSRR**: Used to create a spoofed DNS response, pointing to `192.168.1.5`.
- **queue.bind(0, process_packet)**: Binds the script to iptables' queue `0`.

## Warning

This script is for educational purposes only. Performing DNS spoofing attacks on networks without permission is illegal and unethical.

## License

0x1tsjusthicham
