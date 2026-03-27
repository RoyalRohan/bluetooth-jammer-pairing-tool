# Bluetooth Jammer and Pairing Tool

A Python-based tool for jamming Bluetooth devices and pairing with target devices.

## Overview
This tool allows security researchers and developers to:
- Jam Bluetooth traffic from specified devices
- Pair with target devices programmatically
- Craft custom Bluetooth packets for testing
- Log jamming/pairing events for analysis

## Features
- Multi-target device support
- Custom packet crafting capabilities
- Detailed logging functionality
- Error handling and graceful failure recovery
- Cross-platform compatibility

## Requirements
- Python 3.7+
- Scapy library
- Linux kernel with Bluetooth support (tested on Ubuntu 20.04+)
- Bluetooth adapter with HCI monitor support

## Installation
```bash
git clone https://github.com/RoyalRohan/bluetooth-jammer-pairing-tool.git
cd bluetooth-jammer-pairing-tool
pip install -r requirements.txt
```
### Quick Start

# Basic jamming
```bash
python bluetooth_jammer.py -t "00:11:22:33:44:55"
```
# Advanced jamming with pairing
```bash
python bluetooth_jammer.py -t "00:11:22:33:44:55,AA:BB:CC:DD:EE:FF" --pair
```

# Custom packet crafting
```bash
python bluetooth_jammer.py -t "00:11:22:33:44:55" --custom-packets
Options
```
-t, --targets: Comma-separated MAC addresses (required)
--pair: Enable pairing with target devices
--custom-packets: Enable custom packet crafting
--log-level: Logging verbosity (debug/info/warn/error)
--config-file: Load configuration from file
Logging
All activities are logged to bluetooth_jammer.log with timestamp and metadata.
