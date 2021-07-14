from datetime import datetime
from pprint import pprint

import requests as requests

from application.magic import check_EGRUL, PROZR_B, check_IP, prozr

key = "6b6d3dc1db81eb304b998af41ef6e91d47b3bb5f"


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
            result_dict.update({"": check})
        return result_dict


class ULSearcher:
    def __init__(self, inn, session):
        self.inn = inn
        self.session = session

    def handle(self):
        result_dict = dict()
        raw_eg = check_EGRUL(self.inn)
        r = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}", )
        if r:
            status = r.json().get("items")[0].get("ЮЛ").get("Статус")
            deyat = r.json().get("items")[0].get("ЮЛ").get("ОснВидДеят").get("Текст")
            date_reg = r.json().get("items")[0].get("ЮЛ").get("ДатаРег")
            result_dict.update({"status": status, "deyat": deyat, "date_reg": date_reg})
        r1 = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}")
        if r1:
            kapital = r.json().get("items")[0].get("ЮЛ").get("Капитал").get("СумКап")
            result_dict.update({"kapital": kapital})
        if raw_eg.get("rows"):
            address = raw_eg.get("rows")[0].get("a")
            name = raw_eg.get("rows")[0].get("c")
            full_name = raw_eg.get("rows")[0].get("n")
            director = raw_eg.get("rows")[0].get("g")
            inn = raw_eg.get("rows")[0].get("i")
            ogrn = raw_eg.get("rows")[0].get("o")
            kpp = raw_eg.get("rows")[0].get("p")
            ogrn_date = raw_eg.get("rows")[0].get("r")
            result_dict.update(
                {"date": datetime.date(datetime.today()), "type": "Юридическое лицо", "addr": address,
                 "name": name,
                 "full_name": full_name,
                 "director": director, "inn": inn,
                 "ogrn": ogrn,
                 "kpp": kpp,
                 "ogrn_date": ogrn_date})

        return result_dict


if __name__ == '__main__':
    pprint(check_EGRUL("7713398595"))
    # s = ULSearcher("7713398595")
    # result = s.handle()
    # a = PROZR_B("7713398595")
    # print(a)
    # r1 = requests.get(f"https://api-fns.ru/api/egr?req=7713398595&key={key}", )
    # pprint(r1.json())
