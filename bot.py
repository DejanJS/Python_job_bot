#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import threading
from datetime import datetime
from time import strftime
import os


current_day =int(datetime.today().strftime("%d")) 
skills = None
def scrape(url,interestedin):
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html.parser')
    find_lastpage = soup.find("i",{"class":"uk-icon-angle-double-right"}) #double arrow right with attribute of the last page of job post,pagination bar on bottom of the page e.g(1,2,3,4 pages..)
    last_page_number = find_lastpage.find_parent("a")['data-page']
    for page in range(int(last_page_number)):#for n of pages create each thread and scrape everything
       page_url = f"https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today"
       job_thread = threading.Thread(target=scrape_jobs,args=(page_url,interestedin)) 
       job_thread.start()   
   # print("Python jobs links : ",interested_links)
    

def scrape_jobs(url,interestedin):
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html.parser')
    #this can be cached in the future so i am not parsing same page n number of times later..
    print(url,"scrape description")
    posts = soup.findAll('div',id=re.compile("oglas_[0-9]*"))
    job_company_tags = soup.select('p.uk-margin-remove > a')
    job_companies = [company.text.strip() for company in job_company_tags] #name of the companies for each job
    jobs = [JobFinder(post) for post in posts]
    interests = [job.interested(interestedin) for job in jobs] #this filters jobs by interested in array
    interested_jobs = list(filter(lambda job : job.interested(interestedin),jobs))
    interested_job_titles = [interested.title for interested in interested_jobs]
    interested_links = [interested.link for interested in interested_jobs]
    if len(interested_links) > 0:
        with open(os.path.expanduser(os.path.join("~/Desktop",f"jobs_day_{current_day}.txt")),"w+") as f:
            f.write(f" Jobs for {datetime.today().strftime('%d.%B|%Y')} for keywords : {','.join(str(word) for word in skills)} ".center(60,"=") + ("\n")*2) 
            for i,v in enumerate(interested_links):
                f.write(interested_job_titles[i]+f" ({job_companies[i]})" + " - " + v + '\n'*2) #should print me all links
    else:
        print("no jobs today :(")

    print('Interested Jobs : ',interested_job_titles)
    print('Interested Links : ',interested_links)


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
        
    def page_finder(post):
        find_page = post.select('li.uk-icon-angle-double-right') 
        print("our find page",find_page)
    def __str__(self):
        return f'{self.title}'

#input prompt
def get_interests():
    global skills
    print("What skills do you have?")
    keywords = input().lower().split(",")
    skills = keywords
#    return input().lower().split(",")
    return keywords 

main_thread = threading.Thread(target=scrape,args=("https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today",get_interests()))
# url for the jobs today/current https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50&vreme_postavljanja=today
#https://poslovi.infostud.com/oglasi-za-posao/beograd?category%5B0%5D=5&dist=50
main_thread.start()
