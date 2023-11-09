#include <HCSR04.h>

boolean newData = true;

// data parsing
const byte numChars = 32;
char receivedChars[numChars];
char tempChar[numChars]; // temporary array used for parsing

// Pin set up + library initializations
// Ultrasonic
const byte x_trig_pin = 22;
const byte x_echo_pin = 24;
const byte y_trig_pin = 26;
const byte y_echo_pin = 28; 
UltraSonicDistanceSensor X_sensor(x_trig_pin, x_echo_pin);
UltraSonicDistanceSensor Y_sensor(y_trig_pin, y_echo_pin);

// drive motors
int motor1pin1 = 2;
int motor1pin2 = 3;
int motor2pin1 = 4;
int motor2pin2 = 5;

// variable initializations
int driveAction;
int shootAction;
int feedAction;
float x_dist; // ultrasonic
float y_dist; // ultrasonic
int sendX; // target X
int sendY; // target Y
int leftMotor; // drive motor speed
int rightMotor; // drive motor speed


void setup() {
menu://applications/Development/arduino.desktop
  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(9,  OUTPUT); 
  pinMode(10, OUTPUT);

  Serial.begin(115200);
  // Serial.println("<Arduino is ready>");

}   

void loop() {

  x_dist = X_sensor.measureDistanceCm();
  y_dist = Y_sensor.measureDistanceCm();

  // recvWithStartEndMarkers();

  // if (newData == true){  
  //   parseData();
    sendRecievedData();
  //   newData = false;
  // }
  commandMotors();
  // commandFeed();
  // commandShoot();
  // delay(100);
}
//====================================
void recvWithStartEndMarkers() {
      
    static boolean recvInProgress = false;
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
                receivedChars[ndx] = '\0'; 
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
  
  strcpy(tempChar,receivedChars); 
  char *strIndexer = strtok(tempChar,","); 

  driveAction = atoi(strIndexer);
  strIndexer = strtok(NULL,",");
  sendX = atoi(strIndexer);
  strIndexer = strtok(NULL,",");
  sendY = atoi(strIndexer);
  strIndexer = strtok(NULL,",");
  feedAction = atoi(strIndexer);
  strIndexer = strtok(NULL,",");
  shootAction = atoi(strIndexer);
}

//=====================================

void sendRecievedData(){
  
   Serial.print(x_dist);
   Serial.print(',');
   Serial.println(y_dist);

}

//=======================================
void commandMotors(){
  switch (driveAction) {
    case 0:
      moveStraight();
      break;
    case 1:
      turnLeft();
      break;
    case 2:
      turnRight();
      break;
    case 3:
      moveBackwards();
      break;
    default:
      stopMoving();
      break;
  }

  if (y_dist < 41){
    stopMoving();
  }
  else if (x_dist <130)
    stopMoving();
}

void commandFeed(){
  switch (feedAction) {
    case 0:
      // prime
      break;
    case 1:
      // release + drop puck
      break;
    default:
      // do nothing
      break;
  }
}
void commandShoot(){
  switch (shootAction) {
    case 0:
      // prime
      break;
    case 1:
      // release + shoot
      break;
    default:
      // do nothing
      break;
  }
}


void moveStraight(){
  analogWrite(9, 80); //ENA   pin
  analogWrite(10, 80); //ENB pin
  
  // left fwd
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  // right fwd
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

void moveBackwards(){
  analogWrite(9, 80); //ENA   pin
  analogWrite(10, 80); //ENB pin
  
  // left bkwd
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  // right bkwd 
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

}

void turnRight(){
  analogWrite(9, 80); //ENA   pin
  analogWrite(10, 80); //ENB pin


  // left fwd
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  // right bkwd 
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}

void turnLeft(){
  analogWrite(9, 80); //ENA   pin
  analogWrite(10, 80); //ENB pin

  // left bkwd
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
    
  // right fwd
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

}

void stopMoving(){
  analogWrite(9, 0); //ENA   pin
  analogWrite(10, 0); //ENB pin

  // left bkwd
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
    
  // right fwd
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}





// void commandMotors(){ // drive motors


//    m.setM1Speed(leftMotor);
//    m.setM2Speed(rightMotor);
// }

//=======================================


// still need:

// function for stepper motors for feeder (PI?)

// function for 2 shooter motors
