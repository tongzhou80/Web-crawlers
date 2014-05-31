#coding=utf-8
import sys
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import StringIO
from PIL import Image

#-------------------------------------------------------------------log in part
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36'}
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
#print logginPage
soup = BeautifulSoup(logginPage)
imgUrl=soup.find(attrs={'id':'captcha_image'})['src']
captcha_id=soup.find(attrs={'name':'captcha-id'})['value']
buffer=urllib2.urlopen(imgUrl).read()
im=Image.open(StringIO.StringIO(buffer))
im.show()
captcha_solution= raw_input("Captcha is:")
data={'source':'simple',
      'redir':'http://www.douban.com/people/77250418/contacts',
      "form_email":your email,
      'form_password':your password,
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
            sys.exit(0)

#-------------------------------------------------------------------mining part，threes steps
contact = file('contact.txt', 'w')
nickName = file('nickName.txt',mode='a')
databasePath = './database/'

userList = []
UserContactsUrl = 'http://www.douban.com/people/77250418/contacts'
UserReviewsUrl = 'http://www.douban.com/people/77250418/reviews'
UserHomeUrl = 'http://www.douban.com/people/77250418'
userCnt = 0
searchCnt = 0
maxUserNum = 10000
unicode_identityStart=4
requestTimes=0

with open('contacts list.txt', 'r') as readContacts:
    for eachLine in readContacts:
        userList.append(eachLine.strip('\n'))

for i in range(0, len(userList)):
    searchCnt += 1
    print 'till now,', searchCnt
    #-------------------------------------------------------------------get nickname
    currentUser = userList.pop(0)
    print 'current user:',currentUser
    UserHomeUrl = UserHomeUrl[0:29]
    UserHomeUrl += currentUser
    keepRequest = 1
    while keepRequest == 1:
        try:
            req = urllib2.Request(UserHomeUrl, headers=headers)
            HomePage = urllib2.urlopen(req, timeout=1).read()
        except:
            print 'request again'
        else:
            keepRequest = 0
    soup = BeautifulSoup(HomePage)
    h1 = soup.find('h1')
    if h1==None:
        continue
    if h1.find('span') == None:  #判断是否有甚么个性签名
        userName = h1.get_text(strip=True)
    else:
        h1.find('span').extract()  #名字夹在很多换行、空格中需要处理
        userName = h1.get_text(strip=True)
    print userName
    nickName.write(currentUser.encode('utf-8') + ' | ' + userName.encode("utf-8") + "\n")
    nickName.flush()
    #-------------------------------------------------------------------get contacts list
    # UserContactsUrl=UserContactsUrl[0:29]
    # UserContactsUrl+=currentUser+'/contacts'
    # keepRequest=1
    # contactsPage=''
    # while keepRequest==1:
    #     try:
    #         req=urllib2.Request(UserContactsUrl,headers=headers)
    #         contactsPage = urllib2.urlopen(req,timeout=1).read()
    #     except:
    #         print 'request again'
    #     else:
    #         keepRequest=0
    # #print contactsPage
    # soup = BeautifulSoup(contactsPage)
    # contactList=soup.findAll('dt')
    # contactId=''
    #
    # #print len(contactList)
    # for i in range(0,len(contactList)):
    #     currentContact=contactList[i]
    #     contactLink=currentContact.contents[0].contents[0]['src']
    #     contactLink=contactLink[29:len(contactLink)]
    #     #print contactLink
    #     for letter in contactLink:
    #         if letter=='-':
    #             break
    #         if letter>='0' and letter<='9':
    #             contactId+=letter
    #     #print  contactId
    #     if contactId=='':
    #         continue
    #     else:
    #         contact.write(currentUser+' '+contactId+'\n')
    #         if userCnt<maxUserNum:
    #             userList.append(contactId)
    #             userCnt+=1
    #         contactId=''
    # contact.flush()
    # print 'by now,',searchCnt,'users\'contacts have been scrapped'
    #-------------------------------------------------------------------get reviews list
    originalPath = databasePath
    UserReviewsUrl = UserReviewsUrl[0:29]
    UserReviewsUrl += currentUser + '/reviews'
    reviewsPage = ''
    keepRequest = 1
    while keepRequest == 1:
        try:
            req = urllib2.Request(UserReviewsUrl, headers=headers)
            reviewsPage = urllib2.urlopen(req, timeout=1).read()
        except:
            print 'request again'
        else:
            keepRequest = 0
    #print reviewsPage
    soup = BeautifulSoup(reviewsPage)
    reviewList = soup.findAll(attrs={'class': 'tlst clearfix'})
    itemTitle = ''
    commentTitle = ''
    commentLink = ''
    if reviewList != None:
        for i in range(0, len(reviewList)):
            itemTitle = reviewList[i].find(attrs={'class': 'ilst'}).find('a')['title']
            if len(itemTitle)==0:
                itemTitle = reviewList[i].find(attrs={'class': 'starb'}).find_all('a')[1].get_text()
            commentTitle = reviewList[i].contents[1].contents[0].contents[1].string
            commentLink = reviewList[i].contents[1].contents[0].contents[1]['href']
            #print itemTitle,currentUser,commentTitle,commentLink
            info = itemTitle + ' | ' + currentUser + ' | ' + commentTitle + ' | ' + commentLink + '\n'
            #print info,
            print itemTitle[0]
            if itemTitle[0]>'龟'.decode('utf-8') or itemTitle[0]<'一'.decode('utf-8'): #此处比较时仍是用unicode
                filePath='others'
            else:
                utfString = repr(itemTitle)[unicode_identityStart:]
                filePath = utfString[0:2]
            print filePath
            databasePath += filePath
            reviewInfo = file(databasePath, mode='a')
            reviewInfo.write(info.encode('utf-8'))
            reviewInfo.flush()
            reviewInfo.close()
            databasePath = originalPath

    nextPageList = soup.find(attrs={'class': 'paginator'})
    if nextPageList != None:
        nextPageList = nextPageList.findAll('a')
        nextPageList.pop()
        #print nextPageList
        for each in nextPageList:
            UserReviewsUrl=each['href']
            keepRequest = 1
            while keepRequest == 1:
                try:
                    req = urllib2.Request(UserReviewsUrl, headers=headers)
                    reviewsPage = urllib2.urlopen(req, timeout=1).read()
                except:
                    print 'request again'
                else:
                    keepRequest = 0
            #print reviewsPage
            soup = BeautifulSoup(reviewsPage)
            reviewList = soup.findAll(attrs={'class': 'tlst clearfix'})
            itemTitle = ''
            commentTitle = ''
            commentLink = ''
            for i in range(0, len(reviewList)):
                itemTitle = reviewList[i].find(attrs={'class': 'ilst'}).find('a')['title']
                if len(itemTitle)==0:
                    itemTitle = reviewList[i].find(attrs={'class': 'starb'}).find_all('a')[1].get_text()
                commentTitle = reviewList[i].contents[1].contents[0].contents[1].string
                commentLink = reviewList[i].contents[1].contents[0].contents[1]['href']
                #print itemTitle,currentUser,commentTitle,commentLink
                info = itemTitle + ' | ' + currentUser + ' | ' + commentTitle + ' | ' + commentLink + '\n'
                #print info,
                print itemTitle[0]
                if itemTitle[0]>'龟'.decode('utf-8') or itemTitle[0]<'一'.decode('utf-8'): #此处比较时仍是用unicode
                    filePath='others'
                else:
                    #print 'is chinese'
                    utfString = repr(itemTitle)[unicode_identityStart:]
                    filePath = utfString[0:2]
                print filePath
                databasePath += filePath
                reviewInfo = file(databasePath, mode='a')
                reviewInfo.write(info.encode('utf-8'))
                reviewInfo.flush()
                reviewInfo.close()
                databasePath = originalPath

contact.close()
nickName.close()
readContacts.close()
