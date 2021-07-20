import locale
from datetime import datetime
from pprint import pprint
import socks
import socket
import requests as requests
from threading import Thread

from application.functions import check_EGRUL, check_IP, kadarbitr_1, PB_ul

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

        pb = PB_ul(self.inn)
        # pb = mock(self.inn)
        # print(pb)
        if pb:
            status = "Действующая" if not pb.get("vyp").get("НаимСтатусЮЛСокр") else pb.get("vyp").get(
                "НаимСтатусЮЛСокр")
            kapital = pb.get("vyp").get("СумКап")

            date_reg = pb.get("vyp").get("ДатаРег")
            time_delta = None
            if date_reg:
                time_delta = (datetime.date(datetime.today()) - datetime.strptime(date_reg,
                                                                                  '%Y-%m-%d').date()).days // 365
                date_reg = str(datetime.strptime(date_reg, '%Y-%m-%d').date().strftime("%-d %B %Y"))

            masaddress = len(pb.get("masaddress"))
            #print(masaddress)
            taxmode = "Специальный налоговый режим не применяется" if pb.get("vyp").get(
                "hastaxmode") == 0.0 else "Применяется специальный налоговый режим"
            msp = "Не является субъектом МСП" if pb.get("vyp").get("rsmpcategory") == 0.0 else "Является субъектом МСП"
            # print(pb.get("is_p_offense") is False)
            nalog_offense = f"есть нарушения (общая сумма штрафов- {str(calculate_offense_sum(pb.get('offense')))}руб.)" if pb.get(
                "is_p_offense") else "Сведения отсутствуют"
            if kapital:
                kapital = '{:,}'.format(int(kapital)) + " руб"
            if pb.get("vyp").get("pr_zd") == 1.0:
                nalog_debt = "Имеет задолженности"
            elif pb.get("vyp").get("pr_zd") == 0.0:
                nalog_debt = "Не имеет задолженность"
            else:
                nalog_debt = None
            if pb.get("vyp").get("is_protch_przd") == 1.0:
                nalog_info = "Представляет налоговую отчетность"
            elif pb.get("vyp").get("is_protch_przd") == 0.0:
                nalog_info = "Не представляет налоговую отчетность"
            else:
                nalog_info = None
            fine_sum = pb.get("vyp").get("totalarrearsum")
            if fine_sum:
                fine_sum = '{:,}'.format(int(fine_sum)) + " руб"
            result_dict.update(
                {"kapital": kapital,
                 "masaddress": masaddress,
                 "msp": msp,
                 "nalog_debt": nalog_debt,
                 "status": status,
                 "nalog_offense":nalog_offense,
                 "taxmode": taxmode,
                 "fine_sum": fine_sum,
                 "nalog_info": nalog_info,
                 "date_reg": date_reg,
                 "time_delta": time_delta})

            # court_total, court_ist, court_ans, court_th_l, court_other = kadarbitr_1(self.inn)
            # #Thread(target=kadarbitr_1, args=(self.inn)).start()
            # #court_other = int(court_total) - int(court_ist) - int(court_ans) - int(court_th_l)
            # result_dict.update(
            #     {"court_total": court_total, "court_ist": court_ist, "court_ans": court_ans, "court_th_l": court_th_l,
            #      "court_other": court_other})

            # r = requests.get(f"https://api-fns.ru/api/egr?req={self.inn}&key={key}", )
            # if r:
            #     status = r.json().get("items")[0].get("ЮЛ").get("Статус", "mock")
            #     deyat = r.json().get("items")[0].get("ЮЛ").get("ОснВидДеят").get("Текст", "mock")
            #     date_reg = r.json().get("items")[0].get("ЮЛ").get("ДатаРег", "mock")
            #     kapital = r.json().get("items")[0].get("ЮЛ").get("Капитал").get("СумКап", "mock")
            #     # print(kapital)
            #     result_dict.update({"status": status, "deyat": deyat, "date_reg": str(datetime.strptime(date_reg,
            #                                                                                             '%Y-%m-%d').date()),
            #                         "kapital": '{:,}'.format(int(kapital)) + " руб",
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
                 "ogrn_date": str(datetime.strptime(ogrn_date, '%d.%m.%Y').date().strftime("%-d %B %Y"))})
        return result_dict


def calculate_offense_sum(array):
    res = 0
    for item in array:
        res += item.get("offensesum", 0)
    return res


if __name__ == '__main__':
    pass
    # pprint(check_EGRUL("7713398595"))
    # s = ULSearcher("7713398595")
    # result = s.handle()
    # a = PROZR_B("7713398595")
    # print(a)
    # r1 = requests.get(f"https://api-fns.ru/api/egr?req=7713398595&key={key}", )
    # pprint(r1.json())
