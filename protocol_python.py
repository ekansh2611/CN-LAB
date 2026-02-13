import csv

# Read protocol hierarchy CSV exported from Wireshark
with open("protocol.csv", "r") as file:

    reader = csv.reader(file)

    next(reader)  # skip header

    print("Protocol Hierarchy Analysis:\n")

    total_packets = 0

    for row in reader:

        protocol = row[0]
        count = int(row[1])

        print("Protocol:", protocol, "Packets:", count)

        total_packets += count

    print("\nTotal Protocol Entries:", total_packets)
