#!/bin/sh
cd ~/mlab-ndt/dashboard
screen -d -m python -m SimpleHTTPServer 9000

cd ~/mlab-ndt/ndt-runner
screen -d -m python main.py web100clt