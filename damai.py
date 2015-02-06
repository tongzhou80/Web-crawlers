#encoding:utf-8
#-----------------------------------------
#-----------------------------------------
import sys
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import StringIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from bidict import bidict
import json
import time

category={}
mcid={'演唱会':1,'音乐会':2,'话剧歌剧':3,'舞蹈芭蕾':4,'曲苑杂坛':5,'体育比赛':6,'度假休闲':7}

ccid={'流行':9,'摇滚':10,'民族':11,'音乐节':12,'其他演唱会':13,
      '管弦乐':14, '独奏':15,'室内乐及古乐':16, '声乐及合唱':17, '其他音乐会':18,
      '话剧 ':19,'歌剧 ':20,'歌舞剧 ':21,'音乐剧 ':22,'儿童剧 ':23,
      '舞蹈 ':24,'芭蕾 ':25,'舞剧 ':26,
      '相声 ':27,'魔术 ':28,'马戏 ':29,'杂技 ':30,'戏曲 ':31,'其他曲苑杂坛 ':32,
      '球类运动':33,'搏击运动':34,'其它竞技':35,
      '主题公园':36, '风景区':37, '展会':38, '特色体验':39, '温泉':40, '滑雪':41, '游览线路':42, '度假村':43, '代金券':44, '酒店住宿':45
      }
mcidDict=~bidict(mcid)
ccidDict=~bidict(ccid)

cj = cookielib.CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers = { 'User-Agent': ' Chrome/35.0.1916.114 Safari/537.36' }

def get_source(url):
    global cj,opener,headers
    keepRequest=1
    tryTimes=0
    page=''

    while keepRequest==1 :
        tryTimes+=1
        if tryTimes>5:
            break
        try:
            req=urllib2.Request(url,headers=headers)
            page=urllib2.urlopen(req,timeout=2).read()
            # page=urllib2.urlopen(url,timeout=1).read()
        except:
            print 'request again'
        else:
            keepRequest=0
    return page

def Spider():
    global mcidDict,ccidDict

    global cj,opener,headers
    outcomePathHead='C:/Users/Gentlyguitar/Desktop/MyWork/damai/outcome/'
    # get_source('http://www.damai.cn/projectlist.do?mcid=1&ccid=9')
    # print get_source('http://item.damai.cn/66780.html')
    ccidThresh={1:13,2:18,3:23,4:26,5:32,6:35,7:45}
    startMcid=3
    startCcid=21
    mcid=startMcid
    ccid=startCcid

    while mcid<=7:
        while ccid<=ccidThresh[mcid]: #
            print '当前数据存放地址：'
            path=outcomePathHead+mcidDict[mcid]+'/'+ccidDict[ccid]+'.txt'
            # path=outcomePathHead+'test.txt'
            print path
            uipath = unicode(path , "utf8")
            fileOut=open(uipath,'w')
            pageIndex=1
            while 1: # index of page keep changing until there is no perform list in the page
                try:
                    performListPage='http://www.damai.cn/projectlist.do?mcid='+str(mcid)+'&ccid='+str(ccid)+'&pageIndex='+str(pageIndex)
                    print '当前页面目录：',performListPage
                    listPage=get_source(performListPage)
                    soup=BeautifulSoup(listPage)
                    performList=soup.find(attrs={'id':'performList'})
                    titleList=performList.find_all('h2')
                    linkList=[]
                    for each in titleList:
                        a=each.find('a')
                        linkList.append(a['href'])

                    if len(titleList)== 0: # indicate the index of page has come to an end, ccid therefore needs to change
                        print 'this is an empty page'
                        break

                    for eachshow in linkList:
                        time=[]
                        price=[]
                        print eachshow
                        showpage=get_source(eachshow)
                        # showpage=get_source('http://item.damai.cn/70686.html')
                        soup=BeautifulSoup(showpage,"html.parser")

                        try:
                            title=soup.find(attrs={'class':'title'}).get_text().strip() # get the title
                        except:
                            title='待定'
                        try:
                            location=soup.find(attrs={'itemprop':'location'}).get_text().strip() # get the location
                        except:
                            location='待定'

    # try:
                        try:
                            timeList=soup.find(attrs={'id':'perform'}).find_all('a') # get the time, which is a list
                            for index,eachtime in enumerate(timeList):
                                time.append(eachtime.get_text().encode('utf-8'))
                            pidList=[]
                            for index,eachtime in enumerate(timeList): # get the price for each time
                                pid=eachtime['pid']
                                # print eachtime['class'],type(eachtime['class'])
                                if eachtime['class']==[u'grey']:
                                    price.append('暂无')
                                    continue
                                if index>0:
                                    data={'type':'33',
                                          'performID':pid,
                                          'business':'1',
                                          'IsBuyFlow':'False',
                                          'sitestaus':'3'}
                                    post_data=urllib.urlencode(data)
                                    url='http://item.damai.cn/ajax.aspx'
                                    keepRequest=1
                                    tryTimes=0
                                    while keepRequest==1: # a time limit is needed
                                        tryTimes+=1
                                        if tryTimes>5:
                                            break
                                        try:
                                            req=urllib2.Request(url,post_data,headers)
                                            newpage=urllib2.urlopen(req).read()
                                        except:
                                            print 'click problem'
                                        else:
                                            keepRequest=0
                                    soup=BeautifulSoup(newpage,"html.parser")
                                    priceLinkList=soup.find_all('a',attrs={'class':True,'price':True})

                                else:
                                    priceLinkList=soup.find(attrs={'id':'price'}).find_all('a')
                                priceList=[]
                                for eachlink in priceLinkList:
                                    norlizedPrice=eachlink.get_text()
                                    norlizedPrice=norlizedPrice.replace(u'暂时无货，登记试试运气~',u' ( 无货 )').replace(u'点击进行预定登记',u' ( 可预定 )')
                                    priceList.append(norlizedPrice.encode('utf-8'))
                                price.append(priceList)

                        except:
                            time.append('待定')
                            price.append('待定')

                        mcidName=mcidDict[mcid]
                        ccidName=ccidDict[ccid]
                        titleName=title.encode('utf-8')
                        placeName=location.encode('utf-8')
                        data=[{"mcid": mcidName},
                              {"ccid": ccidName},
                              {"title": titleName},
                              {"place": placeName},
                              {"time": time},
                              {"price": price}]

                        normalizedData= json.dumps(data,ensure_ascii=False,sort_keys=True,indent=1)
                        normalizedData=normalizedData.replace('[\n {\n','{\n').replace('\n }\n]','\n}').replace('\n }, \n {\n',' ,\n')
                        #print normalizedData
                        fileOut.write(normalizedData+'\n\n\n')
                        fileOut.flush()

                        del time[:]
                        del price[:]
                except:
                    print 'something wrong'
                pageIndex+=1
            ccid+=1
        mcid+=1






if __name__ == "__main__":
    Spider()
