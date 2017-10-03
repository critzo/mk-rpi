# M-Lab Test Runner

This README pertains only to the `mkit` branch and provides and overview of how to setup a Raspberry Pi 3 to serve as an automated M-Lab test runner.

A modified setup script (`setup.sh`) configures a newly installed Raspberry Pi and builds [Measurement Kit](https://github.com/measurement-kit/measurement-kit), a C++ library providing multiple M-Lab and non- M-Lab network measurement tests.

Also included is a Python wrapper (`test-runner/run.py`) which runs the NDT test via Measurement Kit at regular poisson intervals. 

## Installation

* Install the latest Raspbian OS (Debian 9/Stretch) onto an SD card, insert into your Pi, boot it up, configure users, hostname, passwords, etc. to your liking.
* Run updates: `$ sudo apt update && sudo apt upgrade`
* Install git: `$ sudo apt install git`
* Create a folder to store the files in this repo: `$ mkdir mlab-pi`
* Clone this repository into the folder, selecting the `mkit` branch: `$ git clone --recursive git@github.com:critzo/ndt-raspi-prototype.git -b mkit .`
* Run `setup.sh`: `$ sudo ./setup.sh` to install required packages, build the Measurement Kit program, and configure the target system.
* Run `test-runner/run.py` to start automated NDT tests
  * Tp test that everything is working, run this from the root folder of this repo on your pi: `$ python test-runner/run.py`
  * To run the test in the background, use screen: `$ screen -d -m python test-runner/run.py`

We advise you to read the screen manual page: `$ man screen`, but also the commands below will be useful to monitor what screen sessions are running:

* `$ screen -list` - lists all running screen sessions and begins with the screen process ID. Example output: `9281..odroid	(07/30/2017 09:47:25 PM)	(Detached)`
* `$ screen -r 9281` - reattaches you to a specific screen using the screen process ID
* Press `Ctrl a d` to detatch from a screen session and leave it running in the background
* When you log back into your Pi, reconnect to a single running screen session using `$ screen -x`

## TO DO LIST

This branch is intended to fully replace the master branch. This will include:

* Replacing the data dashboard with data from Measurement Kit run tests
* Extending the Paris Traceroute analysis to use a choice of user-provided URLs instead of the Alexa top sites
* Providing support for additional tests through Measurement Kit
* Providing support to post test results to a third party collector
* Providing code and instructions on how to set up a third party collector
* Extend support to other armhf platforms such as Odroid.