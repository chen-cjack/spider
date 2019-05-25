# -*- coding: utf-8 -*-
import scrapy
from novel.items import ChapterItem

class ChapterSpider(scrapy.Spider):

    name = 'chapter'
    custom_settings = {
        "ITEM_PIPELINES": {
            'novel.pipelines.ChapterPipeline':301
        }
    }
    allowed_domains = ['www.quanshuwang.com']

    def __init__(self):
        from novel.myexecute import get_novel_url

        self.novel_url = get_novel_url()
        # self.start_urls = [novel_url]
        self.start_urls = [self.novel_url]

    def parse(self, response):
        import re
        #目录 //div[@id='chapter']/div/div/ul//li/a/@href  http://www.quanshuwang.com/book/90/90295/26084016.html
        #字数 //div[@id='chapter']/div/div/ul//li/a/@title  要拼接 第0003章 密林救美，共2706字
        #章节名称//div[@id='chapter']/div/div/ul//li/a/text()

        chapter_list = response.xpath("//div[@id='chapter']/div/div/ul//li")
        for chapter in chapter_list:
            chapter_name = chapter.xpath("./a/text()").extract_first()
            chapter_size = chapter.xpath("./a/@title").extract_first().split("，")[-1]
            chapter_url = chapter.xpath("./a/@href").extract_first()
            chapter_id = chapter_url.split("/")[-1].split(".")[0]
            chapter_novelid = chapter_url.split('/')[-2]


            item = ChapterItem()
            item["chapter_name"] = chapter_name
            item["chapter_id"] = chapter_id
            item["chapter_size"] = chapter_size
            item["chapter_url"] =  chapter_url
            item["chapter_novelid"] = chapter_novelid
            yield scrapy.Request(url=chapter_url,callback=self.charter_parse,meta={"chapter":item})

    def charter_parse(self, response):
        item = response.meta['chapter']
        contents  = response.xpath('//div[@id="content"]/text()').extract()#列表
        chapter_content = ""
        for content in contents:
            chapter_content += content
        item['chapter_content'] = chapter_content
        yield item



