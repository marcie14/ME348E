//////////// V1 CODE BELOW /////////////

#include <HCSR04.h>

// Pin set up + library initializations
// Ultrasonic
const byte x_trig_pin = 12;
const byte y_trig_pin = 13;
const byte x_echo_pin = 6;
const byte y_echo_pin = 8; 

UltraSonicDistanceSensor X_sensor(x_trig_pin, x_echo_pin);
UltraSonicDistanceSensor Y_sensor(y_trig_pin, y_echo_pin);

float x_dist = -1;
float y_dist = -1; // for ultrastonic


void setup () {
    Serial.begin(115200);  // We initialize serial connection so that we could print values from sensor.
}

void loop () {
    // Every 500 miliseconds, do a measurement using the sens or and print the distance in centimeters.
    // read ultrasonic sensors
    x_dist = X_sensor.measureDistanceCm();
    y_dist = Y_sensor.measureDistanceCm();

     
    Serial.print(x_dist);
    Serial.print(",");
    Serial.println(y_dist);
    delay(500);
}
