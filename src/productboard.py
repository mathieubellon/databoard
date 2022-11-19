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

url = "https://api.productboard.com/features"

headers = { 
        "Content-Type": "application/json", 
        "Authorization": os.getenv("PRODUCTBOARD_TOKEN"),
        "X-Version" : "1" 
      }

batch = []

def getBatch(url):
  print("Get page : " + url)
  response = requests.get(url, headers=headers)
  print(response.json()["data"])
  for feature in response.json()["data"]:
    resp = es.index(index="productboard", id=feature["id"], document=feature)
    print(resp)
  if "next" in response.json()["links"]:
    getBatch(response.json()["links"]["next"])


getBatch(url)

