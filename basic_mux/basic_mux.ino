

#include <light_CD74HC4067.h>

               // s0 s1 s2 s3: select pins
CD74HC4067 mux(2,4,5,18);  // create a new CD74HC4067 object with its four select lines

const int signal_pin = 35; // Pin Connected to Sig pin of CD74HC4067

void setup()
{
    Serial.begin(115200);
    pinMode(signal_pin, INPUT); // Set as input for reading through signal pin
}

void loop()
{
  // loop through channels 0 - 15
    for (int i = 0; i < 16; i++) {
        mux.channel(i);
        int val = analogRead(signal_pin);                       // Read analog value
        Serial.println("Channel "+String(i)+": "+String(val));  // Print value
        delay(200);
    }
  delay(2000);
}
