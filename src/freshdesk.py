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

freshdesk_url = "https://sekoia.freshdesk.com/api/v2/tickets?per_page=100"
headers = { 
        "Content-Type": "application/json", 
        "Authorization":os.getenv("FRESHDESK_API_TOKEN")
      }

batch = []

def getBatch(url):
  print("Get page :" + url)
  response = requests.get(url, headers=headers)
  for ticket in response.json():
    resp = es.index(index="freshdesk", id=ticket["id"], document=ticket)
    print(resp)
  if "next" in response.links:
    getBatch(response.links["next"]["url"])


getBatch(freshdesk_url)

