import boto3
import csv

client = boto3.client('s3')
bucket_name = '{{bucket-name}}'
files = [['Links']]
files_total = 3851
last_key = None

print('Getting files names from S3\n')
count = 0
while(len(files) < files_total):
    response = client.list_objects(Bucket=bucket_name) if last_key is None else client.list_objects(Bucket=bucket_name, Marker=last_key)
    if response['Contents']:
        last_key = response['Contents'][len(response['Contents'])-1]['Key']
        for item in response['Contents']:
            files.append(['http://bucket.s3.amazonaws.com/{0}'.format(item['Key'])])
            print('Processing File: {0}'.format(item['Key']))

print('\nAll Links: \n')
print(files)
print('\nAll of file paths were received')

with open('s3-assets.csv', 'w') as _file:
    writer = csv.writer(_file)
    writer.writerows(files)
