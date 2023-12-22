# Install mongodb : 
### Windows : https://www.mongodb.com/docs/v3.0/tutorial/install-mongodb-on-windows/
### Mac : https://www.mongodb.com/docs/v3.0/tutorial/install-mongodb-on-os-x/
### Linux : https://www.mongodb.com/docs/v3.0/administration/install-on-linux/

# Install mongodb compass (mongo UI)
### Install Python (Python3) and pip
PIP is the standard package manager for Python. It is used to install and manage additional packages that are not part of the python standard library. Note: If you have Python version 3.4 or later, PIP is included by default.

> pip install faker

> pip install pymongo

> pip install beautifulsoup4

> pip install pandas

> pip install requests

# Launch data generation
> python generate-trades.py
# Execute aggregation : generate flows grouped by date
> python aggregation-aggregate-by-date.py
# Execute aggregation : generate flows aggregated by tree at a given date, with remaining nominal
> python aggregation-forward.py




