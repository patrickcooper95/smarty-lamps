![](android-chrome-192x192.png)
# Smarty Lamps 

## Description

A more interactive, personalized LED lighting option.

Using the Python NeoPixel library and a compatible LED strip,
Smarty Lamps becomes a fully-customizable, Wi-Fi accessible lighting
device.

## Getting Started
Clone the repository to `~/DEV`. This will allow you to use the
`start.sh` script to kick off the API and database-watching daemon.
Note: startup documentation is incomplete, as numerous hardware
requirements must be met first (to be detailed later).

## Some Details
The core service is built using Flask API. When the service is running
the endpoints can be viewed and accessed at `[ip address]:5000/swagger`.
From here, the user can add, modify, and delete programs/colors, devices, update devices,
and times (used for clock-based programs).

If a request is received to update a device's current program,
`wapid.py`, the Smarty Lamps daemon, will observe the change
made to the database and carry out this action.

## Models
### Device
In theory, the API can service many devices at once. Multiple devices
can be added via the `devices` endpoint. Changing a device's program
will change the LED's current settings (e.g., `PUT` device_1 to `red`).

`identifier`: `Desk-LED`,  
`name`: `Desk-LED`,  
`device_type`: `lighting`,  
`program`: `blue`,  
`controller_gateway`: `192.168.1.230`  


### Program
Programs represent LED settings. The simplest examples are static colors
such as `blue`: `r`:`0`, `g`:`0`,`b`:`255`. Programs can be python callables
allowing for endless dynamic/changing lighting options on the LEDs.
Further complexity includes designing python callable programs based
on external factors, such as time-based lighting (i.e. lights turn on
at sunset and off at sunrise).

`identifier`: `blue`,  
`r`: `0`,  
`g`: `0`,  
`b`: `255`,  
`callable`: `null`  

#
![](https://www.raspberrypi.org/app/uploads/2017/06/Powered-by-Raspberry-Pi-Logo_Outline-Colour-Screen-500x153.png)
