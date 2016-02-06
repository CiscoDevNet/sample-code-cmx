# Track a Single Client

**Description**: This example will query the CMX for the history of motions of a device(mac address is specified in the config file) using an API and then use a visualization tool to present device location in a intuitive graphic way. This example uses the Plotly Framework as a visualization tool to show the motion of the device. The history of clients could be used in various scenarios such as visulaizing the motion of the user and identifying the populated areas, or perform some statistics on the users motion data and then can have some frontend application showing the results in the form of 2D, 3D graphs or may be visualizing the results in a tabular way etc.

**Possible Application Scenarios:**

1. Set a particular time window for the history data.
2. Try different path visualization tools instead of Plotly.

  - **Technology stack**: CMX MSE 8.0, python 3.4.3
  - **Status**: 1.0
  - **Links to Cisco CMX resource**: To understand more on how CMX works, please visit [DevNet CMX](http://developer.cisco.com/site/cmx-mobility-services/).

## Dependencies

1. This example was developed and tested using Python version 3.4.3. Follow the instructions to [prepare python environment](../../Prepare_Python_Environment/README.md).
2. The sample code will need following python libraries:
    - **XML Python parser in case you are using XML response.**
        
        In Windows, please use code:

        `pip install beautifulsoup4`
        
        In Mac OS or Linux, please use code:
        
        `pip3 install beautifulsoup4`
        
        or `sudo pip3 install beautifulsoup4`
        
        If you have any further issues, visit [Beautiful Soup Documentation](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
        
    - **JSON Python parser in case you are using JSON response.**
    
        In Windows, please use code:

        `pip install json`
        
        In Mac OS or Linux, please use code:
        
        `pip3 install json`
        
        or `sudo pip3 install json`
        
        You can get the json python source library at         [json-py](http://sourceforge.net/projects/json-py/)
        
    - **Plotly library (7.1.2) for map to be displayed.**
    
        In Windows, please use code:

        `pip install plotly`
        
        In Mac OS or Linux, please use code:
        
        `pip3 install plotly`
        
        or `sudo pip3 install plotly`
        
        If you have any further issues, visit  [Getting Started: Plotly for Python](https://plot.ly/python/getting-started/)
    
3. The sample code uses DevNet Sandbox CMX environment (MSE8.0) which is already included in config.ini file. You can visit [DevNet Sandbox page](https://msesandbox.cisco.com:8082/demo/start) to get the list of mac addresses to try.

## What's in this example

1. There are 2 files inside the src folder.
2. File track_single_client.py is the business logic. File config.ini is the environment configurations for user to change.

## Installation

1. Use git clone <repo URL> or download the source code onto your machine. If you have any issues, visit [Clone a repository](https://help.github.com/articles/cloning-a-repository/)
2. Open the terminal on your machine.
3. Navigate to the directory where you downloaded the code. Your current working directory should be <Downloaded code directory>/sample-code-cmx/MSE8.X/track_single_client/src
4. Run the file track_single_client.py by issuing the following command:

    In Windows, please use code:

    `python track_single_client.py`

    In Mac OS or Linux, please use code:

    `python3 track_single_client.py`
    
5. **Output :** On running this program, you will see your web browser automatically opens a web page showing the users motion on the Plotly Web Framework. You do not need to enter the URL in the browser and the web page will automatically open in the browser.

## Usage

This code example uses the CMX API to retrieve location data that is rendered using the Plotly library. You can also extend this example to calculate statistics on the movement of users.

## Configuration

1. You can change the CMX MSE information and other information such as Mac address to track or the response_format from the MSE in config.ini file. 
2. Visit [DevNet Sandbox page](https://msesandbox.cisco.com:8082/demo/start) to get the list of mac addresses to try.

## CMX APIs used

1. [Get history of the locations visited by the device to be tracked](https://developer.cisco.com/site/cmx-mobility-services/documents/api-reference-manual/index.gsp#get-location-history)
    `http(s)://<MSE IPADDRESS>/api/contextaware/v1/location/history/clients/<MAC-ADDRESS>`


## How to test the software

Not applicable to this sample code.

## Known issues

1. The response from sandbox can be slow sometimes depending on your network status. Sometimes it may take several minutes for web-browser to open the web page.
2. The mobility simulation service for MSE8.X may not be stable some times. We suggest you change the environment to your own CMX setup and then run the code.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

## Getting involved

For general instructions on _how_ to contribute, please visit [CONTRIBUTING](CONTRIBUTING.md).

## Open source licensing info

1. [LICENSE](LICENSE)

## Credits and references

None
