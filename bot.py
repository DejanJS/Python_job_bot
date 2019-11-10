#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import threading

def scrape(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html.parser')
    posts = soup.findAll('div',id=re.compile("oglas_[0-9]*"))
    jobs = [JobFinder(post) for post in posts]
    interestedin = ['react','javascript','node','python']
    interests = [job.interested(interestedin) for job in jobs]
    interested_jobs = list(filter(lambda job : job.interested(interestedin),jobs))
    interested_links = [interested.link for interested in interested_jobs]
    print("Python jobs links : ",interested_links)
    print("job titles",[post.title for post in jobs])
    

class JobFinder():
    def __init__(self,post):
        self.post = post
        #print('what is here',post.select('h2.uk-margin-remove'))
        item = post.select('h2.uk-margin-remove')[0] # <h2...>
        self.title = item['title']
        self.href = item.select('a')[0]['href']
        self.link = f'https://poslovi.infostud.com{self.href}'
        # <a class="uk-button uk-button-mini __jobtag full" data-tag-id="69" href="#">Python</a>
        self.tags = [tag.getText().lower() for tag in post.select('a.__jobtag') ]
        #self.interested = 'react' in self.tags or 'javascript' in self.tags
        #print("interested",self.interested)
    
    def interested(self,tags):
        return len( set(tags).intersection( set(self.tags) ) ) > 0
        
    def __str__(self):
        return f'{self.title}'


main_thread = threading.Thread(target=scrape,args=("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5b0%5d=5&dist=50&vreme_postavljanja=today",))
main_thread.start()
"""
data = requests.get("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5b0%5d=5&dist=50&vreme_postavljanja=today")
soup = beautifulsoup(data.text,'html.parser')
#job_titles = list(map(lambda item:item['title'],soup.select("h2.uk-margin-remove")))
# job_titles = [item['title'] for item in soup.select("h2.uk-margin-remove")]
posts = soup.findall('div',id=re.compile("oglas_[0-9]*"))
jobs = [jobfinder(post) for post in posts]
#print('test',jobs)
#print('posts',[post.title for post in jobs])
interestedin = ['react','javascript','node','python']
interests = [job.interested(interestedin) for job in jobs]
interested_jobs = list(filter(lambda job : job.interested(interestedin),jobs))
interested_links = [interested.link for interested in interested_jobs]
print("python jobs links : ",interested_links)
#print('intrests',interests)
print("job titles",[post.title for post in jobs])
"""
