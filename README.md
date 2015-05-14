# NDT Personal Performance Web Dashboard

This is project is a prototype for a web application that displays the user's Internet performance over time.

This project consists of three parts:

* dashboard - The web front end that displays the results in a graphical, organized format
* ndt-runner - Python wrapper over the NDT C client. Runs as a daemon collecting NDT results to all local M-Lab servers.
* pt-analysis - Determines the AS paths to the top 500 Alexa sites as well as the AS paths to the nearest M-Lab NDT servers.

# To Run

The steps below work on a Raspberry Pi B (versions 1 and 2). They should work on any Debian Linux system and will likely work on Ubuntu as well.

1. Build the NDT C client: `sudo ndt-runner/build-ndt.sh`
1. Start collecting NDT results: `cd ndt-runner; screen python main.py /path/to/web100clt`
1. Install paris-traceroute
1. Build PT dataset: `cd pt-analysis; sudo python main.py`
1. Copy PT data to the web dashboard: `cp *.csv dashboard/data/`
1. Start the web server: `cd dashboard; python -m SimpleHTTPServer 9000`
1. View results at http://localhost:9000/

# Hacks to be aware of
In a few places, I've hardcoded the start date when I started collecting data (2015-03-22) or the metro I'm using (lga) or the transit providers for my specific metro (Tata, Internap, etc.). You will likely want to change these values if you're in a different metro or collecting data from a different date.
