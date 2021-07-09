from bs4 import BeautifulSoup as bs

with open("qwe/1.xml", encoding="utf-8") as file:
    # xml = file.read()
    # print(xml)
    # soup = BeautifulSoup(xml, "lxml")
    # print(soup)
    # a = soup.find_all("Документ")
    #print(a)
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")
    print(bs_content)