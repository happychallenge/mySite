#-*- coding:utf-8 -*-
import re

import requests
from collections import Counter
from bs4 import BeautifulSoup
from konlpy.tag import Kkma

# Extract Source Name
def extract_name(url):
    name = re.findall('\.?(\w+)\.(?=com?|net|org|kr)', url)
    return name[0]

# Insight
def get_contents_from_huffingtonpost(url):
    result = {}

    html = requests.get(url).text
    try:
        response = requests.get(url, headers={'Accept-Encoding': 'gzip'}).text
        # html = response.content.decode('cp949') "Accept-Encoding", "gzip"

        # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
        # html = script.sub('', html)
        soup = BeautifulSoup(html, 'lxml')
    
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'id':'mainentrycontent'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('span.posted time')[0].get_text()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_huffingtonpost('http://www.huffingtonpost.kr/2017/07/29/story_n_17621212.html'))


# PPSS
def get_contents_from_ppss(url):
    result = {}

    # html = requests.get(url).text
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
    
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'itemprop':'articleBody'}).get_text()
        result['content'] = content

        p_time = soup.find('time', attrs={'class': 'entry-time'})
        result['published_at'] = p_time['datetime'][:10]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ppss('http://ppss.kr/archives/34222'))


# Insight
def get_contents_from_insight(url):
    result = {}

    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'class':'news__view__article'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('span.news__view__header__date')[0].get_text()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_insight('http://www.insight.co.kr/news/115737'))


# Naver
def get_contents_from_gdnews(url):
    result = {}

    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'class':'cnt_view'}).get_text()
        
        result['content'] = content
        pdate = soup.select('ul.art_info > li')[1].get_text()[3:]
        result['published_at'] = pdate[:4] + '-' + pdate[5:7] + '-' + pdate[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_gdnews('http://www.gdnews.kr/news/article.html?no=2986'))


# Naver
def get_contents_from_naver(url):
    result = {}

    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
        
    result['title'] = soup.find('h3', id='articleTitle' ).get_text()
    content = soup.find('div', id='articleBodyContents').get_text()
    result['published_at'] = soup.find('span', {'class':'t11'}).get_text()[:10]
    result['content'] = content
    
    return result

# print(get_contents_from_naver('http://sports.news.naver.com/kbaseball/news/read.nhn?oid=052&aid=0001044585'))
# print(get_contents_from_naver('http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=032&aid=0002809430'))


# Naver
def get_contents_from_peoplepower21(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'class':'xe_content'}).get_text()
        
        result['content'] = content
        # result['published_at'] = soup.select('ul li > span')[0].get_text()[:10]
    except AttributeError as e:
        print(e)
    
    return result
# print(get_contents_from_peoplepower21('http://www.peoplepower21.org/Whistleblower/1365271'))

# yonhapnews
def get_contents_from_yonhapnews(url):
    result = {}

    response = requests.get(url)
    html = response.content.decode('utf-8')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
        
    result['title'] = soup.find('h1', {'class':'tit-article'} ).get_text()
    content = soup.find('div', { 'class':'article'}).get_text()
    result['content'] = content
    span = soup.select('.share-info .tt > em')[0].get_text()
    result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    # 
    
    return result

# print(get_contents_from_yonhapnews('http://www.yonhapnews.co.kr/bulletin/2017/06/07/0200000000AKR20170607062900003.HTML'))

# Daum
def get_contents_from_daum(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
        
    result['title'] = soup.find('h3', {'class':'tit_view'} ).get_text()
    content = soup.find('div', { 'class':'article_view'}).get_text()
    result['content'] = content
    span = soup.select('.head_view .info_view > span.txt_info')[1].get_text()[3:]
    result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] 
    # 
    
    return result

# print(get_contents_from_daum('http://v.media.daum.net/v/20170521112047313'))

