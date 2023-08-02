#include <BluetoothSerial.h>

// Define the number of input channels
const int numChannels = 16;

// Array to store the ADC values for each channel
int adcValues[numChannels];

// Current channel being read
int currentChannel = 0;

// BluetoothSerial object
BluetoothSerial SerialBT;

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(115200);

  // Initialize the ADC
  adcSetup();

  // Initialize Bluetooth
  SerialBT.begin("ESP32-Bluetooth"); // Change the name to your preference
  Serial.println("Bluetooth started. You can now connect to ESP32.");
}

void loop() {
  // Read analog value from the current channel
  adcValues[currentChannel] = analogReadMilliVolts(currentChannel);

  // Move to the next channel
  currentChannel++;

  // If all channels have been read, send the data through Bluetooth and reset the current channel
  if (currentChannel >= numChannels) {
    currentChannel = 0;
    sendBluetoothData();
  }

  // Delay between readings (you can also use timer-based methods for more precise timing)
  delay(10); // Adjust as needed
}

void adcSetup() {
  // Set the ADC resolution to 12 bits (0-4095)
  analogReadResolution(12);

  // No need to set ADC clock frequency for ESP32, it's fixed at 1.1 MHz

  // Set the attenuation to 11dB (ADC range 0-3.3V)
}

void sendBluetoothData() {
  // Prepare a string to hold the data
  String dataString = "";

  // Concatenate all the ADC values to the data string
  for (int channel = 0; channel < numChannels; channel++) {
    dataString += String(adcValues[channel]) + ",";
  }

  // Remove the trailing comma
  dataString.trim();

  // Send the data over Bluetooth
  SerialBT.println(dataString);

  // Print the data to Serial Monitor for debugging
  Serial.println(dataString);
}
