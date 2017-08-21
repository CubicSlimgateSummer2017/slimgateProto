//define switch
#define LEVER_SWITCH_PIN_TOP 2
#define LEVER_SWITCH_PIN_BOTTOM 3
int pressSwitchTop = 0;
int pressSwitchBottom = 0;

// defines pins numbers
const int stepPin = 11;
const int dirPin = 12;
const int alarmPin = 10;
int incomingByte = 0;

int count = 0;
bool motorOn = false;

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(alarmPin, OUTPUT);
  pinMode(LEVER_SWITCH_PIN_TOP,INPUT);
  pinMode(LEVER_SWITCH_PIN_BOTTOM,INPUT);
  Serial.begin(115200);
}
void loop() {
  pressSwitchTop = digitalRead(LEVER_SWITCH_PIN_TOP);
  pressSwitchBottom = digitalRead(LEVER_SWITCH_PIN_BOTTOM);
  /*
  if(pressSwitch == LOW)
    {
      //Serial.println("close limit");
      //delay(500);
    }
  else if(pressSwitch2 == LOW)
  {
    //Serial.println("open limit");
    //delay(500);
  }
  */
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
  }
  /*
  if (pressSwitchTop == LOW) {
    Serial.println("TOP");
  }
  if (pressSwitchBottom == LOW) {
    Serial.println("BOTTOM");
  }*/
  if (char(incomingByte) == 'q' && motorOn == false) {
    motorOn = true;
    int countTemp = 0;
    digitalWrite(dirPin, LOW); // Enables the motor to move in a particular direction
    //rotates until hits limit switch
    while (digitalRead(LEVER_SWITCH_PIN_BOTTOM) == HIGH) {
      if (countTemp < 100) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(25000 - countTemp * 50);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(25000 - countTemp * 50);
      }
      else {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(10000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(10000);
      }
      countTemp++;
    }
  }
  if (char(incomingByte) == 'w' && motorOn == false) {
    motorOn = true;
    int countTemp = 0;
    digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
    //rotate until hits limit switch
    while (digitalRead(LEVER_SWITCH_PIN_TOP) == HIGH) {
      if (countTemp < 100) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(25000 - countTemp * 50);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(25000 - countTemp * 50);
      }
      else {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(10000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(10000);
      }
      countTemp++;
    } 
  }
  if (char(incomingByte) == 'c' && motorOn == true) {
    motorOn = false;
  }

  if (char(incomingByte) == 'r') {
    count = 0;
    Serial.println(count);
  }
}
/*
void gateOpen() {
//  Serial.print("open");
  digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for (int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(3000) ;
  }
}

void gateClose() {
//  Serial.print("close");
  digitalWrite(dirPin, LOW);
  for (int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(3000);
  }
}
*/
