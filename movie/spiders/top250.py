import scrapy
from movie.items import Movie, Celebrity, Comment, People


class Top250Spider(scrapy.Spider):
    name = "top250"
    allowed_domains = ["movie.douban.com"]
    base_url = "https://movie.douban.com/top250?filter="
    index = 0

    def start_requests(self):
        yield scrapy.Request(self.base_url)

    def parse(self, response, **kwargs):
        for m in response.css("div.item"):
            link = m.xpath('./div[@class="pic"]/a/@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_detail, cb_kwargs=dict(link=link))
        if self.index < 225:
            self.index += 25
            next_page = f"{self.base_url}&start={self.index}"
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response, link):
        item = Movie(
            title=response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[
                0
            ],
            link=response.meta["link"],
            img=response.xpath('//img[@rel="v:image"]/@src').extract()[0],
            rating_num=response.xpath(
                '//strong[@property="v:average"]/text()'
            ).extract()[0],
        )
        director = []
        actors = []
        for people in response.xpath(
            '//ul[contains(@class, "celebrities-list")]/li[@class="celebrity"]'
        ):
            role = people.xpath('.//span[@class="role"]/@title').extract()[0]
            celebrity = Celebrity(
                name=people.xpath('.//a[@class="name"]/@title').extract()[0],
                link=people.xpath("./a/@href").extract()[0],
            )
            if role == "导演":
                director.append(celebrity)
            else:
                actors.append(celebrity)
        item["director"] = director
        item["actors"] = actors
        hot_comments = []
        for comment in response.xpath(
            '//div[@id="hot-comments"]/div[contains(@class, "comment-item")]'
        ):
            author = People(
                name=comment.xpath('.//span[@class="comment-info"]/a/text()').extract()[
                    0
                ],
                link=comment.xpath('.//span[@class="comment-info"]/a/@href').extract()[
                    0
                ],
            )

            rating = comment.xpath(
                './/span[contains(@class, "rating")]/@class'
            ).extract()
            if len(rating) == 1:
                rating = rating[0].replace(" rating", "").replace("allstar", "")
            else:
                rating = "00"
            c = Comment(
                author=author,
                rating=rating,
                comment_time=comment.xpath(
                    './/span[contains(@class, "comment-time")]/@title'
                ).extract()[0],
                content=comment.xpath('.//span[@class="short"]/text()').extract()[0],
            )
            hot_comments.append(c)
        item["hot_comments"] = hot_comments
        yield item
