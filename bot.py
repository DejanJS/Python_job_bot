from bs4 import BeautifulSoup
import requests

data = requests.get("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today")
soup = BeautifulSoup(data.text,'html.parser')
job_titles = list(map(lambda item:item['title'],soup.select("h2.uk-margin-remove")))

print("job titles",job_titles)
