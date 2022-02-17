import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = (20, 8)

PACKETS = 500
MIN_RSSI = -100
MAX_RSSI = -10
BINS = [i * (PACKETS / 10) for i in range(11)]

SCATTER = 5

props = dict(boxstyle='round', facecolor='#cccccc', alpha=0.5)

PhantomNode1 = '5a7a.b713.0074.1200'


def extract_packet_data(filename):
    """
    This method will take a file of packet readings as input and go through each line.
    If any line has the IP address defined above, it will fill in the points array with
    the corresponding RSSI value and another array with sequence number

    There will be four arrays returned at last, two with RSSI readings and two with seq.

    [INFO: EavesDr   ] Received 0 from 0f2a.7d13.0074.1200 [RSSI: -60 | LQI: 107]
    """
    file_node_lines = filename.readlines()
    node_points_h1 = []
    node_seq_h1 = []

    for line in file_node_lines:
        if PhantomNode1 in line:
            try:
                line_as_list = line.split(' ')
                rssi = int(line_as_list[-4])
                seq = int(line_as_list[-8])
                node_points_h1.append(rssi)
                node_seq_h1.append(seq)
            except:
                continue
    print("Parsing files ...")
    return node_points_h1, node_seq_h1


#######################################################################################################################
# Files                                                                                                               #
#######################################################################################################################
Ev1 = open('Eaves-1.txt', 'r')
Ev2 = open('Eaves-2.txt', 'r')
Ev3 = open('Eaves-3.txt', 'r')
Ev4 = open('Eaves-4.txt', 'r')
Ph2 = open('Receive.txt', 'r')

#######################################################################################################################
# Raw Data                                                                                                            #
#######################################################################################################################
(P1_E1, S_P1_E1) = extract_packet_data(Ev1)
(P1_E2, S_P1_E2) = extract_packet_data(Ev2)
(P1_E3, S_P1_E3) = extract_packet_data(Ev3)
(P1_E4, S_P1_E4) = extract_packet_data(Ev4)
(P1_P2, S_P1_P2) = extract_packet_data(Ph2)

#######################################################################################################################
# Plots                                                                                                               #
#######################################################################################################################
f, ((ev1, ev2, ev3, ev4, pha), (fr1, fr2, fr3, fr4, fde)) = plt.subplots(2, 5, sharey=False)

f.suptitle('RSSI Measurements', fontweight='bold')

prr = 'PRR:' + str(round((len(P1_E1) / PACKETS), 3) * 100)[:4] + '%'
ev1.scatter(S_P1_E1, P1_E1, s=SCATTER, label='from node 1')
ev1.plot([np.mean(P1_E1) for _ in range(PACKETS)], label='node 1 mean')
ev1.set_xlim(0, PACKETS)
ev1.set_ylim(MIN_RSSI, MAX_RSSI)
ev1.set_title('Eaves 01')
ev1.set_xlabel('Sequence number')
ev1.set_ylabel('RSSI (dBm)')
ev1.text(0.3, 0.95, prr, transform=ev1.transAxes, fontsize=8,
         verticalalignment='center', bbox=props)
print("EV 1 Ready")

prr = 'PRR:' + str(round((len(P1_E2) / PACKETS), 3) * 100)[:4] + '%'
ev2.scatter(S_P1_E2, P1_E2, s=SCATTER, label='from node 1')
ev2.plot([np.mean(P1_E2) for _ in range(PACKETS)], label='node 1 mean')
ev2.set_xlim(0, PACKETS)
ev2.set_ylim(MIN_RSSI, MAX_RSSI)
ev2.set_title('Eaves 02')
ev2.set_xlabel('Sequence number')
ev2.text(0.4, 0.95, prr, transform=ev2.transAxes, fontsize=8,
         verticalalignment='center', bbox=props)
print("EV 2 Ready")

prr = 'PRR:' + str(round((len(P1_E3) / PACKETS), 3) * 100)[:4] + '%'
ev3.scatter(S_P1_E3, P1_E3, s=SCATTER, label='from node 1')
ev3.plot([np.mean(P1_E3) for _ in range(PACKETS)], label='node 1 mean')
ev3.set_xlim(0, PACKETS)
ev3.set_ylim(MIN_RSSI, MAX_RSSI)
ev3.set_title('Eaves 03')
ev3.set_xlabel('Sequence number')
ev3.text(0.4, 0.95, prr, transform=ev3.transAxes, fontsize=8,
         verticalalignment='center', bbox=props)
print("EV 3 Ready")

prr = 'PRR:' + str(round((len(P1_E4) / PACKETS), 3) * 100)[:4] + '%'
ev4.scatter(S_P1_E4, P1_E4, s=SCATTER, label='from node 1')
ev4.plot([np.mean(P1_E4) for _ in range(PACKETS)], label='node 1 mean')
ev4.set_xlim(0, PACKETS)
ev4.set_ylim(MIN_RSSI, MAX_RSSI)
ev4.set_title('Eaves 04')
ev4.set_xlabel('Sequence number')
ev4.text(0.4, 0.95, prr, transform=ev4.transAxes, fontsize=8,
         verticalalignment='center', bbox=props)
print("EV 4 Ready")

prr = 'PRR:' + str(round((len(P1_P2) / PACKETS), 3) * 100)[:4] + '%'
pha.scatter(S_P1_P2, P1_P2, s=SCATTER, label='from node 1')
pha.plot([np.mean(P1_P2) for _ in range(PACKETS)], label='node 1 mean')
pha.set_xlim(0, PACKETS)
pha.set_ylim(MIN_RSSI, MAX_RSSI)
pha.set_title('In-body')
pha.set_xlabel('Sequence number')
pha.text(0.4, 0.95, prr, transform=pha.transAxes, fontsize=8,
         verticalalignment='center', bbox=props)
print("Phantom Ready")

#######################################################################################################################
# Fast RSSI Sampling                                                                                                  #
#######################################################################################################################
fr1.hist(S_P1_E1, BINS, label='count', alpha=0.7, rwidth=0.9)
fr1.set_xlabel('Sequence Range')
fr1.set_ylabel('Count')
fr2.hist(S_P1_E2, BINS, label='count', alpha=0.7, rwidth=0.9)
fr2.set_xlabel('Reading instance')
fr3.hist(S_P1_E3, BINS, label='count', alpha=0.7, rwidth=0.9)
fr3.set_xlabel('Reading instance')
fr4.hist(S_P1_E4, BINS, label='count', alpha=0.7, rwidth=0.9)
fr4.set_xlabel('Reading instance')

ev1.grid(True, axis='y', alpha=0.35)
ev2.grid(True, axis='y', alpha=0.35)
ev3.grid(True, axis='y', alpha=0.35)
ev4.grid(True, axis='y', alpha=0.35)
pha.grid(True, axis='y', alpha=0.35)

fr1.grid(True, axis='y', alpha=0.35)
fr2.grid(True, axis='y', alpha=0.35)
fr3.grid(True, axis='y', alpha=0.35)
fr4.grid(True, axis='y', alpha=0.35)

# The legend is kept outside as all the graphs in each row share the same wording
handles_e, labels_e = ev1.get_legend_handles_labels()
handles_f, labels_f = fr1.get_legend_handles_labels()
f.legend(handles_e + handles_f, labels_e + labels_f, loc='lower right', bbox_to_anchor=(0.88, 0.2))
f.delaxes(fde)

plt.savefig('results.png', dpi=300)

plt.show()
