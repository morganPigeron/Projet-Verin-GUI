#include <Servo.h>

#include "src/SerialTransfer/src/SerialTransfer.h"
#include "src/AccelStepper/AccelStepper.h"

#define MAXSPEED 1200
#define STEPPIN1 2
#define DIRPIN1 5
#define STEPPIN2 3
#define DIRPIN2 6
#define STEPPIN3 4
#define DIRPIN3 7
#define ENABLEPIN 8

#define STEPENABLEPIN 8

#define SERVOPIN 9
#define SERVOANGLE 45

#define INTERPIN1 10
#define INTERPIN2 11

struct STRUCT {
  uint32_t nema1G;
  uint32_t nema1D;
  uint32_t nema1vit;
  uint32_t nema2G;
  uint32_t nema2D;
  uint32_t nema2vit;
  uint32_t nema3G;
  uint32_t nema3D;
  uint32_t nema3vit;
  uint32_t servo;
  uint32_t inter1;
  uint32_t inter2;
} trame;

SerialTransfer myTransfer;

//create 3 stepper objects
AccelStepper stepper1(AccelStepper::DRIVER, STEPPIN1, DIRPIN1);
AccelStepper stepper2(AccelStepper::DRIVER, STEPPIN2, DIRPIN2);
AccelStepper stepper3(AccelStepper::DRIVER, STEPPIN3, DIRPIN3);

//stepper direction
int step1Dir = 1;
int step2Dir = 1;
int step3Dir = 1;

//steper Runing
int step1Run = 0;
int step2Run = 0;
int step3Run = 0;

//create Servo object
Servo servo1;
int angle = 0;

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);

  stepper1.setMaxSpeed(MAXSPEED);
  stepper1.setSpeed(0);
  
  stepper2.setMaxSpeed(MAXSPEED);
  stepper2.setSpeed(0);

  stepper3.setMaxSpeed(MAXSPEED);
  stepper3.setSpeed(0);

  servo1.attach(SERVOPIN);

  pinMode(INTERPIN1, OUTPUT);
  digitalWrite(INTERPIN1, LOW);

  pinMode(ENABLEPIN, OUTPUT);
  digitalWrite(INTERPIN1, LOW);
  
  pinMode(INTERPIN2, OUTPUT);
  digitalWrite(INTERPIN2, LOW);

  trame.nema1G =0;
  trame.nema1D =0;
  trame.nema1vit =0;
  trame.nema2G =0;
  trame.nema2D =0;
  trame.nema2vit =0;
  trame.nema3G =0;
  trame.nema3D =0;
  trame.nema3vit =0;
  trame.servo =0;
  trame.inter1 = 0;
  trame.inter2 = 0;
}


void loop()
{
  if(myTransfer.available())
  {

    myTransfer.rxObj(trame, sizeof(trame));
       
    myTransfer.sendData(myTransfer.txObj(trame, sizeof(trame)));


    //update stepper 1 ------------------
    if(trame.nema1G)
    {
      step1Dir = 1;
      step1Run = 1;
    }
    else if(trame.nema1D)
    {
      step1Dir = -1;
      step1Run = 1;
    }
    else
    {
      step1Run = 0;
    }


    //update stepper 2 ------------------
    if(trame.nema2G)
    {
      step2Dir = 1;
      step2Run = 1;
    }
    else if(trame.nema2D)
    {
      step2Dir = -1;
      step2Run = 1;
    }
    else
    {
      step2Run = 0;
    }

    //update stepper 3 ------------------
    if(trame.nema3G)
    {
      step3Dir = 1;
      step3Run = 1;
    }
    else if(trame.nema3D)
    {
      step3Dir = -1;
      step3Run = 1;
    }
    else
    {
      step3Run = 0;
    }

    //update Servo ---------------------
    if(trame.servo)
    {
      servo1.write(SERVOANGLE);
    }
    else
    {
      servo1.write(0);
    }

    //update inter1 ---------------------
    if(trame.inter1)
    {
      digitalWrite(INTERPIN1, HIGH);
    }
    else
    {
      digitalWrite(INTERPIN1, LOW);
    }

    //update inter2 ---------------------
    if(trame.inter2)
    {
      digitalWrite(INTERPIN2, HIGH);
    }
    else
    {
      digitalWrite(INTERPIN2, LOW);
    }
  }

  //update stepper1 ---------------------
  if(step1Run)
  {
    stepper1.setSpeed(step1Dir * map(trame.nema1vit,0,100,0,MAXSPEED));
    stepper1.runSpeed();
  }
  else
  {
    stepper1.stop();
  }

  //update stepper2 ---------------------
  if(step2Run)
  {
    stepper2.setSpeed(step2Dir * map(trame.nema2vit,0,100,0,MAXSPEED));
    stepper2.runSpeed();
  }
  else
  {
    stepper2.stop();
  }

  //update stepper3 ---------------------
  if(step3Run)
  {
    stepper3.setSpeed(step3Dir * map(trame.nema3vit,0,100,0,MAXSPEED));
    stepper3.runSpeed();
  }
  else
  {
    stepper3.stop();
  }
}
