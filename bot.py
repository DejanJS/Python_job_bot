from bs4 import BeautifulSoup
import requests

data = requests.get("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today")
soup = BeautifulSoup(data.text,'html.parser')
job_titles = []
for i in soup.select("h2.uk-margin-remove"):
	job_titles.append(i['title'])

print("job titles",job_titles)
