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


def PROZR_B(inn):
    '''REGINA'''
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
    result = requests.post(url, data=data).text
    json_res_1 = json.loads(result)
    return json_res_1


def prozr(data):
    '''REGINA'''
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


def kadarbitr(inn):
    '''REGINA'''
    url = "https://kad.arbitr.ru/Kad/SearchInstances"

    for i in range(-1, 3):
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
        cnt = 0
        res = response.text
        soup = BeautifulSoup(res, 'html.parser')
        for tr in soup.findAll("tr"):
            class_num = tr.find("td", class_="num").find("div", class_="b-container")
            type = class_num.find("div").get("class")
            date = class_num.find("div").get("title")
            ssylka = class_num.find("a").get("href")
            num = class_num.find("a", class_="num_case").text.replace(" ", "").rstrip()
            cnt += 1
            # print("type= ", type[0])
            # print("date= ", date)
            # print("ssylka= ", ssylka)
            # print("num= ", num)

            class_court = tr.find("td", class_="court").find("div", class_="b-container")
            court = class_court.find("div", class_="judge").get("title")
            sud = class_court.find_all("div")[1].get("title")
            # print("court= ", court)
            # print("sud= ", sud)

            class_plaintiff = tr.find("td", class_="plaintiff").find("div", class_="b-container")
            plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find("strong").text
            # print("plaintiff= ", plaintiff)
            try:
                # inn = tr.find("td", class_="plaintiff").find_all("div")[2].get_text()
                inn_plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find_all("div")[0].text.replace(
                    " ", "").rstrip()
                # print("inn_plaintiff= ", inn_plaintiff)
            except Exception as e:
                pass
            try:
                inn_plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find_all("div")[0].text.replace(
                    " ", "").rstrip() + "" + class_plaintiff.find("span", class_="g-highlight").text
                # print("inn_plaintiff= ", inn_plaintiff)
            except Exception as e:
                pass

            class_respondent = tr.find("td", class_="respondent").find("div", class_="b-container")
            try:
                respondent = class_respondent.find("span", class_="js-rolloverHtml").find("strong").text
                # print("respondent= ", respondent)
            except Exception as e:
                pass
            try:
                inn_respondent = class_respondent.find("span", class_="js-rolloverHtml").find_all("div")[
                    0].text.replace(" ", "").rstrip()
                # print("inn_respondent= ", inn_respondent)
            except Exception as e:
                pass
        if i == -1:
            print("Найдено ", cnt, " (всего)")
        elif i == 0:
            print("Найдено ", cnt, " (истец)")
        elif i == 1:
            print("Найдено ", cnt, " (ответчик)")
        elif i == 2:
            print("Найдено ", cnt, " (третье лицо)")
        elif i == 3:
            print("Найдено ", cnt, " (иное лицо)")


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
    for i in range(-1, 3):
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
            # print("Найдено ", cnt, " (иное лицо)")
    return total, ist, ans, th_l, other_l


if __name__ == '__main__':
    #fedresurs("7728168971")
    #print(kadarbitr_1("7728168971"))
    # pprint(PROZR_B("7713398595"))
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    # print(kadarbitr_1("7728168971"))
    a = PROZR_B("7713398595")
    print("------------------")
    # b = prozr(a).get("vyp").get("СумКап")
    b = prozr(a)
    pprint(b)
    #time.sleep(1)
    # deyat = a.get("ul").get("data")[0].get("okved2name")
    # check_EGRUL("143400305674")
    # print(kadarbitr("7728168971"))
