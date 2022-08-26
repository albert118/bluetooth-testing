import asyncio
from datetime import datetime
from typing import Any, Callable

from aioconsole import ainput
from bleak import BleakClient, discover

#############
# Constants
#############


address = "AC:13:3F:5A:6A:50" # A demo address to connect to
read_characteristic = "0000fff1-0000-1000-8000-00805f9b34fb"
write_characteristic = "0000fff2-0000-1000-8000-00805f9b34fb"

class Connection:
    client: BleakClient = None

    def __init__(self, loop: asyncio.AbstractEventLoop, read_characteristic: str, write_characteristic: str, data_dump_handler: Callable[[str, Any], None], data_dump_size: int = 256):
        self.loop = loop
        self.read_characteristic = read_characteristic
        self.write_characteristic = write_characteristic
        self.data_dump_handler = data_dump_handler

        self.last_packet_time = datetime.now()
        self.dump_size = data_dump_size
        self.connected = False
        self.connected_device = None

        self.rx_data = []
        self.rx_timestamps = []
        self.rx_delays = []

    def on_disconnect(self):
        self.connected = False
        print(f"Disconnected from {self.connected_device.name}")

    async def cleanup(self):
        if self.client:
            await self.client.stop_notify(read_characteristic)
            await self.client.disconnect()

    async def manager(self):
        print("Starting connection manager")
        while True:
            if self.client:
                await self.connect()
            else:
                await self.select_device()
                await asyncio.sleep(15.0, loop=self.loop)

    async def connect(self):
        if self.connected:
            return
        try:
            await self.client.connect()
            self.connected = await self.client.is_connected()
            if self.connected:
                print(F"Connected to {self.connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.read_characteristic, 
                    self.notification_handler
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(3.0, loop=self.loop)
            else:
                print(f"Failed to connect to {self.connected_device.name}")
        except Exception as e:
            print(e)

    async def select_device(self):
        print("Bluetooh LE hardware warming up...")
        # Wait for BLE to initialize.
        await asyncio.sleep(2.0, loop=self.loop)
        devices = await discover()

        print("Please select device: ")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name}")

        response = -1
        while True:
            response = await ainput("Select device: ")
            try:
                response = int(response.strip())
            except:
                print("Please make valid selection.")

            if response > -1 and response < len(devices):
                break
            else:
                print("Please make valid selection.")

        print(f"Connecting to {devices[response].name}")
        self.connected_device = devices[response]
        self.client = BleakClient(devices[response].address, loop=self.loop)

    def record_time_info(self):
        present_time = datetime.now()
        self.rx_timestamps.append(present_time)
        self.rx_delays.append(
            (present_time - self.last_packet_time).microseconds)
        self.last_packet_time = present_time

    def notification_handler(self, data: Any):
        self.rx_data.append(int.from_bytes(data, byteorder="big"))
        self.record_time_info()

        if len(self.rx_data) >= self.dump_size:
            self.data_dump_handler(
                self.rx_data,
                self.rx_timestamps,
                self.rx_delays
            )
            self._clear_lists()

    def _clear_lists(self):
        self.rx_data.clear()
        self.rx_delays.clear()
        self.rx_timestamps.clear()
