# Install mongodb : 
### Windows : https://www.mongodb.com/docs/v3.0/tutorial/install-mongodb-on-windows/
### Mac : https://www.mongodb.com/docs/v3.0/tutorial/install-mongodb-on-os-x/
### Linux : https://www.mongodb.com/docs/v3.0/administration/install-on-linux/

# Install mongodb compass (mongo UI)
### Install Python (Python3) and pip
### There will be some python libs that need to be installed using pip (See errors at first launch)

# Launch data generation
> python generate-trades.py
# Execute aggregation : generate flows grouped by date
> python aggregation-aggregate-by-date.py
# Execute aggregation : generate flows with remaining nominal at date
> python  (output output-forward.json) 



