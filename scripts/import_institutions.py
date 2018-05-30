# coding=utf-8
import json
import codecs

from models import Institution, Keyword

institutions = json.load(codecs.open('institutions.json', encoding='utf-8'))
for institution in institutions:
    tem = Institution(
        name=institution['name'],
        short_name=institution['short_name'],
        district=u'深圳市',
        url=institution['url'],
        url_list=institution['url_list'],
        remarks=institution['remarks'],
        item_xpath=institution['item_xpath'],
        title_xpath=institution['title_xpath'],
        url_xpath=institution['url_xpath'],
        pub_date_xpath=institution['pub_date_xpath'],
    )
    keywords = []
    for j in range(1, 4):
        for i in institution['words' + str(j)]:
            try:
                keywords.append(Keyword.objects.get(word=i, type=j))
            except:
                Keyword.objects.create(word=i, type=j)
                keywords.append(Keyword.objects.get(word=i, type=j))
    tem.keywords = keywords
    tem.save()
