#-*- coding:utf-8 -*-
import re
import requests
from collections import Counter
from bs4 import BeautifulSoup

# Extract Source Name
def extract_name(url):
    name = re.findall('\.(\w+)\.com?', url)
    return name[0]

# def get_person_name(html):
#     return None

# def get_person_name(html):
#     old = [ '정부의', '정부가', '지지율', '호남의', '하지만',  '구치소', '문제가', '복잡한', '대통령', '문제다', '지난해', '보이지', '사람이', '심지어', '기록이', '방대한', '제대로', '상당한', '인력이', '아니다', '어렵다', '이라고', '정치적', '자기가', '유리한', '아니면', '시간이', '태극기', '인상이', '한동안', '최대한', '설치로', '이동식', '나머지', '시설도', '반입한', '반입해', '여의도', '갈등이', '위기가', '예정인', '보인다', '기반인']
#     pattern = re.compile(r'\b[김이박최정강조윤장임오한신서권황안송류홍전고문손양배조백허남심유노하전정곽성차유구우주임나신민진지엄원채강천양공현방변함노염여추변도석신소선주설방마정길위연표명기금왕반옥육진인맹제탁모남궁여장어유국은편용강구예봉한경소사석부황보가복천목태지형피계전감음두진동장온송경제갈사공호하빈선우연채우범설양갈좌노반팽승공간상기국시서문위도시이호채강진빈방단서견원방창당순마화구모이양종승성독고옹빙장추편아도평대풍궁강연견점흥섭국내제여낭봉해판초필궉근사매동방호두미요옹야묵자만운환범탄곡종창사영포엽수애단부순순돈학비개영후십뇌난춘수준초운내묘담장곡어금강전삼저군초교영순단후누돈소봉][^히은는을를늘에르었겼엔워할에쉬했떻쩌렇드디갔움들팎\.\s\(\)][^히은는을를늘에르었겼엔워할에된와야과했디체터니데\"\.\s\(\)=]\b', re.MULTILINE)
#     names = pattern.findall(html)
# 
#     result = []
#     count = Counter(names)
#     # print(count.most_common(2))
#     for name,value in count.most_common(2):
#         if name not in old:
#             result.append(name)
#     return result

# Naver
def get_contents_from_naver(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'html.parser')
        
    result['title'] = soup.find('h3', id='articleTitle' ).get_text()
    content = soup.find('div', id='articleBodyContents').get_text()
    result['published_at'] = soup.find('span', {'class':'t11'}).get_text()
    result['content'] = content[:400]

    # names = get_person_name(content)
    result['names'] = names
    
    return result

# print(get_contents_from_naver('http://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=100&cid=1045984&iid=49376956&oid=001&aid=0009223780&ptype=052'))


# yonhapnews
def get_contents_from_yonhapnews(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
        
    result['title'] = soup.find('h1', {'class':'tit-article'} ).get_text()
    content = soup.find('div', { 'class':'article'}).get_text()
    result['content'] = content[:400]
    span = soup.select('.share-info .tt > em')[0].get_text()
    result['published_at'] = span
    # result['names'] = get_person_name(content)
    
    return result

# print(get_contents_from_yonhapnews('http://www.yonhapnews.co.kr/bulletin/2017/04/12/0200000000AKR20170412112300054.HTML'))

# Daum
def get_contents_from_daum(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
        
    result['title'] = soup.find('h3', {'class':'tit_view'} ).get_text()
    content = soup.find('div', { 'class':'article_view'}).get_text()
    result['content'] = content[:400]
    span = soup.select('.head_view .info_view > span.txt_info')[1].get_text()[3:]
    result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] + span[11:]
    # result['names'] = get_person_name(content)
    
    return result

# print(get_contents_from_daum('http://v.media.daum.net/v/20170521112047313'))

# JOONGANG 
def get_contents_from_joins(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    result['title'] = soup.find('h1', id='article_title' ).get_text()
    content = soup.find('div', id='article_body').get_text()
    result['content'] = content[:400] + ' ......'
    span = soup.select('div.byline > em')[1].get_text()[3:]
    result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10]
    # result['names'] = get_person_name(content)

    return result

# print(get_contents_from_joins('http://news.joins.com/article/21593657?cloc=joongang|article|clickraking'))

# Donga
def get_contents_from_donga(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        content = soup.find('div', {'class':'article_txt'}).get_text()
        result['content'] = content[:400]
        result['published_at'] = soup.select('div.title_foot > span')[1].get_text()[3:]
        # result['names'] = get_person_name(content)

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_donga('http://news.donga.com/Main/3/all/20170521/84484495/1'))

#SBS
def get_contents_from_sbs(url):
    result = {}
    result['url'] = url
    result['media'] = extract_name(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('h3', {'id':'vmNewsTitle'}).get_text()
        content = soup.find('div', {'class':'main_text'}).get_text()
        result['content'] = content[:400]
        result['published_at'] = soup.select('span.date > span')[0].get_text()
        # result['names'] = get_person_name(content)

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_sbs('http://news.sbs.co.kr/news/endPage.do?news_id=N1004206472&plink=TOPHEAD&cooper=SBSNEWSMAIN'))

# Hani
def get_contents_from_hani(url):
    result = {}
    result['media'] = extract_name(url)
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('span', {'class':'title'}).get_text()
        content = soup.find('div', {'class':'text'}).get_text()[:400]
        result['content'] = content[:400]
        result['published_at'] = soup.select('p.date-time > span')[0].get_text()[4:]
        # result['names'] = get_person_name(content)
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)
    return result

