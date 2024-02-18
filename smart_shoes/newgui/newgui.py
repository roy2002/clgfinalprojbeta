import streamlit as st
import serial
from serial.tools import list_ports
import json
from datetime import datetime
import pandas as pd
import time
import os

def read_serial_data(ser, sensor_name):
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)
        sensor_labels = list(sensor_data.keys())
        sensor_values = [value for value in sensor_data.values()]
        return sensor_labels, sensor_values
    except json.JSONDecodeError as e:
        st.write(f"Error decoding JSON ({sensor_name}): {e}")
        return None, None

def scan_com_ports():
    com_ports = [port.device for port in list_ports.comports()]
    return com_ports

# Streamlit App
st.title("Sensor Data Visualization")

# Tabs for COM Port Selection
selected_tab1 = st.sidebar.selectbox("Select COM Port 1", scan_com_ports(), key="com_port_1")
selected_tab2 = st.sidebar.selectbox("Select COM Port 2", scan_com_ports(), key="com_port_2")

sensor_name1 = st.text_input("Enter Sensor Name 1:")
sensor_name2 = st.text_input("Enter Sensor Name 2:")

# Timer input in minutes
record_time_minutes = st.slider("Select Recording Time (minutes):", min_value=1, max_value=300, value=60)

# Open serial ports
ser1, ser2 = serial.Serial(selected_tab1, 115200), serial.Serial(selected_tab2, 115200)

# Create DataFrames to store sensor data
csv_file1, csv_file2 = f'sensor_data_{sensor_name1}.csv', f'sensor_data_{sensor_name2}.csv'

# Dynamically generate headers based on a common pattern
common_labels = [f'Sensor{i}' for i in range(1, 6)]  # Assuming 5 sensors, adjust the range as needed
csv_header1 = ['Timestamp'] + [f'{sensor_name1}_{label}' for label in common_labels]
csv_header2 = ['Timestamp'] + [f'{sensor_name2}_{label}' for label in common_labels]

df1, df2 = pd.DataFrame(columns=csv_header1), pd.DataFrame(columns=csv_header2)

# Arrange components in three columns
col1, col2, col3 = st.columns(3)

# Display real-time sensor data
message_box1 = col1.empty()
message_box2 = col2.empty()

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= record_time_minutes * 60:
    # Synchronize timestamp for both sensors
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Read data from the first serial input
    sensor_labels1, sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_labels1 and sensor_values1:
        new_data = {
            'Timestamp': timestamp,
            **{f'{sensor_name1}_{label}': value for label, value in zip(common_labels, sensor_values1)}
        }
        df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)

        # Display the latest data in the app
        latest_data1 = df1.tail(1)[df1.columns.intersection(csv_header1)]
        message_box1.write(f"Latest data for {sensor_name1}:")
        message_box1.write(latest_data1)

    # Read data from the second serial input
    sensor_labels2, sensor_values2 = read_serial_data(ser2, sensor_name2)
    if sensor_labels2 and sensor_values2:
        new_data = {
            'Timestamp': timestamp,
            **{f'{sensor_name2}_{label}': value for label, value in zip(common_labels, sensor_values2)}
        }
        df2 = pd.concat([df2, pd.DataFrame([new_data])], ignore_index=True)

        # Display the latest data in the app
        latest_data2 = df2.tail(1)[df2.columns.intersection(csv_header2)]
        message_box2.write(f"Latest data for {sensor_name2}:")
        message_box2.write(latest_data2)

# Delete button for Sensor 1 data
delete_csv1 = col3.button(f"Delete {sensor_name1}'s CSV")
if delete_csv1:
    try:
        os.remove(csv_file1)
        st.success(f"{csv_file1} deleted.")
    except FileNotFoundError:
        st.warning(f"{csv_file1} not found. No file deleted.")

# Delete button for Sensor 2 data
delete_csv2 = col3.button(f"Delete {sensor_name2}'s CSV")
if delete_csv2:
    try:
        os.remove(csv_file2)
        st.success(f"{csv_file2} deleted.")
    except FileNotFoundError:
        st.warning(f"{csv_file2} not found. No file deleted.")

st.write("Recording complete.")

# Close serial ports
ser1.close()
ser2.close()

# Take user input for the merged CSV file name
merged_csv_name = st.text_input("Enter Merged CSV Name:")
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# Save the collected data to CSV files
csv_file1 = os.path.join(output_folder, f'{sensor_name1}.csv')
csv_file2 = os.path.join(output_folder, f'{sensor_name2}.csv')
df1.to_csv(csv_file1, index=False)
df2.to_csv(csv_file2, index=False)
st.write(f"Data saved to {csv_file1}")
st.write(f"Data saved to {csv_file2}")

# Merge the two DataFrames
merged_df = pd.merge(df1, df2, on='Timestamp', how='outer')

# Save the merged data to a CSV file in the 'output' folder
merged_csv_file = os.path.join(output_folder, f'{merged_csv_name}.csv')
merged_df.to_csv(merged_csv_file, index=False)
st.write(f"Merged data saved to {merged_csv_file}")
