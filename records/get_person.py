import re
import json
import requests
from bs4 import BeautifulSoup

def get_person_info(person):
    search_url = 'http://people.search.naver.com/search.naver'  # Search URL
    params = { 'where':'nexearch' , 'query': person }           # Search Parameters
    html = requests.get(search_url, params=params).text
    soup = BeautifulSoup(html, 'html.parser')                          # BeautifulSoup
    pattern = re.compile('(?<=oAPIResponse :)(.*?)(?=, sAPIURL)', re.DOTALL)
    matches = pattern.search(html)
    if matches == None:
        return None

    data = matches[0]
    result = json.loads(data)           # Json Data Load from Javascript

    listPerson = result['data']['result']['itemList']           # Get person info

    result = {}                         # 리턴값 초기

    for index, item in enumerate(listPerson):
        sub = {}
        sub['id'] = item['object_id']   # ID Read
        sub['name'] = item['m_name']    # name
        sub['birth_year'] = item['birth_year']      # Birth Year
        
        job = []
        for jobs in item['job_info']:
            job.append(jobs['job_name'])
        sub['job'] = job
        result[index] = sub
        if index == 1:
            break

    return result

if __name__ == '__main__':
    print(get_person_info('최경환'))