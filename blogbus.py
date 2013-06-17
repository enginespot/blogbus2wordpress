#coding=utf-8

import re, urllib2
#import string
#import socks
#import socket
import lxml.html

def blogbus2wordpress(blogname):
    blogurl = getBlogUrl(blogname)
    if(blogurl==''):
        return ''
    maxpage = getMaxPage(blogurl)

    if(maxpage==''):
        return ''
    #socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
    #socket.socket = socks.socksocket

    wpxml = r'<?xml version="1.0" encoding="UTF-8" ?>'
    wpxml += '<rss version="2.0" '
    wpxml += ' xmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"'
    wpxml += ' xmlns:content="http://purl.org/rss/1.0/modules/content/"'
    wpxml += ' xmlns:wfw="http://wellformedweb.org/CommentAPI/"'
    wpxml += ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
    wpxml += ' xmlns:wp="http://wordpress.org/export/1.1/"'
    wpxml += ' >'
    wpxml += ' <channel>'
    wpxml += ' <wp:wxr_version>1.1</wp:wxr_version>'
    for i in range(1, maxpage + 1):
        data = urllib2.urlopen(blogurl+'/index_' + str(i) + '.html').read();
        dom = lxml.html.fromstring(data);
        #    posts=dom.xpath("//ul[@id=\"posts\"]/li")
        posts = dom.xpath("//ul[@id=\"posts\"]//li[div[@class='postHeader']]")
        #    postdata = re.findall("<ul id=\"posts\">(.*?)</ul>", data, re.S)[0]
        #    posts = re.findall("<li>\n<div class=\"postHeader\">(.*?)</li", postdata, re.S);
        for node in posts:
            post = lxml.html.tostring(node)
            #    for post in posts:
            wpxml += '<item>'
            posttime = re.findall("<h3>(.*?)</h3>", post, re.S)[0]
            posttitle = re.findall("<h2><a href(.*?)>(.*?)</a>(.*?)</h2>", post, re.S)[0][1]
            if len(re.findall("<div class=\"postBody\">(.*?)<div class=\"clear\">", post, re.S))==0:
                postbody = re.findall("<div class=\"postBody\">(.*?)</div>", post, re.S)[0]
            else:
                postbody = re.findall("<div class=\"postBody\">(.*?)<div class=\"clear\">", post, re.S)[0]
            wpxml += '<wp:status>'
            wpxml += 'publish'
            wpxml += '</wp:status>'
            wpxml += '<wp:post_type>'
            wpxml += 'post'
            wpxml += '</wp:post_type>'
            wpxml += '<title>'
            wpxml += posttitle
            wpxml += '</title>'
            wpxml += '<wp:post_date>'
            wpxml += posttime
            wpxml += '</wp:post_date>'
            wpxml += '<dc:creator>xrm</dc:creator>'
            wpxml += '<content:encoded><![CDATA['
            wpxml += postbody
            wpxml += ']]></content:encoded>'
            wpxml += '</item>'
    wpxml += '</channel>'
    wpxml += '</rss>'
    f = file('blogbus.xml', 'w')
    f.write(wpxml)
    return wpxml


def getMaxPage(blogurl):
    try:
        data = urllib2.urlopen(blogurl).read()
    except :
        return ''
    dom = lxml.html.fromstring(data);
#    查找class名为pageNavi的div，其最后一个a元素的href
#    href=dom.xpath("//div[@class=\"pageNavi\"]/a[position() = last()]/@href")
    href=dom.xpath("//div[@class=\"pageNavi\"]")
    if(len(href)==0):
        return ''

    lasthref=href[0]
    maxPage=int(re.search(r'\d+', lasthref.text).group())
    return maxPage

def getBlogUrl(blogName):
    blogName=blogName.strip()
    if blogName=='':
        return ''
    return '%s%s%s' % ('http://', blogName, ".blogbus.com")


#blogbus2wordpress('lollipop320')

