#_*_coding:utf-8_*_
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'开始爬取内容... '

    def getsource(self,url):
        html = requests.get(url)
        return html.text

    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self,source):
        everyclass = re.findall('(<li id=".*?</li>)',source,re.S)
        return everyclass

    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('alt="(.*?)">',eachclass,re.S).group(1)
        info['content'] = re.search('display: none;">(.*?)</p>',eachclass,re.S).group(1).strip()
        timeandlevel = re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0].strip()
        info['classtime'] = re.sub('\n\t*','',info['classtime'])
        info['classlevel'] = timeandlevel[1].strip()
        info['learnnum'] = re.search('"learn-number">(.*?)</em>',eachclass,re.S).group(1)
        return info

    def saveinfo(self,classinfo):
        f = open('classinfo.txt','w')
        for each in classinfo:
            f.write('title: ' + each['title'] + '\n')
            f.write('content: ' + each['content'] + '\n')
            f.write('classtime: ' + each['classtime'] + '\n')
            f.write('classlevel: ' + each['classlevel'] + '\n')
            f.write('learnnum: ' + each['learnnum'] + '\n')
            f.writelines('===========================================================' + '\n')
        f.close()



if __name__ == "__main__":

    classinfo = []
    url = "http://www.jikexueyuan.com/course/?pageNum=1"
    jikespider = spider()
    all_links = jikespider.changepage(url,20)
    for link in all_links:
        print u'正在处理页面: ' + link
        html = jikespider.getsource(link)
        everyclass = jikespider.geteveryclass(html)
        for each in everyclass:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)
