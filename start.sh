#! /bin/bash

echo "Starting SmartyLamps in $1 environment."

# export relevant ENV vars
export ENVIRONMENT=$1
export PYTHON_BASE=/home/pi/env/bin

# activate python virtual environment
source $PYTHON_BASE/activate

# Run alembic migrations
echo "--- Applying alembic upgrades, if any ---"
alembic upgrade head

# Start the WAPI API and WAPI daemon.
echo "--- Starting WAPI daemon ---"
python /home/pi/$1/smarty-lamps/wapid.py

echo "--- Starting Flask API ---"
python /home/pi/$1/smarty-lamps/run.py &

echo "SmartyLamps started."
