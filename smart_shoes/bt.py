# import serial
# import json
# import csv
# from datetime import datetime
#
# ser = serial.Serial('COM8', 115200)  # Replace 'COM10' with your COM port
#
# csv_file = 'sensor_data.csv'  # Your CSV file name
# csv_header = ['Timestamp', 'Sensor_Labels', 'Sensor_Values']  # Updated header
#
# with open(csv_file, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(csv_header)
#
#     while True:
#         try:
#             data = ser.readline().decode().strip()
#             sensor_data = json.loads(data)  # Decode JSON data
#
#             # Extract sensor labels and values separately
#             sensor_labels = list(sensor_data.keys())
#             sensor_values = list(sensor_data.values())
#
#             for i in range(0, len(sensor_values)):
#                 sensor_values[i] = sensor_values[i] * 0.00244
#             print(sensor_values)
#
#             # Get the current timestamp
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format as YYYY-MM-DD HH:MM:SS.mmm
#             print(str(timestamp))
#             # Write the data to the CSV file
#             writer.writerow([timestamp, sensor_labels, sensor_values])
#
#         except json.JSONDecodeError as e:
#             print("Error decoding JSON:", e)

import serial
import json
import csv
from datetime import datetime

# Replace 'COM8' and 'COM12' with your respective COM ports
ser1 = serial.Serial('COM8', 115200)
ser2 = serial.Serial('COM12', 115200)

csv_file = 'sensor_data.csv'  # Your CSV file name
csv_header = ['Timestamp', 'Sensor_Labels1', 'Sensor_Values1', 'Sensor_Labels2', 'Sensor_Values2']  # Updated header

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    while True:
        try:
            # Read data from the first serial input
            data1 = ser1.readline().decode().strip()
            sensor_data1 = json.loads(data1)

            # Extract sensor labels and values separately
            sensor_labels1 = list(sensor_data1.keys())
            sensor_values1 = list(sensor_data1.values())

            for i in range(0, len(sensor_values1)):
                sensor_values1[i] = sensor_values1[i] * 0.00244

            # Read data from the second serial input
            data2 = ser2.readline().decode().strip()
            sensor_data2 = json.loads(data2)

            # Extract sensor labels and values separately
            sensor_labels2 = list(sensor_data2.keys())
            sensor_values2 = list(sensor_data2.values())

            for i in range(0, len(sensor_values2)):
                sensor_values2[i] = sensor_values2[i] * 0.00244

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format as YYYY-MM-DD HH:MM:SS.mmm

            # Write the data to the CSV file
            writer.writerow([timestamp, sensor_labels1, sensor_values1, sensor_labels2, sensor_values2])

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
