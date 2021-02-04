# edupage-auto-connect


Connects you automatically to online meetings.
For teachers, it shows you are on a lesson by triggering a js switch.
I recommend getting a server where you can run this 24/7.

Installation:
- Install python from https://www.python.org/downloads/
- After installation open cmd, and write the following:
py -m pip install requests&py -m pip install datetime

Usage:
- Update credentials for your edupage in settings.json
- Update school URL in settings.json
- Update lesson times in settings.json
- Run by double-clicking sps.py or py .\main.py in PowerShell.

Troubleshooting:
- Error when running file, module is missing. Install given module using py -m pip install
- Getting error "Trying again.", ur teacher didn't enter the meeting URL or your lesson times are not correct.
