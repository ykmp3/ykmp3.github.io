#--coding:utf-8--
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

import time ,urllib2 ,re ,json ,os , urlparse

# Create your views here.

def index(request):
    return render(request, 'index.html', context={})
def news(request):
    return render(request, 'news.html', context={})
def contact(request):
    return render(request, 'news.html', context={})
def termsofuse(request):
    return render(request, 'termsofuse.html', context={})
def convert(request):
    if request.method == 'POST':
        url =  request.POST['video']
        print(url)
        parsedurl = urlparse.urlparse(url)
        if('youku' not in parsedurl.netloc or parsedurl.scheme == ''):
            return render(request, 'index.html', context={"error": u"链接地址有误：%s" % url.encode('utf-8')})
        vid = get_vid(url)
        m3u8_url, title = get_m3u8(url, vid)
        print(m3u8_url)
        print(title)

        mp3file = down_m3u8(m3u8_url, vid)
        if(mp3file):
            with open(mp3file) as f:
                data = f.read()
            response = HttpResponse(data, content_type = 'APPLICATION/OCTET-STREAM')
            response['Content-Disposition'] = 'attachment;filename=%s.mp3' % title.replace(' ', '').encode('utf-8')
            response['Content-Length'] = os.path.getsize(mp3file)
            return response
        else:
            return render(request, 'index.html', context={"error":"Sorry, Internal error!"})
    pass
def get_vid(url):
    result = re.findall(r"id_(.*?==)", url)
    if (len(result) >0):
        return result[0]
    else:
        result = re.findall(r"id_(.*?)\.html", url)
        if len(result) >0:
            return result[0]+ "=="
        else:
            return False
def get_m3u8(url, vid):
    #utid_url = 'http://gm.mmstat.com/yt/ykcomment.play.commentInit'
    #request = urllib2.Request(utid_url)
    #
    #request.add_header("Accept", "text/html,*/*") 
    opener = urllib2.build_opener() 
    #response = opener.open(request)
    #cookie_str = response.headers.dict['set-cookie']
    #utid = cookie_str[4:28]
    #if(utid != 'rjVrETO4v0oCAXVJkKWLTkoS'):
    #    print("utid=%s" % utid)
    utid = 'rjVrETO4v0oCAXVJkKWLTkoS'

    client_ts = int(time.time())

    ups_url = 'https://ups.youku.com/ups/get.json?vid=%s&ccode=0401&client_ip=192.168.1.1&utid=%s&client_ts=%d' % (vid, utid, client_ts)
    print(ups_url)
    ups_req = urllib2.Request(ups_url)
    ups_req.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0")
    ups_req.add_header("Accept", "text/html,*/*")
    ups_req.add_header("Referer", "http://www.youku.com")
    response = opener.open(ups_req)
    json_str = response.read()
    print(json_str)
    json_content = json.loads(json_str)
    
    m3u8_url = json_content['data']['stream'][0]['m3u8_url']
    title = json_content['data']['video']['title']


    return m3u8_url, title
def down_m3u8(url, vid):
    mp3file = os.getcwd() + "/tomp3/static/mp3/%s.mp3" % vid
    if(os.path.exists(mp3file)):
        return mp3file
    ups_req = urllib2.Request(url)
    ups_req.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0")
    ups_req.add_header("Accept", "text/html,*/*")
    ups_req.add_header("Referer", "http://www.youku.com")
    opener = urllib2.build_opener() 
    response = opener.open(ups_req)
    m3u8 = response.read()
    m3u8file = os.getcwd() + "/tomp3/static/m3u8/%s.m3u8" % vid
    with open(m3u8file, "w") as f:
        f.write(m3u8)
    err = os.system("ffmpeg -v 8 -i %s %s" % ( m3u8file, mp3file))
    if(err == 0):
        return mp3file
    else:
        return False
