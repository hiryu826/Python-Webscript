#첫 번째: 페이지를 가져온다
#두 번째: request 만들기
#세 번째: job 추출하기

#Python에서 HTTP에 요청을 보내는 모듈 requests
import requests

#beautiful soup을 통해 data 추출(어던 dada를 찾아주는 Object)
from bs4 import BeautifulSoup

# 1. URL 입력
URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

# 2. 요청할 Page의 마지막 Page 호출
def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  # title = html.find("h2", {"class": "job-link"}).find("a")
  # print(title)
  # title = html.find("div", {"class": "-title g-row"}).find("h2").find("a")["title"]
  # company = html.find("div", {"class": "-job-summary"}).find("div", {"class": "-title g-row"}).find("h2").find("a")["title"]
  # company_row = html.find("div", {"class":"-company g-row"}).find_all("span")
  # company_row = html.find("div", {"class":"-company"}).find_all("span")
  # title = html.find("h2").get_text()
  # company, location = html.find("h3").find_all("span", recursive=False)
  # company = company.get_text(strip=True)
  # location = location.get_text(strip=True)
  # job_id = html['data-jobid']
  # return {
  #   'title': title, 
  #   'company': company, 
  #   'location': location, 
  #   "apply_link": f"https://stackoverflow.com/jobs/{job_id}"
  # }
  title = html.find("h2").get_text()
  company, location = html.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']
  return {
    'title': title, 
    'company': company, 
    'location': location, 
    "apply_link": f"https://stackoverflow.com/jobs/{job_id}"
  }

# 3. 전체 페이지 및 직업 호출
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping sof Page: {page}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
      
def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs