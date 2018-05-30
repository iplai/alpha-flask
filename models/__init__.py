# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from mongoengine import *

type_choices = (
    (1, '政策通知'),
    (2, '项目公示'),
    (3, '无关信息')
)


class Keyword(Document):
    word = StringField(max_length=255, verbose_name='名称')
    type = IntField(unique_with='word', choices=type_choices)


class Institution(Document):
    name = StringField(max_length=255, verbose_name='名称', unique=True)
    short_name = StringField(max_length=255, verbose_name='别名')
    keywords = ListField(ReferenceField(Keyword))
    district = StringField(max_length=255, verbose_name='地区')
    url = URLField(verbose_name='URL地址', unique=True)
    url_list = ListField(URLField(), verbose_name='爬取页面')
    remarks = StringField(verbose_name='备注', null=True, blank=True)
    item_xpath = StringField(max_length=255)
    title_xpath = StringField(max_length=255)
    url_xpath = StringField(max_length=255)
    pub_date_xpath = StringField(max_length=255)
    date_created = DateTimeField(default=datetime.datetime.utcnow, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow, required=True)

    crawl_latest = BooleanField(default=False)
    crawl_all = BooleanField(default=False)
    last_crawled = IntField(default=0)

    def __unicode__(self):
        return self.short_name if self.short_name else self.name


class Info(Document):
    title = StringField(max_length=255, verbose_name='标题')
    url = URLField(verbose_name='URL地址', unique=True)
    pub_date = DateTimeField()
    type = IntField(choices=type_choices)
    institution = ReferenceField(Institution)

    def __unicode__(self):
        return self.title
