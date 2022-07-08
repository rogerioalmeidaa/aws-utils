import boto3
import os

client = boto3.client('s3')
bucket_name = '{{bucket-name}}'
files = []
files_total = 724
last_key = None

print('Getting files names from S3')
while(len(files) < files_total):
    response = client.list_objects(Bucket=bucket_name) if last_key is None else client.list_objects(Bucket=bucket_name, Marker=last_key)
    for item in response['Contents']:
        files.append(item['Key'])
    last_key = files[len(files)-1]

print(files)
print('All of file names were received')

for file_path in files:
    file_path_splitted = file_path.split('/')
    path = file_path_splitted[0:len(file_path_splitted)-1] if len(file_path_splitted) > 1 else file_path_splitted[0]

    if len(file_path_splitted) == 1:
        client.download_file(bucket_name, file_path, 'downloaded/{}'.format(path))
        print('Downloading file: ','downloaded/{}'.format(path))
    
    else:
        path = '/'.join(path)
        if not os.path.exists('downloaded/{}'.format(path)):
            os.makedirs('downloaded/{}'.format(path))
        
        client.download_file(bucket_name, file_path, 'downloaded/{}/{}'.format(path, file_path_splitted[-1]))
        print('Downloading file: ','downloaded/{}/{}'.format(path, file_path_splitted[-1]))