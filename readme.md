# atmos
## Summary
This project contains various atmospheric property calculators based on [The US Standard Atmosphere 1976](https://www.pdas.com/atmos.html).
## Dependencies
 - [Python (>=3.4)](https://www.python.org/downloads/)
 - [Numpy](https://numpy.org/doc/stable/reference/)
 - [Matplotlib](https://matplotlib.org/stable/api/index.html)
 - [CoolProp](https://github.com/CoolProp/CoolProp)

## Project Motivation
The US Standard Atmosphere 1976 data is limited to standard atmospheric conditions and quite cumbersome to delve through. This project is meant to provide a means to easily incorporate various aspects of the CoolProp library into calculations that depend on accurate atmospheric calculations.<br>
<br>
Future plans for this project are to create a PyPI installer in order to make this more portable and easy to install in the correct path.

## File Descriptions
Right now the files that we would interact with are:
 - ***StdAtmos.py***<br>Contains StdAtmos class that allows a user to access features of standard atmosphere calculations. This is meant to be a jumping off point since most calculations start with a standard atmosphere component.
 - ***admin.py***<br>Houses quality control methods for improved program functionality.
 - ***constants.py***<br>Many of the manual calculations use universally understood constants. This file is accessed within other files in this project and should be accessed by the user as well for consistent constants and psuedo-constants (i.e. variables that many assume to be constant but have slight variability).
 - ***main.py***<br>This file is a carryover from when this program was create using Java.
 - ***humidity.py***<br>Incorporates humidity calculations utilizing the CoolProp library.

## Licensing and Acknowledgements
[The US Standard Atmosphere 1976](https://www.pdas.com/atmos.html) and [CoolProp](https://github.com/CoolProp/CoolProp) are extensively leveraged and must be given the proper kudos.
