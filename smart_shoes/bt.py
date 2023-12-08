import serial
import json
import csv

ser = serial.Serial('COM10', 9600)  # Replace 'COM10' with your COM port

csv_file = 'sensor_data.csv'  # Your CSV file name
csv_header = ['Sensor_Labels', 'Sensor_Values']  # Adjust as needed

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

            # Write the data to the CSV file
            writer.writerow([sensor_labels, sensor_values])

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
