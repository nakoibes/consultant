from pprint import pprint

from dadata import Dadata

token = "af2bd19181ddb7d4c79b33595f17d619f4cecabc"
secret = "4c433020a67bb059d1cf22d8c245310bce313c66"
data = Dadata(token, secret)
result = data.find_by_id("party", "7713398595")
pprint(result)
