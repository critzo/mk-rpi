FROM resin/raspberrypi3-debian:stretch

ENV INITSYSTEM on

LABEL io.resin.device-type="raspberry-pi"

RUN apt-get update && apt-get install -y git wget build-essential dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 libc++-dev make libssl-dev libevent-dev libgeoip-dev python python-dev python-setuptools virtualenv python-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git

ADD test-runner/requirements.txt /mk-rpi/test-runner/

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig
RUN mv /mk-rpi/measurement-kit/GeoIP* /mk-rpi/test-runner/
RUN virtualenv /mk-rpi/test-runner/
RUN source /mk-rpi/test-runner/bin/activate
RUN pip install -r /mk-rpi/test-runner/requirements.txt

WORKDIR /mk-rpi/test-runner
CMD ["python", "run.py"]
