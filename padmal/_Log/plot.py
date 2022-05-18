import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = (20, 8)

POWER_L = int(input("POWER: ") or "0")
RATE_P = int(input("RATE: ") or "50")
PACKETS = int(input("PACKETS: ") or "2500")

MIN_RSSI = -100
MAX_RSSI = -10
BIN_PORTION = PACKETS / 10
BINS = [i * BIN_PORTION for i in range(11)]

SCATTER = 5
L_WIDTH = 0.5

props = dict(boxstyle='round', facecolor='#cccccc', alpha=0.5)

TX_NODE = '67b5.5e11.0074.1200'

ttl = 'RSSI Measurements {Total Packet Count: ' \
      + str(PACKETS) + '; Transmit Power: ' \
      + str(POWER_L) + ' dBm; Packet Rate: ' \
      + str(RATE_P) + ' ms; Packets per Bin: ' + str(int(BIN_PORTION)) + ' packets}'


def extract_packet_data(filename):
    """
    This method will take a file of packet readings as input and go through each line.
    If any line has the IP address defined above, it will fill in the points array with
    the corresponding RSSI value and another array with sequence number

    There will be four arrays returned at last, two with RSSI readings and two with seq.

    [INFO: EavesDr   ] Received 0 from 0f2a.7d13.0074.1200 [RSSI: -60 | LQI: 107]
    """
    file_node_lines = filename.readlines()
    node_points = []
    node_seq = []

    for line in file_node_lines:
        if TX_NODE in line:
            try:
                line_as_list = line.split(' ')
                rssi = int(line_as_list[-4])
                seq = int(line_as_list[-8])
                node_points.append(rssi)
                node_seq.append(seq)
            except:
                continue
    print("Parsing", filename.name)
    return node_points, node_seq


#######################################################################################################################
# Files                                                                                                               #
#######################################################################################################################
Ev1 = open('Eaves-1.txt', 'r')
Ev2 = open('Eaves-2.txt', 'r')
Ev3 = open('Eaves-3.txt', 'r')
Ev4 = open('Eaves-4.txt', 'r')
Ph2 = open('Receive.txt', 'r')

#######################################################################################################################
# Plot preparation                                                                                                            #
#######################################################################################################################
f, ((ev1, ev2, ev3, ev4, pha), (fr1, fr2, fr3, fr4, fr5)) = plt.subplots(2, 5)

eAxes = [ev1, ev2, ev3, ev4, pha]
fAxes = [fr1, fr2, fr3, fr4, fr5]

f.suptitle(ttl, fontweight='bold')

(P1_E1, S_P1_E1) = extract_packet_data(Ev1)
(P1_E2, S_P1_E2) = extract_packet_data(Ev2)
(P1_E3, S_P1_E3) = extract_packet_data(Ev3)
(P1_E4, S_P1_E4) = extract_packet_data(Ev4)
(P1_P2, S_P1_P2) = extract_packet_data(Ph2)

PacketList = [P1_E1, P1_E2, P1_E3, P1_E4, P1_P2]
SequenceList = [S_P1_E1, S_P1_E2, S_P1_E3, S_P1_E4, S_P1_P2]

#######################################################################################################################
# Plots                                                                                                  #
#######################################################################################################################

for f in range(len(fAxes)):
    title = 'Eaves ' + str(f + 1)
    if f == 4:
        title = 'In-body'

    eAx = eAxes[f]

    prr = 'PRR:' + str(round((len(PacketList[f]) / PACKETS), 3) * 100)[:4] + '%'
    eAx.scatter(SequenceList[f], PacketList[f], s=SCATTER, label='from transmitter')
    eAx.plot([np.mean(PacketList[f]) for _ in range(PACKETS)], label='rssi mean', linewidth=L_WIDTH)
    eAx.set_xlim(0, PACKETS)
    eAx.set_ylim(MIN_RSSI, MAX_RSSI)
    eAx.set_title(title)
    eAx.set_xlabel('Sequence number')
    if f == 0:
        eAx.set_ylabel('RSSI (dBm)')
    eAx.text(0.3, 0.95, prr, transform=eAx.transAxes, fontsize=8, verticalalignment='center', bbox=props)

    fAxes[f].hist(SequenceList[f], BINS, label='count', alpha=0.7, rwidth=0.9)
    if f == 0:
        fAxes[f].set_ylabel("Count")
    fAxes[f].set_xlabel("Sequence Range")
    fAxes[f].grid(True, axis='y', alpha=0.35)

    eAx.grid(True, axis='y', alpha=0.35)
    print("Done:", f)

plt.savefig('results.png', dpi=300)

NOTES = input("Notes: ")
Notes_File = open("Notes.txt", 'a')
Notes_File.write(NOTES)
Notes_File.close()

plt.show()
