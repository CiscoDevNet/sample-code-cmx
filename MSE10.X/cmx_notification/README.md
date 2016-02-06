# Get Notifications

**Description**: You can use CMX to get notifications when traveling through an area. This is applicable to all geo-fencing scenarios. This code example uses a web service to address CMX MSE cross-domain communication. You can also use this example to connect it to your frontend UI.

Possible Application Scenarios:

1. Retail stores can get notifications of incoming customers
2. Queuing systems of service store, bank, etc.

  - **Technology stack**: CMX MSE 10.0, python 3.4.x, noticifcation web service module.
  - **Status**: 1.0
  - **Links to Cisco CMX resource**: To understand more on how CMX works, please visit [DevNet CMX](http://developer.cisco.com/site/cmx-mobility-services/).

## Dependencies

1. This example was developed and tested using Python version 3.4.3. Follow the instructions to [prepare python environment](../../Prepare_Python_Environment/README.MD).
2. The sample code will need a Preconfigured Flask used for RESTful APIs. Use these steps to install:

    In Windows, please use code:

    `pip install flask`

    In Mac OS or Linux, please use code:

    `pip3 install flask`

    or `sudo pip3 install flask`

    If you have any further issues, visit [Flask](http://flask.pocoo.org/)

3. The sample code uses DevNet Sandbox CMX environment (MSE10.0) which is already included in config.ini file.
4. It is recommended that you use [Postman](https://www.getpostman.com/) to test API call.

## What's in this example

1. There are 4 files and 1 folder in this example.
2. File app.py is the business logic. File config.ini is the environment configurations for user to change. File cmxutil.py is none-business-related network request functions. File crosutil.py is Flask cross domain functions.

## Installation

1. Use git clone <repo URL> or download the source code onto your machine.
2. Open the terminal on your machine.
3. Navigate to the directory where you downloaded the code. Your current working directory should be <Downloaded code directory>/sample-code-cmx/MSE10.X/cmx_notification/src
4. Launch server.

    In Windows, please use code:

    `python app.py`

    In Mac OS or Linux, please use code:

    `python3 app.py`

## Usage

**Get all clients, [GET]http://<your IP>:5000/cmx/clients** 
<br>You can use Postman to GET http://127.0.0.1:5000/cmx/clients with header Accept: application/json, Content-Type: application/json. You will get all current wifi clients back in JSON.

**Get info of an area, [GET]http://<your IP>:5000/cmx/areas/<areaID>**
<br>You can use Postman to GET http://127.0.0.1:5000/cmx/areas/area1 with header Accept: application/json, Content-Type: application/json. You will get info of area 1 back in JSON.

**Get all  clients in an area, [GET]http://<your IP>:5000/cmx/clients/area/<areaID>**
<br>You can use Postman to GET http://127.0.0.1:5000/cmx/clients/area/area1, to get the clients information in area1.

**Get area info of target mac address, [GET]http://<your IP>:5000/cmx/areas/mac/<mac_address>**
<br>You can use Postman to GET http://127.0.0.1:5000/cmx/areas/mac/00:00:2a:01:00:37, to get the current area of device with mac address as 00:00:2a:01:00:37. 
You can visit [DevNet Sandbox page](https://msesandbox.cisco.com:8082/demo/start) to get the list of mac addresses to try.

## Configuration

1. You can change the CMX MSE information and your proxy server IP in config.ini file.
2. You can define your own areas in app.py file.

## CMX APIs used

1. [Get real time location for all clients](https://developer.cisco.com/site/cmx-mobility-services/documents/api-reference-manual/index.gsp#get-location)
	`http(s)://<MSE IPADDRESS>/api/location/v2/clients/`

## How to test the software

Not applicable to this sample code.

## Known issues

The response from sandbox can be slow sometimes depending on your network status.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

For general instructions on _how_ to contribute, please visit [CONTRIBUTING](CONTRIBUTING.md).

## Open source licensing info

1. [LICENSE](LICENSE)

## Credits and references

None



