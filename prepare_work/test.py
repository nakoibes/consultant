import json
from pprint import pprint
from pymongo import MongoClient
import requests
import json

mongo_client = MongoClient(host="localhost", port=27017)
db = mongo_client.get_database("consultant")
key = "466c09ea169672bed651f6a4a9a90d1f73a4ad73"
# q = "Сбербанк"
q = "Гроднева Галина Александровна"
# inn = "7713398595"
inn = "7709750937"
j = {"inn": "614570014372",
     "requestDate": "2021-06-06"}
# r = requests.get(f"https://api-fns.ru/api/check?req={inn}&key={key}", )
# r = requests.get(f"https://api-fns.ru/api/check?req={inn}&key={key}", )
#r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={key}", )
#r = requests.get(f"https://api-fns.ru/api/fl_status?inn={inn}&key{key}", )
# r = requests.get(f"https://api-fns.ru/api/search?q={q}&key={key}", )
# r = requests.get(f"https://api-fns.ru/api/fl_status?inn=614570014372&key={key}")
# r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={key}",)
# r = requests.post("https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status", json=j)
r = requests.get(f"https://api-fns.ru/api/egr?req={inn}&key={key}", )
text = r.text

db.get_collection("col").insert_one(json.loads(text))
pprint(r.json())
