# Get build tools and required packages
apt-get update
apt-get install -y dh-autoreconf autoconf automake libtool gcc make libssl-dev libevent-dev libgeoip-dev python python-pip paris-traceroute screen

# Build MeasurementKit
cd ~/measurement-kit
./autogen.sh
./configure
make 
make install
ldconfig

# Move the GeoIP files that MeasurementKit needs into a common folder
mv GeoIP* ~/mlab-pi/test-runner/

# leftover from mtlynch's ndt python wrapper - needed for display?
# Install required python libraries
cd ~/mlab-pi/test-runner
pip install pytz tzlocal

# Setup data folder and starter files
mkdir ~/mlab-pi/dashboard/data
touch ~/mlab-pi/dashboard/data/ndt-history.csv
echo "date,ndt_server,upload_throughput,download_throughput" >> ~/mlab-ndt/dashboard/data/ndt-history.csv
touch ~/mlab-pi/dashboard/data/mlab-pt-paths.csv
touch ~/mlab-pi/dashboard/data/alexa-pt-paths.csv