#include <BluetoothSerial.h>
#include <ArduinoJson.h>

BluetoothSerial SerialBT;

const int numSensors = 5;
int sensorData[numSensors];

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32-Bluetooth");

  pinMode(13, INPUT);
  pinMode(12, INPUT);
  pinMode(14, INPUT);
  pinMode(27, INPUT);
  pinMode(26, INPUT);
}

void loop() {
  // Read sensor data
  sensorData[0] = analogRead(26);
  sensorData[1] = analogRead(27);
  sensorData[2] = analogRead(14);
  sensorData[3] = analogRead(12);
  sensorData[4] = analogRead(13);
  
  // Send sensor data over Bluetooth
  sendBluetoothData();

  delay(1000); // Adjust delay as needed
}

void sendBluetoothData() {
  StaticJsonDocument<128> doc; // Adjust size based on your data

  // Add sensor data to the JSON object
  for (int sensor = 0; sensor < numSensors; sensor++) {
    doc["sensor" + String(sensor + 1)] = sensorData[sensor];
  }

  // Serialize JSON to a string
  String jsonString;
  serializeJson(doc, jsonString);

  // Send JSON data over Bluetooth
  if (SerialBT.connected()) {
    SerialBT.println(jsonString);
  }

  Serial.println(jsonString);
}