# JOONGANG 
def get_contents_from_joins(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    result['title'] = soup.find('h1', id='article_title' ).get_text()
    content = soup.find('div', id='article_body').get_text()
    
    result['content'] = content
    span = soup.select('div.byline > em')[1].get_text()[3:]
    result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    # 

    return result

# print(get_contents_from_joins('http://news.joins.com/article/21593657?cloc=joongang|article|clickraking'))

# Donga
def get_contents_from_donga(url):
    result = {}

    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'article_txt'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.title_foot > span')[1].get_text()[3:13]
        # 

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_donga('http://news.donga.com/Main/3/all/20170521/84484495/1'))

#SBS
def get_contents_from_sbs(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('h3', {'id':'vmNewsTitle'}).get_text()
        content = soup.find('div', {'class':'main_text'}).get_text()
        
        result['content'] = content
        span = soup.select('span.date > span')[0].get_text()[:10]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
        # 

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_sbs('http://news.sbs.co.kr/news/endPage.do?news_id=N1004206472&plink=TOPHEAD&cooper=SBSNEWSMAIN'))

# Hani
def get_contents_from_hani(url):
    result = {}

    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('span', {'class':'title'}).get_text()
        content = soup.find('div', {'class':'text'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('p.date-time > span')[0].get_text()[4:14]
        # 
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)
    return result

# print(get_contents_from_hani('http://www.hani.co.kr/arti/culture/entertainment/776675.html?dable=30.52.3'))

# Chosun
def get_contents_from_chosun(url):
    result = {}

    response = requests.get(url)
    html = response.content.decode('cp949')    
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('h1', {'id':'news_title_text_id'}).get_text()
        content = soup.find('div', {'id':'news_body_id'}).get_text()
        
        result['content'] = content
        span = soup.select('div.date_ctrl_2011 > p#date_text')[0].get_text().strip()[5:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
        # 
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)
    return result

# print(get_contents_from_chosun('http://news.chosun.com/site/data/html_dir/2017/05/22/2017052200009.html'))

def get_contents_from_khan(url):
    result = {}

    response = requests.get(url)
    html = response.content.decode('cp949')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('h1', {'id':'article_title'}).get_text()
        content = soup.find('div', {'class':'art_cont'}).get_text()
        
        result['content'] = content
        span = soup.select('div.byline > em')[0].get_text()[5:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
        # 
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_khan('http://news.khan.co.kr/kh_news/khan_art_view.html?artid=200503071727151&code=210000'))

# KoreaTimes
# def get_contents_from_koreatimes(url):
#     result = {}
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'lxml')
    
#     try:
#         result['title'] = soup.find('h1').get_text()
#         content = soup.find('div', {'class':'view_page_news_article_wrapper'}).get_text()
#         result['content'] = content[:400]
#         result['published_at'] = soup.select('div.info_arti span.upload_date')
#         print(span)
#         

#     except AttributeError as e:
#         print(e)
    
#     return result

# print(get_contents_from_koreatimes('http://koreatimes.com/article/20170519/1057078'))

# SeGye
def get_contents_from_segye(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('h1', {'class': 'headline'}).get_text()
        content = soup.find('div', {'id':'article_txt'}).get_text()
        
        result['content'] = content
        span = soup.select('.article_head .clearfx > div')[0].get_text()
        result['published_at'] = span[4:15] 
        # 
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_segye('http://segye.com/newsView/20170521002289'))

# MK
def get_contents_from_mk(url):
    result = {}

    mbn = True
    if mbn :
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            result['title'] = soup.find('p', {'class': 'tit'}).get_text()
            result['content'] = soup.find('div', {'id':'newsViewArea'}).get_text()[:400]
            result['published_at'] = soup.select('span.tim> span')[0].get_text()[5:16]
        except AttributeError as e:
            print(e)
    else:
        response = requests.get(url)
        html = response.content.decode('cp949')
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            result['title'] = soup.find('p', {'class': 'tit'}).get_text()
            result['content'] = soup.find('div', {'id':'newsViewArea'}).get_text()[:400]  + ' ......'
            span = soup.select('div.news_title_author ul > li')[0].get_text()[5:]
            result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
        except AttributeError as e:
            print(e)
        
        return result

