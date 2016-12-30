These five crawlers were written during my undergraduate study due to various ends. They targeted at the following five different sites.

- [douban](http://www.douban.com)
    - To login to douban, you'll need to work around the captcha verification. The simplest solution, which is used in the code, is to suspend the program and download the captcha to local file system. Once the user views the captcha and enters the code, the crawler program continues. Alternatively, you could develop an automatic character recognizing system. It depends on whether you want the data or the functionality of the web crawler system. Note that if you send request too often, douban's server will ban your ip address. You can slow down your script to get around this.
- [zhihu](http://www.zhihu.com)
    - Zhihu dynamically loads new contents as you scroll down. Your web crawler needs to be able to simulate that by sending the same request to the server. You'll need to monitor the network to capture the request being sent when loading new contents.
- [weibo](http://www.weibo.com)
    - There are multiple ports where you can login to weibo, I already forget which login page I was using, but its form contains a random id, possibly preventing cross-site request forgery. You'll need to pass that id with the posted data as well.
- [songtaste](http://www.songtaste.com)
    - Songtaste is a plain website without any data protection strategy, as least at the time when the script was written. Getting its data is straightforward.
    - Update, songtaste is now permanently down :(
- [damai](http://www.damai.cn/)
    - Damai is a ticket booking site. Tickect availability and price may vary according the condition you want to satisfy. To this end, ajax is used extensively. To simulate ajax, you'll need to monitor the network to capture the ajax request.

The code could be outdated and might not run on your machine, but the idea behind the code applies to all sorts of problems in web crawling.
