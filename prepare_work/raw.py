import requests

import json
from flask import Flask
from bs4 import BeautifulSoup

key = "466c09ea169672bed651f6a4a9a90d1f73a4ad73"
app = Flask(__name__)
session = requests.Session()


@app.route('/<user>')
def hello(user):
    return str(primer(user))


# def search(q,page="",filter=""):
#     url = "https://api-fns.ru/api/search?q="+q+"&filter=active"+"&key="+key
#     result = requests.get(url).text
#     json_res = json.loads(result)
#     print(json.dumps(json_res, ensure_ascii=False,indent = 4))
#
# def check(req):
#     url = "https://api-fns.ru/api/check?req="+req+"&key="+key
#     result = requests.get(url).text
#     json_res = json.loads(result)
#     print(json.dumps(json_res, ensure_ascii=False,indent = 4))

# def json_usage():
#     dict = {
#     "items": [
#         {
#             "ЮЛ": {
#                 "ИНН": "2311146207",
#                 "ОГРН": "1122311005453",
#                 "НаимСокрЮЛ": "СНП \"МЕГАТРОН\"",
#                 "НаимПолнЮЛ": "САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО \"МЕГАТРОН\"",
#                 "ДатаОГРН": "2012-06-20",
#                 "Статус": "Действующее",
#                 "АдресПолн": "край Краснодарский, р-н Динской, п. Южный, ул. Строителей, д.64",
#                 "ОснВидДеят": "Управление эксплуатацией нежилого фонда за вознаграждение или на договорной основе",
#                 "ГдеНайдено": "ФИО учредителя (Борунов Алексей Владимирович, ИННФЛ: 231121127449)"
#             }
#         }
#     ],
#     "Count": 1
#     }
#     print(dict['items'][0]['ЮЛ']["ИНН"])

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
    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    # return json.dumps(json_res, ensure_ascii=False,indent = 4)

#проверка ИП на проф налог принимает inn, date возвращает текст
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
    print(res_text)
    return res_text


def check_not_valid_SVID_1(ser, nom):
    data = {
        "ser": ser,
        "nom": nom,
        "month": "0",
        "year": "0"
    }
    for i in range(1, 10):
        res = requests.post(
            "https://www.nalog.gov.ru/rn0" + str(i) + "/service/invalid_cert/?ser=26&nom=002880478&month=0&year=0",
            data=data).text
        soup = BeautifulSoup(res, 'html.parser')
        res_text = soup.find(id="ctl00_ctl00_ctl00_lblError").get_text()
        print(str(i) + " " + res_text)
    for i in range(10, 80):
        res = requests.post(
            "https://www.nalog.gov.ru/rn" + str(i) + "/service/invalid_cert/?ser=26&nom=002880478&month=0&year=0",
            data=data).text
        soup = BeautifulSoup(res, 'html.parser')
        res_text = soup.find(id="ctl00_ctl00_ctl00_lblError").get_text()
        print(str(i) + " " + res_text)
    for i in [86, 87, 89, 91, 92]:
        res = requests.post(
            "https://www.nalog.gov.ru/rn" + str(i) + "/service/invalid_cert/?ser=26&nom=002880478&month=0&year=0",
            data=data).text
        soup = BeautifulSoup(res, 'html.parser')
        res_text = soup.find(id="ctl00_ctl00_ctl00_lblError").get_text()
        print(str(i) + " " + res_text)
    # return res_text


def check_not_valid_SVID_2_FL(inn):
    res = requests.get("https://service.nalog.ru/invalid-inn-fl.html#inn=" + inn).text
    soup = BeautifulSoup(res, 'html.parser')
    res_text = soup.find(id="pnlNoResult").find(class_="msg-no-data").get_text()
    print(res_text)


def check_not_valid_SVID_3_UL(inn):
    res = requests.get("https://service.nalog.ru/invalid-inn-ul.html#inn=" + inn).text
    soup = BeautifulSoup(res, 'html.parser')
    res_text = soup.find(id="pnlNoResult").find(class_="msg-no-data").get_text()
    print(res_text)


def PROZR_B(inn):
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
    json_res = json.loads(result)

    try:
        token = json_res['ip']['data'][0]['token']
    except Exception as e:
        token = json_res['ul']['data'][0]['token']

    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    print("---------------------------------------------------")
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
    json_res = json.loads(result)
    print(json.dumps(json_res, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    #check_not_valid_SVID_2_FL("143400305675")
     #check_not_valid_SVID_1("26", "002880478")
     #check_not_valid_SVID_3_UL("7707083893")
    # check_IP("500111104168","2021-07-04")
    PROZR_B("7709750937")
    # app.run(host='0.0.0.0',debug=True)
    #check_EGRUL("7709750937")
    #check_IP("143400305674","2021-07-04")
# if __name__ == '__main__':
#     # search("Борунов Алексей Владимирович")
#     #json_usage()
#     # check("7706148097")
#     name = input()
#     primer(name)
