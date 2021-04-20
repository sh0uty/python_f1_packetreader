import argparse
import socket
from f1_2020_telemetry.packets import unpack_udp_packet
import sys, os
import packetreader

parser = argparse.ArgumentParser(prog="F1-2020-Telemetry udp reciever", description="Collects telemetry data from F1 2020 udp server")
parser.add_argument("-i", "--ip", help="IP where F1-2020 runs", required=True)
parser.add_argument("-p", "--port", help="Port of the udp server. Default: 20777", type=int, default=20777)

args = parser.parse_args()
def main():
    pr = packetreader.PacketReader(args.ip, args.port)
    pr.run()

    print("Done")

if __name__ == '__main__':
    main()