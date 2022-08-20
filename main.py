import asyncio
from pprint import pformat

from bleak import BleakScanner

SCANNING_WINDOW_SEC = 5.0
class BleDeviceInfo(object):
    def __init__(self, dev):
        self.name = dev.name
        self.rssi = dev.rssi
        self.address = dev.address

    def __repr__(self): return pformat(vars(self), indent=4)

async def main():
    seen_devs = dict()

    while(True):
        # scan a list of devices
        async with BleakScanner() as scanner:
            await asyncio.sleep(SCANNING_WINDOW_SEC)

        filterWithNames = filter(lambda dev: dev.name is not None, scanner.discovered_devices)

        for dev in filterWithNames:
            # track the devices we've already seen
            if (dev.name in seen_devs):
                continue
                
            # Inspect the devices on the console
            seen_devs[dev.name] = BleDeviceInfo(dev)
            print(seen_devs[dev.name])

# Trigger the event loop 
asyncio.run(main())
