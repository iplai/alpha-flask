# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from mongoengine import *

connect('alpha_flask')
# Create your models here.
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

    def __str__(self):
        return self.short_name if self.short_name else self.name
