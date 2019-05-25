# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):

    #小说名
    name = scrapy.Field()
    #作者
    author = scrapy.Field()
    #小说简介
    intro = scrapy.Field()
    #小说链接
    novel_url= scrapy.Field()
    #小说id
    novel_id = scrapy.Field()
    #小说分类
    category = scrapy.Field()
    #小说封面
    img_src = scrapy.Field()




class ChapterItem(scrapy.Item):
    #章节名称
    chapter_name = scrapy.Field()
    #章节id
    chapter_id = scrapy.Field()
    #字数
    chapter_size = scrapy.Field()
    #章节Url
    chapter_url = scrapy.Field()
    #章节内容
    chapter_content = scrapy.Field()
    #novel_id
    chapter_novelid = scrapy.Field()

