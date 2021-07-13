from pprint import pprint

from application.magic import check_EGRUL


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
        raw = check_EGRUL(self.inn)
        if raw.get("rows"):
            name = raw.get("rows")[0].get("n")
            ognip = raw.get("rows")[0].get("o")
            start = raw.get("rows")[0].get("r")
            finish = raw.get("rows")[0].get("e")
            return {"": "Физическое лицо", "ФИО": name, "ОГНИП": ognip, "ИНН": self.inn,
                    "Дата присвоения ОГНИП": start,
                    "Дата прекращения деятельности": finish,
                    }


class ULSearcher:
    def __init__(self, inn):
        self.inn = inn

    def handle(self):
        raw = check_EGRUL(self.inn)
        if raw.get("rows"):
            address = raw.get("rows")[0].get("a")
            name = raw.get("rows")[0].get("c")
            director = raw.get("rows")[0].get("g")
            inn = raw.get("rows")[0].get("i")
            ogrn = raw.get("rows")[0].get("o")
            kpp = raw.get("rows")[0].get("p")
            ogrn_date = raw.get("rows")[0].get("r")
            return {"": "Юридическое лицо", "Адрес": address, "Название": name, "": director, "ИНН": inn,
                    "ОГРН": ogrn,
                    "КПП": kpp,
                    "Дата присвоения ОГРН": ogrn_date}


if __name__ == '__main__':
    #s = Searcher("614704020363")
    result = s.handle()
    print(result)
