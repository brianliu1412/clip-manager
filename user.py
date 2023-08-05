import boto3
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
AWS_KEY = os.getenv("aws_key")
AWS_ID = os.getenv("aws_id")

def add_user(table_name, userID, username):
    dynamodb_resource = boto3.resource("dynamodb", "us-east-2")
    table = dynamodb_resource.Table(table_name)
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_ID
    )
    folder_name = str(userID)
    bucket_name = "clip-manager"
    s3.put_object(Bucket=bucket_name, Key=(folder_name + '/'))
    response = table.put_item(
        Item={
            "userID": userID,
            "username": username,
            "numClips": 0,
            "clips": [],
        },
    )
    print(json.dumps(response, indent=2))

def get_item(table_name, userID):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)
    response = table.get_item(Key={'userID': userID})
    print("Getting Item")
    print(response)
    if 'Item' in response.keys():
        return response['Item']
    else:
        return None

def get_num_clips(table_name, userID):
    return get_item(table_name, userID)['numClips']

def get_clips(table_name, userID):
    return get_item(table_name, userID)['clips']
        

def check_user_in_table(table_name, userID):
    if get_item(table_name, userID) == None:
        return False
    else:
        return True
    
def add_clip(table_name, userID, title, clip_link):
    print(userID)
    dynamodb_resource = boto3.resource("dynamodb", "us-east-2")
    table = dynamodb_resource.Table(table_name)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    response1 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="SET clips=list_append(:clip, clips)",
        ExpressionAttributeValues={
            ":clip": [{"title": title, "link": clip_link, "timestamp": dt_string}]
        },
        ReturnValues="UPDATED_NEW"
    )
    get_num_clips = get_item(table_name, userID)
    numClips = get_num_clips['numClips'] + 1
    response2 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="SET numClips=:n",
        ExpressionAttributeValues={
            ":n": numClips
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response1)
