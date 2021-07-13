import json

import requests as requests


def check_EGRUL(query):
    data = {
        "vyp3CaptchaToken": "",
        "page": "",
        "query": query,
        "region": "",
        "PreventChromeAutocomplete": ""
    }
    res = json.loads(requests.post("https://egrul.nalog.ru/", data=data).text)
    t = res['t']
    url = "https://egrul.nalog.ru/search-result/" + t + "?r=1625573233361&_=1625573233361"
    result = requests.get(url).text
    json_res = json.loads(result)
    #print(json.dumps(json_res, ensure_ascii=False, indent=4))
    return json_res
    #print(json.dumps(json_res, ensure_ascii=False, indent=4))
    #return json.dumps(json_res, ensure_ascii=False,indent = 4)


if __name__ == '__main__':
    check_EGRUL("143400305674")