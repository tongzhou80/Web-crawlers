four crawlers, targeted at four different sites. 
- [douban](www.douban.com) 
- [zhihu](www.zhihu.com)
- [weibo](www.weibo.com)
- [songtaste](www.songtaste.com)


####Difficulties

- douban
    - captcha 
    - block ip
- zhihu
    - dynamic page
- weibo
    - post data has random id
- songtaste


####Solutions

- douban
    - catch the captcha and enter the characters manually 
    - set a interval for each request, or use a proxy
- zhihu
    - use selenium2 and phantomjs instead of urllib2
- weibo
    - catch the random id
- songtaste
    - the simplest one



