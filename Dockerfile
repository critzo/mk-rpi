FROM resin/raspberrypi3-debian:stretch

ENV INITSYSTEM on

LABEL io.resin.device-type="raspberry-pi"

RUN apt-get update
RUN apt-get install -qy git wget build-essential dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 libc++-dev make libssl-dev libevent-dev libgeoip-dev python3 python3-dev python3-setuptools pypy python3-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git

# only until this is pushed upstream, after which remove.
ADD test-runner/* /mk-rpi/test-runner/

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig
RUN mv /mk-rpi/measurement-kit/GeoIP* /mk-rpi/test-runner/

RUN pip-3 install -r /mk-rpi/test-runner/requirements.txt

WORKDIR /mk-rpi/test-runner
CMD ["python", "run.py"]
