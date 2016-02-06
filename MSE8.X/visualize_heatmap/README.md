# Display a Heat Map

**Description**: This example shows how to use CMX to display a heat map based on the density of the devices. It uses the CMX API to retrieve device data that is rendered using the Heatmap.js library.

Possible Application Scenarios:

1. Display the popularity of an area.
2. Indoor route planning.
3. Analyze user activities.

  - **Technology stack**: CMX MSE 8.0, Html + JavaScript, Front End UI module.
  - **Status**: 1.0
  - **Links to Cisco CMX resource**: To understand more on how CMX works, please visit [DevNet CMX](http://developer.cisco.com/site/cmx-mobility-services/).

## Dependencies

1. This example was developed and tested using Python version 3.4.3. Follow the instructions to [prepare python environment](../Prepare_Python_Environment/README.md).
2. The sample code will need a proxy server to address CMX MSE cross-domain communication. Follow the instructions in the [CMX notification sample code](../cmx_notification) to launch the server.
3. The sample code uses DevNet Sandbox CMX environment (MSE8.0) which is already inclued in config.ini file in [CMX notification sample code](../../cmx_notification).
4. This example also utilizes Heatmap.js v2.0.0 JavaScript library which is already included.
5. It is recommended that you use Chrome or Safari when running the server on your machine.

## What's in this example

This example includes a file Index.html for Front End UI, and a heatmap.js in the lib folder.

## Installation

1. Install and launch the proxy server. To do so, follow the steps in [CMX notification sample code](../cmx_notification).
2. Use git clone <repo URL> or download the source code of this example onto your machine. If you have any issues, visit [Clone a repository](https://help.github.com/articles/cloning-a-repository/)
3. Open another terminal on your machine.(You should already have your 1st terminal running app.py as proxy server from step 1)
4. Navigate to the directory where you downloaded the code in the newly openned terminal. Your current working directory should be <Downloaded code directory>/sample-code-cmx/MSE8.X/visualize_heatmap/src.
5. Start a web server. In this sample code, we use a python HTTPServer from the project directory root:

    In Windows, please use code:

    `python -m http.server 1337 &`

    In Mac OS or Linux, please use code:

	`python3 -m http.server 1337 &`

6. Launch your Chrome or Safari browser to the following URL:

	`http://localhost:1337`

	The browser will render `index.html`.

## Usage

This example can be used independently as a Front End visualization tool.

## Configuration

1. You can change the CMX MSE information and/or specify different floor map in config.ini file in [CMX notification sample code](../cmx_notification).

## CMX APIs Used

None

## How to test the software

Not applicable to this sample code.

## Known issues

1. The response from sandbox can be slow sometimes depending on your network status.
2. The mobility simulation service for MSE8.X may not be stable some times. We suggest you change the environment to your own CMX setup and then run the code.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

For general instructions on _how_ to contribute, please visit [CONTRIBUTING](CONTRIBUTING.md).

## Open source licensing info

1. [LICENSE](LICENSE)

## Credits and references

None
