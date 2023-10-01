from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import urllib.parse
import datetime
from googletrans import Translator

translator = Translator()

filename = f"file.html"
filename2 = f"file.py"
file = open(filename, "w", encoding="utf-8")
file2 = open(filename2, "w", encoding="utf-8")

lis = []

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
}

url = "https://github.com/"

res = requests.get(url, headers=headers, timeout=100)

content = res.content

soup = BeautifulSoup(content, "html.parser")
# Remove all script tags from the soup
for script in soup.find_all("script"):
    script.extract()
text = soup.get_text()
lis = [x for x in text.split("\n") if x != ""]

# print(soup)
file.write(str(soup))

dict = {}

for i in lis:
    i = i.strip()
    if i != "":
        # print(i)
        translated_text = translator.translate(i, src="en", dest="hi")
        dict.update({i: translated_text.text})

file2.write(str(dict))
# print(dict)
