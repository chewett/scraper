#!/usr/bin/env python

import urllib.request
import urllib.parse
import urllib.error
import json
import sys
import subprocess

class Scraper:

    USER_AGENT = "Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.29.5"

    def __init__(self, cookie=None):
        #create the build opener
        self.opener = urllib.request.build_opener()
        self.headers = {"User-Agent" : Scraper.USER_AGENT, "Accept" : "*/*"}

        self.wget_vars = "-c -e robots=off --user-agent '" + self.headers['User-Agent'] + "'"

        self.opener.addheaders.append(('User-Agent', self.headers['User-Agent']))
        self.opener.addheaders.append(("Accept", self.headers['Accept']))
        self.cookie = cookie
        if cookie is not None:
            self.opener.addheaders.append(('Cookie', cookie))

    def get(self, url):
        request = urllib.request.Request(url, None, self.headers)
        return self.opener.open(request)

    def post(self, url, data):
        encoded_data = urllib.parse.urlencode(data)
        request = urllib.request.Request(url, str.encode(encoded_data), self.headers)
        return self.opener.open(request)

    def head(self, url):
        request = urllib.request.Request(url, None, self.headers)
        request.get_method = lambda: 'HEAD'
        return self.opener.open(request)

    def url_exists(self, url):
        try:
            response = self.head(url)
            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise


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

        print("\rFinished, Filesize: " + self._nice_size(sizeDownloaded) + " Filename: " + filename)

    def get_wget_command(self, url, saveLocation):
        safe_url = url.replace("\"", "\\\"").replace('`', r'\`')
        command = "wget -O '" + saveLocation + "' \"" + safe_url + "\" " + self.wget_vars
        return command

    def download_file_via_wget(self, url, saveLocation):
        command  = self.get_wget_command(url, saveLocation)
        res = subprocess.call(command, shell=True)
        return res

if __name__ == "__main__":
    s = Scraper()

    print(s._nice_size(234232475))
