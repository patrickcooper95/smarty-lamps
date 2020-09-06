#! /bin/bash

echo "Starting SmartyLamps in $1 environment."

# Set environment for script and export for Python.
ENVIRONMENT=$1
export ENV=$ENVIRONMENT

# Start the WAPI API and WAPI daemon.
echo "--- Starting Flask API ---"
sudo /home/pi/env/bin/python /home/pi/$ENVIRONMENT/smarty-lamps/run.py &

echo "--- Starting WAPI daemon ---"
sudo /home/pi/env/bin/python /home/pi/$ENVIRONMENT/smarty-lamps/wapid.py

echo "SmartyLamps started. Done."
