#! /bin/bash

sudo /env/bin/python /$1/WAPI/smarty-lamps/run.py &
sudo /env/bin/python /$1/WAPI/smarty-lamps/wapid.py
