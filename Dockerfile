FROM resin/raspberrypi3-alpine

LABEL io.resin.device-type="raspberry-pi"

RUN apk add --update \
		less \
		nano \
		net-tools \
		ifupdown \		
		usbutils \
		gnupg \
		raspberrypi \
		raspberrypi-libs \
		raspberrypi-dev \
	&& rm -rf /var/cache/apk/*

RUN apt-get update && apt-get install -y git wget dh-autoreconf autoconf automake libtool gcc gcc-6 g++-6 make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

RUN git clone --recursive https://github.com/opentechinstitute/mk-rpi.git

RUN cd mk-rpi/measurement-kit && ./autogen.sh && ./configure && make && make install && ldconfig

RUN mv GeoIP* ../test-runner/ && cd ../test-runner

RUN cd ../test-runner
CMD ["python", "run-tests.py"]