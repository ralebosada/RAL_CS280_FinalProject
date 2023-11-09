import subprocess
import sys
import os

# Installing Necessary Packages
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', '-r' ,package])
# install('requirements.txt')

# Getting API Key from text file
with open('api_key2.txt') as file:
    api_key = file.readlines()
api_key = ' '.join(api_key)

# Connecting with Youtube API
from googleapiclient.discovery import build
import requests


youtube = build('youtube', 'v3', developerKey=api_key)

data = []
pageToken = ''
while True:
    req_search = youtube.search().list(
    part='snippet',
    maxResults=50,
    q='Truth about Martial Law',
    type='video',
    pageToken=pageToken if pageToken != "" else ""
    ).execute()
    temp = req_search.get('items',[])
    if temp:
        data.extend(temp)
    pageToken = req_search.get('nextPageToken')
    if not pageToken:
        break
print(len(data))

thumbnail_links = [items['snippet']['thumbnails']['high']['url'] for items in data]
titles = [items['snippet']['title'] for items in data]
channelIDs = [items['snippet']['channelId'] for items in data]
videoIDs = [items['id']['videoId'] for items in data]

# Saving Paths
thumbnail_path = os.path.join(os.getcwd(), 'data_thumbnails')
title_path = os.path.join(os.getcwd(),'data_titles')
channelID_path = os.path.join(os.getcwd(),'data_channelIDs')
videoID_path = os.path.join(os.getcwd(), 'data_videoIDs')

# Thumbnails
count = 0
for link in thumbnail_links:
    img_name = 'thumbnail' + str(count) + '.jpg'
    img_data = requests.get(link).content
    filename = os.path.join(thumbnail_path, img_name)
    with open(filename, 'wb') as file:
        file.write(img_data)
    count += 1


# Channel IDs
filename = os.path.join(channelID_path, 'channelIDs.txt')
with open(filename, 'w') as file:
    for channelID in channelIDs:
        file.write(channelID)
        file.write('\n')

# Video IDs
filename = os.path.join(videoID_path, 'videoIDs.txt')
with open(filename, 'w') as file:
    for videoID in videoIDs:
        file.write(videoID)
        file.write('\n')

# Titles
filename = os.path.join(title_path, 'titles.txt')
with open(filename, 'w', encoding='utf-8') as file:
    for title in titles:
        file.write(title)
        file.write('\n')

## DESCRIPTION???

# Video ID details

video_details = ','.join(videoIDs)

req_videos = youtube.videos().list(
    part = "snippet, contentDetails, statistics",
    id = video_details
)

# res_videos = req_videos.execute()
# print(res_videos['items'][0].keys())