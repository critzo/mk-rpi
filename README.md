# NDT Personal Performance Web Dashboard

This is project is a prototype for a web application that displays the user's Internet performance over time using the Network Diagnostic Tool from Internet2, hosted by M-Lab.

This project consists of three parts:

* dashboard - The web front end that displays the results in a graphical, organized format
* ndt-runner - Python wrapper over the NDT C client. Runs as a daemon collecting NDT results to all local M-Lab servers.
* pt-analysis - Determines the AS paths to the top 500 Alexa sites as well as the AS paths to the nearest M-Lab NDT servers.

# To Run

The steps below work on a Raspberry Pi B (versions 1 and 2), Raspberry Pi 3, and the Odroid C1+. They should work on any Debian Linux system and will likely work on Ubuntu as well. These instructions assume have already prepared your target system (installed OS, set passwords, security, etc.) and are logged into the system as root and are in a terminal in your home folder (i.e. '/root/')

1. Install git: `$ apt install git`
1. Create a folder to store the files in this repo: `$ mkdir mlab-ndt`
1. Clone this repo into this folder: `$ cd mlab-ndt && git clone --recursive git@github.com:critzo/ndt-raspi-prototype.git .`
1. Run _setup.sh_: `$ ./setup.sh` to install required packages, build the NDT C client, and configure the target system.
1. Start collecting NDT results: `$ ./run-ndt.sh` This opens a `screen` session in the background as a daemon, running NDT randomly against the closest 6 M-Lab servers nearest you.
1. Build Paris Traceroute dataset: `$ ./run-pt-analysis.sh` - this will take ~?? minutes. Wait until completed befre moving on.
1. Start the web server: `$ ./start-ndt-dashboard.sh`
1. View results at http://localhost:9000/

# Hacks to be aware of (and fix)

* In `dashboard/index.html` 
  * line 235: start date for data collection is hardcoded
  * lines 100-105: values for the M-Lab servers and their transit providers are hardcoded. 

  Until these are set dynamicall, you will likely want to change these values if you're in a different metro or collecting data from a different date.
