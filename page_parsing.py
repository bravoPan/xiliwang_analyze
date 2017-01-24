import pymongo
import time
from bs4 import BeautifulSoup
import requests
import random
import re

#初始化数据库(自我管理）
# client = pymongo.MongoClient('localhost', 27017)
# xipu = client['xipu']
# sel_mag_information = xipu['information']
# self_mag_url_list = xipu['url_list']

#<-------------------------------------------中西文化-------------------------------------------------------->
client = pymongo.MongoClient('localhost', 27017)
xipu = client['xipu']
cul_url_list = xipu['cul_url_list']
cul_info = xipu['cul_info']
#<---------------------------------------------------------------------------------------------------------->

#伪造浏览器
headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Mobile Safari/537.36',
    'Connection':'keep-alive',
    'Cookie':'__cfduid=d6972d84e89a0496f077de2a016ee94f81469152627; RichConsole.WebComponent.Identity=0; VZr4_2132_nofav' \
             'fid=1; ASP.NET_SessionId=jlqbk555khumbcblfmshu0qs; VZr4_2132_home_diymode=1; _ga=GA1.3.918519955.1469152' \
             '630; VZr4_2132_saltkey=g9UKIQhv; VZr4_2132_lastvisit=1484901478; VZr4_2132_ulastactivity=71cdjN2GVboTML' \
             'q72M8rI%2FgrRwDTt7DpbyT00u5L3bydiWtogyG%2F; VZr4_2132_auth=2bb7HGLfUoBbc9MkfAHpIQRAYUAlHdV7AuzsseLOL1Q0m' \
             'bsdaBhCd9NH2t6c6Stn5Vc2qXz9q2w7Rm5ESCvIF7D3Bg; VZr4_2132_lastcheckfeed=10842%7C1484905096; VZr4_2132_lip=' \
             '117.22.22.72%2C1484908362; VZr4_2132_st_t=10842%7C1484908367%7Cf22e96258f030aa09eecb703857be4b3; VZr4_2' \
             '132_forum_lastvisit=D_9_1484905127D_21_1484907563D_19_1484908367; VZr4_2132_visitedfid=19D21D9D34D36D11D' \
             '24D25D15D20; VZr4_2132_smile=1D1; VZr4_2132_st_p=10842%7C1484908651%7C9bc44795edc0ed41fa19ebc37b511f53;' \
             ' VZr4_2132_viewid=tid_3749; VZr4_2132_sid=qJ4kNU; VZr4_2132_lastact=1484908872%09forum.php%09ajax'}

proxy_list = ['http://101.200.38.16:9000',
              'http://117.90.5.0:9000',
              'http://27.22.63.157:808']

#随机获取IP地址
proxy_ip = random.choice(proxy_list)
proxies = {'ip':proxy_ip}

#获取所有列表页面
def get_all_link(page, subject=21):
    url = 'http://utalk.xjtlu.edu.cn/forum/forum.php?mod=forumdisplay&fid={}&page={}'.format(subject, page)
    wb_data = requests.get(url, headers=headers, proxies=proxies)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        for link in soup.select('tr > th > a.s.xst'):
            item_link = link.get('href')
            defact_link = 'http://utalk.xjtlu.edu.cn/forum/' + item_link
            intact_link = 'http://utalk.xjtlu.edu.cn/forum/' + item_link +'&page={}'
            end_number = give_me_last_page_number(defact_link)
            try:
                for t in map(lambda x: intact_link.format(x), [m for m in range(1, int(end_number))]):
                        cul_url_list.insert_one({'url': t})
            except TypeError:
                pass



# 获取所有详细资料
def get_information(url):
    wb_data = requests.get(url, headers=headers, proxies=proxies)
    if wb_data.status_code != 200:
        return
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find_all('a', 'nxt'):
        word = soup.find_all('td', 't_f')
        word_numbers = count_word_numer(word)
        teachers = soup.select('td > a:nth-of-type(2)')
        scores = soup.select('td.xi1')
        resons = soup.select('td.xg1')
        for word_number, teacher, score, reson in zip(word_numbers, teachers, scores, resons):
            data = {
                'word_numer': word_number,
                'teacher': teacher.text,
                'score': score.text[3],
                'reson': reson.text,
                'subject': 19,
                'url':url
            }
            cul_info.insert_one(data)
            print(data)
    else:
        pass


url = 'http://utalk.xjtlu.edu.cn/forum/forum.php?mod=viewthread&tid=3749&extra=page%3D1'



#计算每篇帖子的数目，因为其中含有html标签，所以不太精确，精确度为+50
def count_word_numer(word):
    a = []
    for i in word:
        word_number = len(str(i))
        a.append(word_number)
    return a

#爬去每个主个话题的最终页
def give_me_last_page_number(url):
    try:
        wb_data = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        last_num = soup.select('div > label > span')[1].text
        refined = re.findall(r"\d+\.?\d*", last_num)
        for t in refined:
            return t
    except IndexError:
        pass

give_me_last_page_number(url)



#中西文化http://utalk.xjtlu.edu.cn/forum/forum.php?mod=forumdisplay&fid=21&page=1
#自我管理http://utalk.xjtlu.edu.cn/forum/forum.php?mod=forumdisplay&fid=19&page=1
#详情页面http://utalk.xjtlu.edu.cn/forum/forum.php?mod=viewthread&tid=3843&extra=page%3D1&page=1