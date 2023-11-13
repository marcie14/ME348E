#include <HCSR04.h>
#include <ezButton.h>
boolean newData = true;

// data parsing
const byte numChars = 32;
char receivedChars[numChars];
char tempChar[numChars]; // temporary array used for parsing

// Pin set up + library initializations
// Ultrasonic
// const byte x_trig_pin = 22;
// const byte x_echo_pin = 24;
// const byte y_trig_pin = 26;
// const byte y_echo_pin = 28; 
const byte left_trig = 22;
const byte left_echo = 24;
const byte right_trig = 26;
const byte right_echo = 28;
const byte front_trig = 30; 
const byte front_echo = 32; 
const byte back_trig = 34; 
const byte back_echo = 36; 

// UltraSonicDistanceSensor X_sensor(x_trig_pin, x_echo_pin);
// UltraSonicDistanceSensor Y_sensor(y_trig_pin, y_echo_pin);
UltraSonicDistanceSensor left_sensor(left_trig, left_echo);
UltraSonicDistanceSensor right_sensor(right_trig, right_echo);
UltraSonicDistanceSensor front_sensor(front_trig, front_echo);
UltraSonicDistanceSensor back_sensor(back_trig, back_echo);

// drive motors
int motor1pin1 = 8; // left
int motor1pin2 = 9; // left
int motor2pin1 = 10; // right
int motor2pin2 = 11; // right
int L_ENA = 12;
int R_ENB =13;

// feeder
int feederpin1 = 2;
int feederpin2 = 3;
int feeder_ENA = 6;
ezButton f_prime_switch(53); // limit switch (1 = primed)
ezButton f_drop_switch(51); // limit switch (1 = dropped)

// shooter 
int shooterpin1 = 4;
int shooterpin2 = 5;
int shooter_ENB = 7;
ezButton shoot_switch(49); // limit switch (1 = ?)

// variable initializations
int driveAction = -1;
int shootAction = -1;
int feedAction = -1;
// float x_dist; // ultrasonic
// float y_dist; // ultrasonic
float left; // ultrasonic
float right; // ultrasonic
float front; // ultrasonic
float back; // ultrasonic
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
  
  pinMode(L_ENA,  OUTPUT); 
  pinMode(R_ENB, OUTPUT);

  pinMode(feederpin1, OUTPUT);
  pinMode(feederpin2, OUTPUT);
  pinMode(shooterpin1, OUTPUT);
  pinMode(shooterpin2, OUTPUT);
  pinMode(feeder_ENA,  OUTPUT); 
  pinMode(shooter_ENB, OUTPUT);

//  f_prime_switch.setDebounceTime(0); // set debounce time to 50 milliseconds
//  f_drop_switch.setDebounceTime(0); // set debounce time to 50 milliseconds
//  shoot_switch.setDebounceTime(0); // set debounce time to 50 milliseconds


  Serial.begin(115200);
  // Serial.println("<Arduino is ready>");

}   

void loop() {
  f_prime_switch.loop();
  f_drop_switch.loop();
  shoot_switch.loop();

  // x_dist = X_sensor.measureDistanceCm();
  // y_dist = Y_sensor.measureDistanceCm();
  left = left_sensor.measureDistanceCm();
  right = right_sensor.measureDistanceCm();
  front = front_sensor.measureDistanceCm();
  back = back_sensor.measureDistanceCm();

  recvWithStartEndMarkers();

  if (newData == true){  
    parseData();
    sendRecievedData();
    commandMotors();
    commandFeed();
    commandShoot();
    newData = false;
  }
//  sendRecievedData(); // DEBUG

 




//  testFeeder(); // DEBUG
//  testShooter(); // DEBUG
//  testMotors(); // DEBUG
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
  
  //  Serial.print(x_dist);
  //  Serial.print(',');
  //  Serial.println(y_dist);
//  Serial.print("Ultrasonic: "); // DEBUG
  Serial.print(left);
  Serial.print(',');
  Serial.print(right);
  Serial.print(',');
  Serial.print(front);
  Serial.print(',');
  Serial.print(back);
  Serial.print(',');
//  Serial.print(" Feeder: "); // DEBUG
  Serial.print(f_prime_switch.getState());
  Serial.print(',');
  Serial.print(f_drop_switch.getState());
  Serial.print(',');
//  Serial.print(" Shooter: "); // DEBUG
  Serial.print(shoot_switch.getState());
//  Serial.print("Drive Action: "); // DEBUG
  Serial.print(',');
  Serial.print(driveAction);
  Serial.print(',');
//  Serial.print("Feed Action"); // DEBUG
  Serial.print(feedAction); 
  Serial.print(',');
//  Serial.print("Shoot Action: "); // DEBUG
  Serial.println(shootAction);

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
}

void commandFeed(){
  switch (feedAction) {
    case 1:
      // prime
      if (f_prime_switch.getState() == 1){
//          feederDrop(); //DEBUG = testFeeder()
        feederStop(); //UNCOMMENT
      }
      else{
        feederPrime();
      }
      break;
    case 2:
      // release + drop puck
      if (f_drop_switch.getState() == 1){        
//        feederPrime();//DEBUG = testFeeder()
        feederStop(); //UNCOMMENT
      }
      else{
        feederDrop();
      }
      break;
    default:
      // do nothing
      feederStop();
      break;
  }
}
void commandShoot(){
  switch (shootAction) {
    case 0:
    // prime
      if (shoot_switch.getState() == 0){
        shooterOn();
      }
      else{
        shooterStop();
      }
      break;
    case 1:
    sh
      shooterOn();
      break;
    default:
      // do nothing
      shooterStop();
      break;
  }
}






// ========== Feeder Motor Function ==========
void testFeeder() { //FOR DEBUG
  if (f_prime_switch.getState() == 1){
    feederDrop();
  }
  
  if (f_drop_switch.getState() == 1){
    feederPrime();
  }
//  commandFeed();
  
}
void feederPrime(){
  analogWrite(feeder_ENA, 250); //ENA   pin
  
  // bckwd
  digitalWrite(feederpin1, LOW);
  digitalWrite(feederpin2, HIGH);
}
void feederDrop(){
  analogWrite(feeder_ENA, 250); //ENA   pin
  
  // fwd
  digitalWrite(feederpin1, HIGH);
  digitalWrite(feederpin2, LOW);

}
void feederStop(){
  analogWrite(feeder_ENA, 0); //ENA   pin
    // off
  digitalWrite(feederpin1, LOW);
  digitalWrite(feederpin2, LOW);
}
// ========== Shooter Motor Function ==========
void testShooter(){ // FOR DEBUG
  shootAction = 1;
  commandShoot();
}

void shooterOn(){
  analogWrite(shooter_ENB, 250); //ENA   pin
  // fwd
  digitalWrite(shooterpin1, HIGH);
  digitalWrite(shooterpin2, LOW);
}
void shooterStop(){
  analogWrite(shooter_ENB, 0); //ENA   pin
    // off
  digitalWrite(shooterpin1, LOW);
  digitalWrite(shooterpin2, LOW);
}
// =========== Drive Motors Functions ==============
void testMotors(){ // DEBUG
  moveStraight();
  delay(500);
  stopMoving();
  delay(500);
  turnRight();
  delay(500);
  stopMoving();
  delay(500);
  turnLeft();
  delay(500);
  stopMoving();
  delay(500);
  moveBackwards();
  delay(500);
  stopMoving();
  delay(500);  
  
}


void moveStraight(){
  analogWrite(L_ENA, 150); //ENA   pin
  analogWrite(R_ENB, 150); //ENB pin
  
  // left fwd
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  // right fwd
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
  
}

void moveBackwards(){
  analogWrite(L_ENA, 150); //ENA   pin
  analogWrite(R_ENB, 150); //ENB pin
  
  // left bkwd
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  // right bkwd 
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

}

void turnRight(){
  analogWrite(L_ENA, 150); //ENA   pin
  analogWrite(R_ENB, 150); //ENB pin


  // left fwd
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  // right bkwd 
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}

void turnLeft(){
  analogWrite(L_ENA, 150); //ENA   pin
  analogWrite(R_ENB, 150); //ENB pin

  // left bkwd
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
    
  // right fwd
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

}

void stopMoving(){
  analogWrite(L_ENA, 0); //ENA   pin
  analogWrite(R_ENB, 0); //ENB pin

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

