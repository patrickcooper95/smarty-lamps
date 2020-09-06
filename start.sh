#! /bin/bash

# Put environment configs here

sudo /env/bin/python /$1/smarty-lamps/run.py &
sudo /env/bin/python /$1/smarty-lamps/wapid.py
