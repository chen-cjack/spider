# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from novel.items import NovelItem


class NovelSpider(CrawlSpider):
    name = 'novel'
    #指定pipeline
    custom_settings = {
        "ITEM_PIPELINES"  : {
                'novel.pipelines.NovelPipeline': 300,
        }
    }
    allowed_domains = ['www.quanshuwang.com']
    start_urls = [
                  'http://www.quanshuwang.com/list/1_1.html',
                  'http://www.quanshuwang.com/list/2_1.html',
                  'http://www.quanshuwang.com/list/3_1.html',
                  'http://www.quanshuwang.com/list/4_1.html',
                  'http://www.quanshuwang.com/list/5_1.html',
                  'http://www.quanshuwang.com/list/6_1.html',
                  'http://www.quanshuwang.com/list/7_1.html',
                  'http://www.quanshuwang.com/list/8_1.html',
                  'http://www.quanshuwang.com/list/9_1.html',
                  'http://www.quanshuwang.com/list/10_1.html',
                  'http://www.quanshuwang.com/list/11_1.html'
                  ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='pagelink']/a"),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        #题目  //div[@id='navList']//ul/li/span/a[1]/@title
        #作者  //div[@id='navList']//ul/li/span/a[2]/text()
        #bookid //div[@id='navList']//ul/li/span/a[3]/@href   http://www.quanshuwang.cn/book_197.html
        #类别 //div[@id='navList']/div/a[2]
        #简介 //div[@id='navList']//ul/li/span/em/text()
        #图片//div[@id='navList']//ul/li/a/img/@src
        #提取当前页面所有小说
        books = response.xpath("//div[@id='navList']//ul/li")
        #提取小说类别
        category = response.xpath("//div[@id='navList']/div/a[2]/text()").get()
        for book in books:
            #提取小说名称
            name = book.xpath(".//a[1]/@title").extract_first()
            #提取作者名字
            author = book.xpath(".//a[2]/text()").extract_first()
            #提取小说简介
            intro = book.xpath(".//em/text()").extract_first()
            #提取小说url
            novel_url = book.xpath(".//a[3]/@href").extract_first()
            #提取小说id
            novel_id = novel_url.split('_')[1].split(".")[0]
            #小说封面
            img_src = book.xpath("./a/img/@src").extract_first()

            item = NovelItem()
            item["name"] = name
            item["author"] = author
            item["intro"] = intro
            item["novel_url"] = novel_url
            item["novel_id"] = novel_id
            item["category"] = category
            item["img_src"] = img_src

            yield item
