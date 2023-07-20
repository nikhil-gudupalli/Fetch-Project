# Fetch-Project

#1. How would you deploy this application in production?

I could use either terraform or cloud formation for deploying my resource in cloud .If i have to make a decision if all my resources are in AWS i would like to deploy them using Cloudformation.

#2. What other components would you want to add to make this production ready?

Firstly, I would like to test the code in development stage .To get success response i would like to do unit testing , integration testing before deploying into prod

#3. How can this application scale with a growing dataset. 

I would like to host the application in different regions and AZ .As the traffic increases in would like to auto scale my compute resource and memory .If one server fails i would recommend  Application load balancing in routing the traffic.

#4. How can PII be recovered later on?

I would either use KMS  or any other  de-encrypt methods  to retrieve the data

#5. What are the assumptions you made?

Firstly, I want to run glue job from sqs . But AWS dont support direct datasource from SQS. Instead I triggered lambda function to store the messages in S3 in csv or parquet format .Once I did this process I used Data Crawler to get the schema from s3 object and try to store them in Data Catalog .I used pyspark to do transformations and push the output to postgres database.
