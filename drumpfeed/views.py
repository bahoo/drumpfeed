from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.urls import reverse
from bs4 import BeautifulSoup
import datetime, requests


class LatestEntriesFeed(Feed):
    title = "White House Blog RSS Feed"
    link = "/"
    description = "Tracking Donald's dumb things."

    def __call__(self, request, *args, **kwargs):
      # Cache the RSS feed
      # It has to be done this way because the Feed class is a callable, not a view.
      cache_key = self.get_cache_key(*args, **kwargs)
      response = cache.get(cache_key)

      if response is None:
        response = super(LatestEntriesFeed, self).__call__(request, *args, **kwargs)
        cache.set(cache_key, response, 1800) # cache for 15 minutes

      return response

    def get_cache_key(self, *args, **kwargs):
      # Override this in subclasses for more caching control
      return "%s-%s" % (self.__class__.__module__, '/'.join([ "%s,%s" % (key, val) for key,val in kwargs.items() ])) 

    def items(self):
        req = requests.get('https://www.whitehouse.gov/blog')
        soup = BeautifulSoup(req.text, "html.parser")
        return soup.select('.view-press-office-listings .views-row')

    def item_pubdate(self, item):
        return datetime.datetime.strptime(item.select('.views-field-created')[0].text.strip(), "%B %d, %Y")


    def item_title(self, item):
        return item.select('.views-field-title h3')[0].text

    def item_description(self, item):
        req = requests.get(self.item_link(item))
        soup = BeautifulSoup(req.text, "html.parser")
        return soup.select('.field-item p')[0].text.strip()

    def item_link(self, item):
        return "https://www.whitehouse.gov%s" % item.select('.views-field-title a')[0]['href']