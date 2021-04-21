import socket
import math
import keyboard
from f1_2020_telemetry.packets import unpack_udp_packet, PacketID

class PacketReader():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.frame = None
        self.frame_data = {}

        self.player_car_speed = 0
        self.player_car_engineRPM = 0
        self.player_car_throttle = 0
        self.player_car_brake = 0
        self.player_car_drs = 0
            
    def run(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))

        print(f"packetreader started on port {self.port}")

        try:
            while not (keyboard.is_pressed('q')) :
                packed_packet = sock.recv(2048)
                packet = unpack_udp_packet(packed_packet)
                self.GetDataFromPacket(packet)
        except KeyboardInterrupt:
            self.CreateDataForDisplay()

            sock.close()
            print("stopped packetreader")

    def GetDataFromPacket(self, packet):

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
            if PacketID.CAR_TELEMETRY in self.frame_data:
                self.player_car_speed = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].speed )
                self.player_car_engineRPM = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].engineRPM )
                self.player_car_throttle = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].throttle )
                self.player_car_brake = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].brake )
                self.player_car_drs = ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].drs )
        except KeyError:
            pass

        #until here

        print(f"Speed: {self.player_car_speed}, RPM: {self.player_car_engineRPM}, Throttle: {self.player_car_throttle}, Brake: {self.player_car_brake}, DRS: {self.player_car_drs}")