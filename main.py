import requests
from bs4 import BeautifulSoup
import fake_useragent
from time import sleep
import xlsxwriter as excel

progress = 0

user = fake_useragent.UserAgent().random
headers = {"user-agent": user}
number = 0
page_ = 1

workbook = excel.Workbook(r"C:\Users\ИЛЬЯ-ПК1\Desktop\DataBase_scrapingclub_1.xlsx")
page = workbook.add_worksheet("товары")
page.set_column("A:A", 5)
page.set_column("B:B", 20)
page.set_column("C:C", 10)
page.set_column("D:D", 50)
page.set_column("E:E", 50)
page.set_column("F:F", 50)
row = 0
column = 0

while page_ < 7:
    sleep(3)
    link = f"https://scrapingclub.com/exercise/list_basic/?page={page_}"
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, "lxml")

    block = soup.find_all("div", class_="w-full rounded border")
    for i in block:
        a = {"номер": "",
             "название": "",
             "цена": "",
             "ссылка": "",
             "изображение": "",
             "описание": "",
             }
        href = "https://scrapingclub.com" + i.find("a").get("href")
        a["ссылка"] = href
        response = requests.get(href, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        div = soup.find("div", class_="my-8 w-full rounded border")
        img = "https://scrapingclub.com" + div.find("img").get("src")
        a["изображение"] = img
        name = div.find("h3").text
        a["название"] = name
        price = div.find("h4").text
        a["цена"] = price
        text = div.find("p").text
        a["описание"] = text
        number += 1
        a["номер"] = number
        progress += 5 / 3
        print(str(number) + ")" + "\n" + href + "\n" + img + "\n" + name + "\n" + price + "\n" + text + "\n" + str(round(progress)) + "%" + "\n" + "\n")
        for values in a:
            page.write(row, column, a.get("номер"))
            page.write(row, column + 1, a.get("название"))
            page.write(row, column + 2, a.get("цена"))
            page.write(row, column + 3, a.get("описание"))
            page.write(row, column + 4, a.get("ссылка"))
            page.write(row, column + 5, a.get("изображение"))
        row += 1
        a.clear()
    if number % 10 == 0:
        page_ += 1

workbook.close()
