# -*- coding: utf-8 -*-

# Define here the models for your scraped selfs
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/selfs.html
import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.utils.common import get_md5, convert_int


def content_join(contents):
    return "\n".join(contents)


def str_data(pubtime):
    if '/' in pubtime:
        pubtime = re.match('.*?(\d+.*\d).*', pubtime, re.DOTALL).group(1)
        pubtime = datetime.datetime.strptime(pubtime, '%Y/%m/%d').date()
    else:
        pubtime = datetime.datetime.now().date()
    return pubtime


class ArticleItemLoder(ItemLoader):
    default_output_processor = TakeFirst()


def return_value(args):
    return args


class ArticlespiderItem(scrapy.Item):
    # define the fields for your self here like:
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        input_processor=MapCompose(get_md5),
    )
    title = scrapy.Field()
    pubtime = scrapy.Field(
        input_processor=MapCompose(str_data),
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    praise_num = scrapy.Field(
        input_processor=MapCompose(convert_int),
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(convert_int),
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(convert_int),
    )
    content = scrapy.Field(
        input_processor=MapCompose(content_join),
    )
    image_urls = scrapy.Field(
        out_processor=MapCompose(return_value),
    )
    image_file_path = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO `article_spider`.`jobbole_article`(`pubtime`, `title`, `url`, `url_object_id`, `image_urls`,
            `image_file_path`, `praise_num`, `fav_num`, `comment_num`, `content`, `tags`)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `praise_num`=VALUES (`praise_num`)
        """
        image_urls = ""
        # content = remove_tags(self["content"])

        if self["image_urls"]:
            image_urls = self["image_urls"][0]
        params = (self['pubtime'], self['title'], self['url'], self['url_object_id'], image_urls,
                                  self['image_file_path'], self['praise_num'], self['fav_num'], self['comment_num'],
                                  self['content'], self['tags'])
        return insert_sql, params

