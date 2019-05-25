# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
import pymysql
from novel.items import NovelItem,ChapterItem


class NovelPipeline(object):

    def __init__(self):
        # 获取settings中的参数
        settings = get_project_settings()
        self.host = settings['USER_HOST']
        self.port = settings['USER_PORT']
        self.name = settings['USER_NAME']
        self.password = settings['USER_PASSWORD']
        self.db = settings['USER_DB']
        self.charset = settings['USER_CHARSET']
        #链接mysql
        self.connect = pymysql.Connect(host=self.host,
                        port=self.port,
                        user=self.name,
                        password=self.password,
                        database=self.db,
                        charset=self.charset
                      )
        self.cursor = self.connect.cursor()

        #创建表
        # self.cursor.execute('drop table if exists novel1')
        sql1 = 'select table_name from information_schema.tables where table_name="novel"' #查询是否存在该表
        sql2 = "create table novel(id int primary key auto_increment,name varchar(64),author varchar(64),novel_id varchar(16),category varchar(16),novel_url varchar(255),img_src varchar(255),intro varchar(255))"
        if not self.cursor.execute(sql1):
            self.cursor.execute(sql2)
        self.d_number = 0

    def open_spider(self,spoder):
        import time
        self.start = time.time()

    def process_item(self, item, spider):
        if isinstance(item,NovelItem):
            xs_name = item['name']
            xs_author = item["author"]
            xs_id = item["novel_id"]
            xs_category = item["category"]
            xs_url = item["novel_url"]
            xs_intro = item["intro"]
            xs_img = item["img_src"]
            try:
                sql1 = "select * from novel where novel_id="+xs_id
                sql2 = "insert into novel(name,author,novel_id,category,novel_url,img_src,intro) values('{}','{}','{}','{}','{}','{}','{}')".format(xs_name,xs_author,xs_id,xs_category,xs_url,xs_img,xs_intro)
                if not self.cursor.execute(sql1):
                    self.cursor.execute(sql2)
                    self.d_number += 1
                self.connect.commit()#提交
            except Exception as e:
                print('数据库操作发生异常，数据写入失败：', e)
                self.connect.rollback()
            return item

    def close_spider(self,spider):
        import time
        self.cursor.close()
        self.connect.close()
        print('%d条数据插入成功，数据库已关闭。' % self.d_number)
        end_time = time.time()
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start))  # 转化格式
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))  # 转化格式
        print('爬虫开始结束时间     {}'.format(start_time))
        print('爬虫程序结束时间     {}'.format(finish_time))
        # 运行总耗时，时:分:秒
        Total_time = end_time - self.start
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        print("爬虫程序总耗时       %d时:%02d分:%02d秒" % (h, m, s))


class ChapterPipeline(object):

    def __init__(self):
        # 获取settings中的参数
        settings = get_project_settings()
        self.host = settings['USER_HOST']
        self.port = settings['USER_PORT']
        self.name = settings['USER_NAME']
        self.password = settings['USER_PASSWORD']
        self.db = settings['USER_DB']
        self.charset = settings['USER_CHARSET']
        #链接mysql
        self.connect = pymysql.Connect(host=self.host,
                        port=self.port,
                        user=self.name,
                        password=self.password,
                        database=self.db,
                        charset=self.charset
                      )
        self.cursor = self.connect.cursor()
        #创建表
        self.cursor.execute('drop table if exists chapter')
        sql = "create table chapter(id int primary key auto_increment,chapter_name varchar(64),chapter_id varchar(64),chapter_size varchar(16),chapter_novelid varchar(16),chapter_url varchar(64),chapter_content text)"
        self.cursor.execute(sql)
        #数据操作条数
        self.d_number = 0

    def open_spider(self, spider):
        import time
        self.start = time.time()


    def process_item(self, item, spider):
        if isinstance(item, ChapterItem):
            c_name = item['chapter_name']
            c_id = item["chapter_id"]
            c_size = item["chapter_size"]
            c_url = item["chapter_url"]
            c_content = item["chapter_content"]
            c_novelid = item["chapter_novelid"]

            try:
                sql = "insert into chapter(chapter_name,chapter_id,chapter_size,chapter_novelid,chapter_url,chapter_content) values('{}','{}','{}','{}','{}','{}')".format(c_name, c_id, c_size,c_novelid, c_url, c_content)
                if self.cursor.execute(sql):
                    self.d_number += 1
                self.connect.commit()  # 提交
            except Exception as e:
                print('数据库操作发生异常，数据写入失败：', e)
                self.connect.rollback()
            return item

    def close_spider(self,spider):
        import time
        self.cursor.close()
        self.connect.close()
        print('%d条数据插入成功，数据库已关闭。'%self.d_number)
        end_time = time.time()
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start))  # 转化格式
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))  # 转化格式
        print('爬虫开始结束时间     {}'.format(start_time))
        print('爬虫程序结束时间     {}'.format(finish_time))
        # 运行总耗时，时:分:秒
        Total_time = end_time - self.start
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        print("爬虫程序总耗时       %d时:%02d分:%02d秒" % (h, m, s))

