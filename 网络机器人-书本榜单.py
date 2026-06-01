import csv
import re

import requests
from lxml import html

BOOKS_TOP_URL = "https://books.toscrape.com/"

#保存数据到CSV文件中
def sava_books_info(all_books):
    with open("CSV_data/books_info.csv","w",encoding="utf-8",newline="") as f:
        csv_writer=csv.DictWriter(f,fieldnames=["书名","价格","数量","简介","类型"])
        csv_writer.writeheader()
        csv_writer.writerows(all_books)

    # with open("CSV_data/books_info.csv","w",encoding="utf-8",newline="") as f:
    #     f.write("书名，价格，数量，简介，类型\n")
    #     for book in all_books:
    #         f.write(f"{book['书名']},{book['价格']},{book['数量']},{book['简介']},{book['类型']}\n")


def get_books_price(price):
    price = price.strip() if price else ""
    book_price=re.search(r"(\d+.\d+)", price).group()
    return book_price

def get_books_count(count):
    book_Availability=count.strip() if count else ""
    return re.search(r"(\d+)", book_Availability).group()

#获取书本信息,[书名，价格，数量，简介，类型]
def get_books_info(book_info_url):
    #1.发送请求，获取书本数据
    response=requests.get(book_info_url,timeout=60)



    # 2.解析数据,获取书本信息
    document=html.fromstring(response.text)

    # 得到具体书本信息
    book_name=document.xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1/text()")
    book_price=document.xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[1]/text()")
    book_Availability=document.xpath("//*[@id='content_inner']/article/table/tr[6]/td/text()")
    book_Description=document.xpath("//*[@id='content_inner']/article/p/text()")
    book_type=document.xpath("//*[@id='content_inner']/article/table/tr[2]/td/text()")

    print(f"发送请求到{book_info_url}，还剩{re.search(r"(\d+)", book_Availability[0]).group()},获取书本信息。。。")

    book_info={
        "书名":book_name[0].strip() if book_name else "",
        "价格":get_books_price(book_price[0]),
        "数量":get_books_count(book_Availability[0]),
        "简介":book_Description[0].strip() if book_Description else "",
        "类型":book_type[0].strip() if book_type else ""
    }


    return book_info

# 主函数,定义核心逻辑
def main():

    #1.发送请求，获取榜单数据
    response=requests.get(BOOKS_TOP_URL,timeout=60)
    print("发送请求，获取书本信息。。。")

    #2.解析数据,获取书本列表
    document=html.fromstring(response.text)
    book_list=document.xpath("//*[@id='default']/div/div/div/div/section/div[2]/ol[@class='row']/li")

    all_books=[]
    #3.遍历书本列表，获取书本详情
    for book in book_list:
        book_urls=book.xpath("./article/div/a/@href")
        if book_urls:
            #获取每本书本的url
            book_info_url=BOOKS_TOP_URL+book_urls[0]
            #4.得到书本url，通过访问进行获取书本信息，
            book_info=get_books_info(book_info_url)
            all_books.append(book_info)

    print(f"获取书本信息成功，共有{len(all_books)}本")

    #4.得到书本url，通过访问进行获取书本信息，保存数据，保存为CSV文件
    sava_books_info(all_books)

    print("保存数据成功")

if __name__ == '__main__':
    main()
