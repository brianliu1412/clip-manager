import logging
import boto3
from botocore.exceptions import ClientError
import os
from bs4 import BeautifulSoup
import uuid
import requests
from dotenv import load_dotenv
import uuid
from urllib.parse import urlparse
from botocore.response import StreamingBody



load_dotenv()
AWS_KEY = os.getenv("aws_key")
AWS_ID = os.getenv("aws_id")



def download_file(url):
    print(url)
    a = requests.get(url)
    page = a.content
    soup = BeautifulSoup(page, 'lxml')
    link = soup.find('video').get('src')
    print(link)
    unique_filename = str(uuid.uuid4()) + ".mp4"
    print(unique_filename)
    resp = requests.get(link) # making requests to server
    with open(unique_filename, "wb") as f: # opening a file handler to create new file 
      f.write(resp.content) # writing content to file
    
    return unique_filename

    

def upload_file(local_path, aws_path, bucket, object_name=None):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    args = {'ContentType': 'video/mp4'}
    try:
        
        response = s3.upload_file(local_path, bucket, aws_path, ExtraArgs=args)
        print(f"File {local_path} uploaded to {bucket}/{AWS_KEY}.")

        '''
        with open(file_name, 'rb') as file:
            s3.upload_fileobj(file, bucket, AWS_KEY)
            print(f"File {file_name} uploaded to {bucket}/{AWS_KEY}.")

        '''
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
'''
def new_upload_file(aws_path, bucket, url, filename):
   
    c = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    b = c.get_bucket(bucket, validate=False)

    r = requests.get(url)
    if r.status_code == 200:
    #upload the file
        k = Key(b)
        k.key = name
        print(r.headers['content-type'])
        print(r.content)
        k.content_type = r.headers['content-type']
        k.set_contents_from_string(r.content)

 
 
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    args = {'ContentType': 'video/mp4'}
    try:
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            print(f"Failed to download file from {url}. Status code: {r.status_code}")
            return
       
        response = s3.upload_fileobj(r.raw, bucket, aws_path, ExtraArgs=args)
        print(f"File uploaded to {bucket}/{AWS_KEY}.")
      
        body = StreamingBody(r.raw, r.headers['content-length'])
        s3.put_object(Bucket=bucket, Key=aws_path, Body=body)
        print(f"Video file uploaded successfully to S3 bucket: {bucket}, Object name: {aws_path}")

    except Exception as e:
        print(f"Error uploading file to S3: {e}")



    s3=boto3.client('s3')
    http=urllib3.PoolManager()
    s3.upload_fileobj(http.request('GET', url, preload_content=False), bucket, aws_path)
 
'''

def delete_video(aws_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    try:
        response = s3.delete_object(Bucket='clip-manager', Key=aws_path)
        print(f"File deleted from clip-manager/{AWS_KEY}.")

    except Exception as e:
        print(f"Error deleting file from S3: {e}")