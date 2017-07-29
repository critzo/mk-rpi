# Get build tools and required packages
apt-get update
apt-get install -y automake gcc make libssl-dev libjansson-dev python python-pip paris-traceroute screen

# Build NDT and I2util
cd ~/mlab-ndt
git clone --recursive https://github.com/ndt-project/ndt
cd ~/mlab-ndt/ndt/I2util && ./bootstrap.sh && ./configure && make && make install
cd ~/mlab-ndt/ndt && ./bootstrap && ./configure && make
cd ~/

# Move the NDT Binary (web100clt) to a common location and make a link to it.
# This enables you to run NDT like any other program on your Pi.
mv ~/mlab-ndt/ndt/src/web100clt /opt/web100clt
ln -s /opt/web100clt /usr/local/bin/web100clt

# Install required python libraries
cd ~/mlab-ndt/ndt-runner
pip install pytz tzlocal

# Prepare the Paris Traceroute dataset.
cd ~/mlab-ndt/pt-analysis
python main.py
cp *.csv ~/mlab-ndt/dashboard/data/
