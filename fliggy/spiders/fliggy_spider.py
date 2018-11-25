import scrapy
import datetime
import re
from ..items import FliggyItem

#附加登录信息
#测试


class FliggySpider(scrapy.Spider):
    name = 'fliggy'

    #限定爬取范围
    allow_domains = ["fliggy.com"]
    
    #输入爬取开始日期，格式YYYY-MM-DD
    start_date = datetime.datetime.strptime(input("please input scrapy start date"),'%Y-%m-%d')
    #输入爬取天数，格式正整数
    check_days = int(input("please input how many days you want scrapy?"))
    
    
    #得出一个所有日期的初始网址列表
    default_url0 = "https://sijipiao.fliggy.com/ie/flight_search_result.htm?searchBy=1281&b2g=0&formNo=-1&agentId=-1&needMemberPrice=true&searchJourney="
    default_url1 = "&childPassengerNum=0&infantPassengerNum=0&tripType=0&cardId="
    start_url = []
    for i in range(0,check_days):
        date = start_date + datetime.timedelta(days=i)
        search_info =[{"depCityCode":"CGO","arrCityCode":"MEL","depDate":date.strftime('%Y-%m-%d')}]
        start_url.append(default_url0 + str(search_info) + default_url1)


    def parse(self,response):
        #抓取内容存储列表
        items = []
        #调用爬虫的类，将爬到的内容存在字典中
        item = FliggyItem()
        
        print(response.url)




        item['info'] = response.xpath('/html/body/div[4]/div[5]/div[2]/h3/span[1]/text()').extract()
        
        
        if response.body.findall(r'捷星',response.body):
        #如果爬取结果中有捷星的话，继续找捷星的价格，如果没有的话设价格为空

            for i in range(1,10):
            #搜索前十个结果，捷星在第几项结果中就抓取这一项的价格
                if '捷星' in response.xpath(f'/html/body/div[4]/div[5]/div[5]/div[2]/div/div[1]/div[i]/div/div[1]/table/tbody/tr/td[1]/div/div/p[1]/span/text()').extract():
                    item['lowest_price'] =response.xpath(f'/html/body/div[4]/div[5]/div[5]/div[2]/div/div[1]/div[i]/div/div[1]/table/tbody/tr/td[7]/div/div[1]/span/text()').extract()
                    break
        else:
            item['lowest_price'] = []