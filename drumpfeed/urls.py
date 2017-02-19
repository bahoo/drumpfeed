from django.conf.urls import url
from django.contrib import admin
from .views import LatestEntriesFeed

urlpatterns = [
    url(r'', LatestEntriesFeed()),
    url(r'^admin/', admin.site.urls),
]
