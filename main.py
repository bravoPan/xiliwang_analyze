from page_parsing import get_all_link, get_information, count_word_numer, cul_url_list, cul_info
from multiprocessing import Pool

def get_all_links_from_subject():
    for page in range(1,17):
        get_all_link(page)

db_urls = [item['url'] for item in cul_url_list.find()]
index_urls = [item['url'] for item in cul_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(get_information, rest_of_urls)
    #get_all_links_from_subject()
    pool.close()
    pool.join()