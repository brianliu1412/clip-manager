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
import aiohttp
import asyncio
import aioboto3
import aiofiles




load_dotenv()
AWS_KEY = os.getenv("aws_key")
AWS_ID = os.getenv("aws_id")



async def download_file(url):
    '''
    a = await requests.get(url)
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
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page = await response.read()
            soup = BeautifulSoup(page, 'lxml')
            link = soup.find('video').get('src')
            print(link)
            unique_filename = str(uuid.uuid4()) + ".mp4"
            print(unique_filename)
            async with session.get(link) as video_response:
                video_content = await video_response.read()
                with open(unique_filename, "wb") as f:
                    f.write(video_content)
            return unique_filename

    

async def upload_file(local_path, aws_path, bucket, object_name=None):
    '''
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    args = {'ContentType': 'video/mp4'}
    try:
        
        response = await s3.upload_file(local_path, bucket, aws_path, ExtraArgs=args)
        print(f"File {local_path} uploaded to {bucket}/{AWS_KEY}.")

    except Exception as e:
        print(f"Error uploading file to S3: {e}")
    '''
    args = {'ContentType': 'video/mp4'}
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        try:
            await s3.upload_file(local_path, bucket, aws_path, ExtraArgs=args)
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return
        print(f"File {local_path} uploaded to {bucket}/{AWS_KEY}.")
        return

async def delete_video(aws_path):
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        try:
            await s3.delete_object(Bucket='clip-manager', Key=aws_path)
            print(f"File deleted from clip-manager/{AWS_KEY}.")
        except Exception as e:
            print(f"Error deleting file from S3: {e}")

    