from scapy.all import *
import pandas as pd
import matplotlib.pyplot as plt

# Load capture file (CHANGE PATH if needed)
packets = rdpcap("main.pcap")

# Total packets
total_packets = len(packets)
print("Total packets:", total_packets)

# Total size of data
total_size = sum(len(pkt) for pkt in packets)
print("Total data size:", total_size, "bytes")

# Header size estimation
header_size = sum(len(pkt) - len(pkt.payload) for pkt in packets if pkt.payload)
print("Header size:", header_size)

# Extract communication pairs
pairs = {}

for pkt in packets:
    if IP in pkt:
        pair = (pkt[IP].src, pkt[IP].dst)

        if pair not in pairs:
            pairs[pair] = {
                "packets": 0,
                "bytes": 0,
                "times": []
            }

        pairs[pair]["packets"] += 1
        pairs[pair]["bytes"] += len(pkt)
        pairs[pair]["times"].append(pkt.time)


# Print communication statistics
for pair, data in pairs.items():

    print("\nSource:", pair[0])
    print("Destination:", pair[1])
    print("Packets:", data["packets"])
    print("Bytes:", data["bytes"])

    times = data["times"]

    if len(times) > 1:
        diff = [(times[i+1]-times[i]) for i in range(len(times)-1)]
        avg = sum(diff)/len(diff)
        print("Avg inter packet time:", avg)


# -----------------------------
# GRAPH SECTION (LAB REQUIRED)
# -----------------------------

total_pps = {}
tcp_pps = {}
udp_pps = {}
dns_pps = {}
icmp_pps = {}

for pkt in packets:

    sec = int(pkt.time)

    # Total packets/sec
    total_pps[sec] = total_pps.get(sec, 0) + 1

    # TCP packets/sec
    if TCP in pkt:
        tcp_pps[sec] = tcp_pps.get(sec, 0) + 1

    # UDP packets/sec
    if UDP in pkt:
        udp_pps[sec] = udp_pps.get(sec, 0) + 1

    # DNS packets/sec
    if DNS in pkt:
        dns_pps[sec] = dns_pps.get(sec, 0) + 1

    # ICMP packets/sec
    if ICMP in pkt:
        icmp_pps[sec] = icmp_pps.get(sec, 0) + 1


# Function to plot graph
def plot_graph(data, title):

    x = sorted(data.keys())
    y = [data[i] for i in x]

    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Packets per second")
    plt.grid()
    plt.show()


# Plot required 5 graphs

plot_graph(total_pps, "Packets per Second")
plot_graph(tcp_pps, "TCP Packets per Second")
plot_graph(udp_pps, "UDP Packets per Second")
plot_graph(dns_pps, "DNS Packets per Second")
plot_graph(icmp_pps, "ICMP Packets per Second")


# Protocol totals (for lab record)

tcp_count = sum(1 for pkt in packets if TCP in pkt)
udp_count = sum(1 for pkt in packets if UDP in pkt)
dns_count = sum(1 for pkt in packets if DNS in pkt)
icmp_count = sum(1 for pkt in packets if ICMP in pkt)

print("\nProtocol Counts:")
print("TCP:", tcp_count)
print("UDP:", udp_count)
print("DNS:", dns_count)
print("ICMP:", icmp_count)
