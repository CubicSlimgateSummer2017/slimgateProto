# slimgateProto
Startup:

Run sudo apt-get update and sudo apt-get upgrade on linux to install packages.

Unzip this Slimgate Project.zip on raspberry pi, or clone from github at: https://github.com/CubicSlimgateSummer2017/slimgateProto.git  All files are scripts and ready to run.

To run the program, run bash script with command ./slimgate.sh from the folder. This runs both the gate itself and the flask server.  Code should be run from a raspberry pi, with appropriate packages installed, such as flask, socket.io, gpiozero, etc.  

Programs for motor control and sensor array read are included separately as .ino files as they are uploaded to the Arduino Micros that control them.

Raspberry Pi Code Overview:

*  gate/ - directory that contains all programs relevant to the operation of the gate, its motors and sensors and hardware test programs.
	*  data.txt - data file that allows socket.io bit transfer, there should be a better solution that to do this but linux prevents concurrency issues
	*  run_gate.py - main program that runs the gate, contains gate logic and alarms and deals with all serial readings.

	*  test_gate.py - essentially the same program as run_gate, but with a lot of print statements for debugging purposes.

	*  test_files/ - contains all test programs to test motors, alarms, serial readings, etc
		*  buttonTest.py - test for pushbutton or mock validator
		*  gateTestThread.py - test to use threads to run motor (unsuccessful, ended up using external arduino)
		*  motorSpeedTest.py - test multiple stepper speeds including speed up and speed down
		*  test.py - tests curses key press detection
		*  buzzerTest.py - tests piezo buzzer pattern
		*  ledTest.py - test LED turn on
		*  motorTest2.py - test for motor movement with PWM
		*  writeTest.py - testing writing to serial sensor
		*  gateTest2.py - backup version of state machine simulation
		*  motorClose.py - testing closing motion of gate
		*  motorOpen.py - testing opening motion of gate
		*  readTest.py - testing gathering all sensor readings
		*  gate_test_final.py - final version of gate logic state machine including sensor readings
		*  sensorTest.py - final version of gate state machine simulation

*  webapp/ - directory that contains all programs relevant to the web gui, html templates, and flask server
	*  dataHandler.py - defines a threaded object that handles the reading of data from data.txt in the gate folder
	*  main.py - starts flask server with socket.io, updating the frontend with data from data.txt (which run_gate.py writes into)
	*  static/ - directory containing css files, image files, and other Javascript files like socket.io, boostrap, etc.
	*  templates/ - directory containing html templates to be render by flaks server
		*  display.html - mock lcd screens for dashboard, simulating the two lcd screens on either side of the gate that indicate whether the user would enter
		*  index.html - main dashboard screen, including indicators for all the sensors and keeping track of gate uptime, current state, sensor zone triggers etc.
*  slimgate.sh - main bash file used to start program.  runs run_gate.py in gate directory (gate operation and backend) and main.py in webapp directory (flask server with socket.io)

Arduino Code Overview:

*  StepperTest.ino - First motor/alarm control program with functions set off by Serial readings.  Tried to implement software linear acceleration but ultimately constant speed worked better
*  final_motor_test.ino	- Final motor/alarm control program, uploaded to the board.  Sets off alarm and ran the motors when triggered with certain serial chars.  This step was deemed necessary because context switching in linux caused the need for a new/separate controller for frequency sensitive applications like motor control.
*  limitswitch.ino - test program for reading state of limitswitches
*  sensor_array_readings.ino - final program uploaded to sensors

High Level Architectural Notes:
*  Main program to be run on Pi is run_gate.sh, state machine with infinite while loop collecting data from all sensors.  Current state is represented by a variable, and if statements check the current state and perform transitions if necessary.  Different timers check the amount of times the loop has run and has counters to keep track of the time elapsed.  Serial communication is established between the pi and the arduinos and tera-ranger sensors.  The motor controller arduino will run open the gate upon recieving the char "o" from serial and close the gate upon recieving the char "c" from serial.  Similarly it will start the alarm upon recieving "a" from serial and stop the alarm upon recieving "s" from serial.

Debugging and Troubleshooting:
1.  Check that all USB connections are plugged in.  The blue LEDs from each port on the USB hub need to be on, if they are not on then serial data is not transmitting.

2.  The initialization of the USB ports may change in order, if the sensors are not picking up signal try swapping ports ACM1 and ACM2, or ACM0, etc.  Use web gui to see if sensors are picking up correctly.

3.  If the motor is not working, check the kill switch.  Then check the wiring of the limit switches, if they come off the motor would not run.

4.  If button is not working, check that the button is connected to pin 18 on the raspberry pi (BCM) and the other wire conencted to any GND pin
