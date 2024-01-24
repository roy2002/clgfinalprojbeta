import serial
import json
import csv
from datetime import datetime

ser = serial.Serial('COM8', 115200)  # Replace 'COM10' with your COM port

csv_file = 'sensor_data.csv'  # Your CSV file name
csv_header = ['Timestamp', 'Sensor_Labels', 'Sensor_Values']  # Updated header

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    while True:
        try:
            data = ser.readline().decode().strip()
            sensor_data = json.loads(data)  # Decode JSON data

            # Extract sensor labels and values separately
            sensor_labels = list(sensor_data.keys())
            sensor_values = list(sensor_data.values())

            for i in range(0, len(sensor_values)):
                sensor_values[i] = sensor_values[i] * 0.00244
            print(sensor_values)

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format as YYYY-MM-DD HH:MM:SS.mmm
            print(str(timestamp))
            # Write the data to the CSV file
            writer.writerow([timestamp, sensor_labels, sensor_values])

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
