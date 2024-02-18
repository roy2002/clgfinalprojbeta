import streamlit as st
import serial
from serial.tools import list_ports
import json
from datetime import datetime
import pandas as pd
import time
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def read_serial_data(ser, sensor_name):
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)
        sensor_values = list(sensor_data.values())
        return sensor_values
    except json.JSONDecodeError as e:
        st.write(f"Error decoding JSON ({sensor_name}): {e}")
        return None

def scan_com_ports():
    com_ports = [port.device for port in list_ports.comports()]
    return com_ports

# Streamlit App
st.title("Sensor Data Live Training and Classification")

# Tabs for COM Port Selection
selected_tab1 = st.sidebar.selectbox("Select COM Port 1", scan_com_ports(), key="com_port_1")
selected_tab2 = st.sidebar.selectbox("Select COM Port 2", scan_com_ports(), key="com_port_2")

sensor_name1 = st.text_input("Enter Sensor Name 1:")
sensor_name2 = st.text_input("Enter Sensor Name 2:")

# Timer input in minutes
record_time_minutes = st.slider("Select Recording Time (minutes):", min_value=1, max_value=300, value=5)

# Open serial ports
ser1, ser2 = serial.Serial(selected_tab1, 115200), serial.Serial(selected_tab2, 115200)

# Data storage
data1, data2 = [], []

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= record_time_minutes * 60:
    # Read data from the first serial input
    sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_values1:
        data1.append(sensor_values1)

    # Read data from the second serial input
    sensor_values2 = read_serial_data(ser2, sensor_name2)
    if sensor_values2:
        data2.append(sensor_values2)

st.write("Recording complete.")

# Close serial ports
ser1.close()
ser2.close()

# Combine the collected data into a DataFrame
df1 = pd.DataFrame(data1, columns=[f'{sensor_name1}_Value_{i}' for i in range(len(data1[0]))])
df2 = pd.DataFrame(data2, columns=[f'{sensor_name2}_Value_{i}' for i in range(len(data2[0]))])

# Create a label column (0 for the first set, 1 for the second set)
df1['Label'] = 0
df2['Label'] = 1

# Combine the two sets into a single DataFrame
df_combined = pd.concat([df1, df2], ignore_index=True)

# Prepare the data for training
X = df_combined.drop('Label', axis=1)
y = df_combined['Label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Neural Network Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the Neural Network
model.fit(X_train, y_train, epochs=500, batch_size=32, validation_split=0.2)

# Save the model as a .tftmodel file
model.save('live_trained_model.tftmodel')

# Evaluate on the test set
y_pred = model.predict(X_test)
y_pred_binary = np.round(y_pred)
accuracy = accuracy_score(y_test, y_pred_binary)
st.write(f"Classifier Accuracy: {accuracy}")
