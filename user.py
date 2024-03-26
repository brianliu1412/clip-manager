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

def get_item(table_name, userID):
    dynamodb_resource = boto3.resource("dynamodb", "us-east-2")
    table = dynamodb_resource.Table(table_name)
    response = table.get_item(Key={'userID': userID})
    if 'Item' in response.keys():
        return response['Item']
    else:
        return None

def get_num_clips(userID):
    return get_item('clip-manager', userID)['numClips']

def get_clips(userID):
    return get_item('clip-manager', userID)['clips']
        

def check_user_in_table(userID):
    if get_item('clip-manager', userID) == None:
        return False
    else:
        return True
    
def add_clip(table_name, userID, title, clip_link):
    dynamodb_resource = boto3.resource("dynamodb", "us-east-2")
    table = dynamodb_resource.Table(table_name)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    response1 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="SET clips=list_append(:clip, clips)",
        ExpressionAttributeValues={
            ":clip": [{"title": title, "link": clip_link, "timestamp": dt_string}]
        },
        ReturnValues="UPDATED_NEW"
    )
    numClips = get_num_clips(userID) + 1
    response2 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="SET numClips=:n",
        ExpressionAttributeValues={
            ":n": numClips
        },
        ReturnValues="UPDATED_NEW"
    )

def remove_clip(table_name, userID, idx) -> str:
    dynamodb_resource = boto3.resource("dynamodb", "us-east-2")
    table = dynamodb_resource.Table(table_name)

    print("Removing " + str(idx))
   
    response1 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="REMOVE clips[" +str(idx)+ "]",
        ReturnValues="ALL_OLD"
    )
    link = response1['Attributes']['clips'][int(idx)]['link'].split("/")
    url = link[3] + "/" + link[4]
    numClips = get_num_clips(userID)
    numClips = numClips - 1
    response2 = table.update_item(
        Key={'userID' : userID},
        UpdateExpression="SET numClips=:n",
        ExpressionAttributeValues={
            ":n": numClips
        },
        ReturnValues="UPDATED_NEW"
    )
    return url