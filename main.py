import argparse
import socket
import keyboard
from f1_2020_telemetry.packets import unpack_udp_packet

def main():

    print("Starting UPD listener on Port 20777")
    udp_s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_s.bind(('0.0.0.0', 20777))
    print("Started UDP listener on Port 20777")

    while True:
        print("Inside Loop") 
        udp_p = udp_s.recv(2048)
        print("Recieved Data from F1-2020")
        packet = unpack_udp_packet(udp_p)
        print("Recieved: ", packet)
        print()
        

if __name__ == '__main__':
    main()