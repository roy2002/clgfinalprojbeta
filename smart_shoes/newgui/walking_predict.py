import streamlit as st
import serial
from serial.tools import list_ports
import json
from datetime import datetime
import pandas as pd
import time
from sklearn.externals import joblib

# Load the pre-trained walking pattern model
model = joblib.load('walking_pattern_model.pkl')

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
sensor_name1 = st.text_input("Enter Sensor Name 1:")

# Timer input in minutes
record_time_minutes = st.slider("Select Recording Time (minutes):", min_value=1, max_value=300, value=60)

# Open serial port
ser1 = serial.Serial(selected_tab1, 115200)

# Create DataFrame to store sensor data
csv_file1 = f'sensor_data_{sensor_name1}.csv'
csv_header = ['Timestamp', f'{sensor_name1}_Values', f'{sensor_name1}_Labels']
df1 = pd.DataFrame(columns=csv_header)

# Arrange components in three columns
col1, col2, col3 = st.columns(3)

# Display real-time sensor data
message_box1 = col1.empty()
prediction_box1 = col2.empty()

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= record_time_minutes * 60:
    # Read data from the first serial input
    sensor_labels1, sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_labels1 and sensor_values1:
        timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        new_data = {
            'Timestamp': timestamp1,
            f'{sensor_name1}_Values': sensor_values1,
            f'{sensor_name1}_Labels': sensor_labels1
        }
        df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)

        # Display the latest data in the app
        message_box1.table(df1.tail(1)[df1.columns.intersection(['Timestamp', f'{sensor_name1}_Values', f'{sensor_name1}_Labels'])])

        # Predict walking pattern using the model
        walking_pattern_prediction1 = model.predict(sensor_values1.reshape(1, -1))[0]

        # Display the prediction results
        prediction_box1.write(f'{sensor_name1} Walking Pattern Prediction: {walking_pattern_prediction1}')

# ... (existing code)

st.write("Recording complete.")

# Close serial port
ser1.close()

# Save the collected data to a CSV file
df1.to_csv(csv_file1, index=False)
st.write(f"Data saved to {csv_file1}")

# Check if walking pattern is abnormal based on 40% accuracy threshold
if walking_pattern_prediction1 < 0.4:
    st.warning("Abnormal walking pattern detected!")
else:
    st.success("Normal walking pattern detected.")
