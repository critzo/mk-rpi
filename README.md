# Measurement Kit Rpi (mk-rpi)

`mk-rpi` is a prototype project that automates the setup and installation of network measurement tests on a small computer like a Raspberry Pi, Odroid, or similar. The computer is then connected to an ethernet port or WiFi network, where it runs tests regularly, assessing the speed, quality, and other aspects of its connection to the internet.

Currently, `mk-rpi` supports all tests provided by [Measurement Kit](https://github.com/measurement-kit/measurement-kit), a C++ library providing network measurement tests, and implements one of the supported tests, the Network Diagnostic Tool (NDT). A Python wrapper script (`test-runner/run.py`) runs NDT at regular poisson intervals, saves each test result in JSON format on the computer itself and also submits results to [M-Lab](https://measurementlab.net).

`mk-rpi` is intended to support both individual devices, setup and run by home users, as well as a means of automating many devices for broader research use. The sections below detail _single device setup_ and _device fleet setup_.

## Repository Structure

| File/Folder                  | Description |
|------------------------------|-------------|
| Dockerfile.template          | Dockerfile used for Balena.io device fleet deployment |
| LICENSE.md                   |  |
| @measurement-kit             | Measurement Kit git sub-module. |
| README.md                    |  |
| sample-data                  | Sample data output | 
|   └── ndt-sample-output.txt  |  |
| setup.sh                     | Setup script for single devices |
| test-runner                  |  |
|   ├── run.py                 | Test wrapper for Balena.io device fleet |
|   └── run-single.py          | Test wrapper for single devices |
| WIP                          | Work in progress code. |

## Single Device Setup Alternative

While it is possible to setup mk-rpi on a single device, the project is currently focused on automated fleet deployment for multiple devices. A similar project, [Murkami](https://github.com/m-lab/murakami), was designed for a single device setup.

We currently recommend using Murkami for a single device, though we plan to merge the two intiatives in the future. 

## Device Fleet Setup

### Device Setup and Management

To support and manage multiple measurement devices in the field for specific research projects, we’re using [Balena.io](https://balena.io), which allows us to build our code into a Docker container and push it to a fleet of devices. A "Balena Application” is setup for the production fleet, and another for testing. Each application provides a Git remote URL. Pushing to a Balena git remote triggers an application build on Balena's build service, and then deploys the resulting Docker image(s) to devices assigned to each application. The file `Dockerfile.template` is a Docker Compose file, allowing variables to be used to flexibly deploy to different device architectures from the same code base.

## Supported Network Measurement Tests

Currently the following tests run automatically on a device running this code when deployed to a Balena.io project:

* M-Lab tests:
  * [Network Diagnostic Tool (NDT)](https://www.measurementlab.net/tests/ndt/)
  * [DASH](https://dl.acm.org/citation.cfm?id=2563671)
* Speedtest.net
  * [speedtest-cli](https://github.com/sivel/speedtest-cli)

M-Lab tests are made available by the [Measurement Kit library](https://measurement-kit.github.io). Measurement Kit also supports the [OONI app](https://ooni.torproject.org/nettest/), and a variety of tests available through Measurement Kit have not yet been implemented in this repository.
