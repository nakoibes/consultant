import json
import time
from pprint import pprint
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

import socks
import socket
from collections import OrderedDict
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from requests import session
import requests
import json
import time


def check_EGRUL(query):
    '''REGINA'''
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


def check_IP(guery, date):
    '''REGINA'''
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


def fedresurs(inn):
    '''REGINA'''
    url = "https://fedresurs.ru/"
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path="/home/nakoibes/Рабочий стол/geckodriver", options=options)
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_css_selector(
        "body > fedresurs-app > div:nth-child(3) > home > div > quick-search > div > div > form > input").send_keys(inn)
    time.sleep(0.5)
    driver.find_element_by_css_selector(
        "body > fedresurs-app > div:nth-child(3) > home > div > quick-search > div > div > form > button").click()
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0,10);")
    time.sleep(0.5)
    driver.find_element_by_css_selector(
        "body > fedresurs-app > div:nth-child(3) > search > div > div > div > entity-search > div.row > div > div > form > div > div > div.checkbox > label > span").click()
    time.sleep(0.5)
    driver.find_element_by_css_selector(
        "body > fedresurs-app > div:nth-child(3) > search > div > div > div > entity-search > div.row > div > div > form > button").click()
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    href = driver.find_element_by_css_selector(
        'body > fedresurs-app > div:nth-child(3) > search > div > div > div > entity-search > div.found.person > entity-search-result > loader > div:nth-child(1) > div > div.tab-pane.active > company-search-result > loader > div:nth-child(1) > table > tbody > tr > td.with_link > a').get_attribute(
        'href')
    driver.get(href)
    time.sleep(0.5)
    find_deals = BeautifulSoup(driver.page_source, "html.parser").find(class_='info')
    print(find_deals)
    driver.close()


