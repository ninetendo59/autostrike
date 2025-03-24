# Auto-Strike
A tool for you to automate download from web directories. (may be enhanced in future)

## Description
The purpose of this tools is to make your life easier in order to downlaod the file from web directory into your local storage.
> Of course, pulling web directory is quite unusual IRL but only those who still uses it 😃
- This application is developed with the aid of AI (30% of the code).

## Key Feature
- Provide the web directory and also the location to downlaod the files and directories, by giving the specific time (minute) to start the process again.
- After files and directories has been downloaded, it will check again after the time interval and download again if size/SHA sum is unmatched, or any newly added directories found in web directories.

## Requirements
- Python version: 3.13 and above
- Operating system: Windows, Linux, macOS

## Installation and Execution
- Create an environment using venv command `python -m venv .venv`
- Activate the environment using 
	- Command Prompt: `.venv\Scripts\activate.bat`
	- Powershell: `.venv\Scripts\Activate.ps1`
	- macOS & Linux: `source .venv/bin/activate`
- Run the following command: `pip install -r requirements.txt`
- To execute script, run
	- Windows: `python .\main.py`
	- Linux & Linux: `python ./main.py`

## License
> None

## Collaborator
> ninetendo59
> ks tan

## Future Plan
- fixes any reported vulnerabilities
- properly sync the local directories based on what available in the web (as for now local directories will not automatically delete files/direcoty that is not available in web directory)
