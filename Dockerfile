FROM resin/raspberrypi3-debian:stretch

LABEL io.resin.device-type="raspberry-pi"

RUN apt-get update && apt-get install -y git wget dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 libc++-dev make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig

RUN mv GeoIP* ../test-runner/ && cd ../test-runner

RUN cd ../test-runner
CMD ["python", "run-tests.py"]