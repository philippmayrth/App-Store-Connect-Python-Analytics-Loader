# Overview

A script to download sales data from Apples App Store Connect and load it into a database.


# Installation
  - Get Apples Reporter.jar and place it in the project source dir.
  - Rename ```Reporter.example.properties``` to ```Reporter.properties```
  - Add the API Token to ```Reporter.properties```

# Contributing
You are welcome to contribute to this project.
Just a few things to consider:
  - Please use PEP-8 styling whenever it makes sense (dont overdo it ;-))
  - Please also provide unit tests for the code you write
  - Before commiting write unittests
  - Run the unittests untill everything works before commiting
  - Also note you are required to provide any improvements to this code under the MIT-Licence
  - Feel free to add yourself to the copyright section of the Licence file

# Development
## Install Python Venv
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Testing the code
```
python3 -m unittest
```

# About Apple´s Reporter.jar
This should also run on PC (everything with a Java runtime)
https://help.apple.com/itc/contentreporterguide/en.lproj/static.html
