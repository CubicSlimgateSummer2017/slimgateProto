# slimgateProto

To run the program, run bash script with command ./slimgate.sh from the folder. This runs both the gate itself and the flask server.

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
