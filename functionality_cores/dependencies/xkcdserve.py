import re
import urllib.request
from html.parser import HTMLParser
from typing import Tuple, Union


class ImageFinder(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_image = False
        self.__url = None
        self.__alt = None

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs:
            (_, div_id), *_ = attrs
            if div_id == 'comic':
                self.is_image = True

    def handle_startendtag(self, tag, attrs):
        if self.is_image:
            if tag == 'img':
                (_, url), (_, alt), *_ = attrs
                self.__url = url[2:] # Remove the leading '//'
                self.__alt = alt
                self.is_image = False
    
    @property
    def result(self) -> Union[Tuple[str, str], Tuple[None, None]]:
        out = self.__url, self.__alt
        self.__url = None
        self.__alt = None
        return out

def fetch_comic(number: int) -> Tuple[Union[str, None], str]:
    try:
        handler = ImageFinder()
        with urllib.request.urlopen("https://xkcd.com/{}".format(number)) as xkcd:
            handler.feed(xkcd.read().decode('utf-8'))
        return handler.result
    except urllib.error.HTTPError as e:
        return (None, str(e))


class LatestNumber(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.latest = 0

    def handle_data(self, data):
        match = re.match(r"\sPermanent link to this comic: https://xkcd.com/([0-9]+)/", data)
        if match:
            self.latest = int(match.group(1))

def latest_comic_number() -> int:
    handler = LatestNumber()
    with urllib.request.urlopen("https://xkcd.com") as xkcd:
        handler.feed(xkcd.read().decode('utf-8'))
        return handler.latest