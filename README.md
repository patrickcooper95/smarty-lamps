# SmartyLamps

## Description

Using the NeoPixel 

All responses will have the form

'''json
{
	"data": "Mixed type holding the content of the response",
	"message": "Description of what happened"
}
'''

Subsequent response definitions will only detail the expected value of the 'data field'

### List All Devices

**Definition**

'GET /devices'

**Response**

- '200 OK' on success

'''json

		{
			"identifier": "floor-lamp",
			"name": "Floor Lamp",
			"device_type": "switch",
			"controller_gateway": "192.168.0.2",
			"program": "pulse"
		}

'''

### Registering a New Device

**Definition**

'POST /devices'

**Arguments**

- '"identifier":string' a globally unique identifier for this device
- '"name":string' a friendly name for this device
- '"device_type":string' the type of the device as understood by the client
- '"controller_gateway":string' the IP address of the device's controller
- '"program":string' the initial display state of the device

If a device with the given identifier already exists, the existing device will be overwritten.

**Response**

- '201 Created' on success

'''json

	{	
			"identifier": "desk-led",
			"name": "Desk LEDs",
			"device_type": "Light",
			"controller_gateway": null,
			"program": null
    }
'''

## Lookup device details

'GET /devices/<identifer>'

**Response**


