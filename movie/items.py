# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Celebrity(Item):
    name = Field()
    link = Field()


class People(Item):
    name = Field()
    link = Field()


class Movie(Item):
    title = Field()
    rating_num = Field()
    # List[Celebrity]
    director = Field()
    # List[Celebrity]
    actors = Field()
    img = Field()
    link = Field()
    # List[Comment]
    hot_comments = Field()


class Comment(Item):
    # People
    author = Field()
    rating = Field()
    comment_time = Field()
    content = Field()
