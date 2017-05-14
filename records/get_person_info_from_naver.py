import re
import json
import requests
from bs4 import BeautifulSoup

def get_person_info(person):
    url = 'http://people.search.naver.com/search.naver?sm=tab_hty&where=nexearch&query={}&ie=utf8&x=0&y=0'.format(person)
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    pattern = re.compile('(?<=oAPIResponse :)(.*?)(?=, sAPIURL)', re.DOTALL)
    matches = pattern.search(html)
    data = matches[0]
    result = json.loads(data) # Json

    listPerson = result['data']['result']['itemList'] # Get person info

    result = {} # 리턴값 초기

    for index, item in enumerate(listPerson):

        sub = {}

        sub['id'] = item['object_id']
        sub['name'] = item['m_name']
        sub['birth_year'] = item['birth_year']
        
        job = []
        for jobs in item['job_info']:
            job.append(jobs['job_name'])
        sub['job'] = job

        result[index] = sub

    return result


print(get_person_info('최경'))