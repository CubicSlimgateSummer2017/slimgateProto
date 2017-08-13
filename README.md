# slimgateProto

-  gate/
   contains all programs relevant to the operation of the gate, its motors and sensors and hardware test programs.

	-  run_gate.py
	   main program that runs the gate, contains gate logic and alarms and deals with all serial readings.

	-  test_gate.py
	   essentially the same program as run_gate, but with a lot of print statements for debugging purposes.

	-  test_files/
	   contains all test programs to test motors, alarms, serial readings, etc
-  webapp/
   contains all programs relevant to the web gui, html templates, and flask server
