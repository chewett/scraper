#!/usr/bin/env python
import urllib2
import json
import sys

class Scraper:

    def __init__(self, cookie=None):
        #create the build opener
        self.opener = urllib2.build_opener()
        self.headers = {"User-Agent" : "Opera/9.80 (X11; Linux i686)     Presto/2.12.388 Version/12.14", "Accept" : "text/html, application/xml;q=0.9    , application/xhtml xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=    0.1"}

        self.opener.addheaders.append(('User-Agent', 'Opera/9.80 (X11; Linux i686) Presto/2.12.388 Version/12.14'))
        self.opener.addheaders.append(("Accept", "text/html, application/xml;q=0.9, application/xhtml xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1"))
        if cookie is not None:
            self.opener.addheaders.append(('Cookie', cookie))

    def get(self, url):
        request = urllib2.Request(url, None, self.headers)
        return self.opener.open(request)

    def post(self, url, data):
        request = urllib2.Request(url, data, self.headers)
        return self.opener.open(request)

    def _nice_size(self, size):
        for sizeUnit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%0.2f %s"%(size, sizeUnit)
            size = size / 1024.0
       
        #dont have enough units, multiply by 1024 to get back to right size
        size *= 1024.0
        return "%0.2f %s"%(size, sizeUnit)

    def get_json(self, url):
        jsonData = self.get(url).read()
        return json.loads(jsonData)

    def download_file(self, url, saveLocation):
        r = self.get(url)
        headers = r.info()

        f = open(saveLocation, 'wb')

        filesize = int(headers.getheaders("Content-Length")[0])
        filename = url.rsplit('/',1)[1]

        sizeDownloaded = 0
        blockSize = 8192

        while True:
            buffer = r.read(blockSize)
            if not buffer:
                break

            sizeDownloaded += len(buffer)
            f.write(buffer)

            sys.stdout.write("\rDown: "+self._nice_size(sizeDownloaded)+" of "+self._nice_size(filesize)+" "+ str(((float(sizeDownloaded) / filesize) * 100)) + "%")
            sys.stdout.flush()

        print "\rFinished, Filesize: " + self._nice_size(sizeDownloaded) + " Filename: " + filename

if __name__ == "__main__":
    print s._nice_size(234232475)
