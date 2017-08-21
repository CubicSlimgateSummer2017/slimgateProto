 /*
   This code reports raw readings from 5 sensors each cycle and prints to serial monitor
   Visual Studio program can pick this up and write to csv file
*/

#include <Wire.h>
#include <VL53L0X.h>
#include <math.h>

VL53L0X sensor1;
VL53L0X sensor2;
VL53L0X sensor3;
VL53L0X sensor4;
VL53L0X sensor5;

int zone1 = 0;
int zone2 = 0;

int Shutdown1 = 8;//shutdown pins used on Arduino
int Shutdown2 = 9;
int Shutdown3 = 10;
int Shutdown4 = 11;
int Shutdown5 = 12;
int i = 0;

double read1, read2, read3, read4, read5;

//these are the physical coordinates of the sensors on PCB in mm
double sensor1_x = 67;
double sensor1_y = 10;
double sensor2_x = 56;
double sensor2_y = 28;
double sensor3_x = 44;
double sensor3_y = 45;
double sensor4_x = 27;
double sensor4_y = 65;
double sensor5_x = 5;
double sensor5_y = 60;

//find the angle sensors are pointing at
double sensor1_angle =  atan(sensor1_y / sensor1_x);
double sensor2_angle =  atan(sensor2_y / sensor2_x);
double sensor3_angle =  atan(sensor3_y / sensor3_x);
double sensor4_angle =  atan(sensor4_y / sensor4_x);
double sensor5_angle =  atan(sensor5_y / sensor5_x);

//set the max range
double sensor1_max  = 1000;
double sensor2_max  = 1000;
double sensor3_max  = 1000;
double sensor4_max  = 1000;
double sensor5_max  = 1000;

void setup()
{
  Serial.begin(115200);
  Wire.begin();

  //turn all sensors off first
  pinMode(Shutdown1, OUTPUT);
  pinMode(Shutdown2, OUTPUT);
  pinMode(Shutdown3, OUTPUT);
  pinMode(Shutdown4, OUTPUT);
  pinMode(Shutdown5, OUTPUT);
  digitalWrite(Shutdown1, LOW);
  digitalWrite(Shutdown2, LOW);
  digitalWrite(Shutdown3, LOW);
  digitalWrite(Shutdown4, LOW);
  digitalWrite(Shutdown5, LOW);

  //turn sensor 1 on, initialize comm and set address, then stays on
  digitalWrite(Shutdown1, HIGH);
  sensor1.init();
  sensor1.setTimeout(500);
  sensor1.startContinuous();
  sensor1.setAddress(0x30);

  //turn sensor 2 on, initialize comm and set address, then stays on
  digitalWrite(Shutdown2, HIGH);
  sensor2.init();
  sensor2.setTimeout(500);
  sensor2.startContinuous();
  sensor2.setAddress(0x31);

  //turn sensor 3 on, initialize comm and set address, then stays on
  digitalWrite(Shutdown3, HIGH);
  sensor3.init();
  sensor3.setTimeout(500);
  sensor3.startContinuous();
  sensor3.setAddress(0x32);

  //turn sensor 4 on, initialize comm and set address, then stays on
  digitalWrite(Shutdown4, HIGH);
  sensor4.init();
  sensor4.setTimeout(500);
  sensor4.startContinuous();
  sensor4.setAddress(0x33);
  
  //turn sensor 5 on, initialize comm and set address, then stays on
  digitalWrite(Shutdown5, HIGH);
  sensor5.init();
  sensor5.setTimeout(500);
  sensor5.startContinuous();
  sensor5.setAddress(0x34);

  //Here set the timing budgets of each reading in ns
  //default is ~30ms, higher for more accuracy, lower for higher speed
  //lowest is about 20ms
  sensor1.setMeasurementTimingBudget(40000);
  sensor2.setMeasurementTimingBudget(40000);
  sensor3.setMeasurementTimingBudget(40000);
  sensor4.setMeasurementTimingBudget(40000);
  sensor5.setMeasurementTimingBudget(40000);
}

void loop()
{
  //******************read distance************
  read1 = sensor1.readRangeContinuousMillimeters();
  read2 = sensor2.readRangeContinuousMillimeters();
  read3 = sensor3.readRangeContinuousMillimeters();
  read4 = sensor4.readRangeContinuousMillimeters();
  read5 = sensor5.readRangeContinuousMillimeters();

  //******************filter out of range reading****
  if (read1 > sensor1_max)
  {
    read1 = sensor1_max;
  }
  if (read2 > sensor2_max)
  {
    read2 = sensor2_max;
  }
  if (read3 > sensor3_max)
  {
    read3 = sensor3_max;
  }
  if (read4 > sensor4_max)
  {
    read4 = sensor4_max;
  }
  if (read5 > sensor5_max)
  {
    read5 = sensor5_max;
  }
  
  if (read1 <= sensor1_max - 100 ||
      read2 <= sensor2_max - 100) {
    
    zone1 = 1;
  }
  else {
    zone1 = 0;
  }
  if (read3 <= sensor3_max - 100 ||
      read4 <= sensor4_max - 100 ||
      read5 <= sensor5_max - 100) {
      zone2 = 1;
  }
  else {
    zone2 = 0;
  }


  //***************report coordinates***********


  Serial.print("Zone 1: ");
  Serial.print(zone1);
  Serial.print(" ");
  Serial.print("Zone 2: ");
  Serial.print(zone2);
  Serial.print(" ");
  //Serial.print("Readings: ");
  Serial.print(read1);
  Serial.print(",");
  Serial.print(read2);
  Serial.print(",");
  Serial.print(read3);
  Serial.print(",");
  Serial.print(read4);
  Serial.print(",");
  Serial.print(read5);
  Serial.println();
}