def kadarbitr_1(inn):
    '''REGINA'''
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    url = "https://kad.arbitr.ru/Kad/SearchInstances"
    total = None
    ist = None
    ans = None
    th_l = None
    other_l = None
    for i in range(-1, 4):
        payload = json.dumps({
            "Page": 1,
            "Count": 25,
            "Courts": [],
            "DateFrom": None,
            "DateTo": None,
            "Sides": [
                {
                    "Name": inn,
                    "Type": i,
                    "ExactMatch": False
                }
            ],
            "Judges": [],
            "CaseNumbers": [],
            "WithVKSInstances": False
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'ASP.NET_SessionId=wq2bdjd20p15szbwnsn53ayq; wasm=c28265d6d51e64c76c4333a731c9b0bf;'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.text
        # print(res)
        soup = BeautifulSoup(res, 'html.parser')
        # print(soup)

        # soup = BeautifulSoup('<input id="documentsTotalCount" type="hidden" value="13695"/>')

        cnt = soup.find('input', {'id': 'documentsTotalCount'})['value']
        if i == -1:
            total = cnt
            # print("Найдено ", cnt, " (всего)")
        elif i == 0:
            ist = cnt
            # print("Найдено ", cnt, " (истец)")
        elif i == 1:
            ans = cnt
            # print("Найдено ", cnt, " (ответчик)")
        elif i == 2:
            th_l = cnt
            # print("Найдено ", cnt, " (третье лицо)")
        elif i == 3:
            other_l = cnt
            print("Найдено ", cnt, " (иное лицо)")
    return total, ist, ans, th_l, other_l


# session = requests.Session()


def PB_addr(addr):
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-addr",
        "queryAll": addr,
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
        "queryAddr": addr,
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
        "dateToDoc": ""}

    url = "https://pb.nalog.ru/search-proc.json"
    result = requests.post(url, data=data).text
    json_res = json.loads(result)
    try:
        num = json_res['addr']['data'][0]['masscnt']
        print("Количество организаций ", num)
    except Exception as e:
        print("немассадр")


def PB_neskolko_UL(inn):
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-upr-uchr",
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
        "queryUpr": inn,
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
    result = requests.post(url, data=data).text
    json_res = json.loads(result)
    try:
        name = json_res['uchr']['data'][0]['fl_fullname']
        num = json_res['uchr']['data'][0]['ul_cnt']
        print("ФИО учредителя ", name)
        print("Количество организаций ", num)
    except:
        pass
    try:
        name = json_res['upr']['data'][0]['fl_fullname']
        num = json_res['upr']['data'][0]['ul_cnt']
        print("ФИО руководителя ", name)
        print("Количество организаций ", num)
    except:
        print("не является")


def PB_diskvalif(fio):
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-rdl",
        "queryAll": fio,
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
        "queryRdl": fio,
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
    result = requests.post(url, data=data).text
    json_res = json.loads(result)
    try:
        name = json_res['rdl']['data'][0]['fl_fullname']
        num = json_res['uchr']['data'][0]['ul_cnt']
        print("ФИО учредителя ", name)
        print("Количество организаций ", num)

    except:
        print("не является")


def PB_ip(inn):
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-ip",
        "queryAll": inn,
        "queryUl": "",
        "okvedUl": "",
        "statusUl": "",
        "regionUl": "",
        "isMspUl": "",
        "mspUl1": "1",
        "mspUl2": "2",
        "mspUl3": "3",
        "queryIp": inn,
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
    # print(json.dumps(json_res, ensure_ascii=False,indent = 4))
    # print("======================================================")
    try:
        token = json_res['ip']['data'][0]['token']
        url = "https://pb.nalog.ru/company-proc.json"
        payload = {'token': token, 'method': 'get-request'}
        files = []
        headers = {
            'Cookie': 'JSESSIONID=71D5F26B08127DA75DE2BE6EB401C84F'
        }
        time.sleep(1)
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_res = json.loads(response.text)
        id = json_res['id']
        token = json_res['token']
        data = {
            "id": id,
            "token": token,
            "method": "get-response"
        }
        time.sleep(1)
        result = requests.post(url, data=data).text
        json_res = json.loads(result)
        print(json.dumps(json_res, ensure_ascii=False, indent=4))
    except Exception as e:
        print("не найдено")
        print(e)


def PB_ul(inn):
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    data = {
        "page": "1",
        "pageSize": "10",
        "pbCaptchaToken": "",
        "token": "",
        "mode": "search-ul",
        "queryAll": inn,
        "queryUl": inn,
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
    result = requests.post(url, data=data).text
    json_res = json.loads(result)
    # print(json.dumps(json_res, ensure_ascii=False,indent = 4))
    # print("======================================================")
    try:
        token = json_res['ul']['data'][0]['token']
        url = "https://pb.nalog.ru/company-proc.json"
        payload = {'token': token, 'method': 'get-request'}
        files = []
        headers = {
            'Cookie': 'JSESSIONID=71D5F26B08127DA75DE2BE6EB401C84F'
        }
        time.sleep(1)
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_res = json.loads(response.text)
        id = json_res['id']
        token = json_res['token']
        data = {
            "id": id,
            "token": token,
            "method": "get-response"
        }
        time.sleep(1)
        result = requests.post(url, data=data).text
        json_res = json.loads(result)
        return json_res
        # return json.dumps(json_res, ensure_ascii=False, indent=4)
    except Exception as e:
        print("не найдено")
        print(e)


if __name__ == '__main__':
    # PB_addr('Адыгея Респ,,Майкоп г,,Краснооктябрьская ул,21,,')
    PB_neskolko_UL('221100996554')
    # PB_diskvalif('БАГДАСАРЯН ВЛАДИМИР ГРИГОРЬЕВИЧ')
    # PB_ip('026413007072')
    #pprint(PB_ul('0104009400'))
    # kadarbitr_1("7728168971")
# if __name__ == '__main__':
#     print(kadarbitr_1("7728168971"))
#     #fedresurs("7728168971")
#     #print(kadarbitr_1("7728168971"))
#     # pprint(PROZR_B("7713398595"))
#     # socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
#     # socket.socket = socks.socksocket
#     # print(kadarbitr_1("7728168971"))
#     # a = PROZR_B("7713398595")
#     # print("------------------")
#     # b = prozr(a).get("vyp").get("СумКап")
#     # b = prozr(a)
#     # pprint(b)
#     #time.sleep(1)
#     # deyat = a.get("ul").get("data")[0].get("okved2name")
#     # check_EGRUL("143400305674")
#     # print(kadarbitr("7728168971"))
