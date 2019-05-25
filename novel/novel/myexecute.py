from scrapy import cmdline
import pymysql
import time


def crawl_novel():
    cmdline.execute("scrapy crawl novel".split())


#单本小说整体爬取
def crawl_chapter():
    cmdline.execute("scrapy crawl chapter".split())

#获得小说url
# def get_novel_url(novel_id):
#     novel_id = novel_id
#     novel_url = ""
#
#     if len(novel_id) == 6:
#         novel_url = "http://www.quanshuwang.com/book/" + novel_id[:3] + "/" + novel_id
#
#     elif len(novel_id) == 5:
#         novel_url = "http://www.quanshuwang.com/book/"+novel_id[:2]+"/"+novel_id
#
#     elif len(novel_id) == 4:
#         novel_url = "http://www.quanshuwang.com/book/" + novel_id[:1] + "/" + novel_id
#
#     elif len(novel_id) == 3:
#         novel_url = "http://www.quanshuwang.com/book/0/" + novel_id
#     return novel_url



#查询小说
def get_novel_url():
    # 链接mysql
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'cl970327'
    db = 'novel'
    charset = 'utf8'
    connect = pymysql.connect(host=host,port=port,user=user,password=password,database=db,charset=charset)
    cousor = connect.cursor()
    q_name = input("请输入要爬取小说的名称：")
    sql = "select name,author,novel_id,category,intro  from novel where name='{}'".format(q_name)
    cousor.execute(sql)
    result = cousor.fetchone()
    cousor.close()
    connect.close()

    if result:
        print("*****************************************")
        print('共搜索到一个结果')
        print("书名             ：",result[0])
        print("作者             ：", result[1])
        print("小说id           ：", result[2])
        print("小说类型         ：", result[3])
        print('*****************************************')
        print("开始下载")
        time.sleep(1)
        # print(type(result[2]))
        novel_id = result[2]
        # print(result)
        # print(type(result))

        if len(novel_id) == 6:
            novel_url = "http://www.quanshuwang.com/book/" + novel_id[:3] + "/" + novel_id

        elif len(novel_id) == 5:
            novel_url = "http://www.quanshuwang.com/book/" + novel_id[:2] + "/" + novel_id

        elif len(novel_id) == 4:
            novel_url = "http://www.quanshuwang.com/book/" + novel_id[:1] + "/" + novel_id

        elif len(novel_id) == 3:
            novel_url = "http://www.quanshuwang.com/book/0/" + novel_id
        return novel_url


    else:
        print("暂未收录该小说")







if __name__ == "__main__":
    print("进入爬虫系统中------")

    while True:
        print("请选择任务： 1、更新数据库中的小说信息  2、爬取指定小说内容 ")
        str1 = input('我的选择是：')
        if str1 == "1":

            print("请确认操作:  yes   or    no")
            str2 = input()
            if str2 == "yes":
                crawl_novel()
                break

        if str1 == "2":

            print("正在起动爬虫程序...")

            crawl_chapter()
            break






