import asyncio
from pprint import pformat

from bleak import BleakScanner


class BleDeviceInfo(object):
    def __init__(self, dev):
        self.name = dev.name
        self.rssi = dev.rssi
        self.address = dev.address

    def __repr__(self): return pformat(vars(self), indent=4)

async def main():
    while(True):
        # scan a list of devices
        devices = await BleakScanner.discover()
        # Inspect the devices on the console
        [print(BleDeviceInfo(d)) for d in devices] 

# Trigger the event loop 
asyncio.run(main())
