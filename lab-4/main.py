import socket
import struct
import sys
import time


def get_data(sock):
    data = ''
    try:
        data = sock.recvfrom(65565)
    except:
        print "An error happened: "
        sys.exc_info()
    return data[0]


def get_type_of_service(data):
    precedence = {0: "Routine", 1: "Priority", 2: "Immediate", 3: "Flash", 4: "Flash override", 5: "CRITIC/ECP",
                  6: "Internetwork control", 7: "Network control"}
    delay = {0: "Normal delay", 1: "Low delay"}
    throughput = {0: "Normal throughput", 1: "High throughput"}
    reliability = {0: "Normal reliability", 1: "High reliability"}
    cost = {0: "Normal monetary cost", 1: "Minimize monetary cost"}

    # get the 3rd bit and shift right
    D = data & 0x10
    D >>= 4
    # get the 4th bit and shift right
    T = data & 0x8
    T >>= 3
    # get the 5th bit and shift right
    R = data & 0x4
    R >>= 2
    # get the 6th bit and shift right
    M = data & 0x2
    M >>= 1
    # the 7th bit is empty and shouldn't be analyzed
    tabs = '\n\t\t\t'
    TOS = precedence[data >> 5] + tabs + delay[D] + tabs + throughput[T] + tabs + reliability[R] + tabs + cost[M]
    return TOS


def get_flags(data):
    flag_r = {0: "0 - Reserved bit"}
    flag_df = {0: "0 - Fragment if necessary", 1: "1 - Do not fragment"}
    flag_mf = {0: "0 - Last fragment", 1: "1 - More fragments"}

    # get the 1st bit and shift right
    R = data & 0x8000
    R >>= 15
    # get the 2nd bit and shift right
    DF = data & 0x4000
    DF >>= 14
    # get the 3rd bit and shift right
    MF = data & 0x2000
    MF >>= 13

    tabs = '\n\t'
    flags = flag_r[R] + tabs + flag_df[DF] + tabs + flag_mf[MF]
    return flags

# create a AF_PACKET type raw socket
# define ETH_P_ALL    0x0003
# IPPROTO_TCP for ip
try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    print 'aaa'
except socket.error, message:
    print 'ERROR! Something happened. Error code: ' + str(message)
    sys.exit()

# get every packet
while True:
    # get IP header
    data = get_data(s)

    eth_header_length = 14

    eth_header = data[:eth_header_length]
    unpacked_eth = struct.unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(unpacked_eth[2])

    # Get only IP packets, protocol number 8
    if eth_protocol == 8:
        # unpack first 20 bytes from IP header
        # B - unsigned char (1)
        # H - unsigned short (2)
        # s - string
        ip_header = data[eth_header_length : 20 + eth_header_length]

        unpacked_data = struct.unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = unpacked_data[0]
        version = version_ihl >> 4                   # version of the IP
        ihl = version_ihl & 0xF                      # internet header length
        tos = get_type_of_service(unpacked_data[1])  # type of service
        total_length = unpacked_data[2]
        id = unpacked_data[3]                        # packet ID
        flags = get_flags(unpacked_data[4])          # packet flags
        fragment_offset = unpacked_data[4] & 0x1FFF
        ttl = unpacked_data[5]                       # time to live
        protocol_number = unpacked_data[6]
        checksum = unpacked_data[7]
        src_addr = socket.inet_ntoa(unpacked_data[8])       # source address
        dst_addr = socket.inet_ntoa(unpacked_data[9])       # destination address
        payload = data[20 + eth_header_length :]

        print "-------------------IP Packet-------------------"
        print "An IP packet with the size %i was captured." % (unpacked_data[2])
        print "Raw data: \n" + data
        print "\nParsed data: "
        print "Version: " + str(version)
        print "Header Length: " + str(ihl * 4) + " bytes"
        print "Type of Service: " + str(tos)
        print "Total Length: " + str(total_length)
        print "ID: " + str(id)
        print "Flags: " + str(flags)
        print "Fragment Offset: " + str(fragment_offset)
        print "TTL: " + str(ttl)
        print "Protocol: " + str(protocol_number)
        print "Checksum: " + str(checksum)
        print "Src: " + str(src_addr)
        print "Dst: " + str(dst_addr)
        print "Payload: \n\t{\n\t\t" + str(data[20 + eth_header_length:]) + "\n\t}"

        ip_header_length = ihl * 4    # IP header length

        # check if packet is UDP
        if protocol_number == 17:
            print "-------------------UDP Datagram-------------------"
            u = ip_header_length + eth_header_length
            udp_header_length = 8
            udp_header = data[u : u + 8]

            unpacked_udph = struct.unpack('!HHHH', udp_header)

            print "Raw Datagram:    " + str(unpacked_udph)
            src_port = unpacked_udph[0]
            dst_port = unpacked_udph[1]
            length = unpacked_udph[2]
            checksum = unpacked_udph[3]

            header_size = eth_header_length + ip_header_length + udp_header_length
            data_size = len(data) - header_size

            udp_data = data[header_size:]
            print "Src Port: " + str(src_addr)
            print "Dst Port: " + str(dst_port)
            print "Length: " + str(length)
            print "Checksum: " + str(checksum)
            print "Data: \n{\n" + str(udp_data) + "\n}"
        time.sleep(2)