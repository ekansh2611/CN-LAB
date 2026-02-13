import csv

file_path = "lab7.csv"

pairs = {}

with open(file_path, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        src = row["Address A"]
        dst = row["Address B"]

        packets = int(row["Packets"])
        bytes_data = int(row["Bytes"])

        # Duration used for average inter-packet time
        try:
            duration = float(row["Duration"])
        except:
            duration = 0

        pair = (src, dst)

        pairs[pair] = {
            "packets": packets,
            "bytes": bytes_data,
            "duration": duration
        }


# 1. Pair communicating maximum bytes

max_bytes = 0
max_pair = None

for pair, data in pairs.items():

    if data["bytes"] > max_bytes:

        max_bytes = data["bytes"]
        max_pair = pair


print("\nPair communicating maximum bytes:")
print("Source:", max_pair[0])
print("Destination:", max_pair[1])
print("Bytes:", max_bytes)


# 2. Average inter-packet time difference

print("\nAverage Inter-Packet Time Difference:")

for pair, data in pairs.items():

    if data["packets"] > 0:

        avg_time = data["duration"] / data["packets"]

    else:

        avg_time = 0

    print(pair[0], "<->", pair[1], ":", avg_time)


# 3. Total number of packets transferred between every pair

print("\nTotal packets between each pair:")

for pair, data in pairs.items():

    print(pair[0], "<->", pair[1], ":", data["packets"])
