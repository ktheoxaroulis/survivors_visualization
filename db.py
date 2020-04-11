import pymongo
import pandas as pd
import os

db_url = os.environ['MONGODB_URL']
client = pymongo.MongoClient(db_url)
db = client["test"]

def get_ep_data():
  df = pd.DataFrame(list(db.users.find()))

  # Remove unnecessary columns
  df = df.drop(["tokens", "__v", "password"], axis=1)

  return df

