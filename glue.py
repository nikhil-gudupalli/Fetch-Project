import hashlib
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import udf


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

#function for masking the variables
#example
#payload ={
# "device_id":12222,
# "ip":192.303.233.222,...
# ...
# ..
# }


def transformation(message):
    encrypting_message = hashlib.sha256(message.encode())
    output = encrypting_message.hexdigest()
    return output


#step1
# calling sqs_source with sqs queue url
sqs_source = glueContext.create_dynamic_frame.from_options(
    connection_type="sqs",
    connection_options={
        "sqs.queue.url": "http://localhost:4566/000000000000/login-queue"
    },
    format="json"
)


#step2
#taking the output from sqs and trying to convert it into dataframe and do transformations
df = sqs_source.toDF()
transformation_udf = udf(transformation)
df = df.withColumn("mask_device_id", transformation_udf(df["device_id"]))
df = df.withColumn("mask_ip", transformation_udf(df["ip"]))
df = df.drop("device_id", "ip")



#step3
#writing the dataframe into postgres table

jdbc_url = "jdbc:postgresql://localhost:5432/postgres"
connection_properties = {
    "user": "postgres",
    "password": "postgres"
}
#writing data into postgres
df.write.mode("append").jdbc(jdbc_url, "user_logins", properties=connection_properties)
job.commit()
