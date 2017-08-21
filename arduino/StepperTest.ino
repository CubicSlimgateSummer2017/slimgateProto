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

//0 = closed, 1 = open
int gate = 0;

//0 = off, 1 = on
int alarm = 0;

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

  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    //Serial.print("I received: ");
    //Serial.println(char(incomingByte));
    
    if (gate == 0) {
      if (char(incomingByte) == 'o') {
        gateOpen();
        gate = 1;
      }
    }
    else if (gate == 1) {
      if (char(incomingByte) == 'c') {
        gateClose();
        gate = 0;
      }
    }
    if (alarm == 0) {
      if (char(incomingByte) == 'a') {
        alarm = 1;
        alarmSound();
      }
    }
    //else if (alarm == 1) {
    //  if (char(incomingByte) == 's') {
    //    alarmStop();
    //    alarm = 0;
    //  }
    //}
  }
}

void alarmStop() {
  digitalWrite(alarmPin, LOW);
}

void alarmSound() {
  int x = 0;
  for(;;) {
    int stopBit = Serial.read();
    if (char(stopBit) == 's') {
      //Serial.print("stop");
      digitalWrite(alarmPin, LOW);
      alarm = 0;
      break;
    }
    digitalWrite(alarmPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(alarmPin, LOW);
    delayMicroseconds(2000);
    if (x%350 == 0) {
      digitalWrite(alarmPin, LOW);
      delay(500);
    }
    x++;
  }
}

void gateClose() {
//  Serial.print("close");
  int countTemp = 0;
  digitalWrite(dirPin, LOW); // Enables the motor to move in a particular direction
  //rotate until hits limit switch
  while (digitalRead(LEVER_SWITCH_PIN_BOTTOM) == HIGH) {
    if (countTemp < 50) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(6000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(6000);
    }
    else if (countTemp < 200) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(6000 - countTemp * 10);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(6000 - countTemp * 10);
    }
    else {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(4000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(4000);
    }
    countTemp++;
  } 
}

void gateOpen() {
  //  Serial.print("open");
  int countTemp = 0;
  digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
  //rotates until hits limit switch
  while (digitalRead(LEVER_SWITCH_PIN_TOP) == HIGH) {
    if (countTemp < 50) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(6000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(6000);
    }
    else if (countTemp < 200) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(6000 - countTemp * 10);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(6000 - countTemp * 10);
    }
    else {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(4000);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(4000);
    }
    countTemp++;
  }
}
 
