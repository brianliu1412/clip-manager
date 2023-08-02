import requests
from bs4 import BeautifulSoup
import boto3
import json

URL = "https://uploads.overwolf.com/owclient/direct/2023/07/28/7e52ba47-cf7d-46c0-b640-b95f8c82cfe7.mp4"
FILE_TO_SAVE_AS = "myvideo.mp4" # the name you want to save file as


resp = requests.get(URL) # making requests to server

with open(FILE_TO_SAVE_AS, "wb") as f: # opening a file handler to create new file 
    f.write(resp.content) # writing content to file

a = requests.get(message.content)
soup = BeautifulSoup(a.content, 'html5lib')
links = soup.find_all('video')
for i in links:
    print(i['src'])

