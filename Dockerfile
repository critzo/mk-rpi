FROM resin/raspberrypi3-debian:stretch

ENV INITSYSTEM on

LABEL io.resin.device-type="raspberry-pi"

RUN apt-get update && apt-get install -y git wget build-essential dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 libc++-dev make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig && mv GeoIP* ../test-runner/ && cd ../test-runner && pip install -r requirements.txt

CMD ["python", "run.py"]
