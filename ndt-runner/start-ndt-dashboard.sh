#!/bin/sh
cd ~/dashboard
screen -d -m python -m SimpleHTTPServer 9000

cd ~/ndt-runner
screen -d -m python main.py web100clt