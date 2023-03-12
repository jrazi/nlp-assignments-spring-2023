import scrapy
from scrapy.crawler import CrawlerRunner
import re
from crochet import setup, wait_for

setup()

MAJOR_POETS = {
    'khayyam': {
        'ganjoor_name': 'khayyam',
    },
    'hafez': {
        'ganjoor_name': 'hafez',
    },
    'moulavi': {
        'ganjoor_name': 'moulavi',
    },
    'ferdousi': {
        'ganjoor_name': 'ferdousi',
    },
    'nezami': {
        'ganjoor_name': 'nezami',
    },
    'saadi': {
        'ganjoor_name': 'saadi'
    }
}
class GanjoorSpider(scrapy.Spider):
    name = "GanjoorSpider"
    start_urls = [
        'https://ganjoor.net/khayyam/robaee/sh41',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            # '__main__.ExtractFirstLine': 1
        },
        'FEEDS': {
            'ganjoor.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        for comment in response.css('#comments-block > .ganjoor-comment > blockquote > p::text'):
            yield {
                'poet': '',
                'poem_type': '',
                'poem_no': '',
                'author': '',
                'comment': comment.get()
            }


class ExtractFirstLine(object):
    def process_item(self, item, spider):
        return {'comment': dict(item)["comment"]}

    def __remove_html_tags__(self, text):
        html_tags = re.compile('<.*?>')
        return re.sub(html_tags, '', text)


@wait_for(10000)
def run_spider():
    crawler = CrawlerRunner()
    d = crawler.crawl(GanjoorSpider)
    return d


run_spider()
