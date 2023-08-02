import logging
import boto3
from botocore.exceptions import ClientError
import os
from bs4 import BeautifulSoup
import uuid
import requests
from dotenv import load_dotenv

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
    print(AWS_KEY)
    print(AWS_ID)
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