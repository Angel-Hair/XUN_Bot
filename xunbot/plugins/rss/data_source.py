import time
from typing import Dict, List
from os import path, getcwd

import feedparser
import pandas as pd
from nonebot import scheduler

from ...xlog import xlogger
from xunbot import get_bot

RSSHUBAPP = get_bot().config.RSSHUBAPP


class Subscriber():
    def __init__(self, type: str, id: int, 
                    jointime: float=None):
        self.type = type
        self.id = id
        self.jointime = jointime or time.time()

    def __str__(self):
        return str({name:value for name,value in vars(self).items()})

    def __eq__(self, obj):
        return (self.type == obj.type and self.id == obj.id)


class RSS():
    def __init__(self, rss_route: str, 
                    title: str= None, 
                    lasttitle: List[str]=None, 
                    type: str=None, id: int=None,  
                    jointime: float=None):

        xlogger.info("RSS route {} initializing".format(rss_route))
        self.rss_route = rss_route
        self.subscribers: List[Subscriber] = []
        if (type and id):
            self.subscriber_add(Subscriber(type, id, jointime))
        # self.lasttime = lasttime or time.time()
        self.title = title or []
        self.lasttitle = lasttitle or []

    def __str__(self):
        return "{'route': %s, 'subscribers': %s" % (self.rss_route, self.subscribers)

    def __eq__(self, obj):
        return self.rss_route == obj.rss_route

    # def update(self):
    #     self.lasttime = time.time()

    def update(self, feed: feedparser.FeedParserDict):
        self.title = feed.feed.title
        self.lasttitle = [i.title for i in feed.entries]

    def get_update(self) -> List[Dict[str,str]]:
        lasttitle = self.lasttitle
        rss_feed = RSSHUBAPP + self.rss_route
        xlogger.debug("Rss feed: {} is updating".format(rss_feed))
        d = feedparser.parse(rss_feed)

        if d.status != 200:
            xlogger.error("Failed to update rss feed: {}".format(rss_feed))
            raise RuntimeError("Failed to update rss feed", d)
        
        self.update(d)
        return [{'title': i.title, 'link': i.link} 
                for i in 
                list(filter(lambda i: i.title not in lasttitle, d.entries))]

    # def get_update(self) -> List[Dict[str,str]]:
    #     rss_feed = RSSHUBAPP + self.rss_route
    #     xlogger.debug("Rss feed: {} is updating".format(rss_feed))
    #     d = feedparser.parse(rss_feed)
    #     self.update()

    #     if d.status != 200:
    #         xlogger.error("Failed to update rss feed: {}".format(rss_feed))
    #         raise RuntimeError("Failed to update rss feed", d)
        
    #     return [{'title': i.title, 'link': i.link, 
    #             'author': i.author, 'pubdate': i.published_parsed} 
    #             for i in 
    #             list(filter(lambda i: time.mktime(i.published_parsed) >= self.lasttime, d.entries))]

    def subscriber_add(self, subscriber: Subscriber):
        if subscriber in self.subscribers:
            xlogger.error(
                "Duplicate subscriber: {} is requested to be added".format(subscriber)
                )
            raise RuntimeError("Duplicate subscriber is requested to be added", subscriber)
        
        xlogger.info("Subscriber append: {}".format(subscriber))
        self.subscribers.append(subscriber)

    def subscriber_remove(self, subscriber: Subscriber):
        if subscriber not in self.subscribers:
            xlogger.error(
                "Request to delete subscriber: {} that does not exist".format(subscriber)
                )
            raise RuntimeError("Request to delete subscriber that does not exist", subscriber)

        xlogger.info("Subscriber remove: {}".format(subscriber))
        self.subscribers.remove(subscriber)

    def is_empty(self) -> bool:
        if len(self.subscribers) == 0:
            return True
        return False

    async def test_feed(self) -> bool:
        rss_feed = RSSHUBAPP + self.rss_route
        xlogger.debug("Rss feed: {} is testing".format(rss_feed))

        try:
            d = feedparser.parse(rss_feed)
            if d.status == 200:
                self.update(d)
                xlogger.debug("Test successful")
                return True
        except Exception as e:
            xlogger.error("Test failed: {}".format(e))
            return False
        return False


