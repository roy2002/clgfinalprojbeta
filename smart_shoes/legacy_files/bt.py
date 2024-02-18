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
        return list(sensor_data.keys()), list(sensor_data.values())
    except json.JSONDecodeError as e:
        st.write(f"Error decoding JSON ({sensor_name}): {e}")
        return None, None

def scan_com_ports():
    return [port.device for port in list_ports.comports()]

def save_csv(df, csv_file, folder):
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, csv_file)
    df.to_csv(full_path, index=False)
    return full_path

def display_latest_data(col, df, sensor_name):
    col.table(df.tail(1)[df.columns.intersection(['Timestamp', f'{sensor_name}_Labels', f'{sensor_name}_Values'])])

# Streamlit App
st.title("Sensor Data Visualization")

selected_tab1 = st.sidebar.selectbox("Select COM Port 1", scan_com_ports(), key="com_port_1")
selected_tab2 = st.sidebar.selectbox("Select COM Port 2", scan_com_ports(), key="com_port_2")

sensor_name1 = st.text_input("Enter Sensor Name 1:")
sensor_name2 = st.text_input("Enter Sensor Name 2:")

record_time_minutes = st.slider("Select Recording Time (minutes):", min_value=1, max_value=300, value=60)

csv_folder = st.text_input("Enter Folder Name:", value='output')

ser1, ser2 = serial.Serial(selected_tab1, 115200), serial.Serial(selected_tab2, 115200)

csv_header = ['Timestamp', f'{sensor_name1}_Labels', f'{sensor_name1}_Values', f'{sensor_name2}_Labels', f'{sensor_name2}_Values']
df1, df2 = pd.DataFrame(columns=csv_header), pd.DataFrame(columns=csv_header)

col1, col2 = st.columns(2)

message_box1 = col1.empty()
message_box2 = col2.empty()

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= record_time_minutes * 60:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    sensor_labels1, sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_labels1 and sensor_values1:
        new_data = {'Timestamp': timestamp, f'{sensor_name1}_Labels': sensor_labels1, f'{sensor_name1}_Values': sensor_values1}
        df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)
        display_latest_data(message_box1, df1, sensor_name1)

    sensor_labels2, sensor_values2 = read_serial_data(ser2, sensor_name2)
    if sensor_labels2 and sensor_values2:
        new_data = {'Timestamp': timestamp, f'{sensor_name2}_Labels': sensor_labels2, f'{sensor_name2}_Values': sensor_values2}
        df2 = pd.concat([df2, pd.DataFrame([new_data])], ignore_index=True)
        display_latest_data(message_box2, df2, sensor_name2)

st.write("Recording complete.")

ser1.close()
ser2.close()

df1.to_csv(f'{sensor_name1}.csv', index=False, header=False)
df2.to_csv(f'{sensor_name2}.csv', index=False, header=False)

combined_csv_name = st.text_input("Enter Combined CSV Name:")
combined_csv_path = save_csv(pd.concat([df1, df2], ignore_index=True), f'{combined_csv_name}.csv', csv_folder)

st.write(f"Data saved to {combined_csv_path}")
st.write("View Combined CSV:")
st.write(pd.read_csv(combined_csv_path))
