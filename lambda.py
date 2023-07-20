import boto3
#Here we are trying to trigger sqs with lambda 
#once it invokle lambda function it pushes the message into s3 bucket

s3_client = boto3.client('s3')
def lambda_handler(event, context):
    print(event)
    print(event['Records'])
    print(event['Records'][0]['body'])
    res = event['Records'][0]['body']
    print(type(res))
    
    filename = "filename"
    content ="content"
    print(filename)
        
    bucket_name = 'nikhilrishi'
    key = f'folder-in-s3/{filename}'
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=content)
