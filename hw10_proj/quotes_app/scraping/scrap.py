import os
from datetime import datetime
import json
import scrapy

from scrapy.crawler import CrawlerProcess
from django.conf import settings
from ..models import Author, Quote, Tag

# from pathlib import Path

FIALE_A = os.path.join(settings.JSON_SCR_DIR, "authors.json")
FIALE_Q = os.path.join(settings.JSON_SCR_DIR, "qoutes.json")


class QuotesSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["http://quotes.toscrape.com/"]

    quotes = []
    authors = []

    def parse(self, response, *args):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q = quote.xpath("span[@class='text']/text()").get().strip()

            self.quotes.append(
                {
                    "tags": tags,
                    "author": author,
                    "quote": q,
                }
            )

            yield response.follow(
                url=self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.parse_author,
            )
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response, *args):
        author = response.xpath('/html//div[@class="author-details"]')
        fullname = author.xpath('h3[@class="author-title"]/text()').get().strip()
        born_date = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        description = author.xpath('div[@class="author-description"]/text()').get().strip()

        self.authors.append(
            {
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }
        )

    def to_base(self, reason):

        for author in self.authors:
            born_date_dt = datetime.strptime(author["born_date"], "%B %d, %Y")
            Author.objects.get_or_create(
                fullname=author["fullname"],
                born_date=born_date_dt,
                born_location=author["born_location"],
                description=author["description"],
            )

        for quote in self.quotes:
            tags = []
            for tag in quote["tags"]:
                t, ags = Tag.objects.get_or_create(name=tag)
                tags.append(t)

            author = Author.objects.get(fullname=quote["author"])
            q, args = Quote.objects.get_or_create(
                author=author,
                quote=quote["quote"],
            )
            for tag in tags:
                q.tags.add(tag)

    def close(self, reason):
        self.to_base()
        # with open(FIALE_Q, "w", encoding="utf-8") as fd:
        #     json.dump(self.quotes, fd, ensure_ascii=False, indent=4)
        # with open(FIALE_A, "w", encoding="utf-8") as fd:
        #     json.dump(self.authors, fd, ensure_ascii=False, indent=4)


def start_scrap():
    print("start scpap")
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    print("stop scpap")
