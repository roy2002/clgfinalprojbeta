import bluetooth
import serial.tools.list_ports

def find_device_port_by_name(device_name):
    nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)

    for addr, name, _ in nearby_devices:
        if device_name.lower() in name.lower():
            print(f"Found device '{name}' with MAC address {addr}")
            port = find_device_port_by_address(addr)
            if port:
                print(f"Device '{name}' is connected to COM port {port}")
            else:
                print(f"Device '{name}' is not connected to any COM port")

def find_device_port_by_address(device_address):
    ports = list(serial.tools.list_ports.comports())

    for port, _, hwid in ports:
        if device_address in hwid:
            return port

    return None

if __name__ == "__main__":
    device_name = "LeftFootinsole"  # Replace with the name of your Bluetooth device
    find_device_port_by_name(device_name)
