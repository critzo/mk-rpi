# Get build tools and required packages
apt-get update
apt-get install -y git automake gcc make libssl-dev libjansson-dev python paris-traceroute screen

# Build NDT and I2util
cd ~
git clone --recursive https://github.com/ndt-project/ndt
cd ndt/I2util && ./bootstrap.sh && ./configure && make && make install
cd ~/ndt && ./bootstrap && ./configure && make
cd ~

# Move the NDT Binary (web100clt) to a common location and make a link to it.
# This enables you to run NDT like any other program on your Pi.
mv ndt/src/web100clt /opt/web100clt
ln -s /opt/web100clt /usr/local/bin/web100clt

# Run NDT

# TODO: Add shell command to get the server hostname from mlab-ns instead of hardcoding it
#./src/web100clt -n ndt.iupui.mlab3.lga05.measurement-lab.org
