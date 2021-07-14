import json

import requests as requests
from bs4 import BeautifulSoup


def kadarbitr(inn, ):
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
        'Cookie': 'ASP.NET_SessionId=wq2bdjd20p15szbwnsn53ayq; wasm=c28265d6d51e64c76c4333a731c9b0bf;'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.text
    soup = BeautifulSoup(res, 'html.parser')
    for tr in soup.findAll("tr"):
        class_num = tr.find("td", class_="num").find("div", class_="b-container")
        type = class_num.find("div").get("class")
        date = class_num.find("div").get("title")
        ssylka = class_num.find("a").get("href")
        num = class_num.find("a", class_="num_case").text.replace(" ", "").rstrip()
        print("type= ", type[0])
        print("date= ", date)
        print("ssylka= ", ssylka)
        print("num= ", num)

        class_court = tr.find("td", class_="court").find("div", class_="b-container")
        court = class_court.find("div", class_="judge").get("title")
        sud = class_court.find_all("div")[1].get("title")
        print("court= ", court)
        print("sud= ", sud)

        class_plaintiff = tr.find("td", class_="plaintiff").find("div", class_="b-container")
        plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find("strong").text
        print("plaintiff= ", plaintiff)
        try:
            # inn = tr.find("td", class_="plaintiff").find_all("div")[2].get_text()
            inn_plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find_all("div")[0].text.replace(" ",
                                                                                                                   "").rstrip()
            print("inn_plaintiff= ", inn_plaintiff)
        except Exception as e:
            pass
        try:
            inn_plaintiff = class_plaintiff.find("span", class_="js-rolloverHtml").find_all("div")[0].text.replace(" ",
                                                                                                                   "").rstrip() + "" + class_plaintiff.find(
                "span", class_="g-highlight").text
            print("inn_plaintiff= ", inn_plaintiff)
        except Exception as e:
            pass

        class_respondent = tr.find("td", class_="respondent").find("div", class_="b-container")
        try:
            respondent = class_respondent.find("span", class_="js-rolloverHtml").find("strong").text
            print("respondent= ", respondent)
        except Exception as e:
            pass
        try:
            inn_respondent = class_respondent.find("span", class_="js-rolloverHtml").find_all("div")[0].text.replace(
                " ", "").rstrip()
            print("inn_respondent= ", inn_respondent)
        except Exception as e:
            pass


kadarbitr("7706148097")
