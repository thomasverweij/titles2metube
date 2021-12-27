import os
import requests
from googleapiclient.discovery import build

def load_titles_from_file(titles):
    with open(titles) as file:
        return file.readlines()

def search_youtube_id(title, youtube):
    print(f"Looking for {title}")
    req = youtube.search().list(q=title,part="id",type="video", maxResults=1)
    res = req.execute()
    return res.get("items")[0].get("id").get("videoId")

def request_metube_download(id):
    print(f"Requesting {id}")
    data = {"url":f"https://www.youtube.com/watch?v={id}","quality":"1080","format":"mp4"}
    r = requests.post("http://metube.verweij.network/add", json=data)
    return r.text

if __name__ == "__main__":
    titles = load_titles_from_file("./titles")
    youtube = build('youtube','v3', developerKey = os.getenv("API_KEY"))
    ids = [search_youtube_id(title, youtube) for title in titles]
    status = [request_metube_download(id) for id in ids]

    if all(list(map(lambda x: x == '{"status": "ok"}', status))):
        print("Success")
    else:
        print("Errors occured")