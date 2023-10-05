#include <AStar32U4Motors.h>
#include <Encoder.h>
#include <QTRSensors.h>
QTRSensors qtr;

AStar32U4Motors m; //read the documentation of this library to understand what functions to use to drive the motors and how to use them


const byte numChars = 32;
char receivedChars[numChars];
char tempChar[numChars]; // temporary array used for parsing

// line following:
const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];
uint16_t linePosition;

boolean newData = false;
int leftMotor;
int rightMotor;
int isCross;

Encoder rightwheel(2,3);
Encoder leftwheel(14,15);
long rwPos, lwPos;
float rPos, lPos;

void setup() {
//   pinMode(3, OUTPUT); //left motor
//   pinMode(2,OUTPUT); //left motor
   Serial.begin(115200);
   qtr.setTypeRC(); //this allows us to read the line sensor from didgital pins

   //arduino pin sensornames I am using: 7, 18, 19, 20, 21, 22, 23, 6. UNHOOK THE BLUE JUMPER LABELED BUZZER ON THE ASTAR or pin 6 will cause the buzzer to activate.
   qtr.setSensorPins((const uint8_t[]){7, 18, 19, 20, 21, 22, 23, 6}, SensorCount);

   calibrateSensors();
   Serial.println("<Arduino is ready>");

 
}   

void loop() {

  rwPos = rightwheel.read();
  rPos = 360 * rwPos / 1440;
  lwPos = leftwheel.read();
  lPos = 360 * lwPos / 1440;
  
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

  linePosition = qtr.readLineBlack(sensorValues);
  
//  Serial.print(leftMotor);
//  Serial.print(',');
//  Serial.print(rightMotor);
//  Serial.print(',');
  Serial.print(lPos); // l encoder
  Serial.print(',');
  Serial.print(rPos); // r encoder
  Serial.print(',');
  if(sensorValues[7] > 750 && sensorValues[0] >750){ //meaning both the far left and right sensors see a value above 750, meaning your robot is VERY LIKLY over a cross
    isCross=1; //now I will be sending the string 'cross' to the rpi INSTEAD of a number between 0-7000 that rearesents the line sensor array's position relative to the cross
  }
  if(isCross == 1){ //this commented out if/else statement is a continuation of the example of logic used to send the rpi the value 8000 both left and right sensors see the line, this is a value that LinePosition will never send, so you can have a catch in the Rpi code that checks if linePosition is greater than 7000
    Serial.println('8000');
    isCross=0;
  } 
  else {
    Serial.println(linePosition);
  }
  newData = false;

}

//=======================================


void commandMotors(){

  //read the documentation for the functions that drive the motors in the astar library

  m.setM1Speed(leftMotor);
  m.setM2Speed(rightMotor);
  //uncomment to drive motors
}

//=======================================

void calibrateSensors(){ 

  //THE SENSORS ONLY CALIBRATE WHEN YOU UPLOAD NEW ARDUINO CODE TO THE ASTAR. after that the sensors STAY calibrated as long as the Astar has power.

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode
                                   ///while calibrating, move the sensor over the line a couple times

  // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
  // = ~25 ms per calibrate() call.
  // Call calibrate() 200 times to make calibration take about 5 seconds.
  for (uint16_t i = 0; i < 200; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration
  
}
