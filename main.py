import argparse
import socket
from f1_2020_telemetry.packets import unpack_udp_packet

parser = argparse.ArgumentParser(prog="F1-2020-Telemetry udp reciever", description="Collects telemetry data from F1 2020 udp server")
parser.add_argument("-i", "--ip", help="IP where F1-2020 runs", required=True)
parser.add_argument("-p", "--port", help="Port of the udp server. Default: 20777", type=int, default=20777)

args = parser.parse_args()
def main():

    print("Starting udp listener on port 20777")
    udp_s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_s.bind((args.ip, args.port))
    print("Started udp listener on port 20777")

    while True:
        udp_p = udp_s.recv(2048)
        packet = unpack_udp_packet(udp_p)
        print("Recieved: ", packet)
        print()

if __name__ == '__main__':
    main()