# print(get_contents_from_mk('http://mbn.mk.co.kr/pages/onair/mbnweblive.mbn'))

# Heraldcorp
def get_contents_from_heraldcorp(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('h1').get_text()
        content = soup.find('div', {'id':'articleText'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.find('li', {'class':'ellipsis'}).get_text()[5:16]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_heraldcorp('http://news.heraldcorp.com/view.php?ud=20170502000944&nt=1&md=20170502165557_BL'))

# Pressian
def get_contents_from_pressian(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('div', {'class':'title'}).get_text()
        content = soup.find('div', {'id':'CmAdContent'}).get_text()
        
        result['content'] = content
        span = soup.find('div', {'class':'date'}).get_text().strip()
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_pressian('http://www.pressian.com/news/article.html?no=159852'))

# hankookilbo
def get_contents_from_hankookilbo(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        content = soup.find('article', {'id':'article-body'}).get_text()
        
        result['content'] = content
        span = soup.select('div.writeOption > p')[0].get_text()[5:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_hankookilbo('http://www.hankookilbo.com/v/85f7c84ddb7045258f3f7d626421968e'))

# nocutnews
def get_contents_from_nocutnews(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"og:title"})[0]['content']
        content = soup.find('div', {'id':'pnlContent'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('ul li > span')[0].get_text()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_nocutnews('http://www.nocutnews.co.kr/news/4778190'))

# newsis
def get_contents_from_newsis(url):
    result = {}

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'id':'textBody'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.find('div', {'class':'date'}).get_text()[3:13]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_newsis('http://www.newsis.com/view/?id=NISX20170502_0014869434&cid=10322'))

# wowtv
def get_contents_from_wowtv(url):
    result = {}

    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'viewContent_3'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.find('p', {'class':'writeDate'}).get_text()[5:15]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_wowtv('http://www.wowtv.co.kr/newscenter/news/view.asp?bcode=T30001000&artid=A201705310186'))


# munhwa
def get_contents_from_munhwa(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'NewsAdContent'}).get_text()
        
        result['content'] = content
        # pattern = re.search('(?<=게재 일자 : )(.*?)(?=<\/td>)', re.DOTALL)
        # matches = pattern.search(html)
        # print(matches)
        # result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_munhwa('http://www.munhwa.com/news/view.html?no=20170531MW140230810045'))

# Money Today
def get_contents_from_mt(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'id':'textBody'}).get_text()
        
        result['content'] = content
        span = soup.select('.info .infobox1 span.num')[0].get_text()[2:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_mt('http://news.mt.co.kr/mtview.php?no=2017050214583613009&cast=1&STAND'))

