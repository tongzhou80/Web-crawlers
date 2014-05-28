#coding=utf-8
#tips:
#target site:http://www.zhihu.com/
#result:get the homepage printed

import urllib2
import urllib
import cookielib

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36'}
url = 'http://www.zhihu.com/login'
data={"email":"332012407@qq.com",
      'password':'zt52287800616'}
post_data=urllib.urlencode(data)
req=urllib2.Request(url,post_data,headers)
HomePage = urllib2.urlopen(req).read()
print HomePage

