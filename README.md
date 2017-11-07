# Measurement Kit Rpi (mk-rpi)

`mk-rpi` is a prototype project that automates the setup and installation of network measurement tests on a small computer like a Raspberry Pi, Odroid, or similar. The computer is then connected to a wired ethernet port on a router, where it runs tests regularly, assessing the speed, quality, and other aspects of its connection to the internet.

Currently, `mk-rpi` supports all tests provided by [Measurement Kit](https://github.com/measurement-kit/measurement-kit), a C++ library providing network measurement tests, and implements one of the supported tests, the Network Diagnostic Tool (NDT). A Python wrapper script (`test-runner/run.py`) runs NDT at regular poisson intervals, saves each test result in JSON format on the computer itself and also submits results to [M-Lab](https://measurementlab.net).

`mk-rpi` is intended to support both individual devices, setup and run by home users, as well as a means of automating many devices for broader research use. The sections below detail _single device setup_ and _device fleet setup_.

## Repository Structure

| File/Folder                  | Description |
|------------------------------|-------------|
| Dockerfile.template          | Dockerfile used for Resin.io device fleet deployment |
| LICENSE.md                   |  |
| @measurement-kit             | Measurement Kit git sub-module. |
| README.md                    |  |
| sample-data                  | Sample data output | 
│   └── ndt-sample-output.txt  |  |
| setup.sh                     | Setup script for single devices |
| test-runner                  |  |
│   ├── run.py                 | Test wrapper for Resin.io device fleet |
│   └── run-single.py          | Test wrapper for single devices |
| WIP                          | Work in progress code. |

## Single Device Setup

To setup and run `mk-rpi` on a single device, we provide a setup script (`setup.sh`) to configure a newly installed Raspberry Pi 3. Other platforms such as Odroid, or better resourced computers will likely also work provided they are running Debian 9/Stretch. We have tested single device setup with the Rpi3 thus far.

* Install the latest [Raspbian OS (Debian 9/Stretch Lite)](https://www.raspberrypi.org/downloads/raspbian/) onto an SD card, insert into your Pi, boot it up, hostname, passwords, SSH access, etc. to your liking.
* Run updates: `$ sudo apt update && sudo apt upgrade`
* Install git: `$ sudo apt install git`

The remainder of this guide assumes you are logged into your Pi locally or over SSH, running as the `pi` user with a terminal open to `/home/pi/`.

### Prepare and Install mk-rpi

* Create a folder to store the `mk-rpi` code: `$ mkdir mk-pi && cd mk-pi`
* Clone this repository: 
`$ git clone --recursive git@github.com:opentechinstitute/mk-rpi.git . `
**Note that the ` . ` at the end of this command is not punctuation, but is a part of the command** 
* Run `setup.sh`: `$ sudo ./setup.sh -u pi` to install required packages, build the Measurement Kit program, and configure the target system. **If you choose to run as a different user than `pi`, replace `pi` with your username in the command above.**
* To test that everything is working, run this from the root folder of this repo on your pi (/home/pi/mk-pi/): `$ python test-runner/run-single.py`. An NDT test should run, and then a waiting message should appear in the terminal, similar to this: ` ... INFO Sleeping for 481 seconds ...`. 
* Press Ctrl-c to stop the test runner.
* When you're ready to have the test run in the background, use screen:
`$ screen -d -m python test-runner/run-single.py`

### Accessing Test Result Data

For Single Devices, test results are saved on the Rpi in the folder where the test is run. If using the defaults outlined above, that is in `/home/pi/mk-pi/`. Test result filename look something like this: `report-ndt-2017-10-03T191408Z-0.njson`

### Using Screen

We advise you to read the screen manual page: `$ man screen`, but also the commands below will be useful to monitor what screen sessions are running:

* `$ screen -list` - lists all running screen sessions and begins with the screen process ID. Example output: `9281..odroid	(07/30/2017 09:47:25 PM)	(Detached)`
* `$ screen -r 9281` - reattaches you to a specific screen using the screen process ID
* Press `Ctrl a d` to detatch from a screen session and leave it running in the background
* When you log back into your Pi, reconnect to a single running screen session using `$ screen -x`

## Device Fleet Setup

### Device Setup and Management

To support and manage multiple measurement devices in the field for specific research projects, we’re using [Resin.io](https://resin.io), which allows us to build our code into a Docker container and push it to a fleet of devices. A "Resin Application” is setup for each type of device architecture. Each application provides a Git remote URL. The file `Dockerfile.template` is used by Resin to build and deploy code to multiple device architectures. This file is not used when using `mk-rpi` on a single device as described above. So far we’ve tested two applications, one for a Raspberry Pi 3 and another for an Odroid C1/C1+. When our code is pushed to the Git remote for Rpi3's a container is built and pushed to our Rpi3 devices. Likewise for the Odroid application's Git remote. 

Read more about using Resin.io generally in our [blog post](https://opentechinstitute.github.io/2017/10/deploying-and-managing-a-fleet-of-measurement-kit-devices/).

### Data Collection Server and Visualization

For our fleet deployment devices, a separate test runner script is used (`/test-runner/run.py`) which saves test results on-device and submits them to M-Lab, but also pushes each result from each device to a central [Prometheus](https://prometheus.io/) server. We also then can visualize the metrics collected by deployed devices using [Grafana](https://grafana.com/).

## Future Development - TO DO LIST

### General TO DOs

* Provide support for additional tests through Measurement Kit
* Provide support for additional tests from other providers
* Add Paris Traceroute analysis to use a choice of user-provided URLs or Alexa top sites

### Single Device

* Add a systemd service daemon instead of using screen
* Add support for an on-device data dashboard

### Device Fleet

* Provide code and instructions on how to set up a third party collector
* Provide support to post test results to a third party collector
* Develop a data dashboard with data from other Measurement Kit tests and other open source tests