# fnnews
def get_contents_from_fnnews(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        content = soup.find('div', {'class':'cont_txt_read'}).get_text()
        
        result['content'] = content
        span = soup.select('ul.news_data li.list_02')[0].get_text()[5:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_fnnews('http://www.fnnews.com/news/201705301745340788'))

# kbs
def get_contents_from_kbs(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        content = soup.find('div', {'id':'cont_newstext'}).get_text()
        
        result['content'] = content
        span = soup.select('div.date_area span.date')[0].get_text()[3:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kbs('http://news.kbs.co.kr/news/view.do?ncd=3490361'))

# sedaily (서울경제)
def get_contents_from_sedaily(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'view_con'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.view_top ul li.letter')[0].get_text()[0:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_sedaily('http://www.sedaily.com/NewsView/1OG4Y883DA'))

# kmib 국민일보
def get_contents_from_kmib(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find(attrs={"name":"title"})['content']
        content = soup.find('div', {'id':'articleBody'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.date span.t11')[0].get_text()[0:10]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kmib('http://news.kmib.co.kr/article/view.asp?arcid=0011507380&code=61121111&sid1=soc'))

# kheraldm (Korea Herald)
def get_contents_from_kheraldm(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'articleText'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.writedata p.date')[0].get_text().strip()[12:22]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kheraldm('http://www.koreaherald.com/view.php?ud=20170531000848&kr=1&nt=1'))

# Digital Times 
def get_contents_from_dt(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'NewsAdContent'}).get_text()
        
        result['content'] = content
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_dt('http://www.dt.co.kr/contents.html?article_no=2017060102100932048002'))

# mediatoday
def get_contents_from_mediatoday(url):
    result = {}

    if 'beta' in url:
        response = requests.get(url)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            result['title'] = soup.find('title').get_text()
            content = soup.find('div', {'class':'entry-content'}).get_text()
            result['content'] = content
            result['published_at'] = soup.select('a time.entry-date.published')[0].get_text()
        except AttributeError as e:
            print(e)
    else:
        response = requests.get(url)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        
        try:
            result['title'] = soup.find('title').get_text()
            content = soup.find('div', {'id':'talklink_contents'}).get_text()
            
            result['content'] = content
            span = soup.select('span.arl_view_date')[0].get_text().strip()
            result['published_at'] = span[:4] + '-' + span[6:8] + '-' + span[10:12]
        except AttributeError as e:
            print(e)
    
    print(result)
    return result

# print(get_contents_from_mediatoday('http://beta.mediatoday.co.kr/131631/'))

# hankyung
def get_contents_from_hankyung(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        content = soup.find('div', {'id':'newsView'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.date span.time')[0].get_text().strip()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_hankyung('http://news.hankyung.com/politics/2017/05/31/2017053129231'))

# bloter
def get_contents_from_bloter(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'article--content'}).get_text()
        
        result['content'] = content
        span = soup.select('div.article--date span.publish')[0].get_text()
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_bloter('http://www.bloter.net/archives/281215'))

# seoul
def get_contents_from_seoul(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'atic_txt1'}).get_text()
        
        result['content'] = content
        # result['published_at'] = soup.select('div.v_snt p.v_days')[0].get_text().strip()[5:15]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_seoul('http://www.seoul.co.kr/news/newsView.php?id=20110617025001'))

# ohmynews
def get_contents_from_ohmynews(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'at_contents'}).get_text()
        result['content'] = content
        span = soup.select('div.info_data div')[0].get_text()
        result['published_at'] = '20' + span[:2] + '-' + span[3:5] + '-' + span[6:8]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ohmynews('http://www.ohmynews.com/NWS_Web/View/at_pg.aspx?CNTN_CD=A0002330490&PAGE_CD=ET001&BLCK_NO=1&CMPT_CD=T0016'))

# ytn
def get_contents_from_ytn(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'CmAdContent'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.article_info div.extra_info')[0].get_text().strip()[9:19]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ytn('http://www.ytn.co.kr/_ln/0104_201705021709022162'))

# etnews
def get_contents_from_etnews(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('section', {'id':'articleBody'}).get_text()
        
        result['content'] = content
        span = soup.select('div.article_header_sub time.date')[0].get_text().strip()[6:16]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_etnews('http://www.etnews.com/20170501000134?mc=ns_001_00001'))

# inews24
def get_contents_from_inews24(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'news_content'}).get_text()
        
        result['content'] = content
        span = soup.select('div.info span')[0].get_text().strip()
        result['published_at'] = span[:4] + '-' + span[6:8] + '-' + span[10:12]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_inews24('http://news.inews24.com/php/news_view.php?g_serial=1020560&g_menu=020310'))

# asiae
def get_contents_from_asiae(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'article'}).get_text()
        
        result['content'] = content

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_asiae('http://view.asiae.co.kr/news/view.htm?idxno=2017050216380300711'))

