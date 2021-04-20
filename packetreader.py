import threading
import socket
from f1_2020_telemetry.packets import unpack_udp_packet, PacketID
import math
class PacketReader():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.frame = None
        self.frame_data = {}

        self.player_car_speed = 0
            
    def run(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))

        print(f"packetreader started on port {self.port}")

        try:
            while True:
                packed_packet = sock.recv(2048)
                packet = unpack_udp_packet(packed_packet)
                self.GetData(packet)
        except KeyboardInterrupt:
            self.CreateDataForDisplay()

            sock.close()
            print("stopped packetreader")

    def GetData(self, packet):

        if packet.header.frameIdentifier != self.frame:
            self.CreateDataForDisplay()
            self.frame = packet.header.frameIdentifier
            self.frame_data = {}
        
        self.frame_data[PacketID(packet.header.packetId)] = packet

    def CreateDataForDisplay(self):
        if not bool(self.frame_data):
            return
        all_packets = next(iter(self.frame_data.values()))

        player_car = all_packets.header.playerCarIndex

        #Get all stuff here with try execpt

        try:
            self.player_car_speed = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].speed )
        except:
            pass

        #until here

        print(self.player_car_speed)