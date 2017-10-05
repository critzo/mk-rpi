# Measurement Kit Rpi (mk-rpi)

The mk-rpi repository is prototype code that enables users to set up a Raspberry Pi 3 computer to run available Measurement Kit tests, including NDT from M-Lab.

The current features a setup script (`setup.sh`) configures a newly installed Raspberry Pi and builds [Measurement Kit](https://github.com/measurement-kit/measurement-kit), a C++ library providing network measurement tests.

Also included is a Python wrapper (`test-runner/run.py`) which runs the NDT test via Measurement Kit at regular poisson intervals. By default, the test that will run automatically if you complete these instructions is NDT.

## Getting Started - Setup Your Pi

The first thing to do is install the latest Raspbian OS onto your Pi and configure it to your liking. The remainder of this guide assumes you are logged into your Pi locally or over SSH, running as the `pi` user.

* Install the latest [Raspbian OS (Debian 9/Stretch)](https://www.raspberrypi.org/downloads/raspbian/) onto an SD card, insert into your Pi, boot it up, hostname, passwords, etc. to your liking.
* Run updates: `$ sudo apt update && sudo apt upgrade`
* Install git: `$ sudo apt install git`

## Prepare and Install mk-rpi

* Create a folder to store the files in this repo: `$ mkdir mk-pi && cd mk-pi`
* Clone this repository: `$ git clone --recursive git@github.com:opentechinstitute/mk-rpi.git .`
* Run `setup.sh`: `$ sudo ./setup.sh -u pi` to install required packages, build the Measurement Kit program, and configure the target system. **If you choose to run as a different user than `pi`, replace `pi` with your username in the command above.**
* To test that everything is working, run this from the root folder of this repo on your pi: `$ python test-runner/run.py`. Press Ctrl-C to stop the test runner.
* When you're ready to have the test run in the background, use screen: `$ screen -d -m python test-runner/run.py`

### Using Screen

We advise you to read the screen manual page: `$ man screen`, but also the commands below will be useful to monitor what screen sessions are running:

* `$ screen -list` - lists all running screen sessions and begins with the screen process ID. Example output: `9281..odroid	(07/30/2017 09:47:25 PM)	(Detached)`
* `$ screen -r 9281` - reattaches you to a specific screen using the screen process ID
* Press `Ctrl a d` to detatch from a screen session and leave it running in the background
* When you log back into your Pi, reconnect to a single running screen session using `$ screen -x`

## Future Development - TO DO LIST

The folder `WIP` contains some previous work that we plan to integrate. For now, this folder is a work in progress.

* Provide support to post test results to a third party collector
* Develop a data dashboard with data from Measurement Kit run tests
* Add Paris Traceroute analysis to use a choice of user-provided URLs or Alexa top sites
* Provide support for additional tests through Measurement Kit
* Provide code and instructions on how to set up a third party collector
* Extend support to other armhf platforms such as Odroid