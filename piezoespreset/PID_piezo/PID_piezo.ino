// Define the coefficients for the second-order system
float K = 1.0;       // System gain
float zeta = 0.8;    // Damping ratio
float wn = 10.0;     // Natural frequency

// Define the state variables for the first-order approximation
float prevOutput = 0.0; // Previous output value
float prevInput = 0.0;  // Previous input value

// Function to perform the first-order approximation
float firstOrderApproximation(float input) {
  // Calculate the Pade approximation using the previous input and output values
  float output = (2 * zeta * wn * prevOutput - (wn * wn * prevInput) + K * input) / (2 * zeta * wn + 1);

  // Update the previous input and output values
  prevInput = input;
  prevOutput = output;

  return output;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Read the input value from the sensor or any other source
  float sensorValue = analogRead(35); // Replace A0 with the appropriate analog input pin

  // Perform the first-order approximation
  float approximatedValue = firstOrderApproximation(sensorValue);

  // Output the approximated value
 
  Serial.println(approximatedValue);
 delay(20);
  // Add any necessary delays here to control the sampling rate
}
