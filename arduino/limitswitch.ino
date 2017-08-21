#define LEVER_SWITCH_PIN 2
#define LEVER_SWITCH_PIN2 3
int pressSwitch = 0;
int pressSwitch2 = 0;

void setup()
{
  Serial.begin(9600);
}
 
void loop()
{
  pinMode(LEVER_SWITCH_PIN,INPUT);
  pinMode(LEVER_SWITCH_PIN2,INPUT);
  
  pressSwitch = digitalRead(LEVER_SWITCH_PIN);
  pressSwitch2 = digitalRead(LEVER_SWITCH_PIN2);
  if(pressSwitch == LOW)
    {
      Serial.println("low");
      delay(500);
    }
  else if(pressSwitch2 == LOW)
  {
    Serial.println("low2");
    delay(500);
  }
}

