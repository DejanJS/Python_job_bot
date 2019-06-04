from bs4 import BeautifulSoup
import requests

data = requests.get("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today")
soup = BeautifulSoup(data.text)
print("document",soup)
print("hello bot")
