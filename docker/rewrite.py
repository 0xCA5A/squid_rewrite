#!/usr/bin/env python3
"""Demo code. No warranty of any kind. Use at your own risk!
"""

VERSION = 0.1

import logging
import os
import subprocess
import sys

logging.basicConfig(filename='/var/log/squid/rewrite.log', level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')

LOG = logging.getLogger(__name__)


class RequestData:
    def __init__(self):
        self._ch_id = None
        self._url = None
        self._ipaddr = None
        self._method = None
        self._user = None

    @property
    def ch_id(self):
        return self._ch_id

    @property
    def url(self):
        return self._url

    @property
    def ipaddr(self):
        return self._ipaddr

    @property
    def method(self):
        return self._method

    @property
    def user(self):
        return self._user

    @staticmethod
    def of(request):
        return RequestData()._parse(request)

    def _parse(self, request):
        """Parse request data
        :param request: Request format is based on url_rewrite_extras "%>a %>rm %un"
        """
        [self._ch_id, self._url, self._ipaddr, self._method, self._user] = request.strip().split()
        return self


class ImageManipulator:
    @staticmethod
    def flip(file_path):
        command = "/usr/bin/mogrify -flip {}".format(file_path)
        subprocess.check_call(command.split())

    @staticmethod
    def monochrome(file_path):
        command = "/usr/bin/mogrify -monochrome {}".format(file_path)
        subprocess.check_call(command.split())

    @staticmethod
    def grayscale(file_path):
        command = "/usr/bin/mogrify -type Grayscale {}".format(file_path)
        subprocess.check_call(command.split())


class ImageGetModifier:
    IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']
    METHOD_GET = "GET"
    WEB_SERVER_ROOT = "http://127.0.0.1:8000/"

    def __init__(self, pid, rewrite_dir):
        self._pid = pid
        self._rewrite_dir = rewrite_dir
        self._call_cnt = 0

    def handle(self, request_data):
        self._call_cnt += 1
        if request_data.method != self.METHOD_GET:
            return False

        assumed_image_extension = request_data.url.split('.')[-1].lower()
        if assumed_image_extension in [x.lower() for x in self.IMAGE_EXTENSIONS]:
            cached_file = self._modify_image(request_data, assumed_image_extension)
            return self._build_url(cached_file)

    def _build_url(self, cached_image_file):
        image = cached_image_file.split('/')[-1]
        cache_url = "{}{}".format(self.WEB_SERVER_ROOT, image)
        return cache_url

    def _store_original_image(self, original_image_url, image_extension):
        cached_file = "{}/{}-{}.{}".format(self._rewrite_dir, self._pid, self._call_cnt, image_extension)
        cached_file = cached_file.replace("//", "/")
        command = "/usr/bin/wget -q -O {} {}".format(cached_file, original_image_url)
        subprocess.check_call(command.split())
        return cached_file

    def _modify_image(self, request_data, image_extension):
        cached_file = self._store_original_image(request_data.url, image_extension)
        ImageManipulator.flip(cached_file)
        return cached_file


class Rewriter:
    def __init__(self, pid, rewrite_dir):
        self._image_get_modifier = ImageGetModifier(pid, rewrite_dir)

    def _handle_request(self, request):
        request_data = RequestData.of(request)

        new_image_url = self._image_get_modifier.handle(request_data)
        if new_image_url:
            response = request_data.ch_id + ' OK ' + 'rewrite-url=' + new_image_url
        else:
            response = request_data.ch_id + ' ERR'

        return response

    def run(self):
        """Keep looping and processing requests
        """

        while True:
            request = sys.stdin.readline().strip()
            LOG.info("Processing rewrite request '%s'", request)

            response = self._handle_request(request)
            response += '\n'

            LOG.info("Writing response '%s'", response.strip())

            sys.stdout.write(response)
            sys.stdout.flush()


if __name__ == '__main__':
    Rewriter(os.getpid(), os.getenv('SQUID_REWRITE_DIR', '/tmp')).run()
