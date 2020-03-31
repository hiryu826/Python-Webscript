#Python에서 HTTP에 요청을 보내는 모듈 requests
import requests

#beautiful soup을 통해 data 추출(어던 dada를 찾아주는 Object)
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit=50&limit={LIMIT}"

def extract_indeed_pages():
  #requests 함수를 사용할 변수 선언
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  #HTML 내 headers, text, json 등 호출 가능
  pagination = soup.find("div", {"class":"pagination"})
  links = pagination.find_all('a')
  pages = []
  for link in links[0:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("div", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  if company:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
    company = company.strip()
  else:
    company = None
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]

  return {
    'title': title, 
    'company:': company, 
    'location': location, 
    "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
  }

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job) #jobs array에 삽입
  return jobs
   # print(result.status_code)

def get_jobs():
    last_page = extract_indeed_pages()
    jobs = extract_indeed_jobs(last_page)

    return jobs
