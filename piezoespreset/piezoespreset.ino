int max_value = 0; // Declare max_value as a global variable
unsigned long restartInterval = 500; // Restart interval in milliseconds (60 seconds)

// Function to get the max analog value
int get_max_analog_value(void) {
  return max_value;
}

void setup() {
  Serial.begin(9600); // Initialize serial communication for debugging
}

void loop() {
  static unsigned long lastRestartTime = 0;
  unsigned long currentTime = millis();

  // Check if it's time to restart the device
  if (currentTime - lastRestartTime >= restartInterval) {
    Serial.println("Restarting the device...");
    delay(1); // Give some time for the Serial message to be sent
    ESP.restart(); // Perform the device restart
  }

  int value = analogRead(34); // Read analog value from pin 34
  if (value > max_value) {
    max_value = value; // Update max_value if a new maximum is found
  }

  // Print the maximum analog value
  Serial.print("Max Value: ");
  Serial.println(get_max_analog_value());

  // Add any necessary delays or other code in the loop
}
