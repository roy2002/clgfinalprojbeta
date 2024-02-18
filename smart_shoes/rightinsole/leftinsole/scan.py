import bluetooth
import serial

def connect_and_receive_message(mac_address):
    # Bluetooth serial port profile (SPP) service UUID
    service_uuid = "00001101-0000-1000-8000-00805f9b34fb"

    # Connect to the Bluetooth device using RFCOMM
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((mac_address, 1))

    print(f"Connected to device with MAC address {mac_address}")

    # Open a serial connection to the Bluetooth device
    ser = serial.Serial(sock.fileno(), timeout=1)

    # Receive a message from the device
    received_message = ser.readline().decode('utf-8').strip()

    print(f"Received message: {received_message}")

    # Close the connections
    ser.close()
    sock.close()

if __name__ == "__main__":
    device_mac = "D8:BC:38:E5:9B:16"  # Replace with the MAC address of your Bluetooth device
    connect_and_receive_message(device_mac)
