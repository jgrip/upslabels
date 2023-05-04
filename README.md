# upslabels
Small local service to print UPS thermal labels on linux

A small flask application that allows printing thermal labels from UPS on linux.

UPS has a java based application that runs on windows to allow printing thermal labels from their web page.
It works by running a small web service in port 4349 on the local machine, that can enumerate printers and find matching ones.

This is a reimplementation of this web service.

# Usage
This application requires the `flask` and `sh` python modules to be installed in advance.

This can be done either using `pipenv` in the repo or installing the system packages for these modules:
`sudo apt install python3-flask python3-sh`

Once installed, you can run the application by just calling `python3 upslabels.py` before printing labels on the UPS web page.
