from django.contrib.syndication.views import Feed
from django.urls import reverse
from bs4 import BeautifulSoup
import datetime, requests


class LatestEntriesFeed(Feed):
    title = "White House Blog RSS Feed"
    link = "/"
    description = "Tracking Donald's dumb things."

    def items(self):
        req = requests.get('https://www.whitehouse.gov/blog')
        soup = BeautifulSoup(req.text)
        return soup.select('.view-press-office-listings .views-row')

    def item_pubdate(self, item):
        return datetime.datetime.strptime(item.select('.views-field-created')[0].text.strip(), "%B %d, %Y")


    def item_title(self, item):
        return item.select('.views-field-title h3')[0].text

    def item_description(self, item):
        req = requests.get(self.item_link(item))
        soup = BeautifulSoup(req.text)
        return soup.select('.field-item p')[0].text.strip()

    def item_link(self, item):
        return "https://www.whitehouse.gov%s" % item.select('.views-field-title a')[0]['href']