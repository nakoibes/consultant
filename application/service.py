from datetime import datetime
from pprint import pprint

import requests as requests

from application.magic import check_EGRUL, PROZR_B, check_IP, prozr

key = "6b6d3dc1db81eb304b998af41ef6e91d47b3bb5f"


# class Searcher:
#     def __init__(self, inn):
#         self.inn = inn
#         if len(inn) == 12:
#             self.handler = IPHandler()
#         else:
#             self.handler = ULHandler()
#
#     def handle(self):
#         return self.handler.handle(self.inn)


class IPSearcher:
    def __init__(self, inn):
        self.inn = inn

    def handle(self):
        result_dict = dict()
        raw = check_EGRUL(self.inn)
        if raw.get("rows"):
            name = raw.get("rows")[0].get("n")
            ognip = raw.get("rows")[0].get("o")
            start = raw.get("rows")[0].get("r")
            finish = raw.get("rows")[0].get("e")
            result_dict.update({"": "Физическое лицо", "ФИО": name, "ОГНИП": ognip, "ИНН": self.inn,
                                "Дата присвоения ОГНИП": start,
                                "Дата прекращения деятельности": finish,
                                })
        check = check_IP(self.inn, "2021-07-04")
        if check:
            result_dict.update({"":check})
        return result_dict


class ULSearcher:
    def __init__(self, inn, session):
        self.inn = inn
        self.session = session

    def handle(self):
        result_dict = dict()
        raw_eg = check_EGRUL(self.inn)
        try:
            raw_biz_1 = PROZR_B(self.inn, self.session)
            req = prozr(raw_biz_1)
            #req = PROZR_B("7713398595", requests.Session())
            #print(raw_biz_1)
            if raw_biz_1:
                deyat = raw_biz_1.get("ul").get("data")[0].get("okved2name")

                #print(deyat)
                result_dict.update({"Основной вид деятельности": deyat})
        except:
            #print("--------")
            r = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}", )
            # print(r)
            if r:
                status = r.json().get("items")[0].get("ЮЛ").get("Статус")
                deyat = r.json().get("items")[0].get("ЮЛ").get("ОснВидДеят").get("Текст")
                result_dict.update({"Статус": status, "Основной вид деятельности": deyat})
            r1 = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}", )
            if r1:
                kapital = r.json().get("items")[0].get("ЮЛ").get("Капитал").get("СумКап")
                result_dict.update({"Уставной капитал": kapital})
        if raw_eg.get("rows"):
            address = raw_eg.get("rows")[0].get("a")
            name = raw_eg.get("rows")[0].get("c")
            director = raw_eg.get("rows")[0].get("g")
            inn = raw_eg.get("rows")[0].get("i")
            ogrn = raw_eg.get("rows")[0].get("o")
            kpp = raw_eg.get("rows")[0].get("p")
            ogrn_date = raw_eg.get("rows")[0].get("r")
            result_dict.update(
                {"По состоянию на": datetime.date(datetime.today()), "": "Юридическое лицо", "Адрес": address,
                 "Название": name,
                 "": director, "ИНН": inn,
                 "ОГРН": ogrn,
                 "КПП": kpp,
                 "Дата присвоения ОГРН": ogrn_date})


        # print(r1)
        return result_dict


if __name__ == '__main__':
    # s = ULSearcher("7713398595")
    # result = s.handle()
    # a = PROZR_B("7713398595")
    # print(a)
    r1 = requests.get(f"https://api-fns.ru/api/egr?req=7713398595&key={key}", )
    pprint(r1.json())
