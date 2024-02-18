import serial.tools.list_ports

def scan_serial_ports():
    ports = list(serial.tools.list_ports.comports())

    if not ports:
        print("No serial ports found.")
    else:
        print("Available serial ports:")
        for port, desc, hwid in ports:
            print(f"Port: {port}, Description: {desc}, Hardware ID: {hwid}")

def decode_mac_address(mac_address):
    # Implement your MAC address decoding logic here
    # Example: Splitting MAC address into pairs
    return ':'.join([mac_address[i:i+2] for i in range(0, 12, 2)])

if __name__ == "__main__":
    scan_serial_ports()

   