# print(get_contents_from_hani('http://www.hani.co.kr/arti/culture/entertainment/776675.html?dable=30.52.3'))

# Chosun
def get_contents_from_chosun(url):
    result = {}
    result['media'] = extract_name(url)
    response = requests.get(url)
    html = response.content.decode('cp949')    
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('h1', {'id':'news_title_text_id'}).get_text()
        content = soup.find('div', {'id':'news_body_id'}).get_text()
        result['content'] = content[:400]
        span = soup.select('div.date_ctrl_2011 > p#date_text')[0].get_text().strip()[5:]
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] + span[10:]
        # result['names'] = get_person_name(content)
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)
    return result

# print(get_contents_from_chosun('http://news.chosun.com/site/data/html_dir/2017/05/22/2017052200009.html'))

def get_contents_from_khan(url):
    result = {}
    result['media'] = extract_name(url)
    response = requests.get(url)
    html = response.content.decode('cp949')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('h1', {'id':'article_title'}).get_text()
        content = soup.find('div', {'class':'art_cont'}).get_text()
        result['content'] = content[:400]
        span = soup.select('div.byline > em')[0].get_text()[5:]
        print(span)
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] + span[10:]
        # result['names'] = get_person_name(content)
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_khan('http://news.khan.co.kr/kh_news/khan_art_view.html?artid=201705212228015&code=940301'))

# KoreaTimes
# def get_contents_from_koreatimes(url):
#     result = {}
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'html.parser')
    
#     try:
#         result['title'] = soup.find('h1').get_text()
#         content = soup.find('div', {'class':'view_page_news_article_wrapper'}).get_text()
#         result['content'] = content[:400]
#         result['published_at'] = soup.select('div.info_arti span.upload_date')
#         print(span)
#         result['names'] = get_person_name(content)

#     except AttributeError as e:
#         print(e)
    
#     return result

# print(get_contents_from_koreatimes('http://koreatimes.com/article/20170519/1057078'))

# SeGye
def get_contents_from_segye(url):
    result = {}
    result['media'] = extract_name(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('h1', {'class': 'headline'}).get_text()
        content = soup.find('div', {'id':'article_txt'}).get_text()[:400]
        result['content'] = content[:400]
        span = soup.select('.article_head .clearfix > div')[1].get_text()
        print(span)
        result['published_at'] = span[:4] + '-' + span[5:7] + '-' + span[8:10] + span[10:]
        # result['names'] = get_person_name(content)
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_segye('http://segye.com/newsView/20170521002289'))

# MK
def get_contents_from_mk(url):
    result = {}
    response = requests.get(url)

    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('p', {'class': 'tit'}).get_text()
        result['content'] = soup.find('div', {'id':'newsViewArea'}).get_text()[:400]

    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_mk('http://mbn.mk.co.kr/pages/news/newsView.php?ref=newsstand&news_seq_no=3212989&pos=20001'))

