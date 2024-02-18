#include <BluetoothSerial.h>
#include <ArduinoJson.h>

BluetoothSerial SerialBT;

const int numSensors = 5; // Update the number of sensors to match the pins
int sensorData[numSensors];

void setup() {
  Serial.begin(115200);
  SerialBT.begin("RightFootinsole");

  pinMode(33, INPUT);
  pinMode(32, INPUT);
  pinMode(34, INPUT);
  pinMode(36, INPUT);
  pinMode(35, INPUT);
 
}

void loop() {
  // Read sensor data
  sensorData[0] = analogRead(36);
  sensorData[1] = analogRead(35);
  sensorData[2] = analogRead(34);
  sensorData[3] = analogRead(32);
  sensorData[4] = analogRead(33);
 
  
  // Send sensor data over Bluetooth
  sendBluetoothData();

  delay(1000); // Adjust delay as needed
}
void sendBluetoothData() {
  StaticJsonDocument<256> doc; // Adjust size based on your data

  // Add sensor data to the JSON object
  for (int sensor = 0; sensor < numSensors; sensor++) {
    doc["sensor" + String(sensor + 1)] = sensorData[sensor];
  }

  // Serialize JSON to a string
  String jsonString;
  serializeJson(doc, jsonString);

  // Send JSON data over Bluetooth with explicit encoding
  if (SerialBT.connected()) {
    const uint8_t* jsonData = reinterpret_cast<const uint8_t*>(jsonString.c_str());
    size_t dataSize = jsonString.length();
    SerialBT.write(jsonData, dataSize);
    SerialBT.write('\n');  // Add newline for better parsing on the receiving end
  }

  Serial.println(jsonString);
}