class RSS_reader():
    def __init__(self):
        self.rsss: List[RSS] = []
        self.load_rss()

    def add_rss(self, rss_route: str, 
                    type: str, id: int, 
                    title: str=None, 
                    lasttitle: List[str]=None, 
                    jointime: float=None) -> bool:
        
        try:
            rss = RSS(rss_route, title, lasttitle, type, id, jointime)

            if rss in self.rsss:
                self.rsss[self.rsss.index(rss)].subscriber_add(Subscriber(type,id,jointime))
            else:
                self.rsss.append(rss)

        except RuntimeError:
            return False

        self.save_rss()
        xlogger.info("Subscriber append successfully")
        return True
    
    def remove_subscriber(self, rss_route: str, 
                    type: str, id: int) -> bool:
        
        rss = RSS(rss_route)
        suber = Subscriber(type, id)

        if rss not in self.rsss:
            xlogger.error(
                "Attempting to delete route that does not exist: {}".format(rss_route)
                )
            return False
        else:
            try:
                index = self.rsss.index(rss)

                self.rsss[index].subscriber_remove(suber)
                if self.rsss[index].is_empty():
                    self.rsss.remove(rss)
                    xlogger.info("RSS with empty subscription has been deleted")

            except RuntimeError:
                return False
        
        self.save_rss()
        xlogger.info("Subscriber deleted successfully")
        return True

    def save_rss(self):
        rss_df = pd.DataFrame(columns=["title", "rss_route", "type", 
                                        "id", "jointime", "lasttitle"])
        
        for rss in self.rsss:
            for suber in rss.subscribers:
                info = {"title": rss.title,
                        "rss_route": rss.rss_route, 
                        "type": suber.type, 
                        "id": suber.id, 
                        "jointime": suber.jointime, 
                        "lasttitle": rss.lasttitle}
                
                rss_df = rss_df.append(info, ignore_index=True)
        
        rss_df.to_csv(getcwd()+'\\rss.csv')
        xlogger.info("RSS saved successfully")

    def load_rss(self):
        if path.isfile('rss.csv'):
            rss = pd.read_csv(getcwd()+'\\rss.csv')
            for _, row in rss.iterrows():
                self.add_rss(row['rss_route'], row['type'], 
                            row['id'], row['title'], row['lasttitle'], row['jointime'])

            xlogger.info("rss.csv file loaded successfully")
        else:
            xlogger.info("There is no rss.csv file in the current directory")

    async def send_msg(self):
        bot = get_bot()

        for rss in self.rsss:
            try:
                update_msg = ["{}\n{}".format(item['title'], item['link']) 
                            for item in 
                            rss.get_update()]
            except RuntimeError as e:
                update_msg = ["很抱歉，该订阅节点更新失败，请联系管理员维护或者取消订阅。"]

            if len(update_msg) > 0:
                for suber in rss.subscribers:
                    info = "\n\n".join(update_msg)

                    if suber.type == 'group':
                        msg = "群订阅的《{}》更新了~\n\n".format(rss.title) + info
                        xlogger.debug("send group: {} rss msg".format(suber.id))
                        await bot.send_group_msg(group_id=suber.id, message=msg)

                    elif suber.type == 'private':
                        msg = "你的订阅的《{}》更新了~\n\n".format(rss.title) + info
                        xlogger.debug("send private: {} rss msg".format(suber.id))
                        await bot.send_private_msg(user_id=suber.id, message=msg)

                    elif suber.type == 'discuss':
                        msg = "讨论组订阅的《{}》更新了~\n\n".format(rss.title) + info
                        xlogger.debug("send discuss: {} rss msg".format(suber.id))
                        await bot.send_discuss_msg(discuss_id=suber.id, message=msg)

        self.save_rss()
                   
    def get_routes(self, type: str, id: int) -> set:
        suber = Subscriber(type, id)
        return {rss.rss_route for rss in 
                list(filter(lambda i: suber in i.subscribers, self.rsss))}