# Heraldcorp
def get_contents_from_heraldcorp(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('h1').get_text()
        result['content'] = soup.find('div', {'id':'articleText'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_heraldcorp('http://news.heraldcorp.com/view.php?ud=20170502000944&nt=1&md=20170502165557_BL'))

# Pressian
def get_contents_from_pressian(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('div', {'class':'title'}).get_text()
        result['content'] = soup.find('div', {'id':'CmAdContent'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_pressian('http://www.pressian.com/news/article.html?no=157395'))

# hankookilbo
def get_contents_from_hankookilbo(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        result['content'] = soup.find('article', {'id':'article-body'}).get_text()[:500]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_hankookilbo('http://www.hankookilbo.com/v/b828b5db06e94a66a79e1583a942ce99'))

# nocutnews
def get_contents_from_nocutnews(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"og:title"})[0]['content']
        result['content'] = soup.find('div', {'id':'pnlContent'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_nocutnews('http://www.nocutnews.co.kr/news/4778190'))

# newsis
def get_contents_from_newsis(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        result['content'] = soup.find('div', {'id':'textBody'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_newsis('http://www.newsis.com/view/?id=NISX20170502_0014869434&cid=10322'))

# wowtv
def get_contents_from_wowtv(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'viewContent_3'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_wowtv('http://cast.wowtv.co.kr/20170502/A201705020207.html'))

# munhwa
def get_contents_from_munhwa(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('span', {'class':'title'}).get_text()
        result['content'] = soup.find('div', {'id':'NewsAdContent'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_munhwa('http://www.munhwa.com/news/view.html?no=20170502MW165018122079&w=ns'))

# Money Today
def get_contents_from_mt(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        result['content'] = soup.find('div', {'id':'textBody'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_mt('http://news.mt.co.kr/mtview.php?no=2017050214583613009&cast=1&STAND'))

# fnnews
def get_contents_from_fnnews(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"property":"og:title"})[0]['content']
        result['content'] = soup.find('div', {'class':'cont_txt_read'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_fnnews('http://www.fnnews.com/news/201705021357289379'))

# kbs
def get_contents_from_kbs(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        result['content'] = soup.find('div', {'id':'cont_newstext'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kbs('http://news.kbs.co.kr/news/view.do?ncd=3474362'))

# sedaily (서울경제)
def get_contents_from_sedaily(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        result['content'] = soup.find('div', {'class':'view_con'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_sedaily('http://www.sedaily.com/NewsView/1OFRMZDDZO?OutLink=nstand'))

# kmib 국민일보
def get_contents_from_kmib(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        result['content'] = soup.find('div', {'id':'articleBody'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kmib('http://news.kmib.co.kr/article/view.asp?arcid=0923740805&code=11121900&sid1=pol&cp=nv2'))

# kheraldm (Korea Herald)
def get_contents_from_kheraldm(url):
    result = {}
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'articleText'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_kheraldm('http://khnews.kheraldm.com/view.php?ud=20170502000810&kr=1&nt=1&md=20170502180439_BL&kr=1'))

# Digital Times 
def get_contents_from_dt(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'NewsAdContent'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_dt('http://www.dt.co.kr/contents.html?article_no=2017050202109958033005&naver=stand'))

# mediatoday
def get_contents_from_mediatoday(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'talklink_contents'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_mediatoday('http://www.mediatoday.co.kr/?mod=news&act=articleView&idxno=136601'))

# hankyung
def get_contents_from_hankyung(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.findAll(attrs={"name":"title"})[0]['content']
        result['content'] = soup.find('div', {'id':'newsView'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_hankyung('http://stock.hankyung.com/news/app/newsview.php?aid=2017050237121&nv=3'))

# bloter
def get_contents_from_bloter(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'class':'article--content'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_bloter('http://www.bloter.net/archives/278560'))

# seoul
def get_contents_from_seoul(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    script = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
    html = script.sub('', html)
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'atic_txt1'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_seoul('http://www.seoul.co.kr/news/newsView.php?id=20170503009003&wlog_sub=svt_006'))

# ohmynews
def get_contents_from_ohmynews(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'class':'at_contents'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ohmynews('http://www.ohmynews.com/NWS_Web/View/at_pg.aspx?CNTN_CD=A0002322369&PAGE_CD=N0004&utm_source=naver&utm_medium=newsstand&utm_campaign=top1&CMPT_CD=E0018'))

# ytn
def get_contents_from_ytn(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'CmAdContent'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_ytn('http://www.ytn.co.kr/_ln/0104_201705021709022162'))

# etnews
def get_contents_from_etnews(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('section', {'id':'articleBody'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_etnews('http://www.etnews.com/20170501000134?mc=ns_001_00001'))

# inews24
def get_contents_from_inews24(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'id':'news_content'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_inews24('http://news.inews24.com/php/news_view.php?g_serial=1020560&g_menu=020310'))

# asiae
def get_contents_from_asiae(url):
    result = {}
    response = requests.get(url)
    html = response.content.decode('cp949')
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        result['title'] = soup.find('title').get_text()
        result['content'] = soup.find('div', {'class':'article'}).get_text()[:400]
    except AttributeError as e:
        print(e)
    
    return result

# print(get_contents_from_asiae('http://view.asiae.co.kr/news/view.htm?idxno=2017050216380300711'))



# sources = ['naver', 'daum', 'joins', 'chosun', 'donga', 'sbs']

def get_news(search_url):
    name = extract_name(search_url)
    result = {}
    try:
        result = eval('get_contents_from_'+name+'("' + search_url+'")')
    except NameError as e:
        print(e)

    return result

					
