FROM resin/odroid-c1-debian:stretch
# Enable systemd
ENV INITSYSTEM on
# Your code goes here

RUN apt-get update && apt-get install -y git wget dh-autoreconf autoconf automake libtool gcc make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git
RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig

RUN mv GeoIP* ../test-runner/ && cd ../test-runner

CMD ["python", "run-tests.py"]