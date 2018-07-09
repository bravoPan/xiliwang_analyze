from xiliwang_analyze.page_parsing import sel_mag_information



def filter_score():
    s = 0
    count = 0
    for i in sel_mag_information.find():
        num = i['score']
        s = s + int(num)
        count += 1
    print(s, count, s/count)

filter_score()

