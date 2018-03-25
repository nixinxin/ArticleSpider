# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from urllib.parse import urljoin
from ArticleSpider.items import ArticlespiderItem, ArticleItemLoder
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        获取文章列表页中的文章URL并交给scrapy下载并解析
        :param response:
        :return:
        """
        post_urls = response.css('#archive .post.floated-thumb .post-thumb')
        for post_url in post_urls:
            url = post_url.css("a::attr(href)").extract_first()
            image_urls = post_url.css('a img::attr(src)').extract()
            url = urljoin(response.url, url)
            yield scrapy.Request(url=url, callback=self.detail, meta={"image_urls": image_urls})

        # next_url = response.xpath('//*[@class="next page-numbers"]/@href').extract_first(0)
        # if next_url:
        #     next_url = urljoin(response.url, next_url)
        #     print(response.url)
        #     yield scrapy.Request(url=next_url, callback=self.parse)

    def detail(self, response):
        # item = ArticlespiderItem()
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        # pubtime = response.xpath('//*[@id="post-113778"]/div[2]/p/text()').extract_first().strip().split(" ")[0]
        # tag_list = response.xpath('//*[@id="post-113778"]/div[2]/p/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = "·".join(tag_list)
        # print("xpath选择器", title, pubtime, tags)
        #
        # title = response.css('div.entry-header h1::text').extract_first()
        # pubtime = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip().split(" ")[0]
        # try:
        #     pubtime = datetime.datetime.strptime(pubtime, '%Y/%m/%d').date()
        # except:
        #     pubtime = datetime.datetime.now().date()
        # tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = "·".join(tag_list)
        # # print("css  选择器", title, pubtime, tags)
        #
        # all_num = response.css('.post-adds')
        # praise_num = all_num.css('#113778votetotal::text').extract_first(0)
        # fav_num = all_num.css('.bookmark-btn::text').extract_first("0")
        # match_re = re.match('.*?(\d+).*', fav_num)
        # if match_re:
        #     fav_num = int(match_re.group(1))
        # else:
        #     fav_num = 0
        # comment_num = all_num.css('.fa.fa-comments-o::text').extract_first(0)
        # content = response.css('.entry p::text').extract()
        # contents = "__".join([element for element in content if element])
        # item['title'] = title
        # item['pubtime'] = pubtime
        # item['tags'] = tags
        # item['praise_num'] = praise_num
        # item['fav_num'] = fav_num
        # item['comment_num'] = comment_num
        # item['contents'] = contents
        # item['image_urls'] = response.meta.get('image_urls', "")
        # item['url_object_id'] = get_md5(response.url)
        # item['url'] = response.url

        # ItemLoader
        item_loader = ArticleItemLoder(item=ArticlespiderItem(), response=response)
        item_loader.add_css('title', 'div.entry-header h1::text')
        item_loader.add_css('pubtime', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('praise_num', '.post-adds span h10::text')
        item_loader.add_css('fav_num', '.bookmark-btn::text')
        item_loader.add_css('comment_num', 'a[href="#article-comment"] span::text')
        item_loader.add_css('content', 'div.entry p::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('image_urls', [response.meta.get("image_urls", '')])

        article_item = item_loader.load_item()
        return article_item

