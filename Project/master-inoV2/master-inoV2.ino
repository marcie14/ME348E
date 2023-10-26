// #include <AStar32U4Motors.h>
// #include <Encoder.h>
#include <HCSR04.h>
// AStar32U4Motors m; //read the documentation of this library to understand what functions to use to drive the motors and how to use them


const byte numChars = 32;
char receivedChars[numChars];
char tempChar[numChars]; // temporary array used for parsing
int leftMotor;
int rightMotor;
long rwPos, lwPos;
float rPos, lPos;
float x_dist, y_dist; // for ultrastonic
float L_IR, M_IR, R_IR; // for IR

boolean newData = true;


// Pin set up + library initializations
// Ultrasonic
const byte x_trig_pin = 5;
const byte y_trig_pin = 7;
const byte x_echo_pin = 6;
const byte y_echo_pin = 8; 
UltraSonicDistanceSensor X_sensor(x_trig_pin, x_echo_pin);
UltraSonicDistanceSensor Y_sensor(y_trig_pin, y_echo_pin);

// Drive Motors
const byte RW_Pin1 = 2; 
const byte RW_Pin2 = 3; 
const byte LW_Pin1 = 14; 
const byte LW_Pin2 = 15;
// Encoder rightwheel(RW_Pin1,RW_Pin2);
// Encoder leftwheel(LW_Pin1,LW_Pin2);

// IR sensors


void setup() {
menu://applications/Development/arduino.desktop

   Serial.begin(115200);

   Serial.println("<Arduino is ready>");

 
}   

void loop() {

  // read drive motor encorder
  // rwPos = rightwheel.read();
  // rPos = 360 * rwPos / 1440;
  // lwPos = leftwheel.read();
  // lPos = 360 * lwPos / 1440;

  // read ultrasonic sensors
  x_dist = X_sensor.measureDistanceCm();
  y_dist = Y_sensor.measureDistanceCm();
  
  recvWithStartEndMarkers();


  if (newData == true){
        
    parseData();
    commandMotors();
    sendRecievedData();
    newData = false;
    //why am I setting newdata rwPosequil to false after I send data back to the rpi.
    //what would happen if this line was not here?
    
    }
}


void recvWithStartEndMarkers() {
//this function is the most important one of the whole lab, read the blog post made my Robin2
//some questions:
      //whats the purpose of the start and end markers?
      //Why bother making this code unblocking?
      //why not use the Arduino built in functions for reading serial data?
      
    static boolean recvInProgress = false;
    //what is the purpose of this boolean?
    
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
                                         
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
                                       

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminates the string, frankly unsure why I need 
                                           //this but it breaks if I remove it. Bonus points if you find out why
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//====================================

void parseData(){
  
strcpy(tempChar,receivedChars); //copying recievedChar into tempChar so we dont alter recievedChar

char *strIndexer = strtok(tempChar,","); //dont worry about the *, this isnt a C class and I dont expect you to know how pointers work

leftMotor = atoi(strIndexer);

strIndexer = strtok(NULL,",");

rightMotor = atoi(strIndexer);

}

//=====================================

void sendRecievedData(){
  
  // print current location
  Serial.print(x_dist);
  Serial.print(',');
  Serial.print(y_dist);
  // // print motor encoder values
  // Serial.print(',');
  // Serial.print(lPos); // l encoder
  // Serial.print(',');
  // Serial.println(rPos); // r encoder
  // print IR beacon values
  // Serial.print(',');
  // Serial.print(L_IR); // left IR sensor
  // Serial.print(',');
  // Serial.print(M_IR); // middle IR sensor
  // Serial.print(',');
  // Serial.println(R_IR); // right IR sensor 

}

//=======================================


void commandMotors(){ // drive motors

  //read the documentation for the functions that drive the motors in the astar library

  // m.setM1Speed(leftMotor);
  // m.setM2Speed(rightMotor);
  //uncomment to drive motors
}

//=======================================


// function for ir sensors

// function for stepper motors for feeder (PI?)

// function for 2 shooter motors
