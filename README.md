# Overview

A script to download sales data from Apples App Store Connect and load it into a database.

# Usage
Supportet Systems:
- macOS 10.13+
- Ubuntu 18.04

Supportet Databases:
- MongoDB

```bash
$ python3 main.py --help
usage: main.py [-h] [--yesterday-daily] [--year YEAR] [--month MONTH]
               [--day DAY] [--period {yearly,monthly,weekly,daily}]
               [--log-level {DEBUG}] [--print] [--dry-run]

Load data from App Store Connect to a database.

optional arguments:
  -h, --help            show this help message and exit
  --yesterday-daily     Import daily data from yesterday.
  --year YEAR           The year for the report.
  --month MONTH         The month for the report.
  --day DAY             The day for the report.
  --period {yearly,monthly,weekly,daily}
                        The period for the report.
  --log-level {DEBUG}   The log level to use.
  --print               Display the report data on screen.
  --dry-run             Dont load data into a database.
```

# Need help?
Feel free to open an issue. We give out best to help you with anything related to this projct.

# Installation
  - Get Apples Reporter.jar and place it in the project source dir.
  - Rename ```Reporter.example.properties``` to ```Reporter.properties```
  - Add the API Token to ```Reporter.properties```
  - Rename ```config.example.json``` to ```config.json```
  - Enter your Apple VendorId in ```config.json``` (See Apples docuemtnation for Reporter.jar about how to get it)
  - Setup dependencies with this:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Commercial Support
You want to run this in productiion and its realy important to work?
Commercial Support is available from https://www.AvalonSoft.de.

# Contributing
You are welcome to contribute to this project.
Just a few things to consider:
  - Please use PEP-8 styling whenever it makes sense (dont overdo it ;-))
  - Please also provide unit tests for the code you write
  - Before commiting write unittests
  - Run the unittests untill everything works before commiting
  - Also note you are required to provide any improvements to this code under the MIT-Licence
  - Feel free to add yourself to the copyright section of the Licence file

## Testing the code
Assuming you already insalled the python environement.

Just running the tests.
```bash
pytest
```

Running the tests and generating a coverage report for it.
```
pytest --cov . --cov-report html
```

Documentation for the coverage reporting https://pytest-cov.readthedocs.io/en/latest/config.html


# Timezones
This framework does its best to handle timezones. However there are limits, mainly because Apple does not tell us the timezones of the dates its more of a educated guess.
See also: https://forums.developer.apple.com/thread/47211

# About Apple´s Reporter.jar
This should also run on PC (everything with a Java runtime)
https://help.apple.com/itc/contentreporterguide/en.lproj/static.html


# Troubleshooting
**Error:** ```AppStoreConnectReporterErrors.AmbiguousAccountNumber: You have access to more than one account. Please specify an account number in your properties file or on the command line. To see a list of accounts, run the command getAccounts.```
**Solution:**
  - Run the command ```java -jar Reporter.jar p=Reporter.properties Sales.getAccounts```
  - You should see a list of all the accounts you have access to now
  - Take the number/id after the comma of the account relevant to you and place it in the ```Reporter.properties``` file in the line that says ```Account=```.

**Sugestion:** *If you need to import the statistics of multiple accounts you have access to you can simply deploy this ETL script into several directories each with a uniqe ```Reporter.properties``` file.*
