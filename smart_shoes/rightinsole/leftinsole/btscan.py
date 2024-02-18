import serial.tools.list_ports
import json
import serial
import csv
from datetime import datetime

target_mac_address = 'BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0002\7&304319E3&0&D8BC38E59B16_C00000000'

csv_file = 'sensor_data.csv'  # Your CSV file name
csv_header = ['Timestamp', 'Sensor_Labels1', 'Sensor_Values1', 'Sensor_Labels2', 'Sensor_Values2']  # Updated header

# Find available COM ports
ports = list(serial.tools.list_ports.comports())

# Try to find the port that corresponds to the target MAC address
target_port = None
for port, desc, hwid in ports:
    if target_mac_address in hwid:
        target_port = port
        break

if target_port is None:
    print(f"Device with MAC address {target_mac_address} not found.")
else:
    print(f"Connecting to device with MAC address {target_mac_address} on port {target_port}")

    ser = serial.Serial(target_port, 115200)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

        while True:
            try:
                # Read data from the serial input
                data = ser.readline().decode().strip()
                sensor_data = json.loads(data)

                # Extract sensor labels and values separately
                sensor_labels = list(sensor_data.keys())
                sensor_values = list(sensor_data.values())

                for i in range(0, len(sensor_values)):
                    sensor_values[i] = sensor_values[i] * 0.00244

                # Get the current timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format as YYYY-MM-DD HH:MM:SS.mmm

                # Write the data to the CSV file
                writer.writerow([timestamp, sensor_labels, sensor_values])

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
