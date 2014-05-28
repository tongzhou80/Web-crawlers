#coding=utf-8
#tip:
#1.target site:http://www.douban.com,when sign in you need to input a Captcha
#2.parse:BeautifulSoup,which is awesome
#3.result:stored in "data.txt"

import urllib2
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup
import StringIO
from PIL import Image

#-------------------------------------------------------------------log in part
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers ={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36'}
url = 'https://www.douban.com/accounts/login'
logginPage=''
keepRequest=1
while keepRequest==1:
    try:
        req=urllib2.Request(url,headers=headers)
        logginPage=urllib2.urlopen(req,timeout=1).read()
    except:
        print 'request again'
    else:
        keepRequest=0
print logginPage
soup = BeautifulSoup(logginPage)
imgUrl=soup.find(attrs={'id':'captcha_image'})['src']
captcha_id=soup.find(attrs={'name':'captcha-id'})['value']
buffer=urllib2.urlopen(imgUrl).read()
im=Image.open(StringIO.StringIO(buffer))
im.show()
captcha_solution= raw_input("Captcha is:")
data={'source':'simple',
      'redir':'http://www.douban.com/people/77250418/contacts',
      "form_email":"zt9465@163.com",
      'form_password':'4512686',
      'captcha-solution':captcha_solution,
      'captcha-id':captcha_id,
      'user_login':'登录'
      }
post_data=urllib.urlencode(data)
keepRequest=1
while keepRequest==1:
    try:
        req=urllib2.Request(url,post_data,headers)
        confirmUrl=urllib2.urlopen(req,timeout=1).geturl()
    except:
        print 'request again'
    else:
        keepRequest=0
        if confirmUrl=='http://www.douban.com/people/77250418/contacts':
            print 'sign in success'
        else:
            print 'shit! Please run again'

#-------------------------------------------------------------------mining part
show=file('data.txt','w')
userList = ['77250418']
currentUrl='http://www.douban.com/people/77250418/contacts'
userCnt=0
searchCnt=0
maxUserNum=3000

while searchCnt<maxUserNum:
    currentUrl=currentUrl[0:29]
    #print currentUrl
    currentUser=userList.pop(0)
    currentUrl+=currentUser+'/contacts'
    keepRequest=1
    UserPage=''
    while keepRequest==1:
        try:
            req=urllib2.Request(currentUrl,headers=headers)
            UserPage = urllib2.urlopen(req,timeout=1).read()
        except:
            print 'request again'
        else:
            keepRequest=0
    print UserPage
    soup = BeautifulSoup(UserPage)
    contactList=soup.findAll('dt')
    contactId=''

    print len(contactList)
    for i in range(0,len(contactList)):
        currentContact=contactList[i]
        contactLink=currentContact.contents[0].contents[0]['src']
        contactLink=contactLink[29:len(contactLink)]
        print contactLink
        for letter in contactLink:
            if letter=='-':
                break
            if letter>='0' and letter<='9':
                contactId+=letter
        print  contactId
        if contactId=='':
            continue
        else:
            show.write(currentUser+' '+contactId+'\n')
            if userCnt<maxUserNum:
                userList.append(contactId)
                userCnt+=1
            contactId=''
    show.flush()
    searchCnt+=1
