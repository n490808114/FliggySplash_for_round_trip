import scrapy
import datetime
import re
from ..items import FliggyItem
from scrapy_splash import SplashRequest


# splash lua script
#script = """
#         function main(splash, args)
#             assert(splash:go(args.url))
#             assert(splash:wait(args.wait))
#             js = string.format("document.querySelector('#kw').value=%s;document.querySelector('#su').click()", args.phone)
#             splash:evaljs(js)
#             assert(splash:wait(args.wait))
#             return splash:html()
#         end
#         """

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
    start_urls = []
    for i in range(0,check_days):
        date = start_date + datetime.timedelta(days=i)
        search_info =[{"depCityCode":"CGO","arrCityCode":"MEL","depDate":date.strftime('%Y-%m-%d')}]
        start_urls.append(default_url0 + str(search_info) + default_url1)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                args={ 'wait': 0.5, }
                )
            
    def parse(self,response):
        #抓取内容存储列表
        items = []
        #调用爬虫的类，将爬到的内容存在字典中
        item = FliggyItem()
        
        print(response.url)
        
        item['triptype'] = response.xpath('//*[@id="J_IeSearch"]/div[1]/p/text()').extract()
        item['dep_city'] = response.xpath('//*[@id="J_IeSearch"]/div[1]/div[2]/label[1]/input[1]/@value').extract()
        item['arr_city'] = response.xpath('//*[@id="J_IeSearch"]/div[1]/div[2]/label[2]/input[1]/@value').extract()
        #item['first_dep_date'] = response.xpath('//*[@id="J_IeSearch"]/div[1]/div[3]/label[1]/div/input/@value').extract()
        dep_date = re.findall(r'depDate.*?([0-9]{4}-[0-9]{2}-[0-9]{2})',response.url)
        print(dep_date)
        if len(dep_date) == 1:
            dep_date.append('无')
        item['first_dep_date'],item['second_dep_date']=dep_date
        #item['second_dep_date'] =response.xpath('//*[@id="J_IeSearch"]/div[1]/div[3]/label[2]/div/input/@value').extract()
        
        print(response.xpath('//*[@id="J_Flights"]/div[2]/div//text()').extract())
        print(str(response.xpath('//*[@id="J_Flights"]/div[2]/div/text()').extract()))
        print(re.findall('\u6377\u661f',str(response.xpath('//*[@id="J_Flights"]/div[2]/div/text()').extract())))
        
        #'\u6377\u661f'是‘捷星’的unicode编码
        #if re.findall('\u6377\u661f',str(response.xpath('//*[@id="J_Flights"]/div[2]/div/text()').extract())):
        #如果爬取结果中有捷星的话，继续找捷星的价格，如果没有的话设价格为空
        for i in range(1,10):
            print(f'//*[@id="J_DepResultContainer"]/div[{i}]//table/tbody/tr/td[1]/div/div/p[1]/span')
            print(response.xpath(fr'//*[@id="J_DepResultContainer"]/div[{i}]//table/tbody/tr/td[1]/div/div/p[1]/span/text()').extract())
            #搜索前十个结果，捷星在第几项结果中就抓取这一项的价格
            if '\u6377\u661f' in response.xpath(f'//*[@id="J_DepResultContainer"]/div[{i}]//table/tbody/tr/td[1]/div/div/p[1]/span/text()').extract():
                item['lowest_price'] =response.xpath(f'//*[@id="J_DepResultContainer"]/div[{i}]//table/tbody/tr/td[1]/div/div/p[1]/span/text()').extract()
                break
            else:
                item['lowest_price'] = []
        items.append(item)
        return items
        
