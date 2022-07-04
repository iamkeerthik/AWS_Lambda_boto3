# AWS_Lambda_boto3
AWS Lambda with boto3 real life use cases

1. Deregister ami and delete snapshot
A lambda function that deregister 30 days old ami and delete snapshots based on resource tag


2.Import csv file to dynamodb table
simple python code to import a csv file to dynamodb table 
in csv file 2 nd row must contain data type of a field

>>> python importToDynamo.py <csv data file> <table name>
ex: python importToDynamo.py test.csv test
