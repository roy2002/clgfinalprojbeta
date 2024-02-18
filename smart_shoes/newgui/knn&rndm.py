import streamlit as st
import serial
from serial.tools import list_ports
import json
from datetime import datetime
import pandas as pd
import time
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Function to read data from the serial port
def read_serial_data(ser, sensor_name):
    try:
        data = ser.readline().decode().strip()
        sensor_data = json.loads(data)
        return list(sensor_data.values())
    except json.JSONDecodeError as e:
        st.write(f"Error decoding JSON ({sensor_name}): {e}")
        return None

# Function to scan available COM ports
def scan_com_ports():
    return [port.device for port in list_ports.comports()]

# Function to prepare data for machine learning classification
def prepare_classification_data(df_sensor1, df_sensor2, target_sensor):
    features_sensor1 = df_sensor1.drop(['Timestamp', f'{target_sensor}_Values'], axis=1)
    features_sensor2 = df_sensor2.drop(['Timestamp', f'{target_sensor}_Values'], axis=1)
    target = df_sensor1[f'{target_sensor}_Values']

    # Concatenate features from Sensor1 and Sensor2
    features = pd.concat([features_sensor1, features_sensor2], axis=1)

    return features, target

# Function to train and evaluate machine learning classifiers
def train_and_evaluate_classifiers(features, target):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # K-Nearest Neighbors (KNN) classifier
    knn_classifier = KNeighborsClassifier(n_neighbors=5)
    knn_classifier.fit(X_train, y_train)
    knn_predictions = knn_classifier.predict(X_test)
    knn_accuracy = accuracy_score(y_test, knn_predictions)

    # Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)
    rf_predictions = rf_classifier.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_predictions)

    return knn_classifier, knn_accuracy, rf_classifier, rf_accuracy

# Streamlit App
st.title("Sensor Data Classification")

# Sidebar inputs
selected_tab1 = st.sidebar.selectbox("Select COM Port 1", scan_com_ports(), key="com_port_1")
selected_tab2 = st.sidebar.selectbox("Select COM Port 2", scan_com_ports(), key="com_port_2")

sensor_name1 = st.text_input("Enter Sensor Name 1:")
sensor_name2 = st.text_input("Enter Sensor Name 2:")

# Create DataFrames to store sensor data
csv_header = ['Timestamp', f'{sensor_name1}_Values', f'{sensor_name2}_Values']
df_sensor1, df_sensor2 = pd.DataFrame(columns=csv_header), pd.DataFrame(columns=csv_header)

# Display real-time sensor data
col1, col2 = st.columns(2)
message_box1 = col1.empty()
message_box2 = col2.empty()

recording = st.button("Start Recording")

start_time = time.time()

while recording and (time.time() - start_time) <= 5 * 60:  # Recording for 5 minutes
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # Read data from the first serial input (Sensor 1)
    sensor_values1 = read_serial_data(ser1, sensor_name1)
    if sensor_values1:
        new_data_sensor1 = {
            'Timestamp': timestamp,
            f'{sensor_name1}_Values': sensor_values1
        }
        df_sensor1 = pd.concat([df_sensor1, pd.DataFrame([new_data_sensor1])], ignore_index=True)

        # Display the latest data in the app
        latest_data_sensor1 = df_sensor1.tail(1)[df_sensor1.columns.intersection(csv_header)]
        message_box1.write(f"Latest data for {sensor_name1}:")
        message_box1.write(latest_data_sensor1)

    # Read data from the second serial input (Sensor 2)
    sensor_values2 = read_serial_data(ser2, sensor_name2)
    if sensor_values2:
        new_data_sensor2 = {
            'Timestamp': timestamp,
            f'{sensor_name2}_Values': sensor_values2
        }
        df_sensor2 = pd.concat([df_sensor2, pd.DataFrame([new_data_sensor2])], ignore_index=True)

        # Display the latest data in the app
        latest_data_sensor2 = df_sensor2.tail(1)[df_sensor2.columns.intersection(csv_header)]
        message_box2.write(f"Latest data for {sensor_name2}:")
        message_box2.write(latest_data_sensor2)

# Train and evaluate classifiers using data from Sensor1 and Sensor2
features_combined, target_combined = prepare_classification_data(df_sensor1, df_sensor2, sensor_name1)
knn_classifier, knn_accuracy, rf_classifier, rf_accuracy = train_and_evaluate_classifiers(features_combined, target_combined)

st.write("Classifiers trained and evaluated using data from Sensor1 and Sensor2.")
st.write(f"KNN Classifier Accuracy: {knn_accuracy}")
st.write(f"Random Forest Classifier Accuracy: {rf_accuracy}")

# Save the trained models
joblib.dump(knn_classifier, 'knn_model.joblib')
joblib.dump(rf_classifier, 'rf_model.joblib')

st.write("Trained models saved.")
