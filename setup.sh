while getopts u: option
do
 case "${option}"
 in
 u) USER=${OPTARG};;
 esac
done

# Get build tools and required packages
apt-get update
apt-get install -y git dh-autoreconf autoconf automake libtool gcc make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

# Build MeasurementKit
cd /home/$USER/mk-pi/measurement-kit
./autogen.sh
./configure
make 
make install
ldconfig

# Move the GeoIP files that MeasurementKit needs into a common folder
mv GeoIP* /home/$USER/mk-pi/test-runner/

# leftover from mtlynch's ndt python wrapper - needed for display?
# Install required python libraries
cd /home/$USER/mk-pi/test-runner
pip install pytz tzlocal
