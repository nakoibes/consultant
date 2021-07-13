import json
from pprint import pprint

from bs4 import BeautifulSoup
import requests
from requests import session


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
    # print(json.dumps(json_res, ensure_ascii=False, indent=4))
    return json_res
    # print(json.dumps(json_res, ensure_ascii=False, indent=4))
    # return json.dumps(json_res, ensure_ascii=False,indent = 4)


def PROZR_B(inn, session):
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-all",
        "queryAll": inn,
        "queryUl": "",
        "okvedUl": "",
        "statusUl": "",
        "regionUl": "",
        "isMspUl": "",
        "mspUl1": "1",
        "mspUl2": "2",
        "mspUl3": "3",
        "queryIp": "",
        "okvedIp": "",
        "statusIp": "",
        "regionIp": "",
        "isMspIp": "",
        "mspIp1": "1",
        "mspIp2": "2",
        "mspIp3": "3",
        "queryUpr": "",
        "uprType1": "1",
        "uprType0": "1",
        "queryRdl": "",
        "dateRdl": "",
        "queryAddr": "",
        "regionAddr": "",
        "queryOgr": "",
        "ogrFl": "1",
        "ogrUl": "1",
        "npTypeDoc": "1",
        "ogrnUlDoc": "",
        "ogrnIpDoc": "",
        "nameUlDoc": "",
        "nameIpDoc": "",
        "formUlDoc": "",
        "formIpDoc": "",
        "ifnsDoc": "",
        "dateFromDoc": "",
        "dateToDoc": ""
    }
    url = "https://pb.nalog.ru/search-proc.json"
    result = session.post(url, data=data).text
    json_res_1 = json.loads(result)
    return json_res_1
def prozr(data):
    try:
        token = data['ip']['data'][0]['token']
    except Exception as e:
        token = data['ul']['data'][0]['token']

    # print(json.dumps(json_res, ensure_ascii=False, indent=4))
    # print("---------------------------------------------------")
    url = "https://pb.nalog.ru/company-proc.json"

    payload = {'token': token,
               'method': 'get-request'}
    files = [
    ]
    headers = {
        'Cookie': 'JSESSIONID=71D5F26B08127DA75DE2BE6EB401C84F'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    json_res = json.loads(response.text)
    id = json_res['id']
    data = {
        "id": id,
        "token": token,
        "method": "get-response"
    }
    result = requests.post(url, data=data).text
    json_res_2 = json.loads(result)
    return json_res_2
    # return json_res_1, json_res_2
    # print(json.dumps(json_res, ensure_ascii=False, indent=4))


def check_IP(guery, date):
    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "RFI7klTiv4Jw6nVOeT+E4PN3HYCyprj7CRA4rAbEplXnsYX80vehjoFFOMKNLI+d78VRMQ==",
        "__VIEWSTATEGENERATOR": "112E02C5",
        "ctl00$ctl00$tbINN": guery,  # 143400305674
        "ctl00$ctl00$tbDate": date,  # 2021-07-04
        "ctl00$ctl00$btSend": "Найти"
    }

    res = requests.post("https://npd.nalog.ru/check-status/", data=data).text
    soup = BeautifulSoup(res, 'html.parser')
    res_text = soup.find(id="ctl00_ctl00_lblInfo").get_text()
    # print(res_text)
    return res_text


if __name__ == '__main__':
    pprint(PROZR_B("7713398595", requests.Session()))
    a = PROZR_B("7713398595", requests.Session())
    print("------------------")
    b = prozr(a).get("vyp").get("СумКап")
    pprint(b)
    #deyat = a.get("ul").get("data")[0].get("okved2name")
    #check_EGRUL("143400305674")