# VOP
def get_contents_from_vop(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'contents'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.article-info div.meta-text')[1].get_text().strip()[3:].strip()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_vop('http://www.vop.co.kr/A00001164335.html'))


# imbc
def get_contents_from_imbc(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('section', {'class':'body'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('section.wrap_time span')[1].get_text().strip()[4:].strip()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_imbc('http://imnews.imbc.com/replay/2017/nwdesk/article/4325710_21408.html?xtr_cate=LK&xtr_ref=r8&xtr_kw=N&xtr_area=k18&xtr_cp=c5'))

# sisain
def get_contents_from_sisain(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'itemprop':'articleBody'}).get_text()
        result['content'] = content
        span = soup.select('span.arl_view_date')[0].get_text().strip()
        result['published_at'] = span[:4] + '-' + span[6:8] + '-' + span[10:12]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_sisain('http://www.sisain.co.kr/?mod=news&act=articleView&idxno=29197'))

# ilyo
def get_contents_from_ilyo(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'itemprop':'articleBody'}).get_text()
        
        result['content'] = content
        span = soup.select('div.actInfo p')[0].get_text().strip()[9:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ilyo('http://ilyo.co.kr/?ac=article_view&entry_id=249795'))


# naeil
def get_contents_from_naeil(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"title"})[0]['content']
        content = soup.find('div', {'id':'contents'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.articleArea div.date')[0].get_text().strip()[:10]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_naeil('http://www.naeil.com/news_view/?id_art=239006'))


# ddanzi
def get_contents_from_ddanzi(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'read_body'}).get_text()
        
        result['content'] = content
        result['published_at'] = soup.select('div.read_header p.time')[0].get_text().strip()[:10]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ddanzi('http://www.ddanzi.com/ddanziNews/185892390'))

# tf
def get_contents_from_tf(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'id':'content_area'}).get_text()
        
        result['content'] = content
        span = soup.select('div.readLeft div.timeTxt')[0].get_text().strip()[4:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] 
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_tf('http://news.tf.co.kr/read/economy/1692287.htm?ref=read_top10'))


# asiatoday
def get_contents_from_asiatoday(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('dl', {'itemprop':'articleBody'}).get_text()
        
        result['content'] = content
        span = soup.select('dl dd span.wr_day')[0].get_text().strip()[5:]
        result['published_at'] = span[:4] + '-' + span[6:8] + '-' + span[10:12]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_asiatoday('http://www.asiatoday.co.kr/view.php?key=20170601000925248'))


# lawtimes
def get_contents_from_lawtimes(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('article', {'itemprop':'articleBody'}).get_text()
        
        result['content'] = content        
        result['published_at'] = soup.select('header.article-header time')[0].get_text().strip()[:10]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_lawtimes('https://www.lawtimes.co.kr/Legal-News/Legal-News-View?serial=118415&kind=AE'))



# redian
def get_contents_from_redian(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'redian-view-text'}).get_text()
        
        result['content'] = content
        span = soup.select('div.redian-view-date')[0].get_text().strip()
        result['published_at'] = span[:4] + '-' + span[6:8] + '-' + span[10:12] # 2017년 05월 31일

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_redian('http://www.redian.org/archive/111269'))


# mediaus
def get_contents_from_mediaus(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    # script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    # html = script.sub('', html)
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'content'}).get_text()
        
        result['content'] = content
        span = soup.select('div.info span')[2].get_text().strip()
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] # 2017.06.01 08:47

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_mediaus('http://www.mediaus.co.kr/news/articleView.html?idxno=93165'))



# sources = ['naver', 'daum', 'joins', 'chosun', 'donga', 'sbs']

def get_news(search_url):
    name = extract_name(search_url)
    result = {}
    try:
        result = eval('get_contents_from_'+name+'("' + search_url+'")')
    except NameError as e:
        print(e)

    result['url'] = search_url
    result['media'] = extract_name(search_url)
    print(result)
    return result

					
