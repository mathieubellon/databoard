import requests
import json
import os
import arrow
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ES_CLOUD_ID"),
    basic_auth=("elastic", os.getenv("ES_PASSWORD"))
)

github_url = "https://api.github.com/repos/mathieubellon/app.pilot.pm.old/issues?per_page=100&state=all"

headers = { 
        "Content-Type": "application/json", 
        "Authorization": os.getenv("GITHUB_API_TOKEN") 
      }

batch = []

def getBatch(url):
  print("Get page : " + url)
  response = requests.get(url, headers=headers)
  print(response)
  for issue in response.json():
    resp = es.index(index="github_pilot", id=issue["id"], document=issue)
    print(resp)
  if "next" in response.links:
    getBatch(response.links["next"]["url"])


getBatch(github_url)

