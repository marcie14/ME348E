#include <AStar32U4.h>
#include <AStar32U4Motors.h>

AStar32U4Motors m;
int leftMotor;
int rightMotor;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("<Arduino is ready");

  leftMotor = 300;
  rightMotor = -300;

}

void loop() {
  // put your main code here, to run repeatedly:
  m.setM1Speed(leftMotor);
  m.setM2Speed(rightMotor);
}
