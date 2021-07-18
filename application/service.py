import locale
from datetime import datetime
from pprint import pprint
import socks
import socket
import requests as requests

from application.functions import check_EGRUL, PROZR_B, check_IP, prozr, kadarbitr_1

key = "466c09ea169672bed651f6a4a9a90d1f73a4ad73"


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
    def __init__(self, inn):
        self.inn = inn

    def handle(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        result_dict = dict()
        raw_eg = check_EGRUL(self.inn)

        # court_total, court_ist, court_ans, court_th_l, court_other = kadarbitr_1(self.inn)
        # court_other = int(court_total) - int(court_ist) - int(court_ans) - int(court_th_l)
        # result_dict.update(
        #     {"court_total": court_total, "court_ist": court_ist, "court_ans": court_ans, "court_th_l": court_th_l,
        #      "court_other": court_other})

        # r = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}", )
        # print(r)
        # if r:
        #     status = r.json().get("items")[0].get("ЮЛ").get("Статус", "mock")
        #     deyat = r.json().get("items")[0].get("ЮЛ").get("ОснВидДеят").get("Текст", "mock")
        #     date_reg = r.json().get("items")[0].get("ЮЛ").get("ДатаРег", "mock")
        #     kapital = r.json().get("items")[0].get("ЮЛ").get("Капитал").get("СумКап", "mock")
        #     #print(kapital)
        #     result_dict.update({"status": status, "deyat": deyat, "date_reg": datetime.strptime(date_reg,
        #                                                                                         '%Y-%m-%d').date(),
        #                         "kapital": '{:,}'.format(int(kapital))  + " руб",
        #                         "time_delta": (datetime.date(datetime.today()) - datetime.strptime(date_reg,
        #                                                                                            '%Y-%m-%d').date()).days // 365})

        # r1 = requests.get(f"https://api-fns.ru/api/egr?q={self.inn}&key={key}")
        # if r1:
        #     stop_date = r1.json().get("items")[0].get("ЮЛ").get("ДатаПрекр")
        #     result_dict.update({"stop_date": stop_date})

        # try:
        #     raw_biz_1 = PROZR_B("7713398595")
        #     raw_biz_2 = prozr(raw_biz_1)
        #     deyat = raw_biz_1.get("ul").get("data")[0].get("okved2name")
        #     raw_biz_2 = prozr(raw_biz_1)
        #     kapital = raw_biz_2.get("vyp").get("СумКап")
        #     result_dict.update({"deyat": deyat, "kapital": kapital})
        # except:
        #     pass

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
                {"date": datetime.today().strftime("%-d %B %Y"), "type": "Юридическое лицо", "addr": address,
                 "name": name,
                 "full_name": full_name,
                 "director": director, "inn": inn,
                 "ogrn": ogrn,
                 "kpp": kpp,
                 "ogrn_date": ogrn_date})
        return result_dict


if __name__ == '__main__':
    pass
    # pprint(check_EGRUL("7713398595"))
    # s = ULSearcher("7713398595")
    # result = s.handle()
    # a = PROZR_B("7713398595")
    # print(a)
    # r1 = requests.get(f"https://api-fns.ru/api/egr?req=7713398595&key={key}", )
    # pprint(r1.json())
