import socket
import sys
import keyboard
import logging
import selectors
from f1_2020_telemetry.packets import unpack_udp_packet, PacketID

class PacketReader():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.frame = None
        self.frame_data = {}
        self.socketpair = socket.socketpair()
        self.endSignalFlag = False

    def run(self):
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))

        logging.info(f"Packetreader started on port {self.port}")

        selects = selectors.DefaultSelector()
        key_sock = selects.register(sock, selectors.EVENT_READ)
        key_socketpair = selects.register(self.socketpair[0], selectors.EVENT_READ)

        logging.info(f"Initialized selectors and keys. Going into main loop now")

        end = False
        while not end:
            for (key, mask) in selects.select():
                if key == key_sock:
                    packed_packet = sock.recv(2048)
                    packet = unpack_udp_packet(packed_packet)
                    self.GetDataFromPacket(packet)
                elif key == key_socketpair:
                    end = True

        logging.info("Packetreader main loop exit")

        self.CreateDataForDisplay()

        selects.close()
        sock.close()
        for s in self.socketpair:
            s.close()

        logging.info("Closed every connction")

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
                self.speed = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].speed )
                self.gear = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].gear )
                self.engineRPM = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].engineRPM )
                self.throttle = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].throttle )
                self.brake = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].brake )
                self.drs = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].drs )
                self.tyresInnerTemperature = \
                    ( self.frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].tyresInnerTemperature )

            if PacketID.CAR_STATUS in self.frame_data:
                self.fuelRemainingLaps = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].fuelRemainingLaps )
                self.ersStoreEnergy = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersStoreEnergy )
                self.ersDeployMode = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersDeployMode )
                self.ersDeployedThisLap = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersDeployedThisLap )
                self.ersHarvestedThisLapMGUK = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersHarvestedThisLapMGUK )
                self.ersHarvestedThisLapMGUH = \
                    ( self.frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersHarvestedThisLapMGUH )

            if PacketID.LAP_DATA in self.frame_data:
                self.lastLapTime = \
                    ( self.frame_data[PacketID.LAP_DATA].lapData[player_car].lastLapTime )
                self.currentLapTime = \
                    ( self.frame_data[PacketID.LAP_DATA].lapData[player_car].currentLapTime )
                self.bestLapTime = \
                    ( self.frame_data[PacketID.LAP_DATA].lapData[player_car].bestLapTime )
                self.carPosition = \
                    ( self.frame_data[PacketID.LAP_DATA].lapData[player_car].carPosition )
                self.currentLapNum = \
                    ( self.frame_data[PacketID.LAP_DATA].lapData[player_car].currentLapNum )

        except KeyError:
            logging.warning("Package could not be read correctly. Skipping!")

        #until here

        print(f"Speed: {self.speed}, Gear: {self.gear}, RPM: {self.engineRPM}, Throttle: {self.throttle}, Brake: {self.brake}, DRS: {self.drs}, TyresInnterTemperature: {list(self.tyresInnerTemperature)}")
        #print(f"FuelRemainingLaps: {self.fuelRemainingLaps}, ErsStoreEnergy {self.ersStoreEnergy}, ErsDeployMode {self.ersDeployMode}, ErsDeployedThisLap {self.ersDeployedThisLap}. ErsHarvestedThisLapMGUK {self.ersHarvestedThisLapMGUK}, ErsHarvestedThisLapMGUH {self.ersHarvestedThisLapMGUH}")

    def endSignal(self):
        while True:
            if (keyboard.is_pressed('q')):
                logging.info("Q-key pressed. Attempting to quit now")
                self.socketpair[1].send(b'\x00')
                break;