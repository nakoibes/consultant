import requests
import json
from bs4 import BeautifulSoup
import time

api = "SUJaRSZDek4d"
session = requests.Session()


def ul(region, firstname):
    url = "https://api-ip.fssp.gov.ru/api/v1.0/search/legal?region=" + str(
        region) + "&firstname=" + firstname + "&token=" + api
    result = session.get(url).text
    json_res = json.loads(result)
    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    task = json_res['response']['task']

    url = "https://api-ip.fssp.gov.ru/api/v1.0/status?token=" + api + "&task=" + task
    result = session.get(url).text
    json_res = json.loads(result)
    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    status = json_res['response']['status']
    time.sleep(5)
    while True:
        if status == 0:
            url = "https://api-ip.fssp.gov.ru/api/v1.0/result?token=" + api + "&task=" + task
            result = session.get(url).text
            json_res = json.loads(result)
            print(json.dumps(json_res, ensure_ascii=False, indent=4))
            break
        else:
            result = session.get(url).text
            time.sleep(1)
            print(result)


def api_check(region, firstname, secondname, lastname, birthdate=None):
    url = "https://api-ip.fssp.gov.ru/api/v1.0/search/physical?region=" + str(
        region) + "&lastname=" + lastname + "&firstname=" + firstname + "&token=" + api
    result = session.get(url).text
    json_res = json.loads(result)
    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    task = json_res['response']['task']

    url = "https://api-ip.fssp.gov.ru/api/v1.0/status?token=" + api + "&task=" + task
    result = session.get(url).text
    json_res = json.loads(result)
    print(json.dumps(json_res, ensure_ascii=False, indent=4))
    status = json_res['response']['status']
    time.sleep(5)
    while True:
        if status == 0:
            url = "https://api-ip.fssp.gov.ru/api/v1.0/result?token=" + api + "&task=" + task
            result = session.get(url).text
            json_res = json.loads(result)
            print(json.dumps(json_res, ensure_ascii=False, indent=4))
            break
        else:
            result = session.get(url).text
            time.sleep(1)
            print(result)


def prozrachniy_biznes(inn):
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
    print(json.dumps(json_res, ensure_ascii=False, indent=4))

    try:
        token = json_res['ip']['data'][0]['token']
    except Exception as e:
        token = json_res['ul']['data'][0]['token']

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


# def kadarbitr(inn):
#     url = "https://kad.arbitr.ru/"
#     options = Options()
#     driver = webdriver.Chrome(executable_path = "D:\Рабочий стол\ДОПЫ\Консультант Плюс\chromedriver_win32\chromedriver.exe",options = options)
#     driver.get(url)
#     id = driver.find_element_by_css_selector(".g-ph").send_keys(inn)
#     time.sleep(1)
#     driver.find_element_by_css_selector(".b-promo_notification-popup-close.js-promo_notification-popup-close").click()
#     driver.find_element_by_css_selector(".js-current-text").click()
#     time.sleep(1)
#     driver.find_element_by_id("b-form-submit").click()
#     time.sleep(1)
#     print(driver.page_source)
#     find_deals =  BeautifulSoup(driver.page_source,"html.parser").find(class_='b-found-total')
#     print(find_deals)
#     time.sleep(200)
def kadarbitr(inn):
    url = "https://kad.arbitr.ru/Kad/SearchInstances"

    payload = json.dumps({
        "Page": 1,
        "Count": 25,
        "Courts": [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": [
            {
                "Name": inn,
                "Type": -1,
                "ExactMatch": False
            }
        ],
        "Judges": [],
        "CaseNumbers": [],
        "WithVKSInstances": False
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'ASP.NET_SessionId=5droocyiu42ephsfhodrspo4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    # ul(16,"Камгидромаш")
    # prozrachniy_biznes('143400305674')
    # kadarbitr("7706148097")
    ul('16', "камгидромаш")
    # import requests
    #
    # url = "https://pb.nalog.ru/company-proc.json"
    #
    # payload={'token': '71D0EF7561AAA5E8F1FB9B1C5BEC87514D70213418959B464D9CEA3E64D81CCC878DF4EA471AAED0FE1727339F52AA82FFB151E86AD6F5FD293D7818C46DAE1D278A0D4753D84A162F4C2EBC726A45CF',
    # 'method': 'get-request'}
    # files=[
    #
    # ]
    # headers = {
    #   'Cookie': 'JSESSIONID=BD3701C55716F9D0BE9A54F3A160661D'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload, files=files)
    #
    # print(response.text)
