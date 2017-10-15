FROM resin/raspberrypi3-debian:stretch
ENV INITSYSTEM on

RUN apt-get update
RUN apt-get install -qy git wget build-essential dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 libc++-dev make libssl-dev libevent-dev libgeoip-dev dateutils python python-dev python-setuptools python-crypto python-urllib3 python-tz python-tzlocal python-regex paris-traceroute

RUN git clone --recursive https://github.com/critzo/mk-rpi.git

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig
RUN mv /mk-rpi/measurement-kit/GeoIP* /mk-rpi/test-runner/

WORKDIR /mk-rpi/test-runner
CMD ["python", "run.py"]
