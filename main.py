import argparse
import packetreader
import logging
from threading import Thread


parser = argparse.ArgumentParser(prog="F1-2020-Telemetry udp reciever", description="Collects telemetry data from F1 2020 udp server")
parser.add_argument("-i", "--ip", help="IP where F1-2020 runs", required=True)
parser.add_argument("-p", "--port", help="Port of the udp server. Default: 20777", type=int, default=20777)

args = parser.parse_args()
def main():
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)

    pr = packetreader.PacketReader(args.ip, args.port)
    prthread = Thread(target=pr.run)

    prthread.start()

    logging.info("Packetreader thread started")
    logging.info("Joining thread now")
    
    prthread.join()

    logging.info("Both threads closed. Quitting now")

if __name__ == '__main__':
    main()