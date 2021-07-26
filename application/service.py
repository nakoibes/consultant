import locale
from datetime import datetime
from pprint import pprint
import socks
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from application.functions import check_EGRUL, check_IP, kadarbitr_1, PB_ul


# class IPSearcher:
#     def __init__(self, inn):
#         self.inn = inn
#
#     def handle(self):
#         result_dict = dict()
#         raw = check_EGRUL(self.inn)
#         if raw.get("rows"):
#             name = raw.get("rows")[0].get("n")
#             ognip = raw.get("rows")[0].get("o")
#             start = raw.get("rows")[0].get("r")
#             finish = raw.get("rows")[0].get("e")
#             result_dict.update({"": "Физическое лицо", "ФИО": name, "ОГНИП": ognip, "ИНН": self.inn,
#                                 "Дата присвоения ОГНИП": start,
#                                 "Дата прекращения деятельности": finish,
#                                 })
#         check = check_IP(self.inn, "2021-07-04")
#         if check:
#             result_dict.update({"": check})
#         return result_dict
#

class ULSearcher:
    def __init__(self, inn):
        self.inn = inn

    def handle(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        result_dict = dict()
        try:
            with ThreadPoolExecutor(max_workers=5) as pool:

                pb_res = pool.submit(PB_ul, self.inn)
                kadr_res = pool.submit(kadarbitr_1, self.inn)
                court_total, court_ist, court_ans, court_th_l, court_other = kadr_res.result()
                pb = pb_res.result()
        except:
            print("thread error")

        raw_eg = check_EGRUL(self.inn)

        # pb = PB_ul(self.inn)
        if pb:
            status = "Действующая" if not pb.get("vyp").get("НаимСтатусЮЛСокр") else pb.get("vyp").get(
                "НаимСтатусЮЛСокр")
            kapital = pb.get("vyp").get("СумКап")

            date_reg = pb.get("vyp").get("ДатаРег") or pb.get("vyp").get("ДатаОГРН")
            time_delta = None
            if date_reg:
                time_delta = ((datetime.date(datetime.today()) - datetime.strptime(date_reg,
                                                                                   '%Y-%m-%d').date()).days // 365) or 100
                date_reg = str(datetime.strptime(date_reg, '%Y-%m-%d').date().strftime("%-d %B %Y"))

            deyat = pb.get("vyp").get("НаимОКВЭД")

            masaddress = len(pb.get("masaddress", ''))
            mas_count = masaddress
            if masaddress == 0:
                masaddress = "Не является адресом массовой регистрации"
            else:
                masaddress = "Организации зарегистрировано по этому адресу" + str(masaddress)

            kod_deyat = pb.get("vyp").get("КодОКВЭД")

            taxmodes = []
            if pb.get("vyp").get("hastaxmode"):
                for item in pb.get("taxmode"):
                    if item.get("usn") == 1.0 and item.get("yearcode") == 2019.0:
                        taxmodes.append("Упрощенная система налогообложения")
                    elif item.get("envd") == 1.0 and item.get("yearcode") == 2019.0:
                        taxmodes.append("Единый налог на вменённый доход")
                    elif item.get("eshn") == 1.0 and item.get("yearcode") == 2019.0:
                        taxmodes.append("Единый сельскохозяйственный налог")
                    elif item.get("srp") == 1.0 and item.get("yearcode") == 2019.0:
                        taxmodes.append("соглашение о разделе продукции")
            else:
                taxmodes.append("Специальный налоговый режим не применяется")

            if pb.get("vyp").get("rsmpcategory") == 2.0:
                msp = "Малое предприятие"
            elif pb.get("vyp").get("rsmpcategory") == 1.0:
                msp = "Микропредприятие"
            elif pb.get("vyp").get("rsmpcategory") == 0.0:
                msp = "Не является субъектом МСП"
            else:
                msp = "Среднее предприятие"
            if pb.get('offense'):
                nalog_offense_sum = calculate_offense_sum(pb.get('offense'))
            else:
                nalog_offense_sum = 0
            nalog_offense = f"есть нарушения (общая сумма штрафов- {str(nalog_offense_sum)}руб.)" if pb.get(
                "is_p_offense") else "Сведения отсутствуют"

            if kapital:
                kapital = '{:,}'.format(int(kapital)) + " руб"

            if pb.get("vyp").get("pr_zd") == 1.0:
                nalog_debt = "Имеет задолженности"
            elif pb.get("vyp").get("pr_zd") == 0.0:
                nalog_debt = "Задолженностей не выявлено"
            else:
                nalog_debt = None

            if pb.get("vyp").get("is_protch_przd") == 1.0:
                nalog_info = "Предоставляет налоговую отчетность"
            elif pb.get("vyp").get("is_protch_przd") == 0.0:
                nalog_info = "Не предоставляет налоговую отчетность"
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
                 "nalog_offense_sum": nalog_offense_sum,
                 "mas_count": mas_count,
                 "kod_deyat": kod_deyat,
                 "nalog_offense": nalog_offense,
                 "taxmodes": taxmodes,
                 "fine_sum": fine_sum,
                 "nalog_info": nalog_info,
                 "date_reg": date_reg,
                 "deyat": deyat,
                 "time_delta": time_delta})

        # court_total, court_ist, court_ans, court_th_l, court_other = kadarbitr_1(self.inn)
        # court_other = int(court_total) - int(court_ist) - int(court_ans) - int(court_th_l)
        result_dict.update(
            {"court_total": court_total, "court_ist": court_ist, "court_ans": court_ans, "court_th_l": court_th_l,
             "court_other": court_other})

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


def analyze(map):
    res_map = {}
    status = map.get("status")
    time_delta = map.get("time_delta")
    nalog_debt = map.get("nalog_debt")
    nalog_info = map.get("nalog_info")
    fine_sum = map.get("fine_sum")
    mas_count = map.get("mas_count")
    nalog_offense_sum = map.get("nalog_offense_sum")
    if status != "Действующая":
        res_map.update({"status": status})
    if time_delta and time_delta < 3:
        res_map.update({"time_delta": time_delta})
    if nalog_debt != "Не имеет задолженность":
        res_map.update({"nalog_debt": nalog_debt})
    if nalog_info != "Предоставляет налоговую отчетность":
        res_map.update({"nalog_info": nalog_info})
    if mas_count and mas_count > 2:
        res_map.update({"mas_count": mas_count})
    if nalog_offense_sum and nalog_offense_sum > 0:
        res_map.update({"nalog_offense": map.get("nalog_offense")})
    if fine_sum :
        res_map.update({"fine_sum": map.get("fine_sum")})
    return res_map


if __name__ == '__main__':
    pass
    # pprint(check_EGRUL("7713398595"))
    s = ULSearcher("7713398595")
    result = s.handle()
    print(result)
    # a = PROZR_B("7713398595")
    # print(a)
    # r1 = requests.get(f"https://api-fns.ru/api/egr?req=7713398595&key={key}", )
    # pprint(r1.json())
