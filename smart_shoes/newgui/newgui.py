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
csv_header = ['Timestamp', f'{sensor_name1}_Values', f'{sensor_name2}_Values']
df1, df2 = pd.DataFrame(columns=csv_header), pd.DataFrame(columns=csv_header)

# Arrange components in three columns
col1, col2, col3 = st.columns(3)

# Display real-time sensor data
message_box1 = col1.empty()
message_box2 = col2.empty()

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= record_time_minutes * 60:
    # Read data from the first serial input
    sensor_labels1, sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_labels1 and sensor_values1:
        timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        new_data = {
            'Timestamp': timestamp1,
            f'{sensor_name1}_Values': sensor_values1
        }
        df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)

        # Display the latest data in the app
        message_box1.table(df1.tail(1)[df1.columns.intersection([f'Timestamp', f'{sensor_name1}_Values'])])

    # Read data from the second serial input
    sensor_labels2, sensor_values2 = read_serial_data(ser2, sensor_name2)
    if sensor_labels2 and sensor_values2:
        timestamp2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        new_data = {
            'Timestamp': timestamp2,
            f'{sensor_name2}_Values': sensor_values2
        }
        df2 = pd.concat([df2, pd.DataFrame([new_data])], ignore_index=True)

        # Display the latest data in the app
        message_box2.table(df2.tail(1)[df2.columns.intersection([f'Timestamp', f'{sensor_name2}_Values'])])

# Delete button for Sensor 1 data
delete_csv1 = col3.button(f"Delete {sensor_name1}'s CSV")
if delete_csv1:
    os.remove(csv_file1)
    st.write(f"{csv_file1} deleted.")

# Delete button for Sensor 2 data
delete_csv2 = col3.button(f"Delete {sensor_name2}'s CSV")
if delete_csv2:
    os.remove(csv_file2)
    st.write(f"{csv_file2} deleted.")

st.write("Recording complete.")

# Close serial ports
ser1.close()
ser2.close()

# Save the collected data to CSV files
df1.to_csv(csv_file1, index=False)
df2.to_csv(csv_file2, index=False)
st.write(f"Data saved to {csv_file1}")
st.write(f"Data saved to {csv_file2}")

# Merge the two DataFrames
merged_df = pd.merge(df1, df2, on='Timestamp', how='outer')

# Save the merged data to a CSV file
merged_csv_file = f'merged_sensor_data.csv'
merged_df.to_csv(merged_csv_file, index=False)
st.write(f"Merged data saved to {merged_csv_file}")
