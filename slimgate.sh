#!/bin/bash

cd gate/
python run_gate.py &
cd ..
cd webapp/
python main.py &
cd ..
