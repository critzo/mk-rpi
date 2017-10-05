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
cd /home/$USER/mlab-pi/measurement-kit
./autogen.sh
./configure
make 
make install
ldconfig

# Move the GeoIP files that MeasurementKit needs into a common folder
mv GeoIP* /home/$USER/mlab-pi/test-runner/

# leftover from mtlynch's ndt python wrapper - needed for display?
# Install required python libraries
cd /home/$USER/mlab-pi/test-runner
pip install pytz tzlocal

# Setup data folder and starter files
mkdir /home/$USER/mlab-pi/dashboard/data
touch /home/$USER/mlab-pi/dashboard/data/ndt-history.csv
echo "date,ndt_server,upload_throughput,download_throughput" >> /home/$USER/mlab-ndt/dashboard/data/ndt-history.csv
touch /home/$USER/mlab-pi/dashboard/data/mlab-pt-paths.csv
touch /home/$USER/mlab-pi/dashboard/data/alexa-pt-paths.